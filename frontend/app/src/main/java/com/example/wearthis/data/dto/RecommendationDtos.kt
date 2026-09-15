package com.example.wearthis.data.dto

import com.google.gson.annotations.SerializedName

data class RecommendRequestDto(
    val schedule: List<ScheduleEventDto>
)

data class ScheduleEventDto(
    @SerializedName("event_id")
    val eventId: String,
    @SerializedName("start_time")
    val startTime: String,
    @SerializedName("end_time")
    val endTime: String,
    val activity: String,
    val weather: ScheduleWeatherDto
)

data class ScheduleWeatherDto(
    val status: String,
    @SerializedName("temperature_c")
    val temperatureC: Double,
    val precipitation: String
)

data class RecommendationResponseDto(
    val recommendations: List<TimeRecommendationDto>
)

data class TimeRecommendationDto(
    @SerializedName("event_id")
    val eventId: String,
    @SerializedName("start_time")
    val startTime: String,
    @SerializedName("end_time")
    val endTime: String,
    val activity: String,
    @SerializedName("clothing_item_ids")
    val clothingItemIds: List<String>,
    @SerializedName("keep_item_ids")
    val keepItemIds: List<String>,
    @SerializedName("remove_item_ids")
    val removeItemIds: List<String>,
    @SerializedName("put_on_item_ids")
    val putOnItemIds: List<String>,
    @SerializedName("pack_item_ids")
    val packItemIds: List<String>,
    val reason: String,
    val warnings: List<String>
)
