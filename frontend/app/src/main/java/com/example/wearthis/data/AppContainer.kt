package com.example.wearthis.data

import android.content.Context
import com.example.wearthis.data.local.AppDatabase
import com.example.wearthis.data.local.AuthSessionStore
import com.example.wearthis.data.local.ClothingImageStorage
import com.example.wearthis.data.remote.ApiClient
import com.example.wearthis.data.remote.RetrofitClothingRemoteDataSource
import com.example.wearthis.repository.AuthRepository
import com.example.wearthis.repository.ClothingRepository
import com.example.wearthis.repository.DefaultClothingRepository
import com.example.wearthis.repository.DefaultProfileRepository
import com.example.wearthis.repository.DefaultRecommendationRepository
import com.example.wearthis.repository.ProfileRepository
import com.example.wearthis.repository.RecommendationRepository
import com.example.wearthis.repository.RemoteAuthRepository

class AppContainer private constructor(context: Context) {
    val sessionStore = AuthSessionStore(context)
    private val apiService = ApiClient.create(sessionStore)

    val authRepository: AuthRepository = RemoteAuthRepository(apiService, sessionStore)
    val profileRepository: ProfileRepository = DefaultProfileRepository(apiService)
    val recommendationRepository: RecommendationRepository =
        DefaultRecommendationRepository(apiService)
    val clothingRepository: ClothingRepository = DefaultClothingRepository(
        clothingDao = AppDatabase.getInstance(context).clothingDao(),
        imageStorage = ClothingImageStorage(context),
        remoteDataSource = RetrofitClothingRemoteDataSource(apiService)
    )

    companion object {
        @Volatile
        private var instance: AppContainer? = null

        fun get(context: Context): AppContainer {
            return instance ?: synchronized(this) {
                instance ?: AppContainer(context.applicationContext)
                    .also { instance = it }
            }
        }
    }
}
