from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class AcademicClass(SchedulerBaseModel):
    """
    An academic class/cohort that follows a common timetable.

    Example:
        BCT II/II
        Maximum capacity: 48
        Enrolled students: 20
    """

    id: str = Field(..., min_length=1)

    program_id: str = Field(..., min_length=1)

    year_part: str = Field(..., min_length=1)

    maximum_students: int = Field(..., ge=1)

    enrolled_students: int = Field(..., ge=0)