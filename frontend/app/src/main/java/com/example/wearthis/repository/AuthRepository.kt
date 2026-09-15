package com.example.wearthis.repository

import com.example.wearthis.domain.model.AuthCredentials
import com.example.wearthis.domain.model.AuthSession
import com.example.wearthis.domain.model.AuthUser
import kotlinx.coroutines.delay

interface AuthRepository {
    suspend fun login(credentials: AuthCredentials): Result<AuthSession>

    suspend fun signUp(credentials: AuthCredentials): Result<AuthSession>
}

/**
 * Local stand-in for the backend. Replace this object with a Retrofit-backed
 * implementation without changing the ViewModel or screens.
 */
object MockAuthRepository : AuthRepository {
    override suspend fun login(credentials: AuthCredentials): Result<AuthSession> {
        delay(MOCK_NETWORK_DELAY_MS)
        return authenticate(credentials)
    }

    override suspend fun signUp(credentials: AuthCredentials): Result<AuthSession> {
        delay(MOCK_NETWORK_DELAY_MS)
        return authenticate(credentials)
    }

    private fun authenticate(credentials: AuthCredentials): Result<AuthSession> {
        if (credentials.email.equals("fail@wearthis.app", ignoreCase = true)) {
            return Result.failure(IllegalStateException("Mock authentication failed."))
        }

        return Result.success(
            AuthSession(
                user = AuthUser(
                    id = "mock-user",
                    email = credentials.email
                ),
                accessToken = "mock-access-token",
                refreshToken = "mock-refresh-token"
            )
        )
    }

    private const val MOCK_NETWORK_DELAY_MS = 700L
}
