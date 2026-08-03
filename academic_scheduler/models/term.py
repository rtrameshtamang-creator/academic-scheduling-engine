from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class Term(SchedulerBaseModel):
    """
    Academic term.

    Example:
        Semester I
        Semester II
        Trimester I
    """

    id: str = Field(..., min_length=1)

    program_id: str

    number: int = Field(..., ge=1)

    name: str

    active: bool = True

    description: str | None = None