from academic_scheduler.models.base import SchedulerBaseModel


class SectionPlan(SchedulerBaseModel):
    """
    Academic plan for one section.

    This is defined by the academic office before scheduling.
    """

    code: str

    name: str

    student_count: int