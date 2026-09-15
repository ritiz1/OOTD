package com.example.wearthis.view.auth

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.*
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.wearthis.feature.auth.AuthEvent
import com.example.wearthis.feature.auth.AuthUiState

/** State flows down, events flow up. Only password visibility is local presentation state. */
@Composable
fun AuthScreen(
    state: AuthUiState,
    isSignUp: Boolean,
    onEvent: (AuthEvent) -> Unit,
    onSwitchMode: () -> Unit,
    modifier: Modifier = Modifier,
    onGoogleClick: (() -> Unit)? = null,
    onForgotPasswordClick: (() -> Unit)? = null,
    onBackClick: (() -> Unit)? = null
) {
    val colors = MaterialTheme.colorScheme
    val focusManager = LocalFocusManager.current
    var passwordVisible by rememberSaveable { mutableStateOf(false) }
    val submit = {
        if (!state.isLoading) {
            focusManager.clearFocus()
            onEvent(AuthEvent.Submit)
        }
    }
    BoxWithConstraints(
        modifier = modifier.fillMaxSize().background(colors.background)
            .safeDrawingPadding().imePadding(),
        contentAlignment = Alignment.TopCenter
    ) {
        val minimumHeight = maxHeight
        Column(
            modifier = Modifier.widthIn(max = 480.dp).fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .heightIn(min = minimumHeight)
                .padding(horizontal = 28.dp)
        ) {
            Box(Modifier.fillMaxWidth().padding(top = 12.dp).heightIn(min = 56.dp)) {
                if (onBackClick != null) {
                    IconButton(onClick = onBackClick, enabled = !state.isLoading,
                        modifier = Modifier.align(Alignment.CenterStart)) {
                        AuthIcon(AuthSymbol.Back, colors.onSurfaceVariant)
                    }
                }
                Text("OOTD", modifier = Modifier.align(Alignment.Center),
                    style = MaterialTheme.typography.titleLarge.copy(letterSpacing = 5.sp),
                    color = colors.primary)
            }
            Row(Modifier.fillMaxWidth().padding(top = 22.dp), horizontalArrangement = Arrangement.End) {
                Text("STYLE\nA BRIGHTER\nYOU", style = MaterialTheme.typography.labelSmall.copy(
                    fontSize = 8.sp, lineHeight = 13.sp, letterSpacing = 2.sp), color = colors.outline)
            }
            Spacer(Modifier.height(22.dp))
            Text(if (isSignUp) "Create your\naccount." else "Welcome\nback.",
                style = MaterialTheme.typography.displayMedium, color = colors.primary)
            Spacer(Modifier.height(14.dp))
            Text(if (isSignUp) "Your closet is about to get a lot smarter."
                else "Your closet. Fresh possibilities.",
                style = MaterialTheme.typography.bodyLarge, color = colors.onSurfaceVariant)
            Spacer(Modifier.height(28.dp))
            Column(Modifier.fillMaxWidth().animateContentSize()) {
                AuthField(value = state.email, onValueChange = { onEvent(AuthEvent.EmailChanged(it)) },
                    label = "Email", error = state.emailError, enabled = !state.isLoading,
                    symbol = AuthSymbol.Email,
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email, imeAction = ImeAction.Next),
                    keyboardActions = KeyboardActions(onNext = { focusManager.moveFocus(androidx.compose.ui.focus.FocusDirection.Down) }))
                Spacer(Modifier.height(12.dp))
                AuthField(value = state.password, onValueChange = { onEvent(AuthEvent.PasswordChanged(it)) },
                    label = "Password", error = state.passwordError, enabled = !state.isLoading,
                    symbol = AuthSymbol.Lock,
                    visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password, imeAction = ImeAction.Done),
                    keyboardActions = KeyboardActions(onDone = { submit() }),
                    trailingIcon = {
                        IconButton(onClick = { passwordVisible = !passwordVisible }, enabled = !state.isLoading) {
                            AuthIcon(if (passwordVisible) AuthSymbol.Hide else AuthSymbol.Eye,
                                colors.onSurfaceVariant)
                        }
                    })
                if (!isSignUp && onForgotPasswordClick != null) {
                    TextButton(onClick = onForgotPasswordClick, enabled = !state.isLoading,
                        modifier = Modifier.align(Alignment.End)) { Text("Forgot password?") }
                }
                AnimatedVisibility(state.errorMessage != null) {
                    Text(state.errorMessage.orEmpty(), color = colors.error,
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.padding(top = 12.dp).semantics { liveRegion = LiveRegionMode.Polite })
                }
                Spacer(Modifier.height(22.dp))
                Button(onClick = submit, enabled = !state.isLoading,
                    modifier = Modifier.fillMaxWidth().heightIn(min = 56.dp),
                    shape = RoundedCornerShape(10.dp)) {
                    Box(Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                        if (state.isLoading) {
                            CircularProgressIndicator(Modifier.size(24.dp), strokeWidth = 2.dp,
                                color = colors.onSurface)
                        } else {
                            Text(if (isSignUp) "Create account" else "Sign in",
                                style = MaterialTheme.typography.titleMedium)
                            AuthIcon(AuthSymbol.Arrow, LocalContentColor.current, Modifier.align(Alignment.CenterEnd))
                        }
                    }
                }
                Row(Modifier.fillMaxWidth().padding(vertical = 20.dp), verticalAlignment = Alignment.CenterVertically) {
                    HorizontalDivider(Modifier.weight(1f), color = colors.outlineVariant)
                    Text("or", Modifier.padding(horizontal = 14.dp), color = colors.outline,
                        style = MaterialTheme.typography.bodyMedium)
                    HorizontalDivider(Modifier.weight(1f), color = colors.outlineVariant)
                }
                OutlinedButton(onClick = { onGoogleClick?.invoke() }, enabled = onGoogleClick != null && !state.isLoading,
                    modifier = Modifier.fillMaxWidth().heightIn(min = 52.dp),
                    shape = RoundedCornerShape(10.dp), border = BorderStroke(1.dp, colors.outline)) {
                    Text("G", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.width(16.dp))
                    Text("Continue with Google", style = MaterialTheme.typography.bodyMedium)
                }
                if (onGoogleClick == null) {
                    Text("Google sign-in coming soon", modifier = Modifier.align(Alignment.CenterHorizontally).padding(top = 8.dp),
                        style = MaterialTheme.typography.labelSmall, color = colors.onSurfaceVariant)
                }
            }
            Spacer(Modifier.height(24.dp))
            Column(Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
                Text(if (isSignUp) "Already have an account?" else "New to Wear This?",
                    style = MaterialTheme.typography.bodyMedium, color = colors.onSurfaceVariant)
                TextButton(onClick = onSwitchMode, enabled = !state.isLoading) {
                    Text(if (isSignUp) "Sign in" else "Create an account")
                }
            }
            Spacer(Modifier.weight(1f))
            Box(Modifier.fillMaxWidth().height(110.dp)) {
                Text("CLOTHES.\nIDEAS.\nA BRIGHTER YOU.",
                    modifier = Modifier.align(Alignment.BottomStart).padding(bottom = 24.dp),
                    style = MaterialTheme.typography.labelSmall.copy(fontSize = 7.sp, lineHeight = 12.sp, letterSpacing = 1.5.sp),
                    color = colors.outline)
                BotanicalDetail(Modifier.align(Alignment.BottomEnd).size(100.dp, 110.dp))
            }
        }
    }
}

@Composable
private fun AuthField(
    value: String, onValueChange: (String) -> Unit, label: String, error: String?,
    enabled: Boolean, symbol: AuthSymbol, keyboardOptions: KeyboardOptions,
    keyboardActions: KeyboardActions,
    visualTransformation: VisualTransformation = VisualTransformation.None,
    trailingIcon: (@Composable () -> Unit)? = null
) {
    OutlinedTextField(value = value, onValueChange = onValueChange,
        modifier = Modifier.fillMaxWidth(), enabled = enabled, singleLine = true,
        label = { Text(label) }, shape = RoundedCornerShape(10.dp),
        textStyle = MaterialTheme.typography.bodyLarge,
        leadingIcon = { AuthIcon(symbol, MaterialTheme.colorScheme.onSurfaceVariant) },
        trailingIcon = trailingIcon, isError = error != null,
        supportingText = if (error != null) ({ Text(error, Modifier.semantics { liveRegion = LiveRegionMode.Polite }) }) else null,
        visualTransformation = visualTransformation, keyboardOptions = keyboardOptions,
        keyboardActions = keyboardActions,
        colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = MaterialTheme.colorScheme.outlineVariant))
}

private enum class AuthSymbol { Email, Lock, Eye, Hide, Back, Arrow }

@Composable
private fun AuthIcon(symbol: AuthSymbol, color: Color, modifier: Modifier = Modifier) {
    val description = when (symbol) {
        AuthSymbol.Back -> "Back"
        AuthSymbol.Eye -> "Show password"
        AuthSymbol.Hide -> "Hide password"
        else -> null
    }
    val vector = remember(symbol) {
        androidx.compose.ui.graphics.vector.ImageVector.Builder(
            defaultWidth = 24.dp, defaultHeight = 24.dp, viewportWidth = 24f, viewportHeight = 24f
        ).apply {
            val nodes = androidx.compose.ui.graphics.vector.PathParser().parsePathString(when (symbol) {
                AuthSymbol.Email -> "M4,5 L20,5 L20,19 L4,19 Z M4,6 L12,13 L20,6"
                AuthSymbol.Lock -> "M6,10 L18,10 L18,21 L6,21 Z M8,10 L8,7 C8,1 16,1 16,7 L16,10 M12,14 L12,17"
                AuthSymbol.Eye -> "M2,12 Q12,0 22,12 Q12,24 2,12 Z M15,12 A3,3 0,1 1,9 12 A3,3 0,1 1,15 12"
                AuthSymbol.Hide -> "M2,12 Q12,0 22,12 Q12,24 2,12 Z M3,3 L21,21"
                AuthSymbol.Back -> "M15,4 L7,12 L15,20"
                AuthSymbol.Arrow -> "M4,12 L20,12 M13,5 L20,12 L13,19"
            }).toNodes()
            addPath(nodes, stroke = androidx.compose.ui.graphics.SolidColor(Color.Black), strokeLineWidth = 1.3f)
        }.build()
    }
    Icon(vector, contentDescription = description, tint = color, modifier = modifier.size(22.dp))
}

@Composable
private fun BotanicalDetail(modifier: Modifier = Modifier) {
    val color = MaterialTheme.colorScheme.tertiary.copy(alpha = 0.22f)
    Canvas(modifier) {
        val path = Path().apply {
            moveTo(size.width * .85f, size.height)
            cubicTo(size.width * .7f, size.height * .6f, size.width * .6f, size.height * .3f, size.width * .93f, 0f)
            cubicTo(size.width * .3f, size.height * .08f, size.width * .65f, size.height * .6f, size.width * .85f, size.height)
            moveTo(size.width * .78f, size.height * .8f)
            cubicTo(size.width * .65f, size.height * .45f, size.width * .2f, size.height * .35f, size.width * .1f, size.height * .4f)
            cubicTo(size.width * .3f, size.height * .66f, size.width * .55f, size.height * .58f, size.width * .78f, size.height * .8f)
        }
        drawPath(path, color, style = Stroke(width = 1.dp.toPx()))
        drawLine(color, Offset(size.width * .85f, size.height), Offset(size.width * .93f, size.height * .48f), 1.dp.toPx())
    }
}
