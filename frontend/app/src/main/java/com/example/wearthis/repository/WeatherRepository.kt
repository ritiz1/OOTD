package com.example.wearthis.repository

import android.annotation.SuppressLint
import android.content.Context
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Bundle
import android.os.Looper
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeout
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.HttpUrl.Companion.toHttpUrl
import org.json.JSONObject
import java.time.LocalDateTime
import java.time.ZoneId
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException

// Weather requests use a separate client, so the OOTD bearer token never leaves our API.
data class WeatherPlace(val name: String, val latitude: Double, val longitude: Double)
data class EventWeather(val temperatureC: Double, val status: String, val precipitation: String, val timezone: String)

class WeatherRepository(private val context: Context) {
    private val client = OkHttpClient.Builder().callTimeout(20, java.util.concurrent.TimeUnit.SECONDS).build()

    suspend fun search(query: String): List<WeatherPlace> = withContext(Dispatchers.IO) {
        val url = "https://geocoding-api.open-meteo.com/v1/search".toHttpUrl().newBuilder()
            .addQueryParameter("name", query.trim()).addQueryParameter("count", "5").build()
        val json = get(url.toString())
        val results = json.optJSONArray("results") ?: return@withContext emptyList()
        (0 until results.length()).map { index ->
            val item = results.getJSONObject(index)
            WeatherPlace(listOf(item.getString("name"), item.optString("admin1"), item.optString("country"))
                .filter { it.isNotBlank() }.distinct().joinToString(", "),
                item.getDouble("latitude"), item.getDouble("longitude"))
        }
    }

    suspend fun forecast(place: WeatherPlace, time: LocalDateTime?): EventWeather = withContext(Dispatchers.IO) {
        val url = "https://api.open-meteo.com/v1/forecast".toHttpUrl().newBuilder()
            .addQueryParameter("latitude", place.latitude.toString())
            .addQueryParameter("longitude", place.longitude.toString())
            .addQueryParameter("hourly", "temperature_2m,weather_code,precipitation")
            .addQueryParameter("current", "temperature_2m,weather_code,precipitation")
            .addQueryParameter("timezone", "auto").addQueryParameter("forecast_days", "16").build()
        val json = get(url.toString())
        val timezone = json.getString("timezone")
        if (time == null) {
            val current = json.getJSONObject("current")
            return@withContext EventWeather(current.getDouble("temperature_2m"),
                condition(current.getInt("weather_code")), "${current.getDouble("precipitation")} mm", timezone)
        }
        require(time.isAfter(LocalDateTime.now(ZoneId.of(timezone)))) { "Choose a future time at your destination." }
        val hourly = json.getJSONObject("hourly")
        val times = hourly.getJSONArray("time")
        val hour = time.withMinute(0).withSecond(0).withNano(0)
        val index = (0 until times.length()).firstOrNull { LocalDateTime.parse(times.getString(it)) == hour }
            ?: error("Weather is available for the next 16 days. Choose a nearer date.")
        EventWeather(hourly.getJSONArray("temperature_2m").getDouble(index),
            condition(hourly.getJSONArray("weather_code").getInt(index)),
            "${hourly.getJSONArray("precipitation").getDouble(index)} mm", timezone)
    }

    @SuppressLint("MissingPermission")
    suspend fun currentPlace(): WeatherPlace = withTimeout(20_000) {
        withContext(Dispatchers.Main) {
            val manager = context.getSystemService(Context.LOCATION_SERVICE) as LocationManager
            val provider = listOf(LocationManager.NETWORK_PROVIDER, LocationManager.GPS_PROVIDER)
                .firstOrNull { manager.isProviderEnabled(it) }
                ?: error("Turn on location services or search for your city.")
            val location = suspendCancellableCoroutine<Location> { continuation ->
                val listener = object : LocationListener {
                    override fun onLocationChanged(location: Location) {
                        manager.removeUpdates(this)
                        if (continuation.isActive) continuation.resume(location)
                    }
                    override fun onProviderDisabled(provider: String) {
                        manager.removeUpdates(this)
                        if (continuation.isActive) continuation.resumeWithException(IllegalStateException("Location is disabled. Search for your city."))
                    }
                    override fun onProviderEnabled(provider: String) = Unit
                    @Deprecated("Platform callback")
                    override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) = Unit
                }
                continuation.invokeOnCancellation { manager.removeUpdates(listener) }
                manager.requestSingleUpdate(provider, listener, Looper.getMainLooper())
            }
            WeatherPlace("Current location", location.latitude, location.longitude)
        }
    }

    private fun get(url: String): JSONObject = client.newCall(Request.Builder().url(url).build()).execute().use {
        check(it.isSuccessful) { "Weather is unavailable right now. Please retry." }
        JSONObject(it.body?.string() ?: error("Empty weather response."))
    }

    private fun condition(code: Int) = when (code) {
        0 -> "Clear"
        1, 2 -> "Partly cloudy"
        3 -> "Cloudy"
        45, 48 -> "Foggy"
        in 51..67, in 80..82 -> "Rainy"
        in 71..77, 85, 86 -> "Snowy"
        in 95..99 -> "Thunderstorms"
        else -> "Changeable"
    }
}
