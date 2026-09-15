package com.example.wearthis.data.dto

import com.google.gson.annotations.SerializedName

data class RemoteClothingDto(
    val id: String,
    @SerializedName("image_url") val imageUrl: String,
    @SerializedName("created_at") val createdAt: String
)
