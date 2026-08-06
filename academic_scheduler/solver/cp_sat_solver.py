from ortools.sat.python import cp_model

from academic_scheduler.models.candidate_slot import CandidateSlot
from academic_scheduler.models.session_instance import SessionInstance
from academic_scheduler.solver.variables import VariableBuilder
from academic_scheduler.solver.constraints.constraint_registry import (
    ConstraintRegistry,
)
from academic_scheduler.solver.constraint_context import (
    ConstraintContext,
)

class CPSATSolver:
    """
    Builds and solves the CP-SAT timetable model.
    """

    def __init__(self):

        self.model = cp_model.CpModel()

        self.variable_builder = VariableBuilder()

        self.constraint_registry = ConstraintRegistry()

    def build(
        self,
        sessions: list[SessionInstance],
        candidate_slots: list[CandidateSlot],
    ):

        # -----------------------------------------
        # Create decision variables
        # -----------------------------------------

        variables = self.variable_builder.build(
            self.model,
            candidate_slots,
        )

        context = ConstraintContext(
        model=self.model,
        variables=variables,
        candidate_slots=candidate_slots,
        sessions=sessions,
        teachers=[],
)

        # -----------------------------------------
        # Constraint 1
        # Every session must be assigned exactly once
        # -----------------------------------------

        for constraint in self.constraint_registry.all():

            constraint.apply(context)

        # -----------------------------------------
        # Constraint 2
        # A teacher cannot teach two sessions
        # in the same time slot.
        # -----------------------------------------

        # -----------------------------------------
        # Constraint 4
        # A room cannot host two sessions
        # in the same time slot.
        # -----------------------------------------

        return variables

    def solve(self):

        solver = cp_model.CpSolver()

        status = solver.Solve(self.model)

        return solver, status

    