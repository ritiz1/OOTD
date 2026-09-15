"""Run the sample through ADK, save its JSON, and validate the result.

Usage: .venv/bin/python recommendation/run_sample.py
"""

import asyncio
import json
import sys
from pathlib import Path

from google.adk.runners import InMemoryRunner
from google.genai import types
from litellm.exceptions import ServiceUnavailableError

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from recommendation.agent import root_agent
from recommendation.validate_output import validate_recommendations


INPUT_PATH = HERE / "sample_input.json"
OUTPUT_PATH = HERE / "latest_output.json"


async def request_recommendation(sample: dict) -> dict:
    """Send the sample as one message and parse ADK's final response."""
    message = types.Content(
        role="user",
        parts=[types.Part(text=json.dumps(sample))],
    )
    final_text = None

    async with InMemoryRunner(agent=root_agent, app_name="recommendation_test") as runner:
        await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id="sample-user",
            session_id="sample-run",
        )
        async for event in runner.run_async(
            user_id="sample-user",
            session_id="sample-run",
            new_message=message,
        ):
            if event.error_code:
                raise RuntimeError(f"ADK error: {event.error_code}")
            if event.is_final_response() and event.content:
                final_text = "".join(
                    part.text or "" for part in event.content.parts or []
                )

    if not final_text:
        raise RuntimeError("ADK returned no final text response.")
    return json.loads(final_text)


async def main() -> int:
    sample = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    try:
        response = await request_recommendation(sample)
    except ServiceUnavailableError:
        print("FAIL: Gemini is temporarily unavailable (HTTP 503). Try again later.")
        return 1
    except (RuntimeError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 1

    OUTPUT_PATH.write_text(json.dumps(response, indent=2) + "\n", encoding="utf-8")
    errors = validate_recommendations(sample, response)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"Response saved to {OUTPUT_PATH}")
        return 1

    print(f"PASS: Response saved and validated at {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
