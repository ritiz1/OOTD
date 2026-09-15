package com.example.wearthis.data.remote

import com.example.wearthis.data.dto.ClothingUploadResponseDto

interface ClothingRemoteDataSource {
    suspend fun uploadClothing(
        localId: String,
        imagePath: String
    ): ClothingUploadResponseDto
}
