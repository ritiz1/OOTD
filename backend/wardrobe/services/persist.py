from __future__ import annotations

from typing import Any

from django.db import transaction

from wardrobe.models import (
    BottomAttributes,
    ClothingAnalysis,
    ClothingColorGroup,
    ClothingColorGroupItem,
    ClothingDetailGroup,
    ClothingDetailGroupItem,
    ClothingItem,
    ClothingMaterialGroup,
    ClothingMaterialGroupItem,
    ClothingPatternGroup,
    ClothingPatternGroupItem,
    ClothingPocketGroup,
    ClothingPocketGroupItem,
    ClothingStyleGroup,
    ClothingStyleGroupItem,
    ClothingSubcategory,
    ClothingType,
    Color,
    Detail,
    DressAttributes,
    FootwearAttributes,
    Material,
    OnePieceAttributes,
    OuterwearAttributes,
    Pattern,
    PocketType,
    Style,
    TopAttributes,
    VisualAttributes,
)
from wardrobe.models.core import TYPE_TO_ATTRIBUTE_FIELD


ATTRIBUTE_MODEL_BY_FIELD = {
    "top_attributes": TopAttributes,
    "bottom_attributes": BottomAttributes,
    "dress_attributes": DressAttributes,
    "outerwear_attributes": OuterwearAttributes,
    "footwear_attributes": FootwearAttributes,
    "one_piece_attributes": OnePieceAttributes,
}


def _as_payload(description: Any) -> dict[str, Any]:
    if hasattr(description, "model_dump"):
        return description.model_dump(mode="json")
    if isinstance(description, dict):
        return description
    raise TypeError("description must be a ClothingDescription or dict")


def _percentage(value: float | int | None) -> int | None:
    if value is None:
        return None
    return int(round(float(value)))


def _overall_confidence(styles: list[dict[str, Any]]) -> float | None:
    confidences = [
        float(style["confidence"])
        for style in styles
        if style.get("confidence") is not None
    ]
    return max(confidences) if confidences else None


@transaction.atomic
def persist_clothing_description(
    *,
    user,
    image_url: str,
    description: Any,
    model_name: str,
    model_version: str = "",
) -> ClothingItem:
    """Map an agent clothing-description payload into a ClothingItem for user."""

    payload = _as_payload(description)
    type_data = payload["type"]
    type_name = type_data["name"]
    attribute_field = TYPE_TO_ATTRIBUTE_FIELD[type_name]
    attribute_model = ATTRIBUTE_MODEL_BY_FIELD[attribute_field]

    subcategory, _ = ClothingSubcategory.objects.get_or_create(
        type_name=type_name,
        name=type_data["subcategory"],
    )
    attributes = attribute_model.objects.create(**type_data["attributes"])
    clothing_type = ClothingType(
        name=type_name,
        subcategory=subcategory,
        **{attribute_field: attributes},
    )
    clothing_type.full_clean()
    clothing_type.save()

    color_group = ClothingColorGroup.objects.create()
    for color_data in payload.get("colors", []):
        color, _ = Color.objects.get_or_create(name=color_data["name"])
        ClothingColorGroupItem.objects.create(
            group=color_group,
            color=color,
            role=color_data["role"],
            percentage=_percentage(color_data.get("percentage")),
        )

    material_group = ClothingMaterialGroup.objects.create()
    for material_data in payload.get("materials", []):
        material, _ = Material.objects.get_or_create(name=material_data["name"])
        ClothingMaterialGroupItem.objects.create(
            group=material_group,
            material=material,
            percentage=_percentage(material_data.get("percentage")),
        )

    pattern_group = ClothingPatternGroup.objects.create()
    for pattern_data in payload.get("patterns", []):
        pattern, _ = Pattern.objects.get_or_create(name=pattern_data["name"])
        ClothingPatternGroupItem.objects.create(
            group=pattern_group,
            pattern=pattern,
            scale=pattern_data["scale"],
            density=pattern_data["density"],
            orientation=pattern_data["orientation"],
        )

    detail_group = ClothingDetailGroup.objects.create()
    for detail_name in payload.get("details", []):
        detail, _ = Detail.objects.get_or_create(name=detail_name)
        ClothingDetailGroupItem.objects.create(group=detail_group, detail=detail)

    style_group = ClothingStyleGroup.objects.create()
    styles = payload.get("styles", [])
    for style_data in styles:
        style, _ = Style.objects.get_or_create(name=style_data["name"])
        ClothingStyleGroupItem.objects.create(
            group=style_group,
            style=style,
            confidence=style_data.get("confidence"),
        )

    pocket_group = ClothingPocketGroup.objects.create()
    for pocket_data in payload.get("pockets", []):
        pocket_type, _ = PocketType.objects.get_or_create(name=pocket_data["name"])
        ClothingPocketGroupItem.objects.create(
            group=pocket_group,
            pocket_type=pocket_type,
            count=pocket_data.get("count", 1),
        )

    visual_attributes = VisualAttributes.objects.create(**payload["visual_attributes"])
    analysis = ClothingAnalysis.objects.create(
        model_name=model_name,
        model_version=model_version,
        raw_response=payload,
        overall_confidence=_overall_confidence(styles),
    )

    return ClothingItem.objects.create(
        user=user,
        image_url=image_url,
        type=clothing_type,
        color_group=color_group,
        material_group=material_group,
        pattern_group=pattern_group,
        detail_group=detail_group,
        style_group=style_group,
        pocket_group=pocket_group,
        visual_attributes=visual_attributes,
        analysis=analysis,
    )
