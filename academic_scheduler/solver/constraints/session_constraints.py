from collections import defaultdict

from ortools.sat.python import cp_model

from academic_scheduler.models.candidate_slot import CandidateSlot


class SessionConstraints:

    @staticmethod
    def add_session_assignment_constraint(
        model: cp_model.CpModel,
        variables,
        candidate_slots: list[CandidateSlot],
    ) -> None:
        """
        Every session must be assigned exactly once.
        """

        session_variables = defaultdict(list)

        for candidate in candidate_slots:

            var = variables[
                (
                    candidate.session_id,
                    candidate.time_slot_id,
                    candidate.room_id,
                )
            ]

            session_variables[candidate.session_id].append(var)

        for vars_for_session in session_variables.values():

            model.Add(sum(vars_for_session) == 1)