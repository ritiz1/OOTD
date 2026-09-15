package com.example.wearthis.view.auth

import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.wearthis.feature.auth.AuthEvent
import com.example.wearthis.feature.auth.AuthMode
import com.example.wearthis.feature.auth.AuthUiState
import com.example.wearthis.ui.theme.WearThisTheme
import com.example.wearthis.viewmodel.AuthViewModel

@Composable
fun LoginScreen(
    onLoginClick: () -> Unit,
    onSignUpClick: () -> Unit,
    modifier: Modifier = Modifier,
    onGoogleClick: (() -> Unit)? = null,
    onForgotPasswordClick: (() -> Unit)? = null,
    authViewModel: AuthViewModel = viewModel(
        factory = AuthViewModel.Factory(AuthMode.Login)
    )
) {
    val state by authViewModel.uiState.collectAsState()

    LaunchedEffect(state.isAuthenticated) {
        if (state.isAuthenticated) {
            onLoginClick()
            authViewModel.onEvent(AuthEvent.AuthenticationHandled)
        }
    }

    AuthScreen(
        state = state,
        isSignUp = false,
        onEvent = authViewModel::onEvent,
        onSwitchMode = onSignUpClick,
        modifier = modifier,
        onGoogleClick = onGoogleClick,
        onForgotPasswordClick = onForgotPasswordClick
    )
}

@Preview(showBackground = true, widthDp = 390, heightDp = 844)
@Composable
private fun LoginPreview() {
    WearThisTheme {
        AuthScreen(
            state = AuthUiState(),
            isSignUp = false,
            onEvent = {},
            onSwitchMode = {}
        )
    }
}

@Preview(showBackground = true, widthDp = 390, heightDp = 844)
@Composable
private fun LoginDarkPreview() {
    WearThisTheme(darkTheme = true) {
        AuthScreen(
            state = AuthUiState(),
            isSignUp = false,
            onEvent = {},
            onSwitchMode = {}
        )
    }
}
