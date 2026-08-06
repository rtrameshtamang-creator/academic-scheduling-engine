from dataclasses import dataclass

from ortools.sat.python import cp_model

from academic_scheduler.models.candidate_slot import CandidateSlot
from academic_scheduler.models.session_instance import SessionInstance
from academic_scheduler.models.teacher import Teacher
from academic_scheduler.models.assignments.fixed_room_assignment import (
    FixedRoomAssignment,
)
from academic_scheduler.models.assignments.assignment_set import (
    AssignmentSet,
)

@dataclass
class ConstraintContext:
    """
    Contains everything a constraint needs.
    """

    model: cp_model.CpModel

    variables: dict

    candidate_slots: list[CandidateSlot]

    sessions: list[SessionInstance]

    teachers: list[Teacher]

    assignments: AssignmentSet