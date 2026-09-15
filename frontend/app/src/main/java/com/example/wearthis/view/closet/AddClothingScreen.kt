package com.example.wearthis.view.closet

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil3.compose.AsyncImage
import com.example.wearthis.data.AppContainer
import com.example.wearthis.feature.closet.AddClothingEvent
import com.example.wearthis.feature.closet.AddClothingUiState
import com.example.wearthis.ui.theme.WearThisTheme
import com.example.wearthis.viewmodel.AddClothingViewModel

@Composable
fun AddClothingScreen(
    onSaved: () -> Unit,
    onBack: () -> Unit,
    modifier: Modifier = Modifier,
    addClothingViewModel: AddClothingViewModel = viewModel(
        factory = AppContainer.get(LocalContext.current).let { container ->
            AddClothingViewModel.Factory(
                repository = container.clothingRepository,
                userId = container.sessionStore.userId.orEmpty()
            )
        }
    )
) {
    val state by addClothingViewModel.uiState.collectAsState()
    val imagePicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia()
    ) { uri ->
        uri?.let {
            addClothingViewModel.onEvent(AddClothingEvent.ImageSelected(it.toString()))
        }
    }
    val chooseImage = {
        imagePicker.launch(
            PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
        )
    }

    LaunchedEffect(state.saveCompleted) {
        if (state.saveCompleted) {
            onSaved()
            addClothingViewModel.onEvent(AddClothingEvent.SaveHandled)
        }
    }

    AddClothingContent(
        state = state,
        onChooseImage = chooseImage,
        onRemoveImage = {
            addClothingViewModel.onEvent(AddClothingEvent.RemoveImage)
        },
        onSave = {
            addClothingViewModel.onEvent(AddClothingEvent.SaveClicked)
        },
        onRetry = {
            addClothingViewModel.onEvent(AddClothingEvent.RetryClicked)
        },
        onDismissError = {
            addClothingViewModel.onEvent(AddClothingEvent.ErrorDismissed)
        },
        onBack = onBack,
        modifier = modifier
    )
}

@Composable
private fun AddClothingContent(
    state: AddClothingUiState,
    onChooseImage: () -> Unit,
    onRemoveImage: () -> Unit,
    onSave: () -> Unit,
    onRetry: () -> Unit,
    onDismissError: () -> Unit,
    onBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(
                        MaterialTheme.colorScheme.background,
                        MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.55f)
                    )
                )
            )
            .verticalScroll(rememberScrollState())
            .imePadding()
            .padding(horizontal = 24.dp, vertical = 20.dp)
    ) {
        TextButton(
            onClick = onBack,
            enabled = !state.isSaving
        ) {
            Text("← Back")
        }

        Spacer(modifier = Modifier.height(14.dp))

        Text(
            text = "Add to your closet",
            style = MaterialTheme.typography.headlineLarge,
            color = MaterialTheme.colorScheme.onBackground
        )
        Text(
            text = "Choose a clear photo with one clothing item. We’ll save it locally and upload a copy.",
            modifier = Modifier.padding(top = 10.dp),
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        Spacer(modifier = Modifier.height(26.dp))

        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .height(330.dp),
            shape = RoundedCornerShape(28.dp),
            color = MaterialTheme.colorScheme.surface,
            tonalElevation = 1.dp
        ) {
            if (state.selectedImageUri == null) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Box(
                        modifier = Modifier
                            .size(82.dp)
                            .clip(RoundedCornerShape(24.dp))
                            .background(MaterialTheme.colorScheme.primaryContainer),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "+",
                            style = MaterialTheme.typography.headlineLarge,
                            color = MaterialTheme.colorScheme.onPrimaryContainer
                        )
                    }
                    Text(
                        text = "No image selected",
                        modifier = Modifier.padding(top = 20.dp),
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Text(
                        text = "PNG, JPG or WebP",
                        modifier = Modifier.padding(top = 6.dp),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            } else {
                AsyncImage(
                    model = state.selectedImageUri,
                    contentDescription = "Selected clothing",
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(12.dp)
                        .clip(RoundedCornerShape(20.dp)),
                    contentScale = ContentScale.Fit
                )
            }
        }

        Spacer(modifier = Modifier.height(18.dp))

        OutlinedButton(
            onClick = onChooseImage,
            enabled = !state.isSaving,
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp),
            shape = RoundedCornerShape(16.dp)
        ) {
            Text(if (state.selectedImageUri == null) "Choose from gallery" else "Replace image")
        }

        if (state.selectedImageUri != null) {
            TextButton(
                onClick = onRemoveImage,
                enabled = !state.isSaving,
                modifier = Modifier.align(Alignment.CenterHorizontally)
            ) {
                Text("Remove image")
            }
        }

        state.errorMessage?.let { error ->
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 8.dp),
                color = MaterialTheme.colorScheme.errorContainer,
                contentColor = MaterialTheme.colorScheme.onErrorContainer,
                shape = RoundedCornerShape(16.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(error, style = MaterialTheme.typography.bodyMedium)
                    Row(modifier = Modifier.fillMaxWidth()) {
                        if (state.failedLocalId != null) {
                            TextButton(onClick = onRetry) {
                                Text("Retry upload")
                            }
                        }
                        TextButton(onClick = onDismissError) {
                            Text("Dismiss")
                        }
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(18.dp))

        Button(
            onClick = onSave,
            enabled = state.selectedImageUri != null && !state.isSaving,
            modifier = Modifier
                .fillMaxWidth()
                .height(58.dp),
            shape = RoundedCornerShape(18.dp)
        ) {
            if (state.isSaving) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    strokeWidth = 2.dp,
                    color = MaterialTheme.colorScheme.onPrimary
                )
            } else {
                Text(
                    text = "Add to wardrobe",
                    fontWeight = FontWeight.SemiBold
                )
            }
        }

        Text(
            text = "The backend upload is mocked for now.",
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 12.dp),
            textAlign = TextAlign.Center,
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Preview(showBackground = true, widthDp = 393, heightDp = 852)
@Composable
private fun AddClothingPreview() {
    WearThisTheme(darkTheme = false) {
        AddClothingContent(
            state = AddClothingUiState(),
            onChooseImage = {},
            onRemoveImage = {},
            onSave = {},
            onRetry = {},
            onDismissError = {},
            onBack = {}
        )
    }
}
