package com.example.wearthis.domain.model

data class ClothingDetail(
    val backendId: String,
    val imageUrl: String,
    val category: String,
    val subcategory: String,
    val colors: List<String>,
    val materials: List<String>,
    val patterns: List<String>,
    val details: List<String>,
    val styles: List<String>,
    val confidence: Double?
)
