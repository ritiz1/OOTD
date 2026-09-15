from __future__ import annotations

from rest_framework import serializers

from wardrobe.models import ClothingItem


def absolute_image_url(request, image_url: str) -> str:
    """Expand a stored media path into a URL clients on other devices can load."""

    if request is None:
        return image_url
    return request.build_absolute_uri(image_url)


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


class ClothingItemSummarySerializer(serializers.ModelSerializer):
    """Small, image-first representation used by the wardrobe grid."""

    image_url = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    primary_color = serializers.SerializerMethodField()

    class Meta:
        model = ClothingItem
        fields = ("id", "image_url", "type", "primary_color", "created_at")

    def get_image_url(self, item):
        return absolute_image_url(self.context.get("request"), item.image_url)

    def get_type(self, item):
        return {
            "name": item.type.name,
            "subcategory": item.type.subcategory.name,
        }

    def get_primary_color(self, item):
        color = item.color_group.items.filter(role="primary").select_related("color").first()
        if color is None:
            color = item.color_group.items.select_related("color").first()
        return color.color.name if color else None


class ClothingItemDetailSerializer(serializers.ModelSerializer):
    """Full normalized clothing metadata for the item detail screen."""

    image_url = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    patterns = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    styles = serializers.SerializerMethodField()
    pockets = serializers.SerializerMethodField()
    visual_attributes = serializers.SerializerMethodField()
    analysis = serializers.SerializerMethodField()

    class Meta:
        model = ClothingItem
        fields = (
            "id",
            "image_url",
            "type",
            "colors",
            "materials",
            "patterns",
            "details",
            "styles",
            "pockets",
            "visual_attributes",
            "analysis",
            "created_at",
            "updated_at",
        )

    def get_image_url(self, item):
        return absolute_image_url(self.context.get("request"), item.image_url)

    def get_type(self, item):
        attributes = item.type.attributes
        attribute_values = {
            field.name: getattr(attributes, field.name)
            for field in attributes._meta.concrete_fields
            if field.name != "id"
        }
        return {
            "name": item.type.name,
            "subcategory": item.type.subcategory.name,
            "attributes": attribute_values,
        }

    def get_colors(self, item):
        return [
            {"name": entry.color.name, "role": entry.role, "percentage": entry.percentage}
            for entry in item.color_group.items.select_related("color").all()
        ]

    def get_materials(self, item):
        return [
            {"name": entry.material.name, "percentage": entry.percentage}
            for entry in item.material_group.items.select_related("material").all()
        ]

    def get_patterns(self, item):
        return [
            {
                "name": entry.pattern.name,
                "scale": entry.scale,
                "density": entry.density,
                "orientation": entry.orientation,
            }
            for entry in item.pattern_group.items.select_related("pattern").all()
        ]

    def get_details(self, item):
        return [entry.detail.name for entry in item.detail_group.items.select_related("detail").all()]

    def get_styles(self, item):
        return [
            {"name": entry.style.name, "confidence": entry.confidence}
            for entry in item.style_group.items.select_related("style").all()
        ]

    def get_pockets(self, item):
        return [
            {"name": entry.pocket_type.name, "count": entry.count}
            for entry in item.pocket_group.items.select_related("pocket_type").all()
        ]

    def get_visual_attributes(self, item):
        return {
            field.name: getattr(item.visual_attributes, field.name)
            for field in item.visual_attributes._meta.concrete_fields
            if field.name != "id"
        }

    def get_analysis(self, item):
        if item.analysis is None:
            return None
        return ClothingAnalysisResponseSerializer(item.analysis).data


class ClothingItemUpdateSerializer(serializers.Serializer):
    """Accept an optional replacement of all AI-detected item attributes."""

    image_url = serializers.CharField(required=False, allow_blank=False)
    description = ClothingDescriptionSchemaSerializer(required=False)

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("Provide 'image_url' or 'description'.")
        return attrs


class ScheduleWeatherSerializer(serializers.Serializer):
    status = serializers.CharField()
    temperature_c = serializers.FloatField()
    precipitation = serializers.CharField()


class ScheduleEventSerializer(serializers.Serializer):
    event_id = serializers.CharField()
    start_time = serializers.CharField()
    end_time = serializers.CharField()
    activity = serializers.CharField()
    weather = ScheduleWeatherSerializer()


class RecommendInputSerializer(serializers.Serializer):
    """Validate the schedule sent to the outfit recommendation agent."""

    schedule = ScheduleEventSerializer(many=True, allow_empty=False)


class TimeRecommendationSerializer(serializers.Serializer):
    event_id = serializers.CharField()
    start_time = serializers.CharField()
    end_time = serializers.CharField()
    activity = serializers.CharField()
    clothing_item_ids = serializers.ListField(child=serializers.CharField())
    keep_item_ids = serializers.ListField(child=serializers.CharField())
    remove_item_ids = serializers.ListField(child=serializers.CharField())
    put_on_item_ids = serializers.ListField(child=serializers.CharField())
    pack_item_ids = serializers.ListField(child=serializers.CharField())
    reason = serializers.CharField()
    warnings = serializers.ListField(child=serializers.CharField())


class DailyRecommendationResponseSerializer(serializers.Serializer):
    """Validated outfit plan returned by the recommendation agent."""

    recommendations = TimeRecommendationSerializer(many=True)
