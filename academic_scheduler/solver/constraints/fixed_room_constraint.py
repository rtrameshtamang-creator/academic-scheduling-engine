from academic_scheduler.solver.constraint_context import (
    ConstraintContext,
)
from academic_scheduler.solver.constraints.base_constraint import (
    BaseConstraint,
)


class FixedRoomConstraint(BaseConstraint):
    """
    Enforces fixed room assignments.
    """

    def apply(
        self,
        ctx: ConstraintContext,
    ) -> None:

        model = ctx.model
        variables = ctx.variables
        candidate_slots = ctx.candidate_slots

        fixed_room_lookup = {
            assignment.session_id: assignment.room_id
            for assignment in ctx.assignments.fixed_rooms
        }

        if not fixed_room_lookup:
            return

        for candidate in candidate_slots:

            required_room = fixed_room_lookup.get(candidate.session_id)

            if required_room is None:
                continue

            if candidate.room_id != required_room:

                model.Add(
                    variables[
                        (
                            candidate.session_id,
                            candidate.time_slot_id,
                            candidate.room_id,
                        )
                    ]
                    == 0
                )