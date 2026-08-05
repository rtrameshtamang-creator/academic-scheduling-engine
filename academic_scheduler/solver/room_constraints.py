from collections import defaultdict

from ortools.sat.python import cp_model

from academic_scheduler.models.candidate_slot import CandidateSlot


class RoomConstraintBuilder:
    """
    Builds all room-related hard constraints.
    """

    def add_room_overlap_constraint(
        self,
        model: cp_model.CpModel,
        variables,
        candidate_slots: list[CandidateSlot],
    ) -> None:
        """
        A room cannot host more than one session
        during the same time slot.
        """

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