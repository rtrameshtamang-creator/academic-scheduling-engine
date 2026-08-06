from collections import defaultdict

from academic_scheduler.solver.constraints.base_constraint import (
    BaseConstraint,
)
from academic_scheduler.solver.constraint_context import (
    ConstraintContext,
)


class TeacherOverlapConstraint(BaseConstraint):
    """
    A teacher cannot teach more than one session
    in the same time slot.
    """

    def apply(
        self,
        ctx: ConstraintContext,
    ) -> None:

        model = ctx.model
        variables = ctx.variables
        candidate_slots = ctx.candidate_slots
        sessions = ctx.sessions

        session_lookup = {
            session.id: session
            for session in sessions
        }

        teacher_slot_variables = defaultdict(list)

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

                teacher_slot_variables[
                    (
                        teacher_id,
                        candidate.time_slot_id,
                    )
                ].append(var)

        for vars_for_teacher in teacher_slot_variables.values():

            model.Add(sum(vars_for_teacher) <= 1)