from dataclasses import dataclass

from academic_scheduler.models.timetable_entry import (
    TimetableEntry,
)


@dataclass(slots=True)
class Timetable:
    """
    Complete generated timetable.
    """

    entries: list[TimetableEntry]