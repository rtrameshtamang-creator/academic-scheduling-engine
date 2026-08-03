from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class Department(SchedulerBaseModel):
    """
    Academic department.

    Example:
        Department of Electronics and Computer Engineering
    """

    id: str = Field(..., min_length=1)

    code: str = Field(..., min_length=2)

    name: str

    active: bool = True

    description: str | None = None