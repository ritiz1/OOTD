package com.example.wearthis.feature.closet

data class AddClothingUiState(
    val selectedImageUri: String? = null,
    val isSaving: Boolean = false,
    val errorMessage: String? = null,
    val failedLocalId: String? = null,
    val saveCompleted: Boolean = false
)

sealed interface AddClothingEvent {
    data class ImageSelected(val uri: String) : AddClothingEvent
    data object RemoveImage : AddClothingEvent
    data object SaveClicked : AddClothingEvent
    data object RetryClicked : AddClothingEvent
    data object ErrorDismissed : AddClothingEvent
    data object SaveHandled : AddClothingEvent
}
