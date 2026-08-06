from collections import defaultdict

from ortools.sat.python import cp_model

from academic_scheduler.models.candidate_slot import CandidateSlot
from academic_scheduler.models.session_instance import SessionInstance
from academic_scheduler.models.teacher import Teacher
from academic_scheduler.solver.constraints.session_constraints import (
    SessionConstraints,
)


class HardConstraintBuilder:
    """
    Builds all hard constraints.
    """

    def add_teacher_overlap_constraint(
        self,
        model: cp_model.CpModel,
        variables: dict[
            tuple[str, str, str],
            cp_model.IntVar,
        ],
        candidate_slots: list[CandidateSlot],
        sessions: list[SessionInstance],
    ) -> None:
        """
        A teacher cannot teach more than one session
        in the same time slot.
        """

        session_lookup = {
            session.id: session
            for session in sessions
        }

        teacher_slot_variables = defaultdict(list)

        for candidate in candidate_slots:

            session = session_lookup[candidate.session_id]

            var = variables[
                (
                    candidate.session_id,
                    candidate.time_slot_id,
                    candidate.room_id,
                )
            ]

            for teacher_id in session.teacher_ids:

                teacher_slot_variables[
                    (
                        teacher_id,
                        candidate.time_slot_id,
                    )
                ].append(var)

        for vars_for_teacher in teacher_slot_variables.values():

            model.Add(sum(vars_for_teacher) <= 1)

    def add_section_overlap_constraint(
        self,
        model: cp_model.CpModel,
        variables: dict[
            tuple[str, str, str],
            cp_model.IntVar,
        ],
        candidate_slots: list[CandidateSlot],
        sessions: list[SessionInstance],
    ) -> None:
        """
        A section cannot attend more than one session
        in the same time slot.
        """

        session_lookup = {
            session.id: session
            for session in sessions
        }

        section_slot_variables = defaultdict(list)

        for candidate in candidate_slots:

            session = session_lookup[candidate.session_id]

            var = variables[
                (
                    candidate.session_id,
                    candidate.time_slot_id,
                    candidate.room_id,
                )
            ]

            section_slot_variables[
                (
                    session.section_id,
                    candidate.time_slot_id,
                )
            ].append(var)

        for vars_for_section in section_slot_variables.values():

            model.Add(sum(vars_for_section) <= 1)

    def add_room_overlap_constraint(
        self,
        model: cp_model.CpModel,
        variables,
        candidate_slots: list[CandidateSlot],
    ) -> None:
        """
        A room cannot host more than one session
        in the same time slot.
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

    def add_teacher_daily_load_constraint(
        self,
        model: cp_model.CpModel,
        variables,
        candidate_slots: list[CandidateSlot],
        sessions: list[SessionInstance],
        teachers: list[Teacher],
    ):
        """
        A teacher cannot exceed the maximum
        teaching load per day.
        """