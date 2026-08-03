from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel
from academic_scheduler.models.daily_schedule_template import DailyScheduleTemplate


class Institution(SchedulerBaseModel):
    """
    Root configuration for an institution.
    """

    id: str = Field(..., min_length=1)
    name: str
    timezone: str

    daily_schedule_templates: list[DailyScheduleTemplate]

    active: bool = True

    description: str | None = None
