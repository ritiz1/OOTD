package com.example.wearthis.data.dto

import com.example.wearthis.data.remote.toAbsoluteMediaUrl
import com.example.wearthis.domain.model.ClothingDetail
import com.google.gson.annotations.SerializedName

data class ClothingDetailDto(
    val id: String,
    @SerializedName("image_url") val imageUrl: String,
    val type: ClothingTypeDto,
    val colors: List<NamedShareDto>,
    val materials: List<NamedShareDto>,
    val patterns: List<NamedShareDto>,
    val details: List<String>,
    val styles: List<StyleDto>,
    @SerializedName("visual_attributes") val visualAttributes: Map<String, Any?>? = null,
    val analysis: ClothingAnalysisDto?
)

data class ClothingTypeDto(
    val name: String,
    val subcategory: String
)

data class NamedShareDto(
    val name: String
)

data class StyleDto(
    val name: String,
    val confidence: Double?
)

fun ClothingDetailDto.toDomain(): ClothingDetail {
    return ClothingDetail(
        backendId = id,
        imageUrl = imageUrl.toAbsoluteMediaUrl(),
        category = type.name,
        subcategory = type.subcategory,
        colors = colors.map { it.name },
        materials = materials.map { it.name },
        patterns = patterns.map { it.name },
        details = details,
        styles = styles.map { it.name },
        confidence = analysis?.overallConfidence
    )
}
