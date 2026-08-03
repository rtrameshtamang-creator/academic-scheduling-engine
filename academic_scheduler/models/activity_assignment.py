from pydantic import Field

from academic_scheduler.common.enums import ActivityType, RoomType
from academic_scheduler.models.base import SchedulerBaseModel


class ActivityAssignment(SchedulerBaseModel):
    """
    Represents one schedulable teaching activity.

    Example:
        OOP Theory
        OOP Lab
        Digital Logic Lab
    """

    id: str = Field(..., min_length=1)

    course_id: str

    section_id: str

    activity_type: ActivityType

    teacher_ids: list[str]

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