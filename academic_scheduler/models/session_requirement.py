from pydantic import Field

from academic_scheduler.common.enums import (
    ActivityType,
    RoomType,
)
from academic_scheduler.models.base import SchedulerBaseModel


class SessionRequirement(SchedulerBaseModel):
    """
    Defines one scheduling requirement for a teaching assignment.

    Example:
        - OOP Theory
        - OOP Lab
        - Digital Logic Lab
    """

    id: str = Field(..., min_length=1)

    teaching_assignment_id: str

    activity_type: ActivityType

    occurrences: int = Field(..., ge=1)

    repeat_interval_weeks: int = Field(
        default=1,
        ge=1,
    )

    duration_minutes: int = Field(..., ge=30)

    students_per_session: int = Field(..., ge=1)

    parallel_groups: int = Field(
        default=1,
        ge=1,
    )

    required_room_type: RoomType

    active: bool = True

    description: str | None = None