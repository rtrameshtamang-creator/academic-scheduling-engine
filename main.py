from datetime import time

from academic_scheduler.common.enums import (
    ActivityType,
    DayPart,
)
from academic_scheduler.models.time_block_template import (
    TimeBlockTemplate,
)

t1 = TimeBlockTemplate(
    id="T1",
    code="T1",
    name="Theory 1",
    display_order=1,
    start_time=time(7,10),
    end_time=time(8,40),
    day_part=DayPart.MORNING,
    allowed_activity_types=[
        ActivityType.THEORY
    ]
)

print(t1)
print(t1.duration_minutes)




from academic_scheduler.models.base import SchedulerBaseModel


class Test(SchedulerBaseModel):
    name: str


t = Test(name="  Ramesh  ")

print(t)