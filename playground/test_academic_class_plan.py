from academic_scheduler.common.enums import ActivityType
from academic_scheduler.models.academic_class_plan import (
    AcademicClassPlan,
)
from academic_scheduler.models.class_session import ClassSession


plan = AcademicClassPlan(
    academic_class_id="bct-2-2",
    class_sessions=[
        ClassSession(
            id="bct-2-2-oop-theory",
            academic_class_id="bct-2-2",
            course_id="oop",
            activity_type=ActivityType.THEORY,
            weekly_sessions=3,
            duration_minutes=90,
            teacher_ids=["ramesh"],
        )
    ],
)

print(plan)