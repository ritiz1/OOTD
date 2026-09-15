from __future__ import annotations

import asyncio
import mimetypes
import uuid
from pathlib import Path
from urllib.request import Request, urlopen

from dotenv import load_dotenv
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from gemini_fallback import GeminiUnavailableError, model_order, run_with_gemini_fallback
from wardrobe.serializers import (
    ClothingDescriptionSchemaSerializer,
    ClothingItemDescribeResponseSerializer,
    DescriptionInputSerializer,
    absolute_image_url,
)
from wardrobe.services import persist_clothing_description


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


APP_NAME = "wearthis_description_api"
DEFAULT_MODEL_NAME = model_order()[0]


def _extension_for_mime(mime_type: str, fallback_name: str = "") -> str:
    guessed = mimetypes.guess_extension(mime_type) or ""
    if guessed:
        return guessed
    suffix = Path(fallback_name).suffix
    return suffix if suffix else ".bin"


def save_uploaded_image(
    *, user_id, image_bytes: bytes, mime_type: str, filename: str
) -> tuple[str, str]:
    """Persist uploaded bytes and return its storage path and public media URL."""

    extension = _extension_for_mime(mime_type, filename)
    storage_path = f"wardrobe/{user_id}/{uuid.uuid4().hex}{extension}"
    saved_path = default_storage.save(storage_path, ContentFile(image_bytes))
    return saved_path, default_storage.url(saved_path)


async def run_description_agent(
    image_bytes: bytes,
    mime_type: str,
    *,
    user_id: str,
):
    """Call the configured description agent asynchronously using the ADK runner."""

    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    from description.agent import ClothingDescription, create_agent

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(text="Extract the metadata for this single clothing item."),
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
        ],
    )

    async def call(model_name: str):
        session_service = InMemorySessionService()
        session = await session_service.create_session(app_name=APP_NAME, user_id=user_id)
        runner = Runner(app_name=APP_NAME, agent=create_agent(model_name), session_service=session_service)
        result: object | None = None
        final_text: str | None = None
        async for event in runner.run_async(user_id=user_id, session_id=session.id, new_message=message):
            if event.actions and event.actions.state_delta:
                result = event.actions.state_delta.get("clothing_description", result)
            if event.is_final_response() and event.content:
                final_text = "".join(part.text for part in event.content.parts if getattr(part, "text", None)) or final_text
        if result is None:
            latest_session = await session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session.id)
            result = latest_session.state.get("clothing_description")
        if result is None:
            result = final_text
        if result is None:
            raise RuntimeError("The description agent did not return clothing_description JSON.")
        return ClothingDescription.model_validate_json(result) if isinstance(result, str) else ClothingDescription.model_validate(result)

    return await run_with_gemini_fallback(call)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def describe_clothing_item(request):
    """Accept an image, run the description agent, and persist a ClothingItem."""

    serializer = DescriptionInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    uploaded_image = serializer.validated_data.get("image")
    uploaded_url = serializer.validated_data.get("image_url")
    user_id = str(request.user.id)
    uploaded_storage_path: str | None = None

    if uploaded_image:
        image_bytes = uploaded_image.read()
        mime_type = uploaded_image.content_type or mimetypes.guess_type(uploaded_image.name)[0]
        if not mime_type or not mime_type.startswith("image/"):
            return Response(
                {"detail": "Unsupported image content type."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        uploaded_storage_path, image_url = save_uploaded_image(
            user_id=user_id,
            image_bytes=image_bytes,
            mime_type=mime_type,
            filename=uploaded_image.name,
        )
    elif uploaded_url:
        request_obj = Request(uploaded_url, method="GET")
        with urlopen(request_obj, timeout=30) as response:
            image_bytes = response.read()
            mime_type = response.headers.get_content_type() or "image/jpeg"
        image_url = uploaded_url
    else:
        return Response(
            {"detail": "Provide an uploaded image or image_url."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        model_payload = asyncio.run(
            run_description_agent(image_bytes, mime_type, user_id=user_id)
        )
    except GeminiUnavailableError as exc:
        if uploaded_storage_path:
            default_storage.delete(uploaded_storage_path)
        return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as exc:
        if uploaded_storage_path:
            default_storage.delete(uploaded_storage_path)
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    payload = model_payload.model_dump(mode="json")
    output = ClothingDescriptionSchemaSerializer(data=payload)
    if not output.is_valid():
        if uploaded_storage_path:
            default_storage.delete(uploaded_storage_path)
        return Response(output.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        item = persist_clothing_description(
            user=request.user,
            image_url=image_url,
            description=output.validated_data,
            model_name=DEFAULT_MODEL_NAME,
        )
    except Exception:
        if uploaded_storage_path:
            default_storage.delete(uploaded_storage_path)
        raise

    response = ClothingItemDescribeResponseSerializer(
        {
            "id": item.id,
            "image_url": absolute_image_url(request, item.image_url),
            "user": item.user_id,
            "description": item.analysis.raw_response,
            "analysis": {
                "id": item.analysis_id,
                "model_name": item.analysis.model_name,
                "model_version": item.analysis.model_version,
                "overall_confidence": item.analysis.overall_confidence,
            },
        }
    )
    return Response(response.data, status=status.HTTP_201_CREATED)
