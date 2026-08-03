from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class Course(SchedulerBaseModel):
    """
    Academic course definition.

    This model contains only course metadata.
    Scheduling information belongs to ActivityAssignment.
    """

    id: str = Field(..., min_length=1)

    code: str = Field(..., min_length=2)

    title: str

    credit: float = Field(..., gt=0)

    department_id: str

    program_id: str | None = None

    active: bool = True

    description: str | None = None