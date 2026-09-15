package com.example.wearthis.view.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil3.compose.AsyncImage
import com.example.wearthis.data.ClothingContainer
import com.example.wearthis.domain.model.ClothingItem
import com.example.wearthis.domain.model.UploadStatus
import com.example.wearthis.viewmodel.HomeViewModel
import java.io.File

@Composable
fun HomeScreen(
    onAddClothing: () -> Unit,
    modifier: Modifier = Modifier,
    homeViewModel: HomeViewModel = viewModel(
        factory = HomeViewModel.Factory(
            ClothingContainer.repository(LocalContext.current.applicationContext)
        )
    )
) {
    val state by homeViewModel.uiState.collectAsState()

    Column(modifier = modifier.fillMaxSize().padding(24.dp)) {
        Text(
            text = "Your wardrobe",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.primary
        )
        Text(
            text = "Items saved locally and synced with WearThis.",
            modifier = Modifier.padding(top = 8.dp),
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        Button(
            onClick = onAddClothing,
            modifier = Modifier.fillMaxWidth().padding(top = 20.dp)
        ) {
            Text("Add clothing")
        }

        when {
            state.isLoading -> {
                CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally).padding(32.dp))
            }

            state.items.isEmpty() -> {
                Text(
                    text = "Your wardrobe is empty.",
                    modifier = Modifier.fillMaxWidth().padding(top = 48.dp),
                    textAlign = TextAlign.Center,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            else -> {
                LazyColumn(
                    modifier = Modifier.fillMaxSize().padding(top = 18.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    items(state.items, key = { it.localId }) { item ->
                        ClothingRow(
                            item = item,
                            onRetry = { homeViewModel.retryUpload(item.localId) },
                            onDelete = { homeViewModel.deleteClothing(item.localId) }
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ClothingRow(
    item: ClothingItem,
    onRetry: () -> Unit,
    onDelete: () -> Unit
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(18.dp),
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 1.dp
    ) {
        Row(
            modifier = Modifier.padding(10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            AsyncImage(
                model = File(item.localImagePath),
                contentDescription = "Saved clothing",
                modifier = Modifier.height(92.dp).fillMaxWidth(0.32f),
                contentScale = ContentScale.Crop
            )
            Column(modifier = Modifier.weight(1f).padding(start = 12.dp)) {
                Text(
                    text = item.uploadStatus.name.lowercase().replaceFirstChar(Char::uppercase),
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Text(
                    text = item.backendId ?: "Waiting for backend ID",
                    modifier = Modifier.padding(top = 4.dp),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Row {
                    if (item.uploadStatus == UploadStatus.FAILED) {
                        TextButton(onClick = onRetry) {
                            Text("Retry")
                        }
                    }
                    TextButton(onClick = onDelete) {
                        Text("Delete")
                    }
                }
            }
        }
    }
}
