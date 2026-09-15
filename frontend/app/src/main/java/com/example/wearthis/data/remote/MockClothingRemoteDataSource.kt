package com.example.wearthis.data.remote

import com.example.wearthis.data.dto.ClothingUploadResponseDto
import java.io.File
import kotlinx.coroutines.delay

class MockClothingRemoteDataSource : ClothingRemoteDataSource {
    override suspend fun uploadClothing(
        localId: String,
        imagePath: String
    ): ClothingUploadResponseDto {
        delay(MOCK_UPLOAD_DELAY_MS)
        require(File(imagePath).exists()) { "The local image is missing." }

        val backendId = "cloth_$localId"
        return ClothingUploadResponseDto(
            id = backendId,
            imageUrl = "https://mock.wearthis.app/clothing/$backendId"
        )
    }

    private companion object {
        const val MOCK_UPLOAD_DELAY_MS = 1_000L
    }
}
