package com.example.wearthis.view.auth

import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.wearthis.data.AppContainer
import com.example.wearthis.feature.auth.AuthEvent
import com.example.wearthis.feature.auth.AuthMode
import com.example.wearthis.feature.auth.AuthUiState
import com.example.wearthis.ui.theme.WearThisTheme
import com.example.wearthis.viewmodel.AuthViewModel

@Composable
fun SignUpScreen(
    onSignUpClick: () -> Unit,
    onLoginClick: () -> Unit,
    modifier: Modifier = Modifier,
    onGoogleClick: (() -> Unit)? = null,
    authViewModel: AuthViewModel = viewModel(
        factory = AuthViewModel.Factory(
            mode = AuthMode.SignUp,
            repository = AppContainer.get(LocalContext.current).authRepository
        )
    )
) {
    val state by authViewModel.uiState.collectAsState()

    LaunchedEffect(state.isAuthenticated) {
        if (state.isAuthenticated) {
            onSignUpClick()
            authViewModel.onEvent(AuthEvent.AuthenticationHandled)
        }
    }

    AuthScreen(
        state = state,
        isSignUp = true,
        onEvent = authViewModel::onEvent,
        onSwitchMode = onLoginClick,
        modifier = modifier,
        onGoogleClick = onGoogleClick,
        onBackClick = onLoginClick
    )
}

@Preview(showBackground = true, widthDp = 390, heightDp = 844)
@Composable
private fun SignUpPreview() {
    WearThisTheme {
        AuthScreen(
            state = AuthUiState(),
            isSignUp = true,
            onEvent = {},
            onSwitchMode = {}
        )
    }
}

@Preview(showBackground = true, widthDp = 320, heightDp = 640, fontScale = 1.3f)
@Composable
private fun SignUpCompactPreview() {
    WearThisTheme {
        AuthScreen(
            state = AuthUiState(),
            isSignUp = true,
            onEvent = {},
            onSwitchMode = {}
        )
    }
}
