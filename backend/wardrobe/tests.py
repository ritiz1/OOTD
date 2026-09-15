from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from wardrobe.models import ClothingItem
from wardrobe.services import persist_clothing_description


class _FakeDescription:
    def __init__(self, payload):
        self._payload = payload

    def model_dump(self, mode="json"):
        return self._payload


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
