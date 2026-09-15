package com.example.wearthis.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.wearthis.domain.model.UploadStatus
import com.example.wearthis.feature.closet.AddClothingEvent
import com.example.wearthis.feature.closet.AddClothingUiState
import com.example.wearthis.repository.ClothingRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class AddClothingViewModel(
    private val repository: ClothingRepository,
    private val userId: String
) : ViewModel() {

    private val _uiState = MutableStateFlow(AddClothingUiState())
    val uiState: StateFlow<AddClothingUiState> = _uiState.asStateFlow()

    fun onEvent(event: AddClothingEvent) {
        when (event) {
            is AddClothingEvent.ImageSelected -> {
                _uiState.update {
                    it.copy(
                        selectedImageUri = event.uri,
                        errorMessage = null,
                        failedLocalId = null
                    )
                }
            }

            AddClothingEvent.RemoveImage -> {
                if (!_uiState.value.isSaving) {
                    _uiState.update {
                        it.copy(
                            selectedImageUri = null,
                            errorMessage = null,
                            failedLocalId = null
                        )
                    }
                }
            }

            AddClothingEvent.SaveClicked -> save()
            AddClothingEvent.RetryClicked -> retry()
            AddClothingEvent.ErrorDismissed -> {
                _uiState.update { it.copy(errorMessage = null) }
            }

            AddClothingEvent.SaveHandled -> {
                _uiState.value = AddClothingUiState()
            }
        }
    }

    private fun save() {
        val selectedImageUri = _uiState.value.selectedImageUri
        if (selectedImageUri == null) {
            _uiState.update { it.copy(errorMessage = "Choose an image first.") }
            return
        }
        if (_uiState.value.isSaving) return
        if (userId.isBlank()) {
            _uiState.update {
                it.copy(errorMessage = "Your session expired. Sign in again.")
            }
            return
        }

        _uiState.update { it.copy(isSaving = true, errorMessage = null) }
        viewModelScope.launch {
            repository.addClothing(
                userId = userId,
                selectedImageUri = selectedImageUri
            ).fold(
                onSuccess = {
                    _uiState.update {
                        it.copy(
                            isSaving = false,
                            saveCompleted = true
                        )
                    }
                },
                onFailure = { error ->
                    val failedItem = repository.observeClothing()
                        .first()
                        .firstOrNull { it.uploadStatus == UploadStatus.FAILED }
                    _uiState.update {
                        it.copy(
                            isSaving = false,
                            errorMessage = error.message ?: "Upload failed. Try again.",
                            failedLocalId = failedItem?.localId
                        )
                    }
                }
            )
        }
    }

    private fun retry() {
        val localId = _uiState.value.failedLocalId ?: return
        if (_uiState.value.isSaving) return

        _uiState.update { it.copy(isSaving = true, errorMessage = null) }
        viewModelScope.launch {
            repository.retryUpload(localId).fold(
                onSuccess = {
                    _uiState.update {
                        it.copy(
                            isSaving = false,
                            saveCompleted = true,
                            failedLocalId = null
                        )
                    }
                },
                onFailure = { error ->
                    _uiState.update {
                        it.copy(
                            isSaving = false,
                            errorMessage = error.message ?: "Upload failed again."
                        )
                    }
                }
            )
        }
    }

    class Factory(
        private val repository: ClothingRepository,
        private val userId: String
    ) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            require(modelClass.isAssignableFrom(AddClothingViewModel::class.java))
            return AddClothingViewModel(repository, userId) as T
        }
    }
}
