from ortools.sat.python import cp_model

from academic_scheduler.models.candidate_slot import CandidateSlot


class VariableBuilder:
    """
    Creates all CP-SAT decision variables.
    """

    def build(
        self,
        model: cp_model.CpModel,
        candidate_slots: list[CandidateSlot],
    ) -> dict[
        tuple[str, str, str],
        cp_model.IntVar,
    ]:

        variables = {}

        for candidate in candidate_slots:

            name = (
                f"{candidate.session_id}"
                f"__{candidate.time_slot_id}"
                f"__{candidate.room_id}"
            )

            variables[
                (
                    candidate.session_id,
                    candidate.time_slot_id,
                    candidate.room_id,
                )
            ] = model.NewBoolVar(name)

        return variables