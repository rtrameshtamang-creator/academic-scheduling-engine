from collections import defaultdict

from ortools.sat.python import cp_model

from academic_scheduler.models.candidate_slot import CandidateSlot
from academic_scheduler.models.session_instance import SessionInstance
from academic_scheduler.models.teacher import Teacher
from academic_scheduler.solver.constraints.base_constraint import (
    BaseConstraint,
)


class SessionAssignmentConstraint(BaseConstraint):
    """
    Every session must be assigned exactly once.
    """

    def apply(
        self,
        context,
    ):

        model = context.model
        variables = context.variables
        candidate_slots = context.candidate_slots

        session_variables = defaultdict(list)

        for candidate in candidate_slots:

            var = variables[
                (
                    candidate.session_id,
                    candidate.time_slot_id,
                    candidate.room_id,
                )
            ]

            session_variables[
                candidate.session_id
            ].append(var)

        for vars_for_session in session_variables.values():

            model.Add(sum(vars_for_session) == 1)