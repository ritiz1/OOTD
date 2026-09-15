package com.example.wearthis.data.dto

import com.google.gson.annotations.SerializedName

data class ClothingUploadResponseDto(
    val id: String,
    @SerializedName("image_url")
    val imageUrl: String,
    val user: String,
    val description: Map<String, Any>,
    val analysis: ClothingAnalysisDto
)

data class ClothingAnalysisDto(
    val id: String,
    @SerializedName("model_name")
    val modelName: String,
    @SerializedName("model_version")
    val modelVersion: String,
    @SerializedName("overall_confidence")
    val overallConfidence: Double?
)
