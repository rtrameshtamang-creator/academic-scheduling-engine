from dataclasses import dataclass

from academic_scheduler.common.enums import WeekDay
from academic_scheduler.models.daily_schedule_template import DailyScheduleTemplate


@dataclass(frozen=True, slots=True)
class TimeGridSlot:
    """
    Represents one schedulable time slot.

    Example:
        Sunday - Theory Block 1
        Monday - Theory Block 3
    """

    id: str
    day: WeekDay
    block_id: str
    block_code: str
    block_name: str


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
                    id=f"{day.name}_{block.code}",
                    day=day,
                    block_id=block.id,
                    block_code=block.code,
                    block_name=block.name,
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