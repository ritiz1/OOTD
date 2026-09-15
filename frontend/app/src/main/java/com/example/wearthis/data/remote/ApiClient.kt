package com.example.wearthis.data.remote

import com.example.wearthis.BuildConfig
import com.example.wearthis.data.dto.RefreshTokenRequestDto
import com.example.wearthis.data.local.AuthSessionStore
import kotlinx.coroutines.runBlocking
import okhttp3.OkHttpClient
import okhttp3.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object ApiClient {
    fun create(sessionStore: AuthSessionStore): ApiService {
        val publicService = retrofit(OkHttpClient()).create(ApiService::class.java)

        val authenticatedClient = OkHttpClient.Builder()
            .connectTimeout(20, java.util.concurrent.TimeUnit.SECONDS)
            .readTimeout(120, java.util.concurrent.TimeUnit.SECONDS)
            .writeTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
            .addInterceptor { chain ->
                val request = chain.request()
                val token = sessionStore.accessToken
                val authenticatedRequest = if (
                    token != null && !request.url.encodedPath.isPublicAuthPath()
                ) {
                    request.newBuilder()
                        .header("Authorization", "Bearer $token")
                        .build()
                } else {
                    request
                }
                chain.proceed(authenticatedRequest)
            }
            .authenticator { _, response ->
                val path = response.request.url.encodedPath
                if (path.isPublicAuthPath() || response.responseCount() >= 2) {
                    return@authenticator null
                }

                val refreshToken = sessionStore.refreshToken
                    ?: return@authenticator null
                val refreshed = runBlocking {
                    runCatching {
                        publicService.refreshToken(
                            RefreshTokenRequestDto(refreshToken)
                        )
                    }.getOrNull()
                } ?: run {
                    sessionStore.clear()
                    return@authenticator null
                }

                sessionStore.updateAccessToken(refreshed.access)
                response.request.newBuilder()
                    .header("Authorization", "Bearer ${refreshed.access}")
                    .build()
            }
            .build()

        return retrofit(authenticatedClient).create(ApiService::class.java)
    }

    private fun retrofit(client: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    private fun String.isPublicAuthPath(): Boolean {
        return this == "/api/auth/register/" ||
            this == "/api/auth/token/" ||
            this == "/api/auth/token/refresh/"
    }

    private fun Response.responseCount(): Int {
        var count = 1
        var current = priorResponse
        while (current != null) {
            count++
            current = current.priorResponse
        }
        return count
    }
}
