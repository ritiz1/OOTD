package com.example.wearthis.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.wearthis.view.auth.LoginScreen
import com.example.wearthis.view.auth.SignUpScreen

@Composable
fun AppNavHost() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Routes.Login
    ) {
        composable(Routes.Login) {
            LoginScreen(
                onLoginClick = {
                    // TODO: Navigate to the main app flow after backend auth is connected.
                },
                onSignUpClick = {
                    navController.navigate(Routes.SignUp)
                }
            )
        }

        composable(Routes.SignUp) {
            SignUpScreen(
                onSignUpClick = {
                    // TODO: Navigate to onboarding/profile setup after backend auth is connected.
                },
                onLoginClick = {
                    navController.popBackStack()
                }
            )
        }
    }
}
