package com.example.wearthis.feature.auth

enum class AuthMode {
    Login,
    SignUp
}

data class AuthUiState(
    val email: String = "",
    val password: String = "",
    val emailError: String? = null,
    val passwordError: String? = null,
    val errorMessage: String? = null,
    val isLoading: Boolean = false,
    val isAuthenticated: Boolean = false
)

sealed interface AuthEvent {
    data class EmailChanged(val value: String) : AuthEvent
    data class PasswordChanged(val value: String) : AuthEvent
    data object Submit : AuthEvent
    data object AuthenticationHandled : AuthEvent
}
