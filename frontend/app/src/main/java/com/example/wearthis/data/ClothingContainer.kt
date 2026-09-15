package com.example.wearthis.data

import android.content.Context
import com.example.wearthis.repository.ClothingRepository

object ClothingContainer {
    fun repository(context: Context): ClothingRepository {
        return AppContainer.get(context).clothingRepository
    }
}
