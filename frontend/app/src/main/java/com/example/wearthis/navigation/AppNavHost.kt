package com.example.wearthis.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.wearthis.data.local.OnboardingPreferences
import com.example.wearthis.view.auth.LoginScreen
import com.example.wearthis.view.auth.SignUpScreen
import com.example.wearthis.view.closet.AddClothingScreen
import com.example.wearthis.view.home.HomeScreen
import com.example.wearthis.view.onboarding.OnboardingScreen

@Composable
fun AppNavHost() {
    val navController = rememberNavController()
    val context = LocalContext.current
    val onboardingPreferences = remember(context) {
        OnboardingPreferences(context.applicationContext)
    }
    val startDestination = remember {
        if (com.example.wearthis.data.AppContainer.get(context).sessionStore.accessToken != null) {
            Routes.Home
        } else if (onboardingPreferences.shouldShowOnboarding()) {
            Routes.Onboarding
        } else {
            Routes.Login
        }
    }

    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable(Routes.Onboarding) {
            OnboardingScreen(
                onGetStarted = {
                    onboardingPreferences.markOnboardingCompleted()
                    navController.navigate(Routes.SignUp)
                },
                onSignIn = {
                    onboardingPreferences.markOnboardingCompleted()
                    navController.navigate(Routes.Login)
                }
            )
        }

        composable(Routes.Login) {
            LoginScreen(
                onLoginClick = {
                    navController.navigateAfterAuth()
                },
                onSignUpClick = {
                    navController.navigate(Routes.SignUp)
                }
            )
        }

        composable(Routes.SignUp) {
            SignUpScreen(
                onSignUpClick = {
                    navController.navigateAfterAuth()
                },
                onLoginClick = {
                    if (!navController.popBackStack(Routes.Login, inclusive = false)) {
                        navController.navigate(Routes.Login) {
                            popUpTo(Routes.SignUp) { inclusive = true }
                        }
                    }
                }
            )
        }

        composable(Routes.AddClothing) {
            AddClothingScreen(
                onSaved = {
                    navController.popBackStack()
                },
                onBack = {
                    if (!navController.popBackStack()) {
                        navController.navigate(Routes.Home) {
                            popUpTo(Routes.AddClothing) { inclusive = true }
                        }
                    }
                }
            )
        }

        composable(Routes.Home) {
            HomeScreen(
                onAddClothing = {
                    navController.navigate(Routes.AddClothing)
                },
                onSignOut = {
                    com.example.wearthis.data.AppContainer.get(context).sessionStore.clear()
                    navController.navigate(Routes.Login) {
                        popUpTo(navController.graph.id) { inclusive = true }
                        launchSingleTop = true
                    }
                }
            )
        }
    }
}

private fun NavHostController.navigateAfterAuth() {
    navigate(Routes.Home) {
        popUpTo(graph.id) { inclusive = true }
        launchSingleTop = true
    }
}
