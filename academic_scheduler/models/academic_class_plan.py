from pydantic import Field

from academic_scheduler.models.base import SchedulerBaseModel
from academic_scheduler.models.class_session import ClassSession


class AcademicClassPlan(SchedulerBaseModel):
    """
    Scheduling input for one academic class.

    Contains the class identity and the class sessions
    that must be scheduled for the week.
    """

    academic_class_id: str = Field(..., min_length=1)

    class_sessions: list[ClassSession] = Field(
        default_factory=list
    )