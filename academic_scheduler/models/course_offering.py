from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class CourseOffering(SchedulerBaseModel):
    """
    Represents a course offered to an academic cohort
    during a particular academic term.
    """

    id: str = Field(..., min_length=1)

    course_id: str = Field(..., min_length=1)

    cohort_id: str = Field(..., min_length=1)