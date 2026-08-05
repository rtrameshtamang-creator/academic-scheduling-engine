from ortools.sat.python import cp_model

from academic_scheduler.models.candidate_slot import CandidateSlot
from academic_scheduler.models.session_instance import SessionInstance
from academic_scheduler.solver.variables import VariableBuilder
from academic_scheduler.solver.hard_constraints import HardConstraintBuilder
from academic_scheduler.solver.room_constraints import RoomConstraintBuilder


class CPSATSolver:
    """
    Builds and solves the CP-SAT timetable model.
    """

    def __init__(self):

        self.model = cp_model.CpModel()

        self.variable_builder = VariableBuilder()

        self.constraint_builder = HardConstraintBuilder()

        self.room_constraint_builder = RoomConstraintBuilder()

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

        # -----------------------------------------
        # Constraint 1
        # Every session must be assigned exactly once
        # -----------------------------------------

        self.constraint_builder.add_session_assignment_constraint(
            self.model,
            variables,
            candidate_slots,
        )

        # -----------------------------------------
        # Constraint 2
        # A teacher cannot teach two sessions
        # in the same time slot.
        # -----------------------------------------

        self.constraint_builder.add_teacher_overlap_constraint(
            self.model,
            variables,
            candidate_slots,
            sessions,
        )

        self.constraint_builder.add_section_overlap_constraint(
            self.model,
            variables,
            candidate_slots,
            sessions,
        )

        self.constraint_builder.add_room_overlap_constraint(
            self.model,
            variables,
            candidate_slots,
        )

        # -----------------------------------------
        # Constraint 4
        # A room cannot host two sessions
        # in the same time slot.
        # -----------------------------------------

        self.room_constraint_builder.add_room_overlap_constraint(
            self.model,
            variables,
            candidate_slots,
        )

        return variables

    def solve(self):

        solver = cp_model.CpSolver()

        status = solver.Solve(self.model)

        return solver, status

    