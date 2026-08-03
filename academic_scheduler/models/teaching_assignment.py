from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel


class TeachingAssignment(SchedulerBaseModel):
    """
    Defines which teacher(s) teach a course
    to a particular section.
    """

    id: str = Field(..., min_length=1)

    course_id: str

    section_id: str

    teacher_ids: list[str] = Field(..., min_length=1)

    active: bool = True

    description: str | None = None