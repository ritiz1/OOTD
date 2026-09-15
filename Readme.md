# WearThis

WearThis is an Android wardrobe app backed by a Django REST API. Users can
create an account, describe and save clothing from an image, manage their
wardrobe, and request AI-generated outfit plans for scheduled events.

This guide covers the Android frontend and Django backend in this repository.

## System overview

- **Android app:** Kotlin, Jetpack Compose, Room, Retrofit, Coil, and the
  Android location APIs.
- **Backend:** Django, Django REST Framework, JWT authentication, SQLite for
  local development (or PostgreSQL when `DATABASE_URL` is configured), and
  local media storage.
- **AI features:** Google ADK/LiteLLM with Gemini. The API uses Gemini to
  extract garment metadata from an image and to generate outfit
  recommendations from the user's wardrobe and schedule.

## Prerequisites

- Python 3.10 or newer
- Android Studio with the Android SDK installed
- JDK 17 or newer for the Android Gradle Plugin
- A Gemini API key from Google AI Studio, for clothing-description and
  recommendation requests
- An Android emulator or a physical Android device (min SDK 27)

## Replicate the system locally

### 1. Start the backend

From the repository root, create and activate a virtual environment:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

Install the server dependencies and create the database schema:

```bash
pip install -r requirements.txt
python manage.py migrate
```

Create `backend/.env` from [`backend/.env.example`](backend/.env.example) and
set a unique Django secret plus your Gemini key:

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,10.0.2.2
GEMINI_API_KEY=your-google-ai-studio-key

# Optional. If omitted, the backend tries its built-in Gemini Flash fallback order.
WEARTHIS_GEMINI_MODEL=gemini-3.8-flash
```

Leave `DATABASE_URL` unset to use `backend/db.sqlite3`. To use PostgreSQL,
add a PostgreSQL URL instead:

```dotenv
DATABASE_URL=postgresql://user:password@localhost:5432/wearthis
```

Run the API for an Android emulator:

```bash
python manage.py runserver 0.0.0.0:8000
```

The backend is then available at `http://localhost:8000`. Django serves
uploaded wardrobe images from `/media/` while `DEBUG=True`.

### 2. Configure and run the Android app

Open the `frontend` directory in Android Studio, allow Gradle sync to finish,
then run the `app` configuration on an emulator or device.

The default API URL is already correct for the Android emulator:

```text
http://10.0.2.2:8000/
```

`10.0.2.2` is the emulator's route to the host machine. No frontend
configuration is needed for this setup.

For a physical device on the same Wi-Fi/LAN, identify your computer's LAN IP,
add it to `ALLOWED_HOSTS` in `backend/.env`, start Django on `0.0.0.0:8000`,
and build with that address:

```bash
cd frontend
./gradlew :app:assembleDebug \
  -PWEARTHIS_API_BASE_URL=http://YOUR_COMPUTER_LAN_IP:8000/
```

Alternatively, create `frontend/local.properties` (do not commit it):

```properties
WEARTHIS_API_BASE_URL=http://YOUR_COMPUTER_LAN_IP:8000/
```

For a USB- or wireless-debugged physical device, ADB reverse avoids LAN
configuration:

```bash
adb reverse tcp:8000 tcp:8000
cd frontend
./gradlew :app:assembleDebug \
  -PWEARTHIS_API_BASE_URL=http://127.0.0.1:8000/
```

Run the resulting build from Android Studio, or install it with
`./gradlew :app:installDebug` using the same API-base-URL property. Re-run
`adb reverse` after reconnecting or rebooting the device.

## Verify the installation

With the backend virtual environment active:

```bash
cd backend
python manage.py test users wardrobe recommendation --noinput
```

For the Android project:

```bash
cd frontend
./gradlew :app:assembleDebug :app:testDebugUnitTest
```

AI calls require a valid `GEMINI_API_KEY` and internet access. You can also
exercise the description agent against the bundled sample images:

```bash
cd backend
python description/test_agent.py --image description/img/polo.png
```

## API summary

All endpoints other than registration and token issuance require
`Authorization: Bearer <access-token>`.

| Area | Endpoint | Purpose |
| --- | --- | --- |
| Authentication | `POST /api/auth/register/` | Create an account and return JWT tokens. |
| Authentication | `POST /api/auth/token/` | Sign in with email/password. |
| Authentication | `POST /api/auth/token/refresh/` | Refresh an access token. |
| Profile | `GET` / `PATCH /api/auth/me/` | Read or update the current user. |
| Wardrobe | `POST /api/wardrobe/describe/` | Upload an image (or send `image_url`), generate metadata, and save an item. |
| Wardrobe | `GET /api/wardrobe/items/` | List the current user's clothing. |
| Wardrobe item | `GET` / `PATCH` / `DELETE /api/wardrobe/items/{id}/` | View, edit, or remove one item. |
| Recommendations | `POST /api/wardrobe/recommend/` | Generate outfits for a supplied schedule. |

The Android app manages JWT refresh automatically. It stores the local
wardrobe cache and app state in Room; recommendation plans currently persist
on the device rather than synchronizing between devices.

## Useful backend configuration

| Variable | Required | Description |
| --- | --- | --- |
| `SECRET_KEY` | Yes outside development | Django signing key. |
| `DEBUG` | No | `True` by default for local development. |
| `ALLOWED_HOSTS` | Yes for LAN devices | Comma-separated hostnames/IPs Django may serve. |
| `DATABASE_URL` | No | PostgreSQL URL; omit for SQLite. |
| `GEMINI_API_KEY` | Yes for AI features | Google AI Studio API key. |
| `WEARTHIS_GEMINI_MODEL` | No | Preferred Gemini model, before built-in fallbacks. |

Never commit `.env`, API keys, or machine-specific Android `local.properties`
files.
