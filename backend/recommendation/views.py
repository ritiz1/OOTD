import asyncio
import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from litellm.exceptions import ServiceUnavailableError

from .serializers import RecommendationRequestSerializer
from .service import run_recommendation_agent
from .validate_output import validate_recommendations
from .wardrobe_payload import wardrobe_items_for_user


@api_view(["POST"])
def recommend_outfits(request):
    """Recommend outfits using only the authenticated user's stored wardrobe."""
    serializer = RecommendationRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    clothing_items = wardrobe_items_for_user(request.user)
    if not clothing_items:
        return Response(
            {"detail": "Add at least one clothing item before requesting recommendations."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    payload = {
        "clothing_items": clothing_items,
        "schedule": serializer.validated_data["schedule"],
    }
    try:
        result = asyncio.run(
            run_recommendation_agent(payload, user_id=str(request.user.id))
        )
    except ServiceUnavailableError:
        return Response(
            {"detail": "The recommendation model is temporarily unavailable."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except (RuntimeError, json.JSONDecodeError) as exc:
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    errors = validate_recommendations(payload, result)
    if errors:
        return Response(
            {"detail": "The recommendation response failed validation.", "errors": errors},
            status=status.HTTP_502_BAD_GATEWAY,
        )
    return Response(result)
