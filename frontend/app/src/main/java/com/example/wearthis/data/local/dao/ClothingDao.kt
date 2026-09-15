package com.example.wearthis.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.example.wearthis.data.local.entity.ClothingEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ClothingDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(item: ClothingEntity)

    @Update
    suspend fun update(item: ClothingEntity)

    @Delete
    suspend fun delete(item: ClothingEntity)

    @Query("SELECT * FROM clothing ORDER BY createdAt DESC")
    fun observeAll(): Flow<List<ClothingEntity>>

    @Query("SELECT * FROM clothing WHERE localId = :localId LIMIT 1")
    suspend fun findByLocalId(localId: String): ClothingEntity?

    @Query("SELECT * FROM clothing WHERE backendId = :backendId LIMIT 1")
    suspend fun findByBackendId(backendId: String): ClothingEntity?

    @Query("DELETE FROM clothing WHERE localId = :localId")
    suspend fun deleteByLocalId(localId: String)
}
