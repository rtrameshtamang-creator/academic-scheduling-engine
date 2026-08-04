from pydantic import Field

from academic_scheduler.common.enums import WeekDay
from academic_scheduler.models.base import SchedulerBaseModel


class TeacherAvailability(SchedulerBaseModel):
    """
    Availability of a teacher for a particular
    weekday and time block.
    """

    teacher_id: str = Field(..., min_length=1)

    weekday: WeekDay

    block_id: str

    available: bool = True