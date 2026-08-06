from dataclasses import dataclass, field

from academic_scheduler.models.assignments.fixed_room_assignment import (
    FixedRoomAssignment,
)


@dataclass(slots=True)
class AssignmentSet:
    """
    Holds all scheduling assignments.
    """

    fixed_rooms: list[FixedRoomAssignment] = field(
        default_factory=list
    )