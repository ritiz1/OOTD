package com.example.wearthis.data.remote

import com.example.wearthis.BuildConfig

fun String.toAbsoluteMediaUrl(): String {
    val trimmed = trim()
    if (trimmed.startsWith("http://") || trimmed.startsWith("https://")) {
        return trimmed
    }
    val base = BuildConfig.API_BASE_URL.trimEnd('/')
    return if (trimmed.startsWith("/")) "$base$trimmed" else "$base/$trimmed"
}
