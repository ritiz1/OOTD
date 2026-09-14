# WEARTHIS — Simple Android MVVM Skeleton

## Goal

Keep the project simple for the MVP.

No DI for now.  
No clothing models yet.  
No unnecessary clean-architecture layers.

Use these main packages:

```text
navigation/
data/
domain/
feature/
view/
viewmodel/
repository/
```

---

# Project Structure

```text
com.wearthis.app/
│
├── MainActivity.kt
│
├── WearThisApp.kt
│
├── navigation/
│   ├── AppNavHost.kt
│   └── Routes.kt
│
├── view/
│   ├── splash/
│   │   └── SplashScreen.kt
│   │
│   ├── onboarding/
│   │   └── OnboardingScreen.kt
│   │
│   ├── auth/
│   │   ├── LoginScreen.kt
│   │   └── SignUpScreen.kt
│   │
│   ├── profile/
│   │   ├── ProfileSetupScreen.kt
│   │   └── ProfileScreen.kt
│   │
│   ├── home/
│   │   └── HomeScreen.kt
│   │
│   ├── closet/
│   │   ├── ClosetScreen.kt
│   │   ├── AddClothingScreen.kt
│   │   └── ClothingDetailScreen.kt
│   │
│   └── recommendation/
│       └── RecommendationScreen.kt
│
├── viewmodel/
│   ├── SplashViewModel.kt
│   ├── OnboardingViewModel.kt
│   ├── AuthViewModel.kt
│   ├── ProfileViewModel.kt
│   ├── HomeViewModel.kt
│   ├── ClosetViewModel.kt
│   └── RecommendationViewModel.kt
│
├── repository/
│   ├── AuthRepository.kt
│   ├── ProfileRepository.kt
│   ├── ClothingRepository.kt
│   └── RecommendationRepository.kt
│
├── data/
│   ├── remote/
│   │   ├── ApiService.kt
│   │   └── ApiClient.kt
│   │
│   ├── local/
│   │   ├── AppDatabase.kt
│   │   └── dao/
│   │
│   └── dto/
│
├── domain/
│   ├── model/
│   └── usecase/
│
└── feature/
    ├── auth/
    ├── profile/
    ├── closet/
    ├── home/
    └── recommendation/
```

---

# What Each Package Does

## navigation/

Only app navigation.

```text
Routes.kt
AppNavHost.kt
```

Example flow:

```text
Splash
→ Onboarding
→ Login / Sign Up
→ Profile Setup
→ Home
→ Closet
→ Recommendation
```

---

## view/

All Compose screens.

```text
LoginScreen.kt
HomeScreen.kt
ClosetScreen.kt
RecommendationScreen.kt
```

Responsibilities:

```text
Render UI
Collect ViewModel state
Send user actions to ViewModel
Trigger navigation callbacks
```

Do not call API directly from a Screen.

---

## viewmodel/

One ViewModel per main screen/feature.

Example:

```text
LoginScreen
    ↓
AuthViewModel
```

```text
ClosetScreen
    ↓
ClosetViewModel
```

ViewModel responsibilities:

```text
UI state
Handle button clicks
Call repository/use case
Expose StateFlow
```

---

## repository/

The ViewModel talks to repositories.

Example:

```text
ClosetViewModel
      ↓
ClothingRepository
      ↓
API / Room
```

Repositories hide where data comes from.

Example future methods:

```text
login()
signup()
getProfile()
getClothing()
addClothing()
getRecommendation()
```

Do not define the real clothing objects yet.

---

## data/

Actual data sources live here.

```text
data/
├── remote/
├── local/
└── dto/
```

### remote/

Backend communication.

```text
ApiClient.kt
ApiService.kt
```

### local/

Room / local storage later.

```text
AppDatabase.kt
dao/
```

### dto/

Backend request/response objects later.

Leave empty until API models are finalized.

---

## domain/

App-level models and business actions.

For now:

```text
domain/
├── model/
└── usecase/
```

These can stay empty.

Later:

```text
domain/model/
    ClothingItem.kt

domain/usecase/
    GetWardrobeUseCase.kt
    GetRecommendationUseCase.kt
```

Do not create them yet.

---

## feature/

Use this only for feature-specific reusable code.

Example:

```text
feature/closet/
    ClosetUiState.kt
    ClosetEvent.kt
```

```text
feature/auth/
    AuthUiState.kt
```

Do not duplicate Screens or ViewModels here if they already live under `view/` and `viewmodel/`.

---

# MVVM Flow

Keep the flow simple:

```text
Screen
   ↓
ViewModel
   ↓
Repository
   ↓
API / Room
```

Later, if business logic becomes larger:

```text
Screen
   ↓
ViewModel
   ↓
UseCase
   ↓
Repository
   ↓
API / Room
```

For the MVP, do not create a UseCase for every tiny operation.

---

# Example: Closet

```text
view/
    closet/
        ClosetScreen.kt

viewmodel/
    ClosetViewModel.kt

repository/
    ClothingRepository.kt

data/
    remote/
        ApiService.kt
```

Flow:

```text
ClosetScreen
     ↓
ClosetViewModel
     ↓
ClothingRepository
     ↓
ApiService
```

---

# Example: Login

```text
view/
    auth/
        LoginScreen.kt
        SignUpScreen.kt

viewmodel/
    AuthViewModel.kt

repository/
    AuthRepository.kt
```

Flow:

```text
LoginScreen
    ↓
AuthViewModel
    ↓
AuthRepository
    ↓
ApiService
```

---

# Screens Needed for MVP

```text
SplashScreen
OnboardingScreen

LoginScreen
SignUpScreen

ProfileSetupScreen

HomeScreen

ClosetScreen
AddClothingScreen
ClothingDetailScreen

RecommendationScreen

ProfileScreen
```

---

# Main Rule

Do not over-engineer this yet.

Use:

```text
View
→ ViewModel
→ Repository
→ Data
```

Keep:

```text
navigation
data
domain
feature
view
viewmodel
repository
```

Then add models, Room entities, DTOs, and use cases only when the actual API/data contracts are ready.
