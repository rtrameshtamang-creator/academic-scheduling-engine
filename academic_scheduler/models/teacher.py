from pydantic import Field

from academic_scheduler.common.enums import EmploymentType
from academic_scheduler.models.base import SchedulerBaseModel
from academic_scheduler.models.teacher_availability import TeacherAvailability


class Teacher(SchedulerBaseModel):
    """
    Faculty member.
    """

    id: str = Field(..., min_length=1)

    code: str = Field(..., min_length=2)

    name: str

    employment_type: EmploymentType

    max_periods_per_week: int = Field(..., ge=1)

    max_periods_per_day: int = Field(..., ge=1)

    max_teaching_minutes_per_week: int | None = Field(
        default=None,
        ge=1,
    )

    max_teaching_minutes_per_day: int | None = Field(
        default=None,
        ge=1,
    )

    active: bool = True

    description: str | None = None

    availability: list["TeacherAvailability"] = []