from datetime import time

from academic_scheduler.common.enums import (
    ActivityType,
    DayPart,
)
from academic_scheduler.models.time_block_template import TimeBlockTemplate
from academic_scheduler.models.daily_schedule_template import DailyScheduleTemplate
from academic_scheduler.models.institution import Institution


def main():

    # ----------------------------
    # Create Time Blocks
    # ----------------------------

    t1 = TimeBlockTemplate(
        id="T1",
        code="T1",
        name="Theory Block 1",
        display_order=1,
        start_time=time(7, 10),
        end_time=time(8, 45),
        day_part=DayPart.MORNING,
        allowed_activity_types=[ActivityType.THEORY],
    )

    t2 = TimeBlockTemplate(
        id="T2",
        code="T2",
        name="Theory Block 2",
        display_order=2,
        start_time=time(8, 45),
        end_time=time(10, 15),
        day_part=DayPart.MORNING,
        allowed_activity_types=[ActivityType.THEORY],
    )

    t3 = TimeBlockTemplate(
        id="T3",
        code="T3",
        name="Theory Block 3",
        display_order=3,
        start_time=time(11, 0),
        end_time=time(12, 30),
        day_part=DayPart.AFTERNOON,
        allowed_activity_types=[ActivityType.THEORY],
    )

    t4 = TimeBlockTemplate(
        id="T4",
        code="T4",
        name="Theory Block 4",
        display_order=4,
        start_time=time(12, 30),
        end_time=time(14, 0),
        day_part=DayPart.AFTERNOON,
        allowed_activity_types=[ActivityType.THEORY],
    )

    # ----------------------------
    # Create Daily Schedule
    # ----------------------------

    regular_day = DailyScheduleTemplate(
        id="REGULAR",
        name="Regular Teaching Day",
        time_blocks=[t1, t2, t3, t4]
    )

    # ----------------------------
    # Create Institution
    # ----------------------------

    inst = Institution(
        id="ioe",
        name="Institute of Engineering",
        timezone="Asia/Kathmandu",
        daily_schedule_templates=[regular_day]
    )

    print(inst)

    from academic_scheduler.models.department import Department

    department = Department(
        id="doece",
        code="DOECE",
        name="Department of Electronics and Computer Engineering"
    )

    print(department)


if __name__ == "__main__":
    main()