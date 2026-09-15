from __future__ import annotations

from rest_framework import serializers


class DescriptionInputSerializer(serializers.Serializer):
    """Validate an image upload or an image URL for the description agent."""

    image = serializers.ImageField(required=False, allow_empty_file=False)
    image_url = serializers.URLField(required=False, allow_blank=False)

    def validate(self, attrs):
        has_image = bool(self.initial_data.get("image"))
        has_url = bool(self.initial_data.get("image_url"))
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


class ClothingAnalysisResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    model_name = serializers.CharField()
    model_version = serializers.CharField()
    overall_confidence = serializers.FloatField(allow_null=True)


class ClothingItemDescribeResponseSerializer(serializers.Serializer):
    """Response payload after describe persists a ClothingItem."""

    id = serializers.UUIDField()
    image_url = serializers.CharField()
    user = serializers.UUIDField()
    description = ClothingDescriptionSchemaSerializer()
    analysis = ClothingAnalysisResponseSerializer()
