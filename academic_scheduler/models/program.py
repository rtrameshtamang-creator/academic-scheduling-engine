from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class Program(SchedulerBaseModel):
    """
    Academic program.

    Example:
        Bachelor in Computer Engineering (BCT)
    """

    id: str = Field(..., min_length=1)

    code: str = Field(..., min_length=2)

    name: str

    department_id: str

    total_terms: int = Field(..., ge=1)

    active: bool = True

    description: str | None = None