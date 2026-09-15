"""Check one ADK response against the wardrobe and schedule sent to the agent.

Usage: python recommendation/validate_output.py INPUT.json OUTPUT.json
"""

import argparse
import json
from pathlib import Path

from pydantic import ValidationError

from schemas import DailyRecommendation


ITEM_FIELDS = (
    "clothing_item_ids",
    "keep_item_ids",
    "remove_item_ids",
    "put_on_item_ids",
    "pack_item_ids",
)


def validate_recommendations(sample: dict, response: dict) -> list[str]:
    """Return errors; an empty list means the response passed these checks."""
    try:
        result = DailyRecommendation.model_validate(response)
    except ValidationError as exc:
        return [f"Response shape: {error['loc']}: {error['msg']}" for error in exc.errors()]

    events = sample["schedule"]
    allowed_ids = {item["id"] for item in sample["clothing_items"]}
    errors = []

    if len(result.recommendations) != len(events):
        errors.append(
            f"Expected {len(events)} recommendations; got {len(result.recommendations)}."
        )

    previous_outfit = set()
    for index, recommendation in enumerate(result.recommendations):
        label = f"Recommendation {index + 1}"
        if index < len(events):
            event = events[index]
            for field in ("event_id", "start_time", "end_time", "activity"):
                if getattr(recommendation, field) != event[field]:
                    errors.append(f"{label}: {field} does not match schedule event {index + 1}.")

        for field in ITEM_FIELDS:
            values = getattr(recommendation, field)
            if len(values) != len(set(values)):
                errors.append(f"{label}: {field} contains duplicate IDs.")
            unknown = set(values) - allowed_ids
            if unknown:
                errors.append(f"{label}: {field} has unknown item IDs: {sorted(unknown)}.")

        outfit = set(recommendation.clothing_item_ids)
        packed = set(recommendation.pack_item_ids)
        if outfit & packed:
            errors.append(f"{label}: an item cannot be worn and packed at the same event.")

        expected = {
            "keep_item_ids": previous_outfit & outfit,
            "remove_item_ids": previous_outfit - outfit,
            "put_on_item_ids": outfit - previous_outfit,
        }
        for field, expected_ids in expected.items():
            if set(getattr(recommendation, field)) != expected_ids:
                errors.append(f"{label}: {field} does not match the outfit transition.")

        previous_outfit = outfit

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path, help="JSON sent to the agent")
    parser.add_argument("output_json", type=Path, help="JSON returned by the agent")
    args = parser.parse_args()

    try:
        sample = json.loads(args.input_json.read_text(encoding="utf-8"))
        response = json.loads(args.output_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Could not read JSON: {exc}\n")

    errors = validate_recommendations(sample, response)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: Response shape, supplied IDs, schedule, and transitions are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
