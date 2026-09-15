"""Runtime compatibility for LiteLLM on supported Python versions.

LiteLLM 1.100.1 advertises Python 3.10 support, but one of its optional
Anthropic context-management modules imports ``NotRequired`` from ``typing``.
That name was added to the standard library only in Python 3.11; its supported
backport lives in ``typing_extensions`` on Python 3.10.
"""

from __future__ import annotations

import typing

from typing_extensions import NotRequired


def apply_typing_compatibility() -> None:
    """Provide Python 3.11's ``typing.NotRequired`` on Python 3.10."""

    if not hasattr(typing, "NotRequired"):
        typing.NotRequired = NotRequired


apply_typing_compatibility()
