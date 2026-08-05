from academic_scheduler.models.base import SchedulerBaseModel
from academic_scheduler.common.enums import WeekDay


class CandidateSlot(SchedulerBaseModel):
    """
    Represents one feasible scheduling option
    for a teaching session.
    """

    session_id: str

    time_slot_id: str

    weekday: WeekDay

    room_id: str