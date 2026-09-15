# WearThis outfit recommendation agent

`agent.py` defines only the Google ADK agent. It has no HTTP route, wardrobe
loading, or database write. Wardrobe's `POST /api/wardrobe/recommend/` calls
this module with the authenticated user's resolved wardrobe plus a client-supplied
schedule, then returns the structured daily plan. Recommendations are not
persisted yet.

## Setup

Install the additional packages in the backend virtual environment:

```bash
pip install google-adk litellm pydantic
```

Add the following to `backend/.env` (create it from `.env.example` if needed):

```dotenv
GEMINI_API_KEY=your-google-ai-studio-key
# Optional: defaults to gemini/gemini-3.6-flash
WEARTHIS_GEMINI_MODEL=gemini/gemini-3.6-flash
```

`agent.py` loads that backend `.env` explicitly because ADK's LiteLLM adapter
does not implicitly load it in production mode. The response is constrained by
the Pydantic models in `schemas.py`.

## API

Authenticated `POST /api/wardrobe/recommend/` with JSON body:

```json
{
  "schedule": [
    {
      "event_id": "morning-class",
      "start_time": "09:00",
      "end_time": "11:00",
      "activity": "Class on campus",
      "weather": {
        "status": "cool and breezy",
        "temperature_c": 12,
        "precipitation": "none"
      }
    }
  ]
}
```

The server loads `clothing_items` for the current user (nested, resolved
attributes) and sends `{ "clothing_items": [...], "schedule": [...] }` to the
agent.

## CLI sample run

From the backend directory:

```bash
.venv/bin/python recommendation/run_sample.py
```

That uses `sample_input.json` / validation helpers for offline agent checks.
The API path uses nested wardrobe payloads from `wardrobe_payload.py`.
