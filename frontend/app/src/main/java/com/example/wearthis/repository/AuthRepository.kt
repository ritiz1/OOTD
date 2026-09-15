package com.example.wearthis.repository

import com.example.wearthis.domain.model.AuthCredentials
import com.example.wearthis.domain.model.AuthSession

interface AuthRepository {
    suspend fun login(credentials: AuthCredentials): Result<AuthSession>

    suspend fun signUp(credentials: AuthCredentials): Result<AuthSession>
}
