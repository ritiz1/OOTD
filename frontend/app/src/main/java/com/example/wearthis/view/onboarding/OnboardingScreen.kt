package com.example.wearthis.view.onboarding

import androidx.annotation.DrawableRes
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalInspectionMode
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.zIndex
import com.example.wearthis.R
import com.example.wearthis.ui.theme.ProcessingAmber
import com.example.wearthis.ui.theme.WearThisSage
import com.example.wearthis.ui.theme.WearThisTheme

/**
 * Large PNG cutouts (1–2 MB each) can crash Compose Preview with out-of-memory errors.
 * In preview/inspection mode we draw lightweight placeholders; on device/emulator we load real assets.
 */
@Composable
private fun OnboardingResourceImage(
    @DrawableRes imageRes: Int,
    contentDescription: String?,
    modifier: Modifier = Modifier,
    contentScale: ContentScale = ContentScale.Fit
) {
    if (LocalInspectionMode.current) {
        Box(
            modifier = modifier
                .clip(RoundedCornerShape(8.dp))
                .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.9f)),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "•",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 10.sp
            )
        }
    } else {
        Image(
            painter = painterResource(imageRes),
            contentDescription = contentDescription,
            modifier = modifier,
            contentScale = contentScale
        )
    }
}

@Composable
fun OnboardingScreen(
    onGetStarted: () -> Unit,
    onSignIn: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(
                        MaterialTheme.colorScheme.background,
                        MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.9f)
                    )
                )
            )
            .statusBarsPadding()
            .navigationBarsPadding()
            .verticalScroll(rememberScrollState())
    ) {
        Spacer(modifier = Modifier.height(8.dp))

        TopBrand(modifier = Modifier.padding(horizontal = 8.dp))

        Spacer(modifier = Modifier.height(8.dp))

        OutfitHero()

        Spacer(modifier = Modifier.height(8.dp))

        Headline(modifier = Modifier.padding(horizontal = 22.dp))

        Spacer(modifier = Modifier.height(20.dp))

        FeatureStrip(modifier = Modifier.padding(horizontal = 16.dp))

        Spacer(modifier = Modifier.height(20.dp))

        GetStartedButton(
            modifier = Modifier.padding(horizontal = 16.dp),
            onClick = onGetStarted
        )

        Spacer(modifier = Modifier.height(16.dp))

        SignInRow(
            modifier = Modifier.padding(horizontal = 16.dp),
            onSignIn = onSignIn
        )

        Spacer(modifier = Modifier.height(18.dp))
    }
}

@Composable
private fun TopBrand(modifier: Modifier = Modifier) {
    Row(
        modifier = modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.Top
    ) {
        Column {
            Text(
                text = "OOTD",
                color = MaterialTheme.colorScheme.primary,
                fontSize = 27.sp,
                fontWeight = FontWeight.Medium,
                letterSpacing = 7.sp
            )
            Spacer(modifier = Modifier.height(6.dp))
            Box(
                modifier = Modifier
                    .width(31.dp)
                    .height(1.dp)
                    .background(MaterialTheme.colorScheme.primary)
            )
        }

        Text(
            text = "More than\noutfits.\nA brighter you.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 11.sp,
            lineHeight = 14.sp,
            modifier = Modifier.padding(end = 7.dp, top = 1.dp)
        )
    }
}

@Composable
private fun OutfitHero() {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(365.dp)
    ) {
        OrganicBlob(
            modifier = Modifier
                .align(Alignment.TopStart)
                .offset(x = (-43).dp, y = 31.dp),
            width = 258.dp,
            height = 205.dp,
            color = MaterialTheme.colorScheme.secondaryContainer.copy(alpha = 0.78f),
            corner = 105.dp
        )

        OrganicBlob(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .offset(x = 48.dp, y = 35.dp),
            width = 225.dp,
            height = 220.dp,
            color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.73f),
            corner = 108.dp
        )

        OrganicBlob(
            modifier = Modifier
                .align(Alignment.BottomStart)
                .offset(x = (-35).dp, y = (-4).dp),
            width = 190.dp,
            height = 145.dp,
            color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.8f),
            corner = 82.dp
        )

        OrganicBlob(
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .offset(x = 42.dp, y = 0.dp),
            width = 155.dp,
            height = 170.dp,
            color = MaterialTheme.colorScheme.tertiaryContainer.copy(alpha = 0.82f),
            corner = 85.dp
        )

        EditorialText(
            modifier = Modifier
                .align(Alignment.CenterStart)
                .offset(x = (-3).dp, y = (-54).dp)
                .zIndex(2f)
        )

        LeafCluster(
            modifier = Modifier
                .align(Alignment.BottomStart)
                .offset(x = (-5).dp, y = (-4).dp)
                .zIndex(4f)
        )

        EditorialPhoto(
            imageRes = R.drawable.ootd_right_closet_photo,
            width = 110.dp,
            height = 192.dp,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .offset(x = 18.dp, y = 26.dp)
                .rotate(8f)
                .zIndex(1f)
        )

        EditorialPhoto(
            imageRes = R.drawable.ootd_right_sneakers_photo,
            width = 111.dp,
            height = 196.dp,
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .offset(x = 15.dp, y = (-2).dp)
                .rotate(-10f)
                .zIndex(2f)
        )

        OutfitCard(
            modifier = Modifier
                .align(Alignment.Center)
                .offset(x = 3.dp, y = 6.dp)
                .zIndex(5f)
        )
    }
}

