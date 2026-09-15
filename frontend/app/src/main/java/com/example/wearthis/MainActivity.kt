package com.example.wearthis

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.wearthis.navigation.AppNavHost
import com.example.wearthis.ui.theme.WearThisTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            WearThisTheme {
                AppNavHost()
            }
        }
    }
}