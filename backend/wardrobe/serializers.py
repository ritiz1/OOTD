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
