from academic_scheduler.common.enums import ActivityType
from academic_scheduler.models.class_session import ClassSession


theory = ClassSession(
    id="bct-2-2-oop-theory",
    academic_class_id="bct-2-2",
    course_id="oop",
    activity_type=ActivityType.THEORY,
    weekly_sessions=3,
    duration_minutes=90,
    teacher_ids=["ramesh"],
)

print(theory)