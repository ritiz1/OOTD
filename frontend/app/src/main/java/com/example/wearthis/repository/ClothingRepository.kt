package com.example.wearthis.repository

import com.example.wearthis.domain.model.ClothingItem
import kotlinx.coroutines.flow.Flow

interface ClothingRepository {
    fun observeClothing(): Flow<List<ClothingItem>>

    suspend fun addClothing(
        userId: String,
        selectedImageUri: String
    ): Result<ClothingItem>

    suspend fun retryUpload(localId: String): Result<ClothingItem>

    suspend fun deleteClothing(localId: String)
}
