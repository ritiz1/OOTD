package com.example.wearthis.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.wearthis.domain.model.AuthCredentials
import com.example.wearthis.feature.auth.AuthEvent
import com.example.wearthis.feature.auth.AuthMode
import com.example.wearthis.feature.auth.AuthUiState
import com.example.wearthis.repository.AuthRepository
import com.example.wearthis.repository.MockAuthRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class AuthViewModel(
    private val mode: AuthMode,
    private val repository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(AuthUiState())
    val uiState: StateFlow<AuthUiState> = _uiState.asStateFlow()

    fun onEvent(event: AuthEvent) {
        when (event) {
            is AuthEvent.EmailChanged -> {
                _uiState.update {
                    it.copy(
                        email = event.value,
                        emailError = null,
                        errorMessage = null
                    )
                }
            }

            is AuthEvent.PasswordChanged -> {
                _uiState.update {
                    it.copy(
                        password = event.value,
                        passwordError = null,
                        errorMessage = null
                    )
                }
            }

            AuthEvent.Submit -> submit()
            AuthEvent.AuthenticationHandled -> {
                _uiState.update { it.copy(isAuthenticated = false) }
            }
        }
    }

    private fun submit() {
        val currentState = _uiState.value
        val email = currentState.email.trim()
        val emailError = if (isValidEmail(email)) null else "Enter a valid email address."
        val passwordError = when {
            currentState.password.isBlank() -> "Enter your password."
            mode == AuthMode.SignUp && currentState.password.length < 6 ->
                "Use at least 6 characters."
            else -> null
        }

        if (emailError != null || passwordError != null) {
            _uiState.update {
                it.copy(
                    emailError = emailError,
                    passwordError = passwordError
                )
            }
            return
        }

        _uiState.update {
            it.copy(
                email = email,
                isLoading = true,
                errorMessage = null
            )
        }

        viewModelScope.launch {
            val credentials = AuthCredentials(
                email = email,
                password = currentState.password
            )
            val result = when (mode) {
                AuthMode.Login -> repository.login(credentials)
                AuthMode.SignUp -> repository.signUp(credentials)
            }

            result.fold(
                onSuccess = {
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            isAuthenticated = true
                        )
                    }
                },
                onFailure = { error ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            errorMessage = error.message ?: "Authentication failed. Try again."
                        )
                    }
                }
            )
        }
    }

    private fun isValidEmail(email: String): Boolean {
        return EMAIL_PATTERN.matches(email)
    }

    class Factory(
        private val mode: AuthMode,
        private val repository: AuthRepository = MockAuthRepository
    ) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            require(modelClass.isAssignableFrom(AuthViewModel::class.java))
            return AuthViewModel(mode, repository) as T
        }
    }

    private companion object {
        val EMAIL_PATTERN = Regex("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$")
    }
}
