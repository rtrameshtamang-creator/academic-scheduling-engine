from dataclasses import dataclass

from academic_scheduler.common.enums import WeekDay
from academic_scheduler.models.daily_schedule_template import DailyScheduleTemplate


from datetime import time

from academic_scheduler.common.enums import (
    ActivityType,
    WeekDay,
)


@dataclass(slots=True)
class TimeGridSlot:
    """
    Represents one schedulable time slot.

    Example:
        Sunday - Theory Block 1
        Monday - Lab Block 1
    """

    id: str

    day: WeekDay

    block_id: str

    block_code: str

    block_name: str

    start_time: time

    end_time: time

    duration_minutes: int

    allowed_activity_types: list[ActivityType]


class TimeGrid:
    """
    Generates the complete timetable grid.
    """

    def build(
        self,
        weekdays: list[WeekDay],
        daily_schedule: DailyScheduleTemplate,
    ) -> list[TimeGridSlot]:

        slots: list[TimeGridSlot] = []

        for day in weekdays:

            for block in daily_schedule.time_blocks:

                slot = TimeGridSlot(
                    id=f"{day.value}_{block.code}",
                    day=day,
                    block_id=block.id,
                    block_code=block.code,
                    block_name=block.name,
                    start_time=block.start_time,
                    end_time=block.end_time,
                    duration_minutes=block.duration_minutes,
                    allowed_activity_types=block.allowed_activity_types,
                )

                slots.append(slot)

        return slots

    @staticmethod
    def filter_by_day(
        slots: list[TimeGridSlot],
        day: WeekDay,
    ) -> list[TimeGridSlot]:

        return [slot for slot in slots if slot.day == day]

    @staticmethod
    def filter_by_block(
        slots: list[TimeGridSlot],
        block_id: str,
    ) -> list[TimeGridSlot]:

        return [slot for slot in slots if slot.block_id == block_id]