from academic_scheduler.solver.constraint_context import (
    ConstraintContext,
)
from academic_scheduler.solver.constraints.base_constraint import (
    BaseConstraint,
)


class SameCourseSameDayConstraint(BaseConstraint):
    """
    Prevents multiple THEORY sessions of the
    same course for the same section
    on the same day.
    """

    def apply(
        self,
        ctx: ConstraintContext,
    ) -> None:

        from collections import defaultdict

        from academic_scheduler.common.enums import ActivityType

        model = ctx.model
        variables = ctx.variables
        candidate_slots = ctx.candidate_slots
        sessions = ctx.sessions

        session_lookup = {
            session.id: session
            for session in sessions
        }

        course_day_variables = defaultdict(list)

        for candidate in candidate_slots:

            session = session_lookup[candidate.session_id]

            # Apply only to THEORY sessions
            if session.activity_type != ActivityType.THEORY:
                continue

            var = variables[
                (
                    candidate.session_id,
                    candidate.time_slot_id,
                    candidate.room_id,
                )
            ]

            course_day_variables[
                (
                    session.section_id,
                    session.course_id,
                    candidate.weekday,
                )
            ].append(var)

        for vars_for_day in course_day_variables.values():

            model.Add(
                sum(vars_for_day) <= 1
            )