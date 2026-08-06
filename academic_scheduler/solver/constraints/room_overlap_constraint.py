from collections import defaultdict

from academic_scheduler.solver.constraint_context import (
    ConstraintContext,
)
from academic_scheduler.solver.constraints.base_constraint import (
    BaseConstraint,
)


class RoomOverlapConstraint(BaseConstraint):
    """
    A room cannot host more than one session
    in the same time slot.
    """

    def apply(
        self,
        ctx: ConstraintContext,
    ) -> None:

        model = ctx.model
        variables = ctx.variables
        candidate_slots = ctx.candidate_slots

        room_slot_variables = defaultdict(list)

        for candidate in candidate_slots:

            var = variables[
                (
                    candidate.session_id,
                    candidate.time_slot_id,
                    candidate.room_id,
                )
            ]

            room_slot_variables[
                (
                    candidate.room_id,
                    candidate.time_slot_id,
                )
            ].append(var)

        for vars_for_room in room_slot_variables.values():

            model.Add(sum(vars_for_room) <= 1)