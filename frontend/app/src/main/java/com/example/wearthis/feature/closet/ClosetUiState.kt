package com.example.wearthis.feature.closet

import com.example.wearthis.domain.model.ClothingItem

data class ClosetUiState(
    val items: List<ClothingItem> = emptyList(),
    val isLoading: Boolean = true
)
