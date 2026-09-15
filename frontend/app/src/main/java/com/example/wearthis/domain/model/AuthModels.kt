package com.example.wearthis.domain.model

data class AuthCredentials(
    val email: String,
    val password: String
)

data class AuthUser(
    val id: String,
    val email: String,
    val firstName: String = "",
    val lastName: String = ""
)

data class AuthSession(
    val user: AuthUser,
    val accessToken: String,
    val refreshToken: String
)
