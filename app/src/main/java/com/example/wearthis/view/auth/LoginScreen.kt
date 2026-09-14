package com.example.wearthis.view.auth

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.wearthis.ui.theme.WearThisTheme

@Composable
fun LoginScreen(
    onLoginClick: () -> Unit,
    onSignUpClick: () -> Unit,
    modifier: Modifier = Modifier,
    onSubmitCredentials: ((String, String) -> Unit)? = null,
    onGoogleClick: (() -> Unit)? = null,
    onForgotPasswordClick: (() -> Unit)? = null
) {
    RememberedAuthScreen(
        isSignUp = false,
        onSubmit = { email, password ->
            onSubmitCredentials?.invoke(email, password) ?: onLoginClick()
        },
        onSwitchMode = onSignUpClick,
        modifier = modifier,
        onGoogleClick = onGoogleClick,
        onForgotPasswordClick = onForgotPasswordClick
    )
}

@Preview(showBackground = true, widthDp = 390, heightDp = 844)
@Composable
private fun LoginPreview() {
    WearThisTheme { LoginScreen({}, {}) }
}

@Preview(showBackground = true, widthDp = 390, heightDp = 844)
@Composable
private fun LoginDarkPreview() {
    WearThisTheme(darkTheme = true) { LoginScreen({}, {}) }
}
