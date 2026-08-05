from academic_scheduler.models.base import SchedulerBaseModel


class CandidateSlot(SchedulerBaseModel):
    """
    Represents one feasible scheduling option
    for a teaching session.
    """

    session_id: str

    time_slot_id: str

    room_id: str