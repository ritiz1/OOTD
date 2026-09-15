package com.example.wearthis.repository

import android.net.Uri
import com.example.wearthis.data.local.ClothingImageStorage
import com.example.wearthis.data.local.dao.ClothingDao
import com.example.wearthis.data.local.entity.ClothingEntity
import com.example.wearthis.data.local.toDomain
import com.example.wearthis.data.remote.ClothingRemoteDataSource
import com.example.wearthis.domain.model.ClothingItem
import com.example.wearthis.domain.model.UploadStatus
import java.util.UUID
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class DefaultClothingRepository(
    private val clothingDao: ClothingDao,
    private val imageStorage: ClothingImageStorage,
    private val remoteDataSource: ClothingRemoteDataSource
) : ClothingRepository {

    override fun observeClothing(): Flow<List<ClothingItem>> {
        return clothingDao.observeAll().map { entities ->
            entities.map(ClothingEntity::toDomain)
        }
    }

    override suspend fun addClothing(
        userId: String,
        selectedImageUri: String
    ): Result<ClothingItem> {
        return runCatching {
            val entity = ClothingEntity(
                localId = UUID.randomUUID().toString(),
                backendId = null,
                userId = userId,
                localImagePath = imageStorage.copyIntoAppStorage(Uri.parse(selectedImageUri)),
                remoteImageUrl = null,
                uploadStatus = UploadStatus.PENDING.name,
                createdAt = System.currentTimeMillis()
            )
            clothingDao.insert(entity)
            upload(entity).getOrThrow()
        }
    }

    override suspend fun retryUpload(localId: String): Result<ClothingItem> {
        val entity = clothingDao.findByLocalId(localId)
            ?: return Result.failure(IllegalArgumentException("Clothing item was not found."))
        return upload(entity)
    }

    override suspend fun deleteClothing(localId: String) {
        clothingDao.findByLocalId(localId)?.let { entity ->
            clothingDao.delete(entity)
            imageStorage.delete(entity.localImagePath)
        }
    }

    private suspend fun upload(entity: ClothingEntity): Result<ClothingItem> {
        val uploading = entity.copy(uploadStatus = UploadStatus.UPLOADING.name)
        clothingDao.update(uploading)

        return runCatching {
            remoteDataSource.uploadClothing(
                localId = uploading.localId,
                imagePath = uploading.localImagePath
            )
        }.fold(
            onSuccess = { response ->
                val uploaded = uploading.copy(
                    backendId = response.id,
                    remoteImageUrl = response.imageUrl,
                    uploadStatus = UploadStatus.UPLOADED.name
                )
                clothingDao.update(uploaded)
                Result.success(uploaded.toDomain())
            },
            onFailure = { error ->
                clothingDao.update(
                    uploading.copy(uploadStatus = UploadStatus.FAILED.name)
                )
                Result.failure(error)
            }
        )
    }
}
