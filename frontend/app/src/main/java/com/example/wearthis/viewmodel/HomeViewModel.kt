package com.example.wearthis.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.wearthis.feature.closet.ClosetUiState
import com.example.wearthis.repository.ClothingRepository
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class HomeViewModel(
    private val repository: ClothingRepository
) : ViewModel() {

    val uiState: StateFlow<ClosetUiState> = repository.observeClothing()
        .map { ClosetUiState(items = it, isLoading = false) }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = ClosetUiState()
        )

    fun deleteClothing(localId: String) {
        viewModelScope.launch {
            repository.deleteClothing(localId)
        }
    }

    fun retryUpload(localId: String) {
        viewModelScope.launch {
            repository.retryUpload(localId)
        }
    }

    class Factory(
        private val repository: ClothingRepository
    ) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            require(modelClass.isAssignableFrom(HomeViewModel::class.java))
            return HomeViewModel(repository) as T
        }
    }
}
