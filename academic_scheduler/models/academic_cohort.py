from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel
from academic_scheduler.models.section_plan import SectionPlan


class AcademicCohort(SchedulerBaseModel):
    """
    A cohort of students sharing the same
    program, term, batch, and sections.
    """

    id: str = Field(..., min_length=1)

    program_id: str

    term_id: str

    batch: int = Field(..., ge=2000)

    total_students: int = Field(..., ge=1)

    section_plans: list[SectionPlan]