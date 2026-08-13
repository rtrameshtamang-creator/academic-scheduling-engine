from pydantic import Field, model_validator

from academic_scheduler.common.enums import ActivityType
from academic_scheduler.models.base import SchedulerBaseModel
from academic_scheduler.models.lab_group import LabGroup


class ClassSession(SchedulerBaseModel):
    """
    Defines the weekly teaching requirement for one course activity.

    Examples:

        OOP Theory:
            3 sessions/week
            90 minutes/session
            1 teacher

        OOP Lab:
            1 session/week
            150 minutes/session
            multiple lab groups
    """

    id: str = Field(..., min_length=1)

    academic_class_id: str = Field(..., min_length=1)

    course_id: str = Field(..., min_length=1)

    activity_type: ActivityType

    weekly_sessions: int = Field(..., ge=1)

    duration_minutes: int = Field(..., ge=1)

    teacher_ids: list[str] = Field(default_factory=list)

    lab_groups: list[LabGroup] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_teaching_configuration(self):
        if self.activity_type == ActivityType.LAB:

            if not self.lab_groups:
                raise ValueError(
                    "Lab sessions must have at least one lab group."
                )

        else:

            if not self.teacher_ids:
                raise ValueError(
                    "Non-lab sessions must have at least one teacher."
                )

            if self.lab_groups:
                raise ValueError(
                    "Lab groups can only be defined for lab sessions."
                )

        return self