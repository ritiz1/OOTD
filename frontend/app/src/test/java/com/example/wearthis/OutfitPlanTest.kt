package com.example.wearthis

import com.example.wearthis.domain.model.OutfitPlan
import com.example.wearthis.repository.EventWeather
import com.example.wearthis.repository.WeatherPlace
import com.google.gson.Gson
import org.junit.Assert.*
import org.junit.Test

class OutfitPlanTest {
    private fun plan(end: String = "11:00") = OutfitPlan(
        "event-1", "Class", "2026-09-16", "09:00", end, "Class", "Relaxed",
        WeatherPlace("Austin", 30.27, -97.74), EventWeather(24.5, "Clear", "0.0 mm", "America/Chicago")
    )

    @Test fun requestIncludesDestinationOffsetAndCelsiusWeather() {
        val event = plan().toSchedule()
        assertEquals("2026-09-16T09:00-05:00", event.startTime)
        assertEquals(24.5, event.weather.temperatureC, 0.0)
        assertTrue(event.activity.contains("Austin"))
        val json = Gson().toJson(event)
        assertTrue(json.contains("\"temperature_c\":24.5"))
        assertTrue(json.contains("\"event_id\":\"event-1\""))
    }

    @Test(expected = IllegalArgumentException::class)
    fun rejectsEndBeforeStart() { plan("08:00").toSchedule() }

    @Test fun savedPlansRoundTripWithoutLosingWeather() {
        val value = plan()
        assertEquals(value, Gson().fromJson(Gson().toJson(value), OutfitPlan::class.java))
    }
}
