from collections import defaultdict

from academic_scheduler.solver.constraint_context import (
    ConstraintContext,
)
from academic_scheduler.solver.constraints.base_constraint import (
    BaseConstraint,
)


class SectionOverlapConstraint(BaseConstraint):
    """
    A section cannot attend more than one session
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

        section_slot_variables = defaultdict(list)

        for candidate in candidate_slots:

            session = session_lookup[candidate.session_id]

            var = variables[
                (
                    candidate.session_id,
                    candidate.time_slot_id,
                    candidate.room_id,
                )
            ]

            section_slot_variables[
                (
                    session.section_id,
                    candidate.time_slot_id,
                )
            ].append(var)

        for vars_for_section in section_slot_variables.values():

            model.Add(sum(vars_for_section) <= 1)