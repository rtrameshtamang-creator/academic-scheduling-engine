from academic_scheduler.common.enums import (
    ActivityType,
    RoomType,
)
from academic_scheduler.models.base import SchedulerBaseModel


class TeachingPlan(SchedulerBaseModel):
    """
    Academic teaching plan for a course.

    Defined once by the department.
    """

    course_id: str

    activity_type: ActivityType

    teacher_ids: list[str]

    weekly_sessions: int

    duration_minutes: int

    parallel_groups: int = 1

    parallel_group_teacher_ids: list[list[str]] | None = None

    required_room_type: RoomType