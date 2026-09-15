# WearThis clothing description agent

`agent.py` defines only the Google ADK agent. It has no HTTP route, upload
handler, database write, or image-download logic. Wardrobe's
`POST /api/wardrobe/describe/` calls this module, then persists the result as a
`ClothingItem` for the authenticated user. Callers should give the agent one
image as ADK multimodal content (whether it originated from an upload or a URL)
and read the structured result from the `clothing_description` output key.

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
Pydantic to the values in `WEARTHIS_Clothing_Database_Model.md`; it deliberately
does not return storage-owned fields such as `id`, `user_id`, `image_url`,
foreign-key IDs, or timestamps.

## Test with local images

Put images in `backend/description/img/` and run this from the backend
directory:

```bash
python3 description/test_agent.py
```

The script uses every supported image in `img/`, so each successful response
both verifies `GEMINI_API_KEY` and writes a validated JSON file to
`description/generated_json/`. To process only one image or choose another
output folder:

```bash
python3 description/test_agent.py --image description/img/polo.png --output-dir /tmp/wearthis-json
```
