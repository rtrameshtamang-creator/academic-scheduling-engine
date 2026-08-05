from collections import defaultdict

from ortools.sat.python import cp_model

from academic_scheduler.models.candidate_slot import CandidateSlot


class VariableIndex:
    """
    Provides efficient lookups over CP-SAT variables.
    """

    def __init__(
        self,
        variables: dict[
            tuple[str, str, str],
            cp_model.IntVar,
        ],
        candidate_slots: list[CandidateSlot],
    ):

        self.by_session = defaultdict(list)
        self.by_slot = defaultdict(list)

        for candidate in candidate_slots:

            key = (
                candidate.session_id,
                candidate.time_slot_id,
                candidate.room_id,
            )

            var = variables[key]

            self.by_session[candidate.session_id].append(var)

            self.by_slot[candidate.time_slot_id].append(var)