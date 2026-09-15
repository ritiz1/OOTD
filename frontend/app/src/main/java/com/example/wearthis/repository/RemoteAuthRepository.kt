package com.example.wearthis.repository

import com.example.wearthis.data.dto.AuthResponseDto
import com.example.wearthis.data.dto.LoginRequestDto
import com.example.wearthis.data.dto.RegisterRequestDto
import com.example.wearthis.data.local.AuthSessionStore
import com.example.wearthis.data.remote.ApiService
import com.example.wearthis.data.remote.toApiException
import com.example.wearthis.domain.model.AuthCredentials
import com.example.wearthis.domain.model.AuthSession
import com.example.wearthis.domain.model.AuthUser

class RemoteAuthRepository(
    private val apiService: ApiService,
    private val sessionStore: AuthSessionStore
) : AuthRepository {
    override suspend fun login(credentials: AuthCredentials): Result<AuthSession> {
        return requestSession("Unable to sign in.") {
            apiService.login(
                LoginRequestDto(
                    email = credentials.email,
                    password = credentials.password
                )
            )
        }
    }

    override suspend fun signUp(credentials: AuthCredentials): Result<AuthSession> {
        return requestSession("Unable to create your account.") {
            apiService.register(
                RegisterRequestDto(
                    email = credentials.email,
                    password = credentials.password,
                    passwordConfirm = credentials.password
                )
            )
        }
    }

    private suspend fun requestSession(
        errorMessage: String,
        request: suspend () -> AuthResponseDto
    ): Result<AuthSession> {
        return runCatching {
            request().toDomain().also(sessionStore::save)
        }.recoverCatching { error ->
            throw error.toApiException(errorMessage)
        }
    }
}

private fun AuthResponseDto.toDomain(): AuthSession {
    return AuthSession(
        user = AuthUser(
            id = user.id,
            email = user.email,
            firstName = user.firstName,
            lastName = user.lastName
        ),
        accessToken = access,
        refreshToken = refresh
    )
}