@Composable
private fun OrganicBlob(
    modifier: Modifier,
    width: Dp,
    height: Dp,
    color: Color,
    corner: Dp
) {
    Box(
        modifier = modifier
            .width(width)
            .height(height)
            .clip(
                RoundedCornerShape(
                    topStart = corner,
                    topEnd = corner * 0.72f,
                    bottomEnd = corner,
                    bottomStart = corner * 0.55f
                )
            )
            .background(color)
    )
}

@Composable
private fun EditorialText(modifier: Modifier = Modifier) {
    Column(modifier = modifier.rotate(-9f)) {
        Text(
            text = "Good\nOutfits\nBetter\nDays",
            fontFamily = FontFamily.Cursive,
            fontSize = 26.sp,
            lineHeight = 24.sp,
            fontWeight = FontWeight.Normal,
            color = MaterialTheme.colorScheme.onBackground
        )
        Spacer(modifier = Modifier.height(10.dp))
        Box(
            modifier = Modifier
                .width(54.dp)
                .height(1.dp)
                .background(MaterialTheme.colorScheme.onBackground)
        )
    }
}

@Composable
private fun LeafCluster(modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .width(90.dp)
            .height(145.dp)
    ) {
        Box(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .offset(x = (-3).dp)
                .width(2.dp)
                .height(115.dp)
                .rotate(-12f)
                .background(WearThisSage)
        )

        Leaf(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .offset(x = (-7).dp)
                .rotate(35f),
            width = 34.dp,
            height = 62.dp
        )

        Leaf(
            modifier = Modifier
                .align(Alignment.CenterEnd)
                .offset(x = (-5).dp, y = (-7).dp)
                .rotate(50f),
            width = 32.dp,
            height = 60.dp
        )

        Leaf(
            modifier = Modifier
                .align(Alignment.CenterStart)
                .offset(x = 5.dp, y = 8.dp)
                .rotate(-40f),
            width = 35.dp,
            height = 64.dp
        )

        Leaf(
            modifier = Modifier
                .align(Alignment.BottomStart)
                .offset(x = 9.dp, y = (-13).dp)
                .rotate(-49f),
            width = 35.dp,
            height = 67.dp
        )
    }
}

@Composable
private fun Leaf(
    modifier: Modifier = Modifier,
    width: Dp,
    height: Dp
) {
    Box(
        modifier = modifier
            .width(width)
            .height(height)
            .clip(
                RoundedCornerShape(
                    topStart = height,
                    topEnd = 5.dp,
                    bottomEnd = height,
                    bottomStart = 5.dp
                )
            )
            .background(
                Brush.linearGradient(
                    colors = listOf(
                        WearThisSage.copy(alpha = 0.85f),
                        MaterialTheme.colorScheme.secondary.copy(alpha = 0.75f)
                    )
                )
            )
    )
}

@Composable
private fun EditorialPhoto(
    @DrawableRes imageRes: Int,
    width: Dp,
    height: Dp,
    modifier: Modifier = Modifier
) {
    OnboardingResourceImage(
        imageRes = imageRes,
        contentDescription = null,
        contentScale = ContentScale.Crop,
        modifier = modifier
            .width(width)
            .height(height)
            .shadow(
                elevation = 10.dp,
                shape = RoundedCornerShape(1.dp),
                ambientColor = Color.Black.copy(alpha = 0.08f),
                spotColor = Color.Black.copy(alpha = 0.14f)
            )
    )
}

@Composable
private fun OutfitCard(modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier
            .width(214.dp)
            .shadow(
                elevation = 18.dp,
                shape = RoundedCornerShape(24.dp),
                ambientColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.08f),
                spotColor = Color.Black.copy(alpha = 0.10f)
            ),
        shape = RoundedCornerShape(24.dp),
        color = MaterialTheme.colorScheme.surface
    ) {
        Column(
            modifier = Modifier.padding(
                horizontal = 14.dp,
                vertical = 15.dp
            )
        ) {
            Text(
                text = "TODAY'S OUTFIT",
                color = MaterialTheme.colorScheme.primary,
                fontWeight = FontWeight.SemiBold,
                letterSpacing = 2.7.sp,
                fontSize = 10.sp
            )

            Spacer(modifier = Modifier.height(12.dp))

            OutfitItem(
                imageRes = R.drawable.cream_knit_sweater_cutout,
                name = "Cream knit"
            )

            Spacer(modifier = Modifier.height(6.dp))

            OutfitItem(
                imageRes = R.drawable.taupe_wide_leg_pleated_trousers,
                name = "Relaxed trousers"
            )

            Spacer(modifier = Modifier.height(6.dp))

            OutfitItem(
                imageRes = R.drawable.minimalist_white_sneaker_pair,
                name = "White sneakers"
            )

            Spacer(modifier = Modifier.height(8.dp))

            WeatherCard()
        }
    }
}

@Composable
private fun OutfitItem(
    @DrawableRes imageRes: Int,
    name: String
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(53.dp)
            .clip(RoundedCornerShape(15.dp))
            .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.78f))
            .padding(start = 5.dp, end = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        OnboardingResourceImage(
            imageRes = imageRes,
            contentDescription = name,
            modifier = Modifier
                .width(52.dp)
                .height(47.dp),
            contentScale = ContentScale.Fit
        )

        Spacer(modifier = Modifier.width(5.dp))

        Text(
            text = name,
            modifier = Modifier.weight(1f),
            fontSize = 10.5.sp,
            fontWeight = FontWeight.Normal,
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 1
        )

        Text(
            text = "›",
            fontSize = 22.sp,
            fontWeight = FontWeight.Light,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun WeatherCard() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(50.dp)
            .clip(RoundedCornerShape(15.dp))
            .background(MaterialTheme.colorScheme.secondaryContainer.copy(alpha = 0.65f))
            .padding(horizontal = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = "☼",
            fontSize = 27.sp,
            color = ProcessingAmber,
            fontWeight = FontWeight.Light
        )

        Spacer(modifier = Modifier.width(8.dp))

        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = "Perfect for 68°F",
                fontSize = 10.5.sp,
                fontWeight = FontWeight.Medium,
                color = MaterialTheme.colorScheme.onSurface
            )
            Text(
                text = "Casual · Class · Coffee",
                fontSize = 8.5.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        Text(
            text = "›",
            fontSize = 21.sp,
            fontWeight = FontWeight.Light,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun Headline(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Your closet.\nYour OOTD.",
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Center,
            fontFamily = FontFamily.Serif,
            fontWeight = FontWeight.Medium,
            fontSize = 43.sp,
            lineHeight = 43.sp,
            letterSpacing = (-1.2).sp,
            color = MaterialTheme.colorScheme.onBackground
        )

        Spacer(modifier = Modifier.height(13.dp))

        Text(
            text = "Outfits from the clothes you own —\nstyled for your plans, vibe, and weather.",
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Center,
            fontSize = 16.sp,
            lineHeight = 21.sp,
            fontWeight = FontWeight.Normal,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun FeatureStrip(modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(24.dp),
        color = MaterialTheme.colorScheme.surface.copy(alpha = 0.35f)
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            FeatureStep(
                number = "1",
                text = "Your wardrobe",
                color = MaterialTheme.colorScheme.secondary
            )
            DividerLine()
            FeatureStep(
                number = "2",
                text = "AI styled",
                color = MaterialTheme.colorScheme.primary
            )
            DividerLine()
            FeatureStep(
                number = "3",
                text = "Real life",
                color = MaterialTheme.colorScheme.tertiary
            )
        }
    }
}

@Composable
private fun FeatureStep(
    number: String,
    text: String,
    color: Color
) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Box(
            modifier = Modifier
                .size(26.dp)
                .background(color = color, shape = CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = number,
                color = Color.White,
                fontSize = 11.sp,
                fontWeight = FontWeight.Medium
            )
        }
        Spacer(modifier = Modifier.width(6.dp))
        Text(
            text = text,
            color = MaterialTheme.colorScheme.onSurface,
            fontSize = 10.sp,
            fontWeight = FontWeight.Normal
        )
    }
}

@Composable
private fun DividerLine() {
    Box(
        modifier = Modifier
            .width(12.dp)
            .height(1.dp)
            .background(MaterialTheme.colorScheme.outlineVariant)
    )
}

@Composable
private fun GetStartedButton(
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    Button(
        onClick = onClick,
        modifier = modifier
            .fillMaxWidth()
            .height(57.dp),
        shape = RoundedCornerShape(21.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.primary,
            contentColor = MaterialTheme.colorScheme.onPrimary
        )
    ) {
        Spacer(modifier = Modifier.width(22.dp))
        Text(
            text = "Get started",
            modifier = Modifier.weight(1f),
            textAlign = TextAlign.Center,
            fontSize = 17.sp,
            fontWeight = FontWeight.SemiBold
        )
        Text(
            text = "→",
            fontSize = 25.sp,
            fontWeight = FontWeight.Light
        )
    }
}

@Composable
private fun SignInRow(
    modifier: Modifier = Modifier,
    onSignIn: () -> Unit
) {
    Row(
        modifier = modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = "Already have an account? ",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 13.sp
        )
        Text(
            text = "Sign in",
            color = MaterialTheme.colorScheme.primary,
            fontSize = 13.sp,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier.clickable(onClick = onSignIn)
        )
    }
}

@Preview(
    name = "OOTD Onboarding",
    showBackground = true,
    widthDp = 393,
    heightDp = 852
)
@Composable
private fun OnboardingScreenPreview() {
    WearThisTheme(darkTheme = false) {
        OnboardingScreen(
            onGetStarted = {},
            onSignIn = {}
        )
    }
}
