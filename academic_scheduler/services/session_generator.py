from academic_scheduler.models.session_requirement import SessionRequirement
from academic_scheduler.models.session_instance import SessionInstance
from academic_scheduler.models.teaching_assignment import TeachingAssignment


class SessionGenerator:
    """
    Expands SessionRequirements into SessionInstances.
    """

    def generate(
        self,
        teaching_assignments: list[TeachingAssignment],
        requirements: list[SessionRequirement],
    ) -> list[SessionInstance]:

        sessions: list[SessionInstance] = []

        # Build lookup for fast access
        assignment_lookup = {
            assignment.id: assignment
            for assignment in teaching_assignments
        }

        for requirement in requirements:

            assignment = assignment_lookup[
                requirement.teaching_assignment_id
            ]

            for occurrence in range(1, requirement.occurrences + 1):

                for group in range(1, requirement.parallel_groups + 1):

                    session = SessionInstance(
                        id=f"{requirement.id}-O{occurrence}-G{group}",

                        teaching_assignment_id=assignment.id,

                        course_id=assignment.course_id,

                        section_id=assignment.section_id,

                        teacher_ids=assignment.teacher_ids,

                        activity_type=requirement.activity_type,

                        occurrence=occurrence,

                        group_index=group,

                        duration_minutes=requirement.duration_minutes,

                        students_per_session=requirement.students_per_session,

                        required_room_type=requirement.required_room_type,
                    )

                    sessions.append(session)

        return sessions