# Main app flow

Login and sign-up open Today. Today, Wardrobe, Plan, and Profile share a persistent bottom bar. Uploads return to the previous tab.

## Backend and device setup

Start the existing Django backend with its configured database and Gemini credentials. The Android default API URL is `http://10.0.2.2:8000/` for the emulator. For a physical phone, build with `-PWEARTHIS_API_BASE_URL=http://YOUR_COMPUTER_LAN_IP:8000/` and include that host in Django's `ALLOWED_HOSTS`. Start Django listening on the LAN interface. No database migration is required for the new wardrobe endpoints.

## Data flow

- `MainViewModel` owns profile, wardrobe, planner, loading, and error state. Compose screens call its actions.
- Wardrobe uses the existing Room/photo upload repository. `GET api/wardrobe/items/` synchronizes the signed-in user's photos; `DELETE api/wardrobe/items/{id}/` removes a piece on the server before clearing the local copy.
- Plans and recommendation results persist per account on this device. They do not yet sync between devices.
- Plan submission fetches the selected city's hourly forecast, then sends `schedule[].weather.temperature_c`, weather status, precipitation, destination-offset timestamps, occasion, and vibe through the existing authenticated recommendation endpoint.
- The planner supports future events within the forecast window. It never substitutes invented weather on failure. Location is optional; city/postal-code search is available after denial or timeout.
- Weather uses a separate unauthenticated HTTP client, and the app displays Open-Meteo attribution. API references: https://open-meteo.com/en/docs and https://open-meteo.com/en/docs/geocoding-api. Review provider terms before commercial distribution.
- The Today illustration uses existing bundled assets until the user has wardrobe photos. It is labeled as inspiration, not presented as a generated recommendation.

## Checks

Android: `gradlew.bat :app:assembleDebug :app:testDebugUnitTest`

Backend: `.venv\Scripts\python.exe manage.py test wardrobe recommendation users --noinput`

Unit tests cover event ordering, Celsius serialization, destination time zones, persistence, and account isolation for the new wardrobe endpoints. Live AI calls, device location, and the complete on-device flow still require a configured running backend and device verification.
