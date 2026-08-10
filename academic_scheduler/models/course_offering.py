from academic_scheduler.models.base import SchedulerBaseModel
from academic_scheduler.models.section_plan import (
    SectionPlan,
)

class CourseOffering(SchedulerBaseModel):
    """
    Represents one course offered during a semester.
    """

    course_id: str

    program_id: str

    term_id: str

    batch: int

    total_students: int

    section_plans: list[SectionPlan]