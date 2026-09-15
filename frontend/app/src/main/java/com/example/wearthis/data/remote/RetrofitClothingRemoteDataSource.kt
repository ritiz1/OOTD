package com.example.wearthis.data.remote

import com.example.wearthis.data.dto.ClothingUploadResponseDto
import java.io.File
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody

class RetrofitClothingRemoteDataSource(
    private val apiService: ApiService
) : ClothingRemoteDataSource {
    override suspend fun uploadClothing(
        localId: String,
        imagePath: String
    ): ClothingUploadResponseDto {
        val imageFile = File(imagePath)
        require(imageFile.isFile) { "The selected image is no longer available." }

        val requestBody = imageFile.asRequestBody(
            imageFile.imageMediaType().toMediaType()
        )
        val imagePart = MultipartBody.Part.createFormData(
            name = "image",
            filename = imageFile.name,
            body = requestBody
        )

        return try {
            apiService.describeClothing(imagePart)
        } catch (error: Throwable) {
            throw error.toApiException("Unable to upload and analyze this image.")
        }
    }
}

private fun File.imageMediaType(): String {
    return when (extension.lowercase()) {
        "png" -> "image/png"
        "webp" -> "image/webp"
        "gif" -> "image/gif"
        else -> "image/jpeg"
    }
}
