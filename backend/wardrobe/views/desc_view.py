from __future__ import annotations

import asyncio
import mimetypes
from pathlib import Path
from urllib.request import Request, urlopen

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from description.agent import ClothingDescription, root_agent
from wardrobe.serializers import ClothingDescriptionSchemaSerializer, DescriptionInputSerializer


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


APP_NAME = "wearthis_description_api"
USER_ID = "wearthis_api_user"


async def run_description_agent(image_bytes: bytes, mime_type: str) -> ClothingDescription:
    """Call the configured description agent asynchronously using the ADK runner."""

    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(text="Extract the metadata for this single clothing item."),
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
        ],
    )

    result: object | None = None
    final_text: str | None = None
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.actions and event.actions.state_delta:
            result = event.actions.state_delta.get("clothing_description", result)
        if event.is_final_response() and event.content:
            final_text = "".join(
                part.text for part in event.content.parts if getattr(part, "text", None)
            ) or final_text

    if result is None:
        latest_session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session.id,
        )
        result = latest_session.state.get("clothing_description")
    if result is None and final_text:
        result = final_text
    if result is None:
        raise RuntimeError("The description agent did not return clothing_description JSON.")

    if isinstance(result, str):
        return ClothingDescription.model_validate_json(result)
    return ClothingDescription.model_validate(result)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def describe_clothing_item(request):
    """Accept an uploaded image or remote image URL and return the agent schema payload."""

    serializer = DescriptionInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    uploaded_image = serializer.validated_data.get("image")
    uploaded_url = serializer.validated_data.get("image_url")

    if uploaded_image:
        image_bytes = uploaded_image.read()
        mime_type = uploaded_image.content_type or mimetypes.guess_type(uploaded_image.name)[0]
        if not mime_type or not mime_type.startswith("image/"):
            return Response(
                {"detail": "Unsupported image content type."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    elif uploaded_url:
        request_obj = Request(uploaded_url, method="GET")
        with urlopen(request_obj, timeout=30) as response:
            image_bytes = response.read()
            mime_type = response.headers.get_content_type() or "image/jpeg"
    else:
        return Response(
            {"detail": "Provide an uploaded image or image_url."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        model_payload = asyncio.run(run_description_agent(image_bytes, mime_type))
    except Exception as exc:
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    payload = model_payload.model_dump(mode="json")
    output = ClothingDescriptionSchemaSerializer(data=payload)
    if output.is_valid():
        return Response(output.validated_data, status=status.HTTP_200_OK)
    return Response(output.errors, status=status.HTTP_400_BAD_REQUEST)
