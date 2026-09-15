package com.example.wearthis.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.wearthis.data.AppContainer
import com.example.wearthis.domain.model.*
import com.example.wearthis.repository.*
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.TimeoutCancellationException
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.LocalTime
import java.util.UUID

data class MainUiState(
    val items: List<ClothingItem> = emptyList(), val loading: Boolean = true,
    val user: AuthUser? = null, val plans: List<OutfitPlan> = emptyList(),
    val places: List<WeatherPlace> = emptyList(), val place: WeatherPlace? = null,
    val weather: EventWeather? = null, val weatherBusy: Boolean = false,
    val busy: Boolean = false, val error: String? = null, val message: String? = null,
    val selectedPlan: OutfitPlan? = null
)

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val container = AppContainer.get(application)
    private val weatherRepository = WeatherRepository(application)
    private val preferences = application.getSharedPreferences("outfit_plans", 0)
    private val userId = container.sessionStore.userId.orEmpty()
    private val gson = Gson()
    private val _state = MutableStateFlow(MainUiState())
    val state = _state.asStateFlow()

    init {
        val plans = runCatching {
            gson.fromJson<List<OutfitPlan>>(preferences.getString(userId, "[]"),
                object : TypeToken<List<OutfitPlan>>() {}.type)
        }.getOrDefault(emptyList())
        _state.update { it.copy(plans = plans) }
        viewModelScope.launch {
            container.clothingRepository.observeClothing().collect { items ->
                _state.update { it.copy(items = items, loading = false) }
            }
        }
        refresh()
        loadProfile()
    }

    fun dismiss() { _state.update { it.copy(error = null, message = null) } }
    fun report(message: String) { _state.update { it.copy(error = message) } }
    fun selectPlan(plan: OutfitPlan?) { _state.update { it.copy(selectedPlan = plan) } }
    fun refresh() = viewModelScope.launch {
        container.clothingRepository.refresh().onFailure { report(it.message ?: "Couldn't refresh your wardrobe.") }
    }
    fun loadProfile() = viewModelScope.launch {
        container.profileRepository.getProfile().fold(
            { user -> _state.update { it.copy(user = user) } },
            { report(it.message ?: "Couldn't load your profile.") })
    }
    fun saveProfile(first: String, last: String) = action {
        val user = container.profileRepository.updateProfile(first.trim(), last.trim()).getOrThrow()
        _state.update { it.copy(user = user, message = "Profile updated") }
    }
    fun delete(item: ClothingItem) = action { container.clothingRepository.deleteClothing(item.localId) }
    fun retry(item: ClothingItem) = action { container.clothingRepository.retryUpload(item.localId).getOrThrow() }

    fun search(query: String) = weatherAction {
        require(query.trim().length >= 2) { "Enter a city or postal code." }
        val places = weatherRepository.search(query)
        _state.update { it.copy(places = places) }
        if (places.isEmpty()) error("No locations found. Try a nearby city or postal code.")
    }
    fun useCurrentLocation() = weatherAction {
        val place = weatherRepository.currentPlace()
        val weather = weatherRepository.forecast(place, null)
        _state.update { it.copy(place = place, weather = weather, places = emptyList()) }
    }
    fun choosePlace(place: WeatherPlace) = weatherAction {
        val weather = weatherRepository.forecast(place, null)
        _state.update { it.copy(place = place, weather = weather, places = emptyList()) }
    }

    fun createPlan(title: String, date: String, start: String, end: String, occasion: String, vibe: String) = action {
        require(title.isNotBlank()) { "Give your event a name." }
        val day = LocalDate.parse(date)
        require(LocalTime.parse(end).isAfter(LocalTime.parse(start))) { "End time must be after start time." }
        val place = _state.value.place ?: error("Select a city or use your location first.")
        val weather = weatherRepository.forecast(place, day.atTime(LocalTime.parse(start)))
        val plan = OutfitPlan(UUID.randomUUID().toString(), title.trim(), date, start, end, occasion, vibe, place, weather)
        _state.update { it.copy(plans = (it.plans + plan).sortedBy { p -> p.date + p.start }, selectedPlan = plan) }
        persist()
        recommend(plan)
    }

    fun regenerate(plan: OutfitPlan) = action { recommend(plan) }
    private suspend fun recommend(plan: OutfitPlan) {
        require(_state.value.items.any { it.uploadStatus == UploadStatus.UPLOADED }) {
            "Your event is saved. Add clothing to your wardrobe, then try outfit ideas again."
        }
        val weather = weatherRepository.forecast(plan.place, LocalDate.parse(plan.date).atTime(LocalTime.parse(plan.start)))
        val fresh = plan.copy(weather = weather)
        val recommendations = container.recommendationRepository.getRecommendations(listOf(fresh.toSchedule())).getOrThrow()
        val updated = fresh.copy(recommendations = recommendations)
        _state.update { it.copy(plans = it.plans.map { p -> if (p.id == plan.id) updated else p }, selectedPlan = updated) }
        persist()
    }
    fun removePlan(plan: OutfitPlan) {
        if (_state.value.busy) return
        _state.update { it.copy(plans = it.plans.filterNot { p -> p.id == plan.id }, selectedPlan = null) }
        persist()
    }
    private fun persist() { preferences.edit().putString(userId, gson.toJson(_state.value.plans)).apply() }

    private fun action(block: suspend () -> Unit) {
        if (_state.value.busy) return
        _state.update { it.copy(busy = true, error = null) }
        viewModelScope.launch {
            try { block() } catch (error: Exception) {
                if (error is CancellationException) throw error
                report(error.message ?: "Something went wrong. Please retry.")
            } finally { _state.update { it.copy(busy = false) } }
        }
    }
    private fun weatherAction(block: suspend () -> Unit) {
        if (_state.value.weatherBusy) return
        _state.update { it.copy(weatherBusy = true, error = null) }
        viewModelScope.launch {
            try { block() } catch (error: Exception) {
                if (error is CancellationException && error !is TimeoutCancellationException) throw error
                report(if (error is TimeoutCancellationException) "Location timed out. Search for your city instead."
                    else error.message ?: "Weather is unavailable. Please retry.")
            } finally { _state.update { it.copy(weatherBusy = false) } }
        }
    }
}
