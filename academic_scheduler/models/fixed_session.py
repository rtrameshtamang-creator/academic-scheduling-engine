from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class FixedSession(SchedulerBaseModel):
    """
    Represents a session that must occur
    in a fixed time slot and optionally
    in a fixed room.
    """

    session_id: str = Field(..., min_length=1)

    time_slot_id: str

    room_id: str | None = None