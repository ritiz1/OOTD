package com.example.wearthis.data.local

import android.content.Context

class OnboardingPreferences(context: Context) {
    private val preferences = context.getSharedPreferences(
        PREFERENCES_NAME,
        Context.MODE_PRIVATE
    )

    fun shouldShowOnboarding(): Boolean {
        return !preferences.getBoolean(KEY_ONBOARDING_COMPLETED, false)
    }

    fun markOnboardingCompleted() {
        preferences.edit()
            .putBoolean(KEY_ONBOARDING_COMPLETED, true)
            .apply()
    }

    private companion object {
        const val PREFERENCES_NAME = "wearthis_preferences"
        const val KEY_ONBOARDING_COMPLETED = "onboarding_completed"
    }
}
