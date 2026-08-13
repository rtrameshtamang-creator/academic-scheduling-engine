from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class Section(SchedulerBaseModel):
    """
    Administrative section within a term.
    """

    id: str = Field(..., min_length=1)

    cohort_id: str

    code: str = Field(..., min_length=1)

    name: str

    program_id: str

    term_id: str

    batch: int = Field(..., ge=2000)

    student_count: int = Field(..., ge=1)

    active: bool = True

    description: str | None = None