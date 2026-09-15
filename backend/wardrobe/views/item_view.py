"""Authenticated wardrobe item collection and detail endpoints."""

from __future__ import annotations

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from wardrobe.models import ClothingItem
from wardrobe.serializers import (
    ClothingItemDetailSerializer,
    ClothingItemSummarySerializer,
    ClothingItemUpdateSerializer,
)
from wardrobe.services import replace_clothing_description


ITEM_RELATIONS = (
    "type__subcategory",
    "type__top_attributes",
    "type__bottom_attributes",
    "type__dress_attributes",
    "type__outerwear_attributes",
    "type__footwear_attributes",
    "type__one_piece_attributes",
    "color_group",
    "material_group",
    "pattern_group",
    "detail_group",
    "style_group",
    "pocket_group",
    "visual_attributes",
    "analysis",
)

CATEGORY_ALIASES = {
    "all": None,
    "top": "top",
    "tops": "top",
    "bottom": "bottom",
    "bottoms": "bottom",
    "outerwear": "outerwear",
    "shoe": "footwear",
    "shoes": "footwear",
    "footwear": "footwear",
    "other": ("dress", "one_piece"),
}


def _item_queryset(user):
    return ClothingItem.objects.filter(user=user).select_related(*ITEM_RELATIONS)


def _apply_filters(queryset, params):
    category = params.get("category")
    if category:
        category_value = CATEGORY_ALIASES.get(category.strip().lower())
        if category_value is None and category.strip().lower() != "all":
            return queryset.none()
        if isinstance(category_value, tuple):
            queryset = queryset.filter(type__name__in=category_value)
        elif category_value:
            queryset = queryset.filter(type__name=category_value)

    type_name = params.get("type")
    if type_name:
        queryset = queryset.filter(type__subcategory__name__iexact=type_name.strip())

    color = params.get("color")
    if color:
        queryset = queryset.filter(color_group__items__color__name__iexact=color.strip())

    search = params.get("search")
    if search:
        for term in search.split():
            queryset = queryset.filter(
                Q(type__name__icontains=term)
                | Q(type__subcategory__name__icontains=term)
                | Q(color_group__items__color__name__icontains=term)
                | Q(material_group__items__material__name__icontains=term)
                | Q(style_group__items__style__name__icontains=term)
            )
    return queryset.distinct()


@api_view(["GET"])
def clothing_item_list(request):
    """Return the caller's image-first wardrobe grid, with optional filters."""

    items = _apply_filters(_item_queryset(request.user), request.query_params)
    return Response(ClothingItemSummarySerializer(items, many=True).data)


@api_view(["GET", "PATCH", "DELETE"])
def clothing_item_detail(request, item_id):
    """View, edit, or remove one item owned by the authenticated user."""

    try:
        item = _item_queryset(request.user).get(pk=item_id)
    except ClothingItem.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(ClothingItemDetailSerializer(item).data)

    if request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ClothingItemUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    if "description" in data:
        item = replace_clothing_description(item=item, description=data["description"])
    if "image_url" in data:
        item.image_url = data["image_url"]
        item.save(update_fields=["image_url", "updated_at"])

    item = _item_queryset(request.user).get(pk=item.pk)
    return Response(ClothingItemDetailSerializer(item).data)
