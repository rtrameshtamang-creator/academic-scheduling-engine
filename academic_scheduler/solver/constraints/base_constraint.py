from abc import ABC, abstractmethod

from ortools.sat.python import cp_model

from academic_scheduler.models.candidate_slot import CandidateSlot
from academic_scheduler.models.session_instance import SessionInstance
from academic_scheduler.models.teacher import Teacher


class BaseConstraint(ABC):
    """
    Base class for every scheduling constraint.
    """

    @abstractmethod
    def apply(
        self,
        model: cp_model.CpModel,
        variables,
        candidate_slots: list[CandidateSlot],
        sessions: list[SessionInstance],
        teachers: list[Teacher],
    ):
        pass