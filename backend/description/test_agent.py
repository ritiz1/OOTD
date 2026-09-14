"""Run the WearThis description agent against local clothing images.

This is an integration test, not a unit test: a successful image result proves
that GEMINI_API_KEY is usable and writes the schema-validated JSON payload.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import ClothingDescription, root_agent


DESCRIPTION_DIR = Path(__file__).resolve().parent
DEFAULT_IMAGE_DIR = DESCRIPTION_DIR / "img"
DEFAULT_OUTPUT_DIR = DESCRIPTION_DIR / "generated_json"
APP_NAME = "wearthis_description_test"
USER_ID = "local_test_user"
SUPPORTED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the Gemini key and generate WearThis JSON from images."
    )
    parser.add_argument(
        "--image",
        type=Path,
        action="append",
        help="Image to process. Repeat for multiple images. Defaults to every image in img/.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for JSON files (default: {DEFAULT_OUTPUT_DIR}).",
    )
    return parser.parse_args()


def image_paths(requested_images: list[Path] | None) -> list[Path]:
    paths = requested_images or sorted(
        path for path in DEFAULT_IMAGE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_SUFFIXES
    )
    if not paths:
        raise FileNotFoundError(
            f"No supported images found. Add images to {DEFAULT_IMAGE_DIR} or use --image."
        )

    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Image file(s) not found: {', '.join(missing)}")
    return paths


def payload_from_value(value: object) -> ClothingDescription:
    """Validate either ADK's stored JSON string or its already-parsed object."""

    if isinstance(value, str):
        return ClothingDescription.model_validate_json(value)
    return ClothingDescription.model_validate(value)


async def describe_image(image_path: Path) -> ClothingDescription:
    mime_type, _ = mimetypes.guess_type(image_path.name)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Unsupported image type: {image_path}")

    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)
    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(text="Extract the metadata for this single clothing item."),
            types.Part.from_bytes(data=image_path.read_bytes(), mime_type=mime_type),
        ],
    )

    result: object | None = None
    final_text: str | None = None
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        # output_key is written to state_delta when ADK produces structured output.
        if event.actions and event.actions.state_delta:
            result = event.actions.state_delta.get("clothing_description", result)
        if event.is_final_response() and event.content:
            final_text = "".join(
                part.text for part in event.content.parts if getattr(part, "text", None)
            ) or final_text

    if result is None:
        latest_session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session.id
        )
        result = latest_session.state.get("clothing_description")
    if result is None and final_text:
        result = final_text
    if result is None:
        raise RuntimeError("The agent completed without returning clothing_description JSON.")

    return payload_from_value(result)


async def main() -> int:
    args = parse_args()
    # The agent also loads this file, but checking it here yields a clear message
    # before an image request is made and never prints the secret.
    load_dotenv(DESCRIPTION_DIR.parent / ".env")
    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY is missing from backend/.env.")
        return 2

    paths = image_paths(args.image)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    failures = 0

    for image_path in paths:
        try:
            description = await describe_image(image_path)
            output_path = args.output_dir / f"{image_path.stem}.json"
            output_path.write_text(
                json.dumps(description.model_dump(mode="json"), indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"PASS  {image_path.name} -> {output_path}")
        except Exception as error:
            # Do not include environment contents in failure output.
            failures += 1
            print(f"FAIL  {image_path.name}: {type(error).__name__}: {error}")

    if failures:
        print(f"{failures} image(s) failed. A successful request confirms the API key works.")
        return 1

    print("API key verified and all JSON files were generated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
