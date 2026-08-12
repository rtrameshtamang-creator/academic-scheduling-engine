from academic_scheduler.common.enums import ActivityType
from academic_scheduler.models.base import SchedulerBaseModel


class SessionRequirementTemplate(SchedulerBaseModel):
    """
    Defines the scheduling pattern for one activity type.
    """

    activity_type: ActivityType

    occurrences: int

    repeat_interval_weeks: int = 1