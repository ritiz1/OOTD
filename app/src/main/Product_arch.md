# WEARTHIS

## Production Architecture & Phased Implementation Plan

**Fashion × Lifestyle • AI wardrobe recommendation system**

> **Core rule:** Backend owns product truth. Android owns presentation, user interaction, and local cache.

---

## Production Architecture

```text
Android App
Compose + ViewModel
Room cache + Coil
        |
        v
FastAPI Backend
Auth + Orchestration
Business Rules
   |        |          |              |
   v        v          v              v
PostgreSQL  Object     Gemini         Weather +
Metadata +  Storage    Vision/Stylist Geocoding
Profiles +  Originals  Probabilistic  External Context
Outfits +   + Thumbs   Judgment
Feedback
        |
        v
Async Queue / Worker
Analysis + Retries
```

---

## 1. Separation of Concerns

| Layer | Owns | Must Not Own |
|---|---|---|
| Android | UI, screen state, photo selection, Room cache, rendering, offline UX | Styling business rules, AI prompts, canonical wardrobe |
| FastAPI | Authentication, orchestration, validation, business rules, API contracts | Image bytes as permanent storage |
| PostgreSQL | Canonical metadata, users, profiles, recommendations, feedback | Binary image data |
| Object Storage | Original garment images and thumbnails | Business metadata |
| AI | Garment interpretation and subjective styling judgment | Source of truth or direct DB writes |
| Weather/Location | External environmental context | Wardrobe state |

---

## 2. Canonical Data Ownership

- PostgreSQL is the source of truth for clothing metadata, user profile, recommendations, and feedback.
- Cloud object storage is the source of truth for original garment photos and thumbnails.
- Room mirrors server state for fast rendering/offline access; it is not authoritative.
- Coil handles local image caching for display.
- Gemini produces candidate interpretations; backend validation decides what is persisted.

---

## 3. Phase 0 — Freeze Contracts Before Coding

Before Android and backend development diverge, freeze the shared enums and DTOs.

### Core `ClothingItem`

```text
id
userId
imageKey
thumbnailKey
name
category
subCategory
primaryColor
secondaryColors
pattern
formality
warmth
rainFriendly
styleTags
analysisStatus
createdAt
updatedAt
```

### Recommended Enums

**Category**

```text
TOP
BOTTOM
SHOES
OUTERWEAR
ACCESSORY
```

**Occasion**

```text
CASUAL
CLASS
WORK
INTERVIEW
DATE
DINNER
PARTY
WORKOUT
FORMAL
```

**Vibe**

```text
SAFE
STYLISH
BOLD
```

**Temperature preference**

```text
RUNS_COLD
NORMAL
RUNS_HOT
```

---

## 4. Phase 1 — Basic Wardrobe Vertical Slice

Build a complete end-to-end path before introducing AI.

- Seed wardrobe rows in PostgreSQL.
- Expose `GET /v1/clothing`.
- Render the closet in Android.
- Prove the client-server boundary.

### Backend

```text
ClothingRoute
    ↓
ClothingService
    ↓
ClothingRepository
    ↓
PostgreSQL
```

### Android

```text
ClosetScreen
    ↓
ClosetViewModel
    ↓
GetWardrobeUseCase
    ↓
ClothingRepository
    ↓
Retrofit / Room
```

---

## 5. Phase 2 — Production Image Upload

Do not permanently proxy image bytes through FastAPI.

1. Android requests `POST /v1/clothing/upload-session`.
2. Backend creates `clothingId` and a short-lived signed upload URL.
3. Android uploads directly to a private object-storage bucket.
4. Backend stores the storage object key, not image bytes.
5. Android calls `POST /v1/clothing/{id}/upload-complete`.

---

## 6. Phase 3 — Asynchronous Clothing Analysis

After upload completion:

1. Mark the garment `PROCESSING`.
2. Enqueue an analysis job.
3. A worker reads the image from object storage.
4. The worker sends it to Gemini with a strict schema.
5. Validate the response.
6. Persist normalized metadata.

### State Machine

```text
PENDING_UPLOAD
      ↓
PROCESSING
   ↙     ↘
READY   FAILED
```

