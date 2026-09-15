package com.example.wearthis.repository

import com.example.wearthis.data.dto.RecommendRequestDto
import com.example.wearthis.data.dto.ScheduleEventDto
import com.example.wearthis.data.dto.TimeRecommendationDto
import com.example.wearthis.data.remote.ApiService
import com.example.wearthis.data.remote.toApiException

interface RecommendationRepository {
    suspend fun getRecommendations(
        schedule: List<ScheduleEventDto>
    ): Result<List<TimeRecommendationDto>>
}

class DefaultRecommendationRepository(
    private val apiService: ApiService
) : RecommendationRepository {
    override suspend fun getRecommendations(
        schedule: List<ScheduleEventDto>
    ): Result<List<TimeRecommendationDto>> {
        require(schedule.isNotEmpty()) { "Add at least one schedule event." }

        return runCatching {
            apiService.recommend(RecommendRequestDto(schedule)).recommendations
        }.recoverCatching {
            throw it.toApiException("Unable to create outfit recommendations.")
        }
    }
}
