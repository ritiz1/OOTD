package com.example.wearthis.view.home

import android.Manifest
import android.app.DatePickerDialog
import android.app.TimePickerDialog
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.saveable.rememberSaveableStateHolder
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.graphics.vector.PathParser
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.lifecycle.viewmodel.compose.viewModel
import coil3.compose.AsyncImage
import com.example.wearthis.R
import com.example.wearthis.data.remote.toAbsoluteMediaUrl
import com.example.wearthis.domain.model.*
import com.example.wearthis.viewmodel.MainViewModel
import com.example.wearthis.viewmodel.MainUiState
import java.io.File
import java.time.LocalDate
import java.time.LocalTime
import java.time.ZoneId
import java.time.format.DateTimeFormatter

@Composable
fun HomeScreen(
    onAddClothing: () -> Unit,
    onSignOut: () -> Unit,
    modifier: Modifier = Modifier,
    mainViewModel: MainViewModel = viewModel()
) {
    val state by mainViewModel.state.collectAsState()
    var tab by rememberSaveable { mutableIntStateOf(0) }
    val holder = rememberSaveableStateHolder()
    val snackbar = remember { SnackbarHostState() }
    val context = LocalContext.current
    val locationPermission = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        if (granted) mainViewModel.useCurrentLocation()
        else { tab = 2; mainViewModel.report("Search for your city to add weather without location access.") }
    }
    val useLocation = {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED)
            mainViewModel.useCurrentLocation()
        else locationPermission.launch(Manifest.permission.ACCESS_COARSE_LOCATION)
    }
    LaunchedEffect(Unit) {
        if (state.weather == null && ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED)
            mainViewModel.useCurrentLocation()
    }
    LaunchedEffect(state.error, state.message) {
        (state.error ?: state.message)?.let {
            snackbar.showSnackbar(it, duration = SnackbarDuration.Long)
            mainViewModel.dismiss()
        }
    }
    Scaffold(modifier = modifier, containerColor = MaterialTheme.colorScheme.background,
        snackbarHost = { SnackbarHost(snackbar) },
        bottomBar = {
            NavigationBar(containerColor = MaterialTheme.colorScheme.background, tonalElevation = 0.dp) {
                listOf("Today", "Wardrobe", "Plan", "Profile").forEachIndexed { index, label ->
                    NavigationBarItem(selected = tab == index, onClick = { tab = index },
                        icon = { LineIcon(listOf("home", "hanger", "calendar", "person")[index]) },
                        label = { Text(label) },
                        colors = NavigationBarItemDefaults.colors(indicatorColor = MaterialTheme.colorScheme.primaryContainer))
                }
            }
        }
    ) { padding ->
        Box(Modifier.padding(padding).fillMaxSize(), contentAlignment = Alignment.TopCenter) {
            holder.SaveableStateProvider(tab) {
                val contentModifier = Modifier.widthIn(max = 600.dp).fillMaxSize()
                when (tab) {
                    0 -> TodayContent(state, { tab = 2 }, { tab = 3 }, mainViewModel::selectPlan, useLocation, contentModifier)
                    1 -> WardrobeContent(state, onAddClothing, mainViewModel, contentModifier)
                    2 -> PlanContent(state, mainViewModel, contentModifier)
                    3 -> ProfileContent(state, mainViewModel, onSignOut, contentModifier)
                }
            }
        }
    }
    state.selectedPlan?.let { plan ->
        PlanDetail(plan, state, mainViewModel, onAddClothing)
    }
}

@Composable
private fun BrandHeader(name: String?, onProfile: (() -> Unit)? = null) {
    Row(Modifier.fillMaxWidth().padding(bottom = 12.dp), verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween) {
        Text("OOTD", style = MaterialTheme.typography.headlineMedium.copy(fontFamily = FontFamily.Serif,
            letterSpacing = (-1).sp), color = MaterialTheme.colorScheme.primary)
        if (onProfile != null) {
            FilledTonalIconButton(onClick = onProfile, shape = CircleShape) {
                Text(name?.take(1)?.uppercase()?.ifBlank { "O" } ?: "O")
            }
        } else { LineIcon("sparkle") }
    }
}

@Composable
private fun EditorialTitle(text: String, modifier: Modifier = Modifier) {
    Text(text, modifier, style = MaterialTheme.typography.displayMedium.copy(fontSize = 42.sp, lineHeight = 43.sp),
        color = MaterialTheme.colorScheme.primary)
}

