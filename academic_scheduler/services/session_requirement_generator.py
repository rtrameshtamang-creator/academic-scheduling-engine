from academic_scheduler.models.session_requirement import (
    SessionRequirement,
)
from academic_scheduler.models.session_requirement_template import (
    SessionRequirementTemplate,
)
from academic_scheduler.models.teaching_assignment import (
    TeachingAssignment,
)


class SessionRequirementGenerator:
    """
    Generates SessionRequirement objects from
    TeachingAssignments and SessionRequirementTemplates.
    """

    def generate(
        self,
        teaching_assignments: list[TeachingAssignment],
        templates: list[SessionRequirementTemplate],
    ) -> list[SessionRequirement]:

        requirements = []

        for assignment in teaching_assignments:

            for template in templates:

                if assignment.activity_type != template.activity_type:
                    continue

                requirement = SessionRequirement(

                    id=(
                        f"{assignment.id}-requirement"
                    ),

                    teaching_assignment_id=assignment.id,

                    activity_type=assignment.activity_type,

                    occurrences=template.occurrences,

                    repeat_interval_weeks=template.repeat_interval_weeks,

                    duration_minutes=assignment.duration_minutes,

                    students_per_session=assignment.students_per_session,

                    parallel_groups=1,

                    required_room_type=assignment.required_room_type,

                    teacher_ids=assignment.teacher_ids,
                )

                requirements.append(requirement)

        return requirements