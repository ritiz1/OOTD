"""Load an authenticated user's wardrobe as resolved agent input."""

from django.forms.models import model_to_dict

from wardrobe.models import ClothingItem


TYPE_ATTRIBUTE_FIELDS = (
    "top_attributes",
    "bottom_attributes",
    "dress_attributes",
    "outerwear_attributes",
    "footwear_attributes",
    "one_piece_attributes",
)


def _values(instance, *, exclude=()) -> dict:
    data = model_to_dict(instance, exclude=("id", *exclude))
    return {key: value for key, value in data.items() if value not in (None, "")}


def _group_values(group, relation: str, *, extra_fields=()) -> list[dict]:
    values = []
    for group_item in group.items.all():
        lookup = getattr(group_item, relation)
        value = {"id": str(lookup.id), "name": lookup.name}
        for field in extra_fields:
            field_value = getattr(group_item, field)
            if field_value not in (None, ""):
                value[field] = field_value
        values.append(value)
    return values


def wardrobe_items_for_user(user) -> list[dict]:
    """Return only this user's clothing items with all recommendation data resolved."""
    items = (
        ClothingItem.objects.filter(user=user)
        .select_related(
            "type__subcategory",
            *(f"type__{field}" for field in TYPE_ATTRIBUTE_FIELDS),
            "visual_attributes",
        )
        .prefetch_related(
            "color_group__items__color",
            "material_group__items__material",
            "pattern_group__items__pattern",
            "detail_group__items__detail",
            "style_group__items__style",
            "pocket_group__items__pocket_type",
        )
    )

    payload = []
    for item in items:
        clothing_type = item.type
        attributes = clothing_type.attributes
        payload.append(
            {
                "id": str(item.id),
                "user_id": str(item.user_id),
                "image_url": item.image_url,
                "type": {
                    "id": str(clothing_type.id),
                    "name": clothing_type.name,
                    "subcategory": {
                        "id": str(clothing_type.subcategory_id),
                        "type_name": clothing_type.subcategory.type_name,
                        "name": clothing_type.subcategory.name,
                    },
                    "attributes": {
                        "id": str(attributes.id),
                        **_values(attributes),
                    },
                },
                "colors": _group_values(
                    item.color_group, "color", extra_fields=("role", "percentage")
                ),
                "materials": _group_values(
                    item.material_group, "material", extra_fields=("percentage",)
                ),
                "patterns": _group_values(
                    item.pattern_group,
                    "pattern",
                    extra_fields=("scale", "density", "orientation"),
                ),
                "details": _group_values(item.detail_group, "detail"),
                "styles": _group_values(
                    item.style_group, "style", extra_fields=("confidence",)
                ),
                "pockets": _group_values(
                    item.pocket_group, "pocket_type", extra_fields=("count",)
                ),
                "visual_attributes": {
                    "id": str(item.visual_attributes_id),
                    **_values(item.visual_attributes),
                },
            }
        )
    return payload
