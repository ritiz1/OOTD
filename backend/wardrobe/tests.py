from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from wardrobe.models import (
    ClothingColorGroup,
    ClothingDetailGroup,
    ClothingItem,
    ClothingMaterialGroup,
    ClothingPatternGroup,
    ClothingPocketGroup,
    ClothingStyleGroup,
    ClothingSubcategory,
    ClothingType,
    TopAttributes,
    VisualAttributes,
)
from wardrobe.services import persist_clothing_description
from recommendation.schemas import DailyRecommendation


class _FakeDescription:
    def __init__(self, payload):
        self._payload = payload

    def model_dump(self, mode="json"):
        return self._payload


class LiteLLMCompatibilityTests(TestCase):
    def test_litellm_imports_on_python_310(self):
        """Guard against LiteLLM importing 3.11-only typing names on 3.10."""

        import litellm_compat  # noqa: F401
        import litellm

        self.assertIsNotNone(litellm)


User = get_user_model()


def _jpeg_upload(name: str = "shirt.jpg") -> SimpleUploadedFile:
    buffer = BytesIO()
    Image.new("RGB", (8, 8), color=(10, 20, 30)).save(buffer, format="JPEG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


SAMPLE_DESCRIPTION = {
    "type": {
        "name": "top",
        "subcategory": "t_shirt",
        "attributes": {
            "sleeve_length": "short",
            "sleeve_type": "regular",
            "neckline": "crew",
            "collar_type": "none",
            "shoulder_style": "regular",
            "hem_style": "straight",
            "closure_type": "none",
            "hood_type": "none",
            "fit": "regular",
            "length": "waist",
        },
    },
    "colors": [{"name": "black", "role": "primary", "percentage": 100}],
    "materials": [{"name": "cotton", "percentage": 100}],
    "patterns": [{"name": "solid", "scale": "none", "density": "none", "orientation": "none"}],
    "details": [],
    "styles": [{"name": "casual", "confidence": 0.8}],
    "pockets": [],
    "visual_attributes": {
        "dominant_color_hex": "#000000",
        "brightness": "dark",
        "saturation": "muted",
        "visual_complexity": "simple",
        "statement_level": "basic",
        "structure": "soft",
        "surface_finish": "matte",
        "transparency": "opaque",
        "symmetry": "symmetric",
    },
}


class DescriptionViewSerializerSmokeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="tester@example.com",
            password="strongpass123",
            first_name="Tester",
            last_name="User",
        )
        self.client.force_authenticate(user=self.user)

    def test_description_input_serializer_requires_one_of_image_or_image_url(self):
        response = self.client.post("/api/wardrobe/describe/", {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_description_input_serializer_rejects_mixed_image_inputs(self):
        from wardrobe.serializers import DescriptionInputSerializer

        serializer = DescriptionInputSerializer(
            data={
                "image": _jpeg_upload(),
                "image_url": "https://example.com/image.jpg",
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_clothing_description_schema_serializer_accepts_agent_shape(self):
        from wardrobe.serializers import ClothingDescriptionSchemaSerializer

        serializer = ClothingDescriptionSchemaSerializer(data=SAMPLE_DESCRIPTION)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_unauthenticated_describe_returns_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.post("/api/wardrobe/describe/", {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PersistClothingDescriptionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="strongpass123",
        )

    def test_persist_creates_clothing_item_for_user(self):
        item = persist_clothing_description(
            user=self.user,
            image_url="https://example.com/shirt.jpg",
            description=SAMPLE_DESCRIPTION,
            model_name="gemini/test",
            model_version="1",
        )

        self.assertEqual(item.user_id, self.user.id)
        self.assertEqual(item.image_url, "https://example.com/shirt.jpg")
        self.assertEqual(item.type.name, "top")
        self.assertEqual(item.type.subcategory.name, "t_shirt")
        self.assertEqual(item.color_group.items.count(), 1)
        self.assertEqual(item.material_group.items.count(), 1)
        self.assertEqual(item.pattern_group.items.count(), 1)
        self.assertEqual(item.detail_group.items.count(), 0)
        self.assertEqual(item.pocket_group.items.count(), 0)
        self.assertEqual(item.style_group.items.count(), 1)
        self.assertIsNotNone(item.analysis)
        self.assertEqual(item.analysis.model_name, "gemini/test")
        self.assertEqual(item.analysis.overall_confidence, 0.8)
        self.assertEqual(item.analysis.raw_response["type"]["name"], "top")
        self.assertEqual(ClothingItem.objects.filter(user=self.user).count(), 1)


@override_settings(MEDIA_ROOT="/tmp/wearthis-test-media")
class DescribeClothingItemPersistAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="api@example.com",
            password="strongpass123",
        )
        self.client.force_authenticate(user=self.user)

    @patch("wardrobe.views.desc_view.run_description_agent")
    def test_describe_upload_persists_item(self, mock_agent):
        mock_agent.return_value = _FakeDescription(SAMPLE_DESCRIPTION)

        response = self.client.post(
            "/api/wardrobe/describe/",
            {"image": _jpeg_upload()},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["user"], str(self.user.id))
        self.assertTrue(response.data["image_url"])
        self.assertEqual(response.data["description"]["type"]["name"], "top")
        self.assertEqual(response.data["analysis"]["overall_confidence"], 0.8)

        item = ClothingItem.objects.get(id=response.data["id"])
        self.assertEqual(item.user_id, self.user.id)
        self.assertEqual(item.image_url, response.data["image_url"])
        mock_agent.assert_called_once()
        self.assertEqual(mock_agent.call_args.kwargs["user_id"], str(self.user.id))

    @patch("wardrobe.views.desc_view.run_description_agent")
    def test_describe_upload_removes_image_when_agent_fails(self, mock_agent):
        mock_agent.side_effect = RuntimeError("description service unavailable")

        response = self.client.post(
            "/api/wardrobe/describe/",
            {"image": _jpeg_upload()},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
        self.assertEqual(ClothingItem.objects.filter(user=self.user).count(), 0)
        _, stored_files = default_storage.listdir(f"wardrobe/{self.user.id}")
        self.assertEqual(stored_files, [])

    @patch("wardrobe.views.desc_view.urlopen")
    @patch("wardrobe.views.desc_view.run_description_agent")
    def test_describe_image_url_persists_item(self, mock_agent, mock_urlopen):
        mock_agent.return_value = _FakeDescription(SAMPLE_DESCRIPTION)

        class FakeHeaders:
            def get_content_type(self):
                return "image/jpeg"

        class FakeResponse:
            headers = FakeHeaders()

            def read(self):
                return b"\xff\xd8\xff\xe0fake-jpeg"

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        mock_urlopen.return_value = FakeResponse()
        remote_url = "https://cdn.example.com/shirt.jpg"

        response = self.client.post(
            "/api/wardrobe/describe/",
            {"image_url": remote_url},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["image_url"], remote_url)
        item = ClothingItem.objects.get(id=response.data["id"])
        self.assertEqual(item.user_id, self.user.id)
        self.assertEqual(item.image_url, remote_url)


def _choice_values(model_class) -> dict:
    """Build valid values for every required choice field on a test model."""
    values = {}
    for field in model_class._meta.concrete_fields:
        if (
            isinstance(field, models.CharField)
            and field.choices
            and not field.blank
            and field.name != "id"
        ):
            values[field.name] = field.choices[0][0]
    return values


SAMPLE_SCHEDULE = [
    {
        "event_id": "morning-class",
        "start_time": "09:00",
        "end_time": "11:00",
        "activity": "Class on campus",
        "weather": {
            "status": "cool and breezy",
            "temperature_c": 12,
            "precipitation": "none",
        },
    }
]


class RecommendAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="recommend@example.com",
            password="strongpass123",
        )
        self.client.force_authenticate(user=self.user)

    def _create_item(self, suffix: str) -> ClothingItem:
        attributes = TopAttributes.objects.create(**_choice_values(TopAttributes))
        subcategory = ClothingSubcategory.objects.create(
            type_name="top", name=f"test_top_{suffix}"
        )
        clothing_type = ClothingType.objects.create(
            name="top",
            subcategory=subcategory,
            top_attributes=attributes,
        )
        visual = VisualAttributes.objects.create(**_choice_values(VisualAttributes))
        return ClothingItem.objects.create(
            user=self.user,
            image_url=f"https://example.com/{suffix}.jpg",
            type=clothing_type,
            color_group=ClothingColorGroup.objects.create(),
            material_group=ClothingMaterialGroup.objects.create(),
            pattern_group=ClothingPatternGroup.objects.create(),
            detail_group=ClothingDetailGroup.objects.create(),
            style_group=ClothingStyleGroup.objects.create(),
            pocket_group=ClothingPocketGroup.objects.create(),
            visual_attributes=visual,
        )

    def test_unauthenticated_recommend_returns_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            "/api/wardrobe/recommend/",
            {"schedule": SAMPLE_SCHEDULE},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_schedule_returns_400(self):
        response = self.client.post("/api/wardrobe/recommend/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_schedule_returns_400(self):
        response = self.client.post(
            "/api/wardrobe/recommend/",
            {"schedule": []},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_wardrobe_returns_400(self):
        response = self.client.post(
            "/api/wardrobe/recommend/",
            {"schedule": SAMPLE_SCHEDULE},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("wardrobe", response.data["detail"].lower())

    def test_recommend_input_serializer_accepts_schedule(self):
        from wardrobe.serializers import RecommendInputSerializer

        serializer = RecommendInputSerializer(data={"schedule": SAMPLE_SCHEDULE})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    @patch("wardrobe.views.recommend_view.run_recommendation_agent")
    def test_recommend_returns_plan(self, mock_agent):
        item = self._create_item("owned")
        item_id = str(item.id)
        mock_agent.return_value = DailyRecommendation.model_validate(
            {
                "recommendations": [
                    {
                        "event_id": "morning-class",
                        "start_time": "09:00",
                        "end_time": "11:00",
                        "activity": "Class on campus",
                        "clothing_item_ids": [item_id],
                        "keep_item_ids": [],
                        "remove_item_ids": [],
                        "put_on_item_ids": [item_id],
                        "pack_item_ids": [],
                        "reason": "Wear the available top for class.",
                        "warnings": [],
                    }
                ]
            }
        )

        response = self.client.post(
            "/api/wardrobe/recommend/",
            {"schedule": SAMPLE_SCHEDULE},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data["recommendations"]), 1)
        self.assertEqual(
            response.data["recommendations"][0]["clothing_item_ids"],
            [item_id],
        )
        mock_agent.assert_called_once()
        self.assertEqual(mock_agent.call_args.kwargs["user_id"], str(self.user.id))
        sent_payload = mock_agent.call_args.args[0]
        self.assertEqual(sent_payload["schedule"][0]["event_id"], "morning-class")
        self.assertEqual(sent_payload["clothing_items"][0]["id"], item_id)


class ClothingItemViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="items@example.com", password="strongpass123"
        )
        self.other_user = User.objects.create_user(
            email="other-items@example.com", password="strongpass123"
        )
        self.client.force_authenticate(user=self.user)

    def _create_item(self, user=None, image_url="https://example.com/black-shirt.jpg"):
        return persist_clothing_description(
            user=user or self.user,
            image_url=image_url,
            description=SAMPLE_DESCRIPTION,
            model_name="gemini/test",
        )

    def test_list_returns_only_the_authenticated_users_grid_items(self):
        item = self._create_item()
        self._create_item(user=self.other_user, image_url="https://example.com/other.jpg")

        response = self.client.get("/api/wardrobe/items/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([row["id"] for row in response.data], [str(item.id)])
        self.assertEqual(response.data[0]["type"]["subcategory"], "t_shirt")
        self.assertEqual(response.data[0]["primary_color"], "black")

    def test_list_supports_category_color_and_detected_attribute_search(self):
        item = self._create_item()

        response = self.client.get("/api/wardrobe/items/?category=tops&color=black")
        self.assertEqual([row["id"] for row in response.data], [str(item.id)])

        response = self.client.get("/api/wardrobe/items/?search=black%20casual")
        self.assertEqual([row["id"] for row in response.data], [str(item.id)])

    def test_detail_returns_all_detected_attributes(self):
        item = self._create_item()

        response = self.client.get(f"/api/wardrobe/items/{item.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"]["attributes"]["neckline"], "crew")
        self.assertEqual(response.data["colors"][0]["name"], "black")
        self.assertEqual(response.data["styles"][0]["name"], "casual")

    def test_patch_replaces_detected_metadata_without_changing_item_id(self):
        item = self._create_item()
        description = {**SAMPLE_DESCRIPTION}
        description["colors"] = [{"name": "white", "role": "primary", "percentage": 100}]
        description["styles"] = [{"name": "formal", "confidence": 0.9}]

        response = self.client.patch(
            f"/api/wardrobe/items/{item.id}/",
            {"description": description},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data["id"], str(item.id))
        self.assertEqual(response.data["colors"][0]["name"], "white")
        self.assertEqual(response.data["styles"][0]["name"], "formal")
        self.assertEqual(ClothingItem.objects.filter(pk=item.id).count(), 1)

    def test_item_detail_is_not_available_to_other_users_and_can_be_deleted(self):
        item = self._create_item(user=self.other_user)
        response = self.client.get(f"/api/wardrobe/items/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        own_item = self._create_item()
        response = self.client.delete(f"/api/wardrobe/items/{own_item.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ClothingItem.objects.filter(pk=own_item.id).exists())