@Composable
private fun Eyebrow(text: String) {
    Text(text.uppercase(), style = MaterialTheme.typography.labelSmall.copy(letterSpacing = 2.sp),
        color = MaterialTheme.colorScheme.onSurfaceVariant)
}

@Composable
private fun TodayContent(state: MainUiState, onPlan: () -> Unit, onProfile: () -> Unit,
    onEvent: (OutfitPlan) -> Unit, onWeather: () -> Unit, modifier: Modifier) {
    val today = state.plans.filter { it.date == LocalDate.now(ZoneId.of(it.weather.timezone)).toString() }
    val next = state.plans.filter { it.date >= LocalDate.now().toString() }.take(3)
    val shown = today.ifEmpty { next }
    val latest = state.plans.lastOrNull { it.recommendations.isNotEmpty() }
    val ids = latest?.recommendations?.firstOrNull()?.clothingItemIds.orEmpty()
    val collage = if (ids.isEmpty()) state.items.take(3) else state.items.filter { it.backendId in ids }.take(3)
    LazyColumn(modifier, contentPadding = PaddingValues(24.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) {
        item {
            BrandHeader(state.user?.firstName, onProfile)
            val greeting = when (LocalTime.now().hour) { in 5..11 -> "Good morning"; in 12..17 -> "Good afternoon"; else -> "Good evening" }
            Text("$greeting${state.user?.firstName?.takeIf { it.isNotBlank() }?.let { ", $it" }.orEmpty()}",
                color = MaterialTheme.colorScheme.onSurfaceVariant)
            EditorialTitle("Dress for\nthe day ahead.")
            Spacer(Modifier.height(12.dp))
            Eyebrow("Same days. A brighter you.")
            TextButton(onClick = onWeather, enabled = !state.weatherBusy) {
                LineIcon("pin")
                Spacer(Modifier.width(8.dp))
                Text(if (state.weatherBusy) "Finding local weather…" else state.place?.name ?: "Enable local weather")
            }
        }
        item {
            Surface(shape = RoundedCornerShape(24.dp), color = MaterialTheme.colorScheme.secondaryContainer,
                modifier = Modifier.fillMaxWidth().height(310.dp)) {
                Box {
                    if (collage.isEmpty()) {
                        Image(painterResource(R.drawable.cream_knit_sweater_cutout), null,
                            Modifier.size(210.dp).align(Alignment.CenterStart).rotate(-10f), contentScale = ContentScale.Fit)
                        Image(painterResource(R.drawable.taupe_wide_leg_pleated_trousers), null,
                            Modifier.size(220.dp).align(Alignment.CenterEnd).rotate(8f), contentScale = ContentScale.Fit)
                        Image(painterResource(R.drawable.minimalist_white_sneaker_pair), null,
                            Modifier.size(140.dp).align(Alignment.BottomStart), contentScale = ContentScale.Fit)
                    } else {
                        collage.forEachIndexed { index, item ->
                            ClothingPhoto(item, Modifier.size(if (index == 0) 220.dp else 160.dp)
                                .align(listOf(Alignment.CenterStart, Alignment.TopEnd, Alignment.BottomEnd)[index])
                                .padding(12.dp).rotate(if (index == 0) -7f else 6f).clip(RoundedCornerShape(16.dp)))
                        }
                    }
                    Surface(Modifier.align(Alignment.TopEnd).padding(12.dp), shape = CircleShape,
                        color = MaterialTheme.colorScheme.background.copy(alpha = .95f)) {
                        Text(state.weather?.let { "${it.temperatureC.toInt()}°C · ${it.status}" } ?: "Made for your day",
                            Modifier.padding(horizontal = 12.dp, vertical = 8.dp), style = MaterialTheme.typography.labelMedium)
                    }
                    Surface(Modifier.align(Alignment.BottomCenter).padding(12.dp), shape = RoundedCornerShape(12.dp),
                        color = MaterialTheme.colorScheme.background.copy(alpha = .94f)) {
                        Text(if (collage.isEmpty()) "A little inspiration for your closet" else if (ids.isEmpty()) "Your wardrobe, reimagined" else "Your latest outfit idea",
                            Modifier.padding(10.dp), style = MaterialTheme.typography.labelMedium)
                    }
                }
            }
        }
        item {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Text(if (today.isEmpty() && next.isNotEmpty()) "Coming up" else "Today",
                    style = MaterialTheme.typography.headlineLarge.copy(fontFamily = FontFamily.Serif))
                Text("${shown.size} plans", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        if (shown.isEmpty()) item {
            SoftCard { Text("A little space for possibility.", style = MaterialTheme.typography.titleMedium)
                Text("Add your first event and find an outfit for the time, place, and weather.",
                    color = MaterialTheme.colorScheme.onSurfaceVariant) }
        }
        items(shown, key = { it.id }) { plan ->
            Row(Modifier.fillMaxWidth().clickable { onEvent(plan) }.padding(vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Box(Modifier.size(9.dp).background(MaterialTheme.colorScheme.tertiary, CircleShape))
                Text(formatTime(plan.start), style = MaterialTheme.typography.titleSmall)
                Column(Modifier.weight(1f)) {
                    Text(plan.title, style = MaterialTheme.typography.titleMedium)
                    Text("${plan.date} · ${plan.weather.temperatureC.toInt()}°C · ${plan.weather.status}",
                        style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                LineIcon("arrow")
            }
        }
        item { PrimaryAction("Style my day", onPlan) }
    }
}

@Composable
private fun WardrobeContent(state: MainUiState, onAdd: () -> Unit, vm: MainViewModel, modifier: Modifier) {
    var deleting by remember { mutableStateOf<ClothingItem?>(null) }
    Column(modifier.padding(horizontal = 24.dp)) {
        Spacer(Modifier.height(24.dp))
        BrandHeader(state.user?.firstName)
        Eyebrow("Collected by you")
        EditorialTitle("Your wardrobe.")
        Text("${state.items.size} pieces. Endless possibilities.", Modifier.padding(vertical = 10.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = onAdd, modifier = Modifier.weight(1f)) { Text("+ Add clothing") }
            OutlinedButton(onClick = { vm.refresh() }) { Text("Refresh") }
        }
        if (state.loading) CircularProgressIndicator(Modifier.padding(24.dp))
        else if (state.items.isEmpty()) {
            Spacer(Modifier.height(30.dp))
            SoftCard {
                LineIcon("hanger")
                Text("Start with a favorite.", style = MaterialTheme.typography.titleLarge)
                Text("Upload a photo of a piece you own. Your clothes will appear here, ready to style.")
            }
        } else LazyVerticalGrid(columns = GridCells.Adaptive(140.dp),
            contentPadding = PaddingValues(vertical = 20.dp), horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)) {
            items(state.items, key = { it.localId }) { item ->
                Surface(shape = RoundedCornerShape(18.dp), color = MaterialTheme.colorScheme.surfaceVariant) {
                    Column {
                        ClothingPhoto(item, Modifier.fillMaxWidth().aspectRatio(.85f))
                        Column(Modifier.padding(10.dp)) {
                            Text(when (item.uploadStatus) { UploadStatus.UPLOADED -> "Ready to style"; UploadStatus.FAILED -> "Upload needs a retry";
                                UploadStatus.UPLOADING -> "Analyzing your piece…"; UploadStatus.PENDING -> "Waiting to upload" },
                                style = MaterialTheme.typography.labelMedium)
                            Row {
                                if (item.uploadStatus == UploadStatus.FAILED || item.uploadStatus == UploadStatus.PENDING)
                                    TextButton(onClick = { vm.retry(item) }, enabled = !state.busy) { Text("Retry") }
                                TextButton(onClick = { deleting = item }, enabled = !state.busy && item.uploadStatus != UploadStatus.UPLOADING) { Text("Remove") }
                            }
                        }
                    }
                }
            }
        }
    }
    deleting?.let { item ->
        AlertDialog(onDismissRequest = { deleting = null }, title = { Text("Remove this piece?") },
            text = { Text("It will be removed from your wardrobe and future outfit ideas.") },
            confirmButton = { TextButton(onClick = { deleting = null; vm.delete(item) }) { Text("Remove") } },
            dismissButton = { TextButton(onClick = { deleting = null }) { Text("Keep it") } })
    }
}

@Composable
private fun PlanContent(state: MainUiState, vm: MainViewModel, modifier: Modifier) {
    var title by rememberSaveable { mutableStateOf("") }
    var date by rememberSaveable { mutableStateOf(LocalDate.now().plusDays(1).toString()) }
    var start by rememberSaveable { mutableStateOf("09:00") }
    var end by rememberSaveable { mutableStateOf("11:00") }
    var occasion by rememberSaveable { mutableStateOf("Everyday") }
    var vibe by rememberSaveable { mutableStateOf("Any") }
    var query by rememberSaveable { mutableStateOf("") }
    val context = LocalContext.current
    val uriHandler = LocalUriHandler.current
    val locationPermission = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        if (granted) vm.useCurrentLocation() else vm.report("Location permission wasn't granted. Search for your city below.")
    }
    Column(modifier.verticalScroll(rememberScrollState()).imePadding().padding(24.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        BrandHeader(state.user?.firstName)
        Eyebrow("Plan your outfit")
        EditorialTitle("What's on\nyour schedule?")
        Text("Add an event and we'll dress for the time, place, and weather.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        OutlinedTextField(title, { title = it }, Modifier.fillMaxWidth(), label = { Text("Event") },
            placeholder = { Text("Dinner with friends") }, leadingIcon = { LineIcon("calendar") }, singleLine = true,
            shape = RoundedCornerShape(16.dp), enabled = !state.busy)
        PickerCard("Date", LocalDate.parse(date).format(DateTimeFormatter.ofPattern("EEE, MMM d, yyyy")), "calendar", !state.busy) {
            val initial = LocalDate.parse(date)
            DatePickerDialog(context, { _, y, m, d -> date = LocalDate.of(y, m + 1, d).toString() },
                initial.year, initial.monthValue - 1, initial.dayOfMonth).show()
        }
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Box(Modifier.weight(1f)) { PickerCard("Starts", formatTime(start), "clock", !state.busy) {
                val time = LocalTime.parse(start)
                TimePickerDialog(context, { _, h, m -> start = LocalTime.of(h, m).toString() }, time.hour, time.minute, false).show()
            } }
            Box(Modifier.weight(1f)) { PickerCard("Ends", formatTime(end), "clock", !state.busy) {
                val time = LocalTime.parse(end)
                TimePickerDialog(context, { _, h, m -> end = LocalTime.of(h, m).toString() }, time.hour, time.minute, false).show()
            } }
        }
        SoftCard {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                LineIcon("pin")
                Text(state.place?.name ?: "Where will you be?", style = MaterialTheme.typography.titleMedium)
            }
            Text("Choose a city for event weather. Times use that city's time zone.", style = MaterialTheme.typography.bodySmall)
            OutlinedTextField(query, { query = it }, Modifier.fillMaxWidth(), label = { Text("City or postal code") }, singleLine = true,
                enabled = !state.weatherBusy && !state.busy, shape = RoundedCornerShape(12.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                TextButton(onClick = { vm.search(query) }, enabled = !state.weatherBusy && !state.busy) { Text("Search") }
                TextButton(onClick = {
                    if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED)
                        vm.useCurrentLocation()
                    else locationPermission.launch(Manifest.permission.ACCESS_COARSE_LOCATION)
                }, enabled = !state.weatherBusy && !state.busy) { Text("Use my location") }
            }
            if (state.weatherBusy) LinearProgressIndicator(Modifier.fillMaxWidth())
            state.places.forEach { place -> TextButton(onClick = { vm.choosePlace(place) }, enabled = !state.weatherBusy && !state.busy) { Text(place.name) } }
        }
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Box(Modifier.weight(1f)) { ChoicePicker("Occasion", occasion, listOf("Everyday", "Class", "Work", "Dinner", "Party", "Workout"), !state.busy) { occasion = it } }
            Box(Modifier.weight(1f)) { ChoicePicker("Vibe", vibe, listOf("Any", "Relaxed", "Minimal", "Polished", "Bold"), !state.busy) { vibe = it } }
        }
        SoftCard {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                LineIcon("sun")
                Column {
                    Text("Weather, taken care of.", style = MaterialTheme.typography.titleMedium)
                    Text(state.weather?.let { "Currently ${it.temperatureC.toInt()}°C · ${it.status}. Event forecast is fetched when you submit." }
                        ?: "Select a location to include the temperature automatically.", style = MaterialTheme.typography.bodySmall)
                }
            }
            TextButton(onClick = { uriHandler.openUri("https://open-meteo.com/") }) { Text("Weather by Open-Meteo", style = MaterialTheme.typography.labelSmall) }
        }
        PrimaryAction(if (state.busy) "Finding your outfit…" else "Get outfit ideas", {
            vm.createPlan(title, date, start, end, occasion, vibe)
        }, enabled = !state.busy && !state.weatherBusy)
        if (state.busy) LinearProgressIndicator(Modifier.fillMaxWidth())
        if (state.plans.isNotEmpty()) {
            Text("Your plans", style = MaterialTheme.typography.headlineSmall)
            state.plans.forEach { plan ->
                PickerCard(plan.date, "${plan.title} · ${formatTime(plan.start)}", "calendar") { vm.selectPlan(plan) }
            }
        }
    }
}

@Composable
private fun ProfileContent(state: MainUiState, vm: MainViewModel, onSignOut: () -> Unit, modifier: Modifier) {
    var first by rememberSaveable(state.user?.id, state.user?.firstName) { mutableStateOf(state.user?.firstName.orEmpty()) }
    var last by rememberSaveable(state.user?.id, state.user?.lastName) { mutableStateOf(state.user?.lastName.orEmpty()) }
    Column(modifier.verticalScroll(rememberScrollState()).imePadding().padding(24.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) {
        BrandHeader(state.user?.firstName)
        Eyebrow("A little more you")
        EditorialTitle("Your profile.")
        Text(state.user?.email.orEmpty(), color = MaterialTheme.colorScheme.onSurfaceVariant)
        OutlinedTextField(first, { first = it }, Modifier.fillMaxWidth(), label = { Text("First name") }, singleLine = true, enabled = !state.busy)
        OutlinedTextField(last, { last = it }, Modifier.fillMaxWidth(), label = { Text("Last name") }, singleLine = true, enabled = !state.busy)
        PrimaryAction(if (state.busy) "Saving…" else "Save changes", { vm.saveProfile(first, last) }, !state.busy)
        SoftCard {
            Text("${state.items.size} wardrobe pieces", style = MaterialTheme.typography.titleMedium)
            Text("${state.plans.size} saved plans")
            Text("Small choices. A style that's yours.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        OutlinedButton(onClick = onSignOut, modifier = Modifier.fillMaxWidth(), enabled = !state.busy) { Text("Sign out") }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun PlanDetail(plan: OutfitPlan, state: MainUiState, vm: MainViewModel, onAdd: () -> Unit) {
    ModalBottomSheet(onDismissRequest = { vm.selectPlan(null) }) {
        Column(Modifier.fillMaxWidth().verticalScroll(rememberScrollState()).padding(24.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            EditorialTitle(plan.title)
            Text("${plan.date} · ${formatTime(plan.start)} – ${formatTime(plan.end)}")
            Text("${plan.place.name} · ${plan.weather.temperatureC.toInt()}°C · ${plan.weather.status}")
            state.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
            if (state.busy) { LinearProgressIndicator(Modifier.fillMaxWidth()); Text("Putting your outfit together…") }
            if (plan.recommendations.isEmpty() && !state.busy) {
                Text("Your event is saved. Get an outfit idea from your wardrobe.")
                if (state.items.none { it.uploadStatus == UploadStatus.UPLOADED }) {
                    PrimaryAction("Add clothing", { vm.selectPlan(null); onAdd() })
                } else PrimaryAction("Try outfit ideas", { vm.regenerate(plan) })
            }
            plan.recommendations.forEach { recommendation ->
                val clothing = state.items.filter { it.backendId in recommendation.clothingItemIds }
                clothing.chunked(2).forEach { row ->
                    Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        row.forEach { item -> ClothingPhoto(item, Modifier.weight(1f).height(180.dp).clip(RoundedCornerShape(16.dp))) }
                    }
                }
                Text(recommendation.reason, style = MaterialTheme.typography.bodyLarge)
                recommendation.warnings.forEach { Text(it, color = MaterialTheme.colorScheme.tertiary) }
                val packed = state.items.filter { it.backendId in recommendation.packItemIds }
                if (packed.isNotEmpty()) {
                    Text("Bring along", style = MaterialTheme.typography.titleMedium)
                    packed.forEach { ClothingPhoto(it, Modifier.size(100.dp).clip(RoundedCornerShape(12.dp))) }
                }
            }
            if (plan.recommendations.isNotEmpty()) TextButton(onClick = { vm.regenerate(plan) }, enabled = !state.busy) { Text("Refresh outfit ideas") }
            TextButton(onClick = { vm.removePlan(plan) }, enabled = !state.busy) { Text("Remove event") }
        }
    }
}

@Composable
private fun ClothingPhoto(item: ClothingItem, modifier: Modifier) {
    var failed by remember(item.localId) { mutableStateOf(false) }
    Box(modifier.background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
        AsyncImage(
            model = if (item.localImagePath.isNotBlank() && File(item.localImagePath).exists()) {
                File(item.localImagePath)
            } else {
                item.remoteImageUrl?.takeIf { it.isNotBlank() }?.toAbsoluteMediaUrl()
            },
            contentDescription = "Your uploaded clothing", modifier = Modifier.fillMaxSize(), contentScale = ContentScale.Crop,
            onError = { failed = true }, onSuccess = { failed = false })
        if (failed) Text("Photo unavailable", style = MaterialTheme.typography.labelSmall)
    }
}

@Composable
private fun SoftCard(content: @Composable ColumnScope.() -> Unit) {
    Surface(shape = RoundedCornerShape(18.dp), color = MaterialTheme.colorScheme.surfaceVariant, modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp), content = content)
    }
}

@Composable
private fun PrimaryAction(text: String, onClick: () -> Unit, enabled: Boolean = true) {
    Button(onClick = onClick, enabled = enabled, modifier = Modifier.fillMaxWidth().heightIn(min = 56.dp), shape = RoundedCornerShape(22.dp)) {
        Text(text, style = MaterialTheme.typography.titleMedium)
        Spacer(Modifier.width(14.dp))
        LineIcon("arrow")
    }
}

@Composable
private fun PickerCard(label: String, value: String, icon: String, enabled: Boolean = true, onClick: () -> Unit) {
    OutlinedCard(onClick = onClick, enabled = enabled, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(16.dp)) {
        Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            LineIcon(icon)
            Column(Modifier.weight(1f)) { Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(value, style = MaterialTheme.typography.bodyMedium) }
        }
    }
}

@Composable
private fun ChoicePicker(label: String, value: String, choices: List<String>, enabled: Boolean, onSelect: (String) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    Box {
        PickerCard(label, value, "sparkle", enabled) { expanded = true }
        DropdownMenu(expanded, { expanded = false }) {
            choices.forEach { choice -> DropdownMenuItem(text = { Text(choice) }, onClick = { expanded = false; onSelect(choice) }) }
        }
    }
}

private fun formatTime(value: String): String = LocalTime.parse(value).format(DateTimeFormatter.ofPattern("h:mm a"))

@Composable
private fun LineIcon(name: String) {
    val vector = remember(name) {
        ImageVector.Builder(defaultWidth = 24.dp, defaultHeight = 24.dp, viewportWidth = 24f, viewportHeight = 24f).apply {
            addPath(PathParser().parsePathString(when (name) {
                "home" -> "M3,10 L12,3 L21,10 L21,21 L15,21 L15,14 L9,14 L9,21 L3,21 Z"
                "hanger" -> "M9,6 C9,1 16,1 16,6 C16,9 12,9 12,12 L2,20 L22,20 L12,12"
                "calendar" -> "M4,5 L20,5 L20,21 L4,21 Z M8,2 L8,8 M16,2 L16,8 M4,10 L20,10"
                "person" -> "M16,7 A4,4 0,1 1,8 7 A4,4 0,1 1,16 7 M3,22 C3,10 21,10 21,22 Z"
                "clock" -> "M22,12 A10,10 0,1 1,2 12 A10,10 0,1 1,22 12 M12,5 L12,12 L17,15"
                "pin" -> "M12,22 C8,17 4,12 4,8 A8,8 0,1 1,20 8 C20,12 16,17 12,22 Z M15,8 A3,3 0,1 1,9 8 A3,3 0,1 1,15 8"
                "sun" -> "M17,12 A5,5 0,1 1,7 12 A5,5 0,1 1,17 12 M12,0 L12,3 M12,21 L12,24 M0,12 L3,12 M21,12 L24,12 M3,3 L5,5 M19,19 L21,21"
                "arrow" -> "M3,12 L21,12 M14,5 L21,12 L14,19"
                else -> "M12,2 L15,9 L22,12 L15,15 L12,22 L9,15 L2,12 L9,9 Z"
            }).toNodes(), stroke = SolidColor(Color.Black), strokeLineWidth = 1.5f)
        }.build()
    }
    Icon(vector, null, Modifier.size(24.dp))
}

@androidx.compose.ui.tooling.preview.Preview(showBackground = true, widthDp = 390, heightDp = 844)
@Composable
private fun TodayPreview() {
    com.example.wearthis.ui.theme.WearThisTheme {
        TodayContent(MainUiState(loading = false), {}, {}, {}, {}, Modifier.fillMaxSize())
    }
}
