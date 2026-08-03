from datetime import datetime, time

from pydantic import BaseModel, Field, computed_field, model_validator

from academic_scheduler.common.enums import (
    ActivityType,
    DayPart,
)


from academic_scheduler.models.base import SchedulerBaseModel


class TimeBlockTemplate(SchedulerBaseModel):
    """
    Defines a reusable scheduling block.

    Example
    -------
    T1 : 07:10–08:45
    L1 : 07:10–09:40

    A TimeBlockTemplate is NOT tied to any day.
    """

    id: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    name: str

    display_order: int = Field(..., ge=1)

    start_time: time
    end_time: time

    day_part: DayPart

    allowed_activity_types: list[ActivityType]

    active: bool = True

    description: str | None = None

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError(
                "end_time must be greater than start_time"
            )
        return self

    @computed_field
    @property
    def duration_minutes(self) -> int:
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)

        return int((end - start).total_seconds() // 60)