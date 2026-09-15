package com.example.wearthis.data.remote

import com.example.wearthis.data.dto.ClothingUploadResponseDto
import com.example.wearthis.data.dto.ClothingAnalysisDto
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
            imageUrl = "https://mock.wearthis.app/clothing/$backendId",
            user = "mock-user",
            description = emptyMap(),
            analysis = ClothingAnalysisDto(
                id = "mock-analysis",
                modelName = "mock",
                modelVersion = "1",
                overallConfidence = null
            )
        )
    }

    private companion object {
        const val MOCK_UPLOAD_DELAY_MS = 1_000L
    }
}
