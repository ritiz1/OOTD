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
    private val remoteDataSource: ClothingRemoteDataSource,
    private val sessionStore: com.example.wearthis.data.local.AuthSessionStore,
    private val apiService: com.example.wearthis.data.remote.ApiService
) : ClothingRepository {

    override fun observeClothing(): Flow<List<ClothingItem>> {
        return clothingDao.observeAll().map { entities ->
            entities.filter { it.userId == sessionStore.userId }.map(ClothingEntity::toDomain)
        }
    }

    override suspend fun refresh(): Result<Unit> = runCatching {
        val userId = sessionStore.userId ?: error("Sign in to view your wardrobe.")
        val beforeRefresh = clothingDao.itemsForUser(userId)
        val remote = apiService.clothing()
        // Never merge a response into another account if the user signed out while loading.
        check(userId == sessionStore.userId) { "Your session changed. Please retry." }
        remote.forEach { item ->
            val existing = clothingDao.findByBackendId(item.id)
            if (existing == null) {
                clothingDao.insert(ClothingEntity(
                    localId = java.util.UUID.randomUUID().toString(), backendId = item.id,
                    userId = userId, localImagePath = "", remoteImageUrl = item.imageUrl,
                    uploadStatus = UploadStatus.UPLOADED.name,
                    createdAt = runCatching { java.time.Instant.parse(item.createdAt).toEpochMilli() }.getOrDefault(0)
                ))
            }
        }
        val ids = remote.map { it.id }.toSet()
        beforeRefresh.filter {
            it.uploadStatus == UploadStatus.UPLOADED.name && it.backendId !in ids
        }.forEach { clothingDao.delete(it) }
    }

    override suspend fun addClothing(
        userId: String,
        selectedImageUri: String
    ): Result<ClothingItem> {
        return runCatching {
            check(userId == sessionStore.userId) { "Sign in again before uploading." }
            val entity = ClothingEntity(
                localId = UUID.randomUUID().toString(),
                backendId = null,
                userId = userId,
                localImagePath = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
                    imageStorage.copyIntoAppStorage(Uri.parse(selectedImageUri))
                },
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
        if (entity.userId != sessionStore.userId) return Result.failure(IllegalStateException("Sign in again."))
        return upload(entity)
    }

    override suspend fun deleteClothing(localId: String) {
        clothingDao.findByLocalId(localId)?.let { entity ->
            check(entity.userId == sessionStore.userId) { "Sign in again." }
            entity.backendId?.let { apiService.deleteClothing(it) }
            clothingDao.delete(entity)
            if (entity.localImagePath.isNotBlank()) imageStorage.delete(entity.localImagePath)
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
