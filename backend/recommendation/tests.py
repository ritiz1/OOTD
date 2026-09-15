from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase

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
