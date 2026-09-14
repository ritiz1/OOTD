from __future__ import annotations

from django.conf import settings
from rest_framework import serializers


class DescriptionInputSerializer(serializers.Serializer):
    """Validate an image upload or an image URL for the description agent."""

    image = serializers.ImageField(required=False, allow_empty_file=False)
    image_url = serializers.URLField(required=False, allow_blank=False)

    def validate(self, attrs):
        has_image = "image" in attrs and attrs["image"] is not None
        has_url = "image_url" in attrs and attrs["image_url"]
        if has_image == has_url:
            raise serializers.ValidationError(
                "Provide exactly one of 'image' or 'image_url'."
            )
        return attrs


class ClothingDescriptionSchemaSerializer(serializers.Serializer):
    """Validation-friendly serializer for the Pydantic agent payload."""

    type = serializers.DictField()
    colors = serializers.ListField(child=serializers.DictField())
    materials = serializers.ListField(child=serializers.DictField())
    patterns = serializers.ListField(child=serializers.DictField())
    details = serializers.ListField(child=serializers.CharField())
    styles = serializers.ListField(child=serializers.DictField())
    pockets = serializers.ListField(child=serializers.DictField())
    visual_attributes = serializers.DictField()


class ClothingItemCreateSerializer(serializers.Serializer):
    """Serializer placeholder for turning an agent payload into a wardrobe item."""

    image_url = serializers.CharField(required=False, allow_blank=True)
    type = serializers.CharField(required=False)
    visual_attributes = serializers.DictField(required=False)

    def validate(self, attrs):
        if not attrs.get("image_url"):
            attrs["image_url"] = settings.DEFAULT_FILE_STORAGE
        return attrs
