from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase
from unittest.mock import AsyncMock, patch

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

from .wardrobe_payload import wardrobe_items_for_user


User = get_user_model()


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


class WardrobePayloadTests(TestCase):
    def _create_item(self, user, suffix: str) -> ClothingItem:
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
            user=user,
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

    def test_returns_only_requested_users_items_with_resolved_type(self):
        requested_user = User.objects.create_user(
            email="wardrobe-owner@example.com", password="test-password-123"
        )
        other_user = User.objects.create_user(
            email="other-owner@example.com", password="test-password-123"
        )
        owned_item = self._create_item(requested_user, "owned")
        other_item = self._create_item(other_user, "other")

        payload = wardrobe_items_for_user(requested_user)

        self.assertEqual([item["id"] for item in payload], [str(owned_item.id)])
        self.assertNotIn(str(other_item.id), {item["id"] for item in payload})
        self.assertEqual(payload[0]["user_id"], str(requested_user.id))
        self.assertEqual(payload[0]["type"]["name"], "top")
        self.assertEqual(payload[0]["type"]["subcategory"]["type_name"], "top")
        self.assertEqual(payload[0]["type"]["attributes"]["id"], str(owned_item.type.top_attributes_id))


class RecommendationEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="recommendation-user@example.com", password="test-password-123"
        )
        self.request_data = {
            "schedule": [
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
        }

    def test_requires_authentication(self):
        response = self.client.post(
            "/api/recommendations/", self.request_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("recommendation.views.wardrobe_items_for_user", return_value=[])
    def test_rejects_empty_wardrobe(self, wardrobe_mock):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/recommendations/", self.request_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        wardrobe_mock.assert_called_once_with(self.user)

    @patch("recommendation.views.run_recommendation_agent", new_callable=AsyncMock)
    @patch("recommendation.views.wardrobe_items_for_user")
    def test_returns_validated_agent_response(self, wardrobe_mock, agent_mock):
        item_id = "00000000-0000-4000-8000-000000000101"
        wardrobe_mock.return_value = [
            {"id": item_id, "user_id": str(self.user.id), "type": {"name": "top"}}
        ]
        agent_result = {
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
                    "reason": "Suitable for class and the cool weather.",
                    "warnings": [],
                }
            ]
        }
        agent_mock.return_value = agent_result
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/recommendations/", self.request_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), agent_result)
        payload = agent_mock.await_args.args[0]
        self.assertEqual(payload["clothing_items"], wardrobe_mock.return_value)
        self.assertEqual(agent_mock.await_args.kwargs["user_id"], str(self.user.id))

    @patch("recommendation.views.run_recommendation_agent", new_callable=AsyncMock)
    @patch("recommendation.views.wardrobe_items_for_user")
    def test_rejects_agent_response_with_unknown_item(self, wardrobe_mock, agent_mock):
        wardrobe_mock.return_value = [
            {"id": "owned-item", "user_id": str(self.user.id), "type": {"name": "top"}}
        ]
        agent_mock.return_value = {
            "recommendations": [
                {
                    "event_id": "morning-class",
                    "start_time": "09:00",
                    "end_time": "11:00",
                    "activity": "Class on campus",
                    "clothing_item_ids": ["invented-item"],
                    "keep_item_ids": [],
                    "remove_item_ids": [],
                    "put_on_item_ids": ["invented-item"],
                    "pack_item_ids": [],
                    "reason": "Invalid test response.",
                    "warnings": [],
                }
            ]
        }
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/recommendations/", self.request_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
        self.assertEqual(
            response.json()["detail"],
            "The recommendation response failed validation.",
        )
