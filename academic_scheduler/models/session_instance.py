from dataclasses import dataclass

from academic_scheduler.common.enums import (
    ActivityType,
    RoomType,
)


@dataclass(slots=True)
class SessionInstance:
    """
    One atomic schedulable teaching session.

    This is the object that the CP-SAT solver schedules.
    """

    # Identity
    id: str

    teaching_assignment_id: str

    course_id: str

    section_id: str

    teacher_ids: list[str]

    # Academic
    activity_type: ActivityType

    occurrence: int

    group_index: int

    # Session
    duration_minutes: int

    students_per_session: int

    required_room_type: RoomType