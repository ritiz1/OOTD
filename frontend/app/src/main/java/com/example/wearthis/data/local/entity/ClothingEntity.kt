package com.example.wearthis.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "clothing",
    indices = [Index(value = ["backendId"], unique = true)]
)
data class ClothingEntity(
    @PrimaryKey val localId: String,
    val backendId: String?,
    val userId: String,
    val localImagePath: String,
    val remoteImageUrl: String?,
    val uploadStatus: String,
    val createdAt: Long
)
