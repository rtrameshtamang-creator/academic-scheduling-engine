from dataclasses import dataclass

from academic_scheduler.common.enums import WeekDay


@dataclass(slots=True)
class TimetableEntry:
    """
    One scheduled timetable entry.
    """

    session_id: str

    course_id: str

    section_id: str

    teacher_ids: list[str]

    weekday: WeekDay

    block_id: str

    room_id: str