from academic_scheduler.models.base import SchedulerBaseModel


class InstitutionPolicy(SchedulerBaseModel):
    """
    Institution-wide academic rules.

    These rules determine how sections and lab groups
    are generated before scheduling begins.
    """

    # Maximum students allowed in one section
    max_students_per_section: int

    # Maximum students allowed in one laboratory group
    max_students_per_lab_group: int

    # Automatically split laboratory groups
    auto_split_lab_groups: bool = True

    # Automatically create multiple sections
    auto_create_sections: bool = True