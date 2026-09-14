package com.example.wearthis.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

private val DarkColorScheme = darkColorScheme(
    primary = DarkBerry,
    onPrimary = Color(0xFF3E2833),
    primaryContainer = Color(0xFF533847),
    onPrimaryContainer = Color(0xFFF6DBE6),
    secondary = DarkSage,
    onSecondary = Color(0xFF22382D),
    secondaryContainer = Color(0xFF394F43),
    onSecondaryContainer = Color(0xFFD2E9DA),
    tertiary = DarkTerracotta,
    onTertiary = Color(0xFF512310),
    tertiaryContainer = Color(0xFF6E3923),
    onTertiaryContainer = Color(0xFFFFDBCA),
    background = DarkBackground,
    onBackground = DarkOnSurface,
    surface = DarkSurface,
    onSurface = DarkOnSurface,
    surfaceVariant = DarkSurfaceVariant,
    onSurfaceVariant = Color(0xFFD1C4C8),
    outline = DarkOutline,
    error = Color(0xFFFFB4AB)
)

private val LightColorScheme = lightColorScheme(
    primary = WearThisBerry,
    onPrimary = Color.White,
    primaryContainer = BerryContainer,
    onPrimaryContainer = OnBerryContainer,
    secondary = WearThisSage,
    onSecondary = Color.White,
    secondaryContainer = SageContainer,
    onSecondaryContainer = OnSageContainer,
    tertiary = WearThisTerracotta,
    onTertiary = Color.White,
    tertiaryContainer = TerracottaContainer,
    onTertiaryContainer = OnTerracottaContainer,
    background = WarmIvory,
    onBackground = Charcoal,
    surface = WarmWhite,
    onSurface = Charcoal,
    surfaceVariant = SoftCream,
    onSurfaceVariant = MutedCharcoal,
    outline = LightOutline,
    outlineVariant = LightOutlineVariant,
    error = ErrorRed
)

@Composable
fun WearThisTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }

        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}