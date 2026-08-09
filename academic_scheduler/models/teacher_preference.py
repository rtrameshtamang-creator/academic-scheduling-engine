from academic_scheduler.models.base import SchedulerBaseModel


class TeacherPreference(SchedulerBaseModel):
    """
    Teacher scheduling preferences.

    These are soft preferences used during optimization.
    """

    teacher_id: str

    preferred_weekdays: list[str] = []

    preferred_blocks: list[str] = []