from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class LabGroup(SchedulerBaseModel):
    """
    One student group within a laboratory session.

    The department explicitly defines:
    - number of students in the group
    - teachers assigned to the group
    """

    id: str = Field(..., min_length=1)

    name: str = Field(..., min_length=1)

    student_count: int = Field(..., ge=1)

    teacher_ids: list[str] = Field(..., min_length=1)