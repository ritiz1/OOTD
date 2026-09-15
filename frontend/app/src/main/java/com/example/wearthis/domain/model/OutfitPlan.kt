package com.example.wearthis.domain.model

import com.example.wearthis.data.dto.ScheduleEventDto
import com.example.wearthis.data.dto.ScheduleWeatherDto
import com.example.wearthis.data.dto.TimeRecommendationDto
import com.example.wearthis.repository.EventWeather
import com.example.wearthis.repository.WeatherPlace
import java.time.LocalDate
import java.time.LocalTime
import java.time.ZoneId

// Strings keep persisted plans independent of java.time/Gson reflection adapters.
data class OutfitPlan(
    val id: String,
    val title: String,
    val date: String,
    val start: String,
    val end: String,
    val occasion: String,
    val vibe: String,
    val place: WeatherPlace,
    val weather: EventWeather,
    val recommendations: List<TimeRecommendationDto> = emptyList()
) {
    fun toSchedule(): ScheduleEventDto {
        val day = LocalDate.parse(date)
        val startTime = day.atTime(LocalTime.parse(start))
        val endTime = day.atTime(LocalTime.parse(end))
        require(endTime.isAfter(startTime)) { "End time must be after start time." }
        val zone = ZoneId.of(weather.timezone)
        return ScheduleEventDto(id, startTime.atZone(zone).toOffsetDateTime().toString(),
            endTime.atZone(zone).toOffsetDateTime().toString(),
            "$title. Occasion: $occasion. Vibe: $vibe. Location: ${place.name}.",
            ScheduleWeatherDto(weather.status, weather.temperatureC, weather.precipitation))
    }
}
