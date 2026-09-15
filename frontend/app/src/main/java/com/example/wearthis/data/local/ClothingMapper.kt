package com.example.wearthis.data.local

import com.example.wearthis.data.local.entity.ClothingEntity
import com.example.wearthis.domain.model.ClothingItem
import com.example.wearthis.domain.model.UploadStatus

fun ClothingEntity.toDomain(): ClothingItem {
    return ClothingItem(
        localId = localId,
        backendId = backendId,
        userId = userId,
        localImagePath = localImagePath,
        remoteImageUrl = remoteImageUrl,
        uploadStatus = UploadStatus.valueOf(uploadStatus),
        createdAt = createdAt
    )
}
