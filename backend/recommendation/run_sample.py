"""Run the sample through ADK, save its JSON, and validate the result.

Usage: .venv/bin/python recommendation/run_sample.py
"""

import asyncio
import json
import sys
from pathlib import Path

from litellm.exceptions import ServiceUnavailableError

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from recommendation.service import run_recommendation_agent
from validate_output import validate_recommendations


INPUT_PATH = HERE / "sample_input.json"
OUTPUT_PATH = HERE / "latest_output.json"


async def request_recommendation(sample: dict) -> dict:
    """Send the sample through the same service used by the Django API."""
    return await run_recommendation_agent(sample, user_id="sample-user")


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
