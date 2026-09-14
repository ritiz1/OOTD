package com.example.wearthis.view.auth

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.wearthis.ui.theme.WearThisTheme

@Composable
fun SignUpScreen(
    onSignUpClick: () -> Unit,
    onLoginClick: () -> Unit,
    modifier: Modifier = Modifier,
    onSubmitCredentials: ((String, String) -> Unit)? = null,
    onGoogleClick: (() -> Unit)? = null
) {
    RememberedAuthScreen(
        isSignUp = true,
        onSubmit = { email, password ->
            onSubmitCredentials?.invoke(email, password) ?: onSignUpClick()
        },
        onSwitchMode = onLoginClick,
        modifier = modifier,
        onGoogleClick = onGoogleClick,
        onBackClick = onLoginClick
    )
}

@Preview(showBackground = true, widthDp = 390, heightDp = 844)
@Composable
private fun SignUpPreview() {
    WearThisTheme { SignUpScreen({}, {}) }
}

@Preview(showBackground = true, widthDp = 320, heightDp = 640, fontScale = 1.3f)
@Composable
private fun SignUpCompactPreview() {
    WearThisTheme { SignUpScreen({}, {}) }
}
