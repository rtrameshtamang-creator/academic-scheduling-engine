from pydantic import Field, model_validator

from academic_scheduler.models.base import SchedulerBaseModel
from academic_scheduler.models.time_block_template import TimeBlockTemplate


class DailyScheduleTemplate(SchedulerBaseModel):
    """
    Defines the structure of a normal teaching day.

    Example:
        T1
        T2
        T3
        T4

    or

        L1
        T3
        T4
    """

    id: str = Field(..., min_length=1)

    name: str

    time_blocks: list[TimeBlockTemplate]

    active: bool = True

    description: str | None = None

    @model_validator(mode="after")
    def validate_schedule(self):
        if not self.time_blocks:
            raise ValueError(
                "DailyScheduleTemplate must contain at least one time block."
            )

        codes = [b.code for b in self.time_blocks]

        if len(codes) != len(set(codes)):
            raise ValueError(
                "Duplicate time block codes found."
            )

        display_orders = [b.display_order for b in self.time_blocks]

        if display_orders != sorted(display_orders):
            raise ValueError(
                "Time blocks must be sorted by display_order."
            )

        return self