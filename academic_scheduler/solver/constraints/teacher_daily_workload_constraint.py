from academic_scheduler.solver.constraint_context import (
    ConstraintContext,
)
from academic_scheduler.solver.constraints.base_constraint import (
    BaseConstraint,
)


class TeacherDailyWorkloadConstraint(BaseConstraint):
    """
    Limits the number of sessions
    a teacher can teach in one day.
    """

    def apply(
        self,
        ctx: ConstraintContext,
    ) -> None:

        from collections import defaultdict

        model = ctx.model
        variables = ctx.variables
        candidate_slots = ctx.candidate_slots
        sessions = ctx.sessions

        session_lookup = {
            session.id: session
            for session in sessions
        }

        teacher_day_variables = defaultdict(list)

        for candidate in candidate_slots:

            session = session_lookup[candidate.session_id]

            var = variables[
                (
                    candidate.session_id,
                    candidate.time_slot_id,
                    candidate.room_id,
                )
            ]

            for teacher_id in session.teacher_ids:

                teacher_day_variables[
                    (
                        teacher_id,
                        candidate.weekday,
                    )
                ].append(var)

        teacher_lookup = {
            teacher.id: teacher
            for teacher in ctx.teachers
        }

        for (teacher_id, weekday), vars_for_day in teacher_day_variables.items():

            teacher = teacher_lookup.get(teacher_id)

            if teacher is None:
                continue

            model.Add(
                sum(vars_for_day)
                <= teacher.max_periods_per_day
            )