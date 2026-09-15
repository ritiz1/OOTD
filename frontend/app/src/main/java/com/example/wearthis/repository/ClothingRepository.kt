package com.example.wearthis.repository

import com.example.wearthis.data.dto.ClothingUpdateRequestDto
import com.example.wearthis.domain.model.ClothingDetail
import com.example.wearthis.domain.model.ClothingItem
import kotlinx.coroutines.flow.Flow

interface ClothingRepository {
    suspend fun refresh(): Result<Unit>
    fun observeClothing(): Flow<List<ClothingItem>>

    suspend fun detail(backendId: String): Result<ClothingDetail>

    suspend fun updateClothing(
        backendId: String,
        request: ClothingUpdateRequestDto
    ): Result<ClothingDetail>

    suspend fun addClothing(
        userId: String,
        selectedImageUri: String
    ): Result<ClothingItem>

    suspend fun retryUpload(localId: String): Result<ClothingItem>

    suspend fun deleteClothing(localId: String)
}
