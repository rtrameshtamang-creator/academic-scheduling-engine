from pydantic import Field

from academic_scheduler.common.enums import WeekDay
from academic_scheduler.models.base import SchedulerBaseModel


class RoomAvailability(SchedulerBaseModel):
    """
    Availability of a room for a particular
    weekday and time block.
    """

    room_id: str = Field(..., min_length=1)

    weekday: WeekDay

    block_id: str

    available: bool = True