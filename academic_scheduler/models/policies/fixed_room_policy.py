from dataclasses import dataclass

from academic_scheduler.models.policies.scheduling_policy import (
    SchedulingPolicy,
)


@dataclass(slots=True)
class FixedRoomPolicy(SchedulingPolicy):
    """
    Forces a session to be scheduled
    in a specific room.
    """

    session_id: str

    room_id: str