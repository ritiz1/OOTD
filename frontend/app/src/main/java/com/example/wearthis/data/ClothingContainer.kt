package com.example.wearthis.data

import android.content.Context
import com.example.wearthis.data.local.AppDatabase
import com.example.wearthis.data.local.ClothingImageStorage
import com.example.wearthis.data.remote.MockClothingRemoteDataSource
import com.example.wearthis.repository.ClothingRepository
import com.example.wearthis.repository.DefaultClothingRepository

object ClothingContainer {
    @Volatile
    private var repositoryInstance: ClothingRepository? = null

    fun repository(context: Context): ClothingRepository {
        return repositoryInstance ?: synchronized(this) {
            repositoryInstance ?: DefaultClothingRepository(
                clothingDao = AppDatabase.getInstance(context).clothingDao(),
                imageStorage = ClothingImageStorage(context.applicationContext),
                remoteDataSource = MockClothingRemoteDataSource()
            ).also { repositoryInstance = it }
        }
    }
}
