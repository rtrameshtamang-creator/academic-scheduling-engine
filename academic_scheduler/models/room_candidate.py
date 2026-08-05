from academic_scheduler.models.base import SchedulerBaseModel


class RoomCandidate(SchedulerBaseModel):
    """
    Represents one feasible room for a session.
    """

    session_id: str

    room_id: str