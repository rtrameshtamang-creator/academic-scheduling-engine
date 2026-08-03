from datetime import time

from academic_scheduler.common.enums import ActivityType, DayPart
from academic_scheduler.models.time_block_template import TimeBlockTemplate


def main():
    t1 = TimeBlockTemplate(
        id="T1",
        code="T1",
        name="Theory Block 1",
        display_order=1,
        start_time=time(10, 10),
        end_time=time(8, 45),
        day_part=DayPart.MORNING,
        allowed_activity_types=[ActivityType.THEORY],
    )

    print(f"Block : {t1.code}")
    print(f"Time  : {t1.start_time} - {t1.end_time}")
    print(f"Duration : {t1.duration_minutes} minutes")


if __name__ == "__main__":
    main()