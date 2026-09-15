package com.example.wearthis.repository

import com.example.wearthis.data.dto.UpdateUserRequestDto
import com.example.wearthis.data.dto.UserDto
import com.example.wearthis.data.remote.ApiService
import com.example.wearthis.data.remote.toApiException
import com.example.wearthis.domain.model.AuthUser

interface ProfileRepository {
    suspend fun getProfile(): Result<AuthUser>

    suspend fun updateProfile(firstName: String, lastName: String): Result<AuthUser>
}

class DefaultProfileRepository(
    private val apiService: ApiService
) : ProfileRepository {
    override suspend fun getProfile(): Result<AuthUser> {
        return apiCall("Unable to load your profile.") {
            apiService.getCurrentUser()
        }
    }

    override suspend fun updateProfile(
        firstName: String,
        lastName: String
    ): Result<AuthUser> {
        return apiCall("Unable to update your profile.") {
            apiService.updateCurrentUser(
                UpdateUserRequestDto(
                    firstName = firstName,
                    lastName = lastName
                )
            )
        }
    }

    private suspend fun apiCall(
        fallbackMessage: String,
        request: suspend () -> UserDto
    ): Result<AuthUser> {
        return runCatching { request().toDomain() }
            .recoverCatching { throw it.toApiException(fallbackMessage) }
    }
}

private fun UserDto.toDomain(): AuthUser {
    return AuthUser(
        id = id,
        email = email,
        firstName = firstName,
        lastName = lastName
    )
}
