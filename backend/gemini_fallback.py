"""Retry and model-fallback policy for Gemini API requests.

The ordered models below are general-purpose, multimodal Gemini models that
Google lists with Free Tier standard access.  Keep task-specific agents out of
this list: image-generation, Live, TTS, and computer-use models are not
drop-in replacements for structured-output prompts.
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import Awaitable, Callable
from typing import TypeVar


# Ordered from highest-capability Flash model to lower-cost fallbacks.  See:
# https://ai.google.dev/gemini-api/docs/pricing
FREE_TIER_MODEL_ORDER = (
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
)
BUSY_RETRIES_PER_MODEL = 3

T = TypeVar("T")


class GeminiUnavailableError(RuntimeError):
    """Every configured free-tier model was temporarily unavailable or exhausted."""


def model_order() -> tuple[str, ...]:
    """Return the configured model first, followed by the free-tier fallbacks."""

    configured = os.getenv("WEARTHIS_GEMINI_MODEL", "").removeprefix("gemini/")
    candidates = (configured, *FREE_TIER_MODEL_ORDER) if configured else FREE_TIER_MODEL_ORDER
    return tuple(dict.fromkeys(model for model in candidates if model))


def is_busy_error(error: Exception) -> bool:
    message = str(error).lower()
    return any(marker in message for marker in (
        "503", "service unavailable", "status\": \"unavailable\"", "high demand",
    ))


def is_exhausted_error(error: Exception) -> bool:
    message = str(error).lower()
    return any(marker in message for marker in (
        "429", "resource_exhausted", "resource exhausted", "quota", "rate limit",
    ))


async def run_with_gemini_fallback(
    call: Callable[[str], Awaitable[T]],
) -> T:
    """Run ``call`` with busy retries, then move through the model order.

    A 503 is retried up to three times for the same model with short exponential
    backoff.  A quota/rate-limit exhaustion error immediately advances to the
    next model.  After the three busy attempts, it also advances so a single
    overloaded model cannot block the request.
    """

    failures: list[str] = []
    for model_name in model_order():
        for attempt in range(BUSY_RETRIES_PER_MODEL):
            try:
                return await call(model_name)
            except Exception as error:
                if is_exhausted_error(error):
                    failures.append(f"{model_name}: exhausted")
                    break
                if is_busy_error(error):
                    if attempt == BUSY_RETRIES_PER_MODEL - 1:
                        failures.append(f"{model_name}: busy after {BUSY_RETRIES_PER_MODEL} attempts")
                        break
                    await asyncio.sleep(2**attempt)
                    continue
                raise

    detail = "; ".join(failures) or "no eligible model was available"
    raise GeminiUnavailableError(f"Gemini is temporarily unavailable: {detail}.")
