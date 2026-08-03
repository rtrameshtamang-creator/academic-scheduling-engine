from dataclasses import dataclass

from academic_scheduler.common.enums import (
    ActivityType,
    RoomType,
)


@dataclass(slots=True)
class SessionInstance:
    """
    One schedulable teaching session.

    Generated automatically from SessionRequirement.
    """

    id: str

    teaching_assignment_id: str

    activity_type: ActivityType

    occurrence: int

    group_index: int

    duration_minutes: int

    students_per_session: int

    required_room_type: RoomType