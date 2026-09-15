package com.example.wearthis.domain.model

data class ClothingItem(
    val localId: String,
    val backendId: String?,
    val userId: String,
    val localImagePath: String,
    val remoteImageUrl: String?,
    val uploadStatus: UploadStatus,
    val createdAt: Long
)
