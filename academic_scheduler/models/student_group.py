from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class StudentGroup(SchedulerBaseModel):
    """
    Represents a schedulable student group.

    Examples:
        Whole Section
        Group A
        Group B
    """

    id: str = Field(..., min_length=1)

    section_id: str

    name: str

    student_count: int = Field(..., ge=1)

    active: bool = True

    description: str | None = None