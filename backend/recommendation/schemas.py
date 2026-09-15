"""Structured response from the outfit-planning agent."""

from pydantic import BaseModel, ConfigDict, Field


class TimeRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(description="ID of the matching input schedule event")
    start_time: str = Field(description="Start time copied from that event")
    end_time: str = Field(description="End time copied from that event")
    activity: str = Field(description="Activity copied from that event")
    clothing_item_ids: list[str] = Field(description="Items worn during this event")
    keep_item_ids: list[str] = Field(description="Items kept on from the preceding event")
    remove_item_ids: list[str] = Field(description="Items taken off after the preceding event")
    put_on_item_ids: list[str] = Field(description="Items newly put on for this event")
    pack_item_ids: list[str] = Field(description="Items carried for later use, not worn now")
    reason: str = Field(description="Brief reason for the outfit and transition")
    warnings: list[str] = Field(description="Practical concerns; empty if there are none")


class DailyRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    recommendations: list[TimeRecommendation] = Field(
        description="One recommendation per input event, in chronological order"
    )
