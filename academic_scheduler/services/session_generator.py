from academic_scheduler.models.session_requirement import SessionRequirement
from academic_scheduler.models.session_instance import SessionInstance


class SessionGenerator:
    """
    Expands SessionRequirements into SessionInstances.
    """

    def generate(
        self,
        requirements: list[SessionRequirement],
    ) -> list[SessionInstance]:

        sessions: list[SessionInstance] = []

        for requirement in requirements:

            for occurrence in range(1, requirement.occurrences + 1):

                for group in range(1, requirement.parallel_groups + 1):

                    session = SessionInstance(
                        id=f"{requirement.id}-O{occurrence}-G{group}",
                        teaching_assignment_id=requirement.teaching_assignment_id,
                        activity_type=requirement.activity_type,
                        occurrence=occurrence,
                        group_index=group,
                        duration_minutes=requirement.duration_minutes,
                        students_per_session=requirement.students_per_session,
                        required_room_type=requirement.required_room_type,
                    )

                    sessions.append(session)

        return sessions