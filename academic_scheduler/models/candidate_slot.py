from academic_scheduler.models.base import SchedulerBaseModel
from academic_scheduler.common.enums import WeekDay


class CandidateSlot(SchedulerBaseModel):

    session_id: str

    time_slot_id: str

    weekday: WeekDay

    block_id: str

    room_id: str

    penalty: int = 0