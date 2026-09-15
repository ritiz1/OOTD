"""Run the recommendation agent for a prepared wardrobe and schedule payload."""

import json
import uuid

from google.adk.runners import InMemoryRunner
from google.genai import types

from .agent import root_agent


APP_NAME = "wearthis_recommendation_api"


async def run_recommendation_agent(payload: dict, *, user_id: str) -> dict:
    message = types.Content(
        role="user",
        parts=[types.Part(text=json.dumps(payload))],
    )
    session_id = str(uuid.uuid4())
    final_text = None
    adk_error = None

    async with InMemoryRunner(agent=root_agent, app_name=APP_NAME) as runner:
        await runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message,
        ):
            if event.error_code:
                adk_error = event.error_code
                continue
            if event.is_final_response() and event.content:
                final_text = "".join(
                    part.text or "" for part in event.content.parts or []
                )

    if adk_error:
        raise RuntimeError(f"Recommendation agent error: {adk_error}")
    if not final_text:
        raise RuntimeError("Recommendation agent returned no final response.")
    return json.loads(final_text)
