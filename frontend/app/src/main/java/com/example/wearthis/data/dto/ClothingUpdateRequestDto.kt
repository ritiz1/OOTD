package com.example.wearthis.data.dto

import com.google.gson.annotations.SerializedName

data class ClothingUpdateRequestDto(
    @SerializedName("image_url")
    val imageUrl: String? = null,
    val description: Map<String, Any>? = null
)
