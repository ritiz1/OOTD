from __future__ import annotations

import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recommendation.schemas import DailyRecommendation
from recommendation.validate_output import validate_recommendations
from recommendation.wardrobe_payload import wardrobe_items_for_user
from wardrobe.serializers import (
    DailyRecommendationResponseSerializer,
    RecommendInputSerializer,
)


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


APP_NAME = "wearthis_recommendation_api"


async def run_recommendation_agent(payload: dict, *, user_id: str) -> DailyRecommendation:
    """Call the outfit-planning agent asynchronously using the ADK runner."""

    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    from recommendation.agent import root_agent

    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=user_id)
    runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)

    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=json.dumps(payload))],
    )

    final_text: str | None = None
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=message,
    ):
        if getattr(event, "error_code", None):
            raise RuntimeError(f"ADK error: {event.error_code}")
        if event.is_final_response() and event.content:
            final_text = "".join(
                part.text for part in event.content.parts if getattr(part, "text", None)
            ) or final_text

    if not final_text:
        raise RuntimeError("The recommendation agent did not return a final response.")

    return DailyRecommendation.model_validate_json(final_text)


@api_view(["POST"])
def recommend_outfits(request):
    """Load the user's wardrobe, run the recommendation agent, and return a plan."""

    serializer = RecommendInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    schedule = serializer.validated_data["schedule"]
    clothing_items = wardrobe_items_for_user(request.user)
    if not clothing_items:
        return Response(
            {"detail": "Add clothing items to your wardrobe before requesting recommendations."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    agent_input = {
        "clothing_items": clothing_items,
        "schedule": schedule,
    }
    user_id = str(request.user.id)

    try:
        model_payload = asyncio.run(
            run_recommendation_agent(agent_input, user_id=user_id)
        )
    except Exception as exc:
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    payload = model_payload.model_dump(mode="json")
    output = DailyRecommendationResponseSerializer(data=payload)
    if not output.is_valid():
        return Response(output.errors, status=status.HTTP_400_BAD_REQUEST)

    errors = validate_recommendations(agent_input, output.validated_data)
    if errors:
        return Response(
            {"detail": errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(output.validated_data, status=status.HTTP_200_OK)
