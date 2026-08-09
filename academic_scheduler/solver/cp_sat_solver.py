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
from academic_scheduler.models.teacher import Teacher

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
        teachers: list[Teacher],
        assignments,
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
            teachers=teachers,
            assignments=assignments,
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

        # -----------------------------------------
        # Objective (temporary)
        # -----------------------------------------

        # No optimization objective yet.
        # We will add one in the next step.

        # -----------------------------------------
        # Optimization Objective
        # -----------------------------------------

        objective_terms = []

        for candidate in candidate_slots:

            var = variables[
                (
                    candidate.session_id,
                    candidate.time_slot_id,
                    candidate.room_id,
                )
            ]

            objective_terms.append(
                candidate.penalty * var
            )

        self.model.Minimize(
            sum(objective_terms)
        )

        return variables

    def solve(self):

        solver = cp_model.CpSolver()

        status = solver.Solve(self.model)

        return solver, status

    