`FAILED` is a recoverable terminal state.

> Gemini never writes directly to PostgreSQL.

---

## 7. Phase 4 — User Profile

Persist small, high-value personalization fields first:

```text
stylePreference
temperatureSensitivity
preferredColors
dislikedColors
```

Expose:

```text
GET /v1/profile
PATCH /v1/profile
```

Room caches the profile locally.

---

## 8. Phase 5 — Location and Weather

Android sends:

```text
destination
scheduled time
occasion
vibe
```

Backend resolves location and weather through provider-specific integrations behind:

```text
WeatherService
LocationService
```

`OutfitRecommendationService` should consume an internal `WeatherContext`, not provider-specific response objects.

---

## 9. Phase 6 — Candidate Filtering

Never send a 100-item wardrobe directly to the LLM.

Filter deterministically first by:

```text
category
weather
warmth
rain suitability
occasion/formality
```

Example:

```text
140 wardrobe items
        ↓
15–20 plausible candidates
```

---

## 10. Phase 7 — AI Styling

Send to Gemini:

```text
candidate metadata
thumbnails
user profile
occasion
vibe
weather
```

Require the model to choose only supplied clothing IDs.

Before persisting anything, backend validates that selected IDs:

- belong to the authenticated user
- were part of the candidate set

---

## 11. Phase 8 — Persist Recommendation History

| Table | Purpose / Key Fields |
|---|---|
| `outfit_requests` | `user_id`, `destination`, `scheduled_at`, `occasion`, `vibe`, `weather_snapshot` |
| `outfit_recommendations` | `request_id`, `confidence`, `reason`, `model`, `prompt_version` |
| `outfit_items` | `recommendation_id`, `clothing_item_id`, `role` |
| `recommendation_feedback` | `recommendation_id`, `user_id`, `accepted`, `reason` |

---

## 12. Complete Recommendation Sequence

```text
Android
  ↓
FastAPI
  ↓
authenticated user
  ↓
ProfileService + WardrobeRepository + WeatherService
  ↓
CandidateSelector
  ↓
StylingService
(Gemini + thumbnails + metadata)
  ↓
RecommendationValidator
  ↓
OutfitRepository
  ↓
PostgreSQL
  ↓
response DTO
  ↓
Android Compose UI
```

---

## 13. Backend Package Boundaries

```text
api/            HTTP routes and auth dependencies
services/       business orchestration
repositories/   database access only
models/         SQLAlchemy persistence models
schemas/        Pydantic request/response contracts
integrations/   Gemini, storage, weather, geocoding
workers/        asynchronous jobs and retryable processing
db/             session and Alembic migrations
```

---

## 14. Android Package Boundaries

```text
core/       networking, Room, auth, design system
feature/    closet, add clothing, home, recommendation, profile
data/       repository implementations, DTO/entity mapping
domain/     use cases and domain models
```

ViewModels should never contain:

```text
Retrofit calls
SQL
Gemini prompts
weather parsing
```

---

## 15. Recommended Production Stack

| Area | Stack |
|---|---|
| Android | Kotlin, Jetpack Compose, Material 3, ViewModel, StateFlow, Hilt, Room, DataStore, WorkManager, Retrofit, OkHttp, kotlinx.serialization, Coil |
| Backend | Python, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic |
| Data | PostgreSQL |
| Media | Private GCS/S3-style object storage with signed upload/download URLs |
| Async | Managed task queue / worker |
| AI | Gemini multimodal model with structured outputs |
| External context | Weather API + geocoding/places |
| Operations | Containerized deployment, secret manager, structured logging, Sentry, CI/CD |

---

## 16. Hackathon Implementation Order

| Phase | Deliverable |
|---|---|
| A | PostgreSQL + seed wardrobe + `GET /clothing` + Android closet |
| B | `POST /recommend` + weather + Gemini + return outfit |
| C | Polished recommendation screen using real cloud-hosted wardrobe images |
| D | Cloud upload + Gemini garment analysis |
| E | Feedback, retry handling, polish, demo |

> **Implementation principle:** Each phase must leave the system in a demoable state. Never build three layers in parallel without a working vertical slice.
