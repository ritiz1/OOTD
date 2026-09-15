from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=200)
    temperature_c = serializers.FloatField()
    precipitation = serializers.CharField(max_length=100)


class ScheduleEventSerializer(serializers.Serializer):
    event_id = serializers.CharField(max_length=100)
    start_time = serializers.RegexField(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    end_time = serializers.RegexField(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    activity = serializers.CharField(max_length=300)
    weather = WeatherSerializer()

    def validate(self, attrs):
        if attrs["end_time"] <= attrs["start_time"]:
            raise serializers.ValidationError("end_time must be after start_time.")
        return attrs


class RecommendationRequestSerializer(serializers.Serializer):
    schedule = ScheduleEventSerializer(many=True, allow_empty=False)

    def validate_schedule(self, events):
        event_ids = [event["event_id"] for event in events]
        if len(event_ids) != len(set(event_ids)):
            raise serializers.ValidationError("event_id values must be unique.")
        if events != sorted(events, key=lambda event: event["start_time"]):
            raise serializers.ValidationError("Events must be in chronological order.")
        return events
