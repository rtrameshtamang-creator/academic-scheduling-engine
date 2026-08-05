from ortools.sat.python import cp_model

from academic_scheduler.models.session_instance import SessionInstance
from academic_scheduler.models.candidate_slot import CandidateSlot
from academic_scheduler.models.timetable import Timetable
from academic_scheduler.models.timetable_entry import TimetableEntry


class TimetableBuilder:
    """
    Converts the CP-SAT solution into a Timetable.
    """

    def build(
        self,
        solver: cp_model.CpSolver,
        variables: dict,
        sessions: list[SessionInstance],
        candidate_slots: list[CandidateSlot],
    ) -> Timetable:

        session_lookup = {
            session.id: session
            for session in sessions
        }

        entries: list[TimetableEntry] = []

        for candidate in candidate_slots:

            key = (
                candidate.session_id,
                candidate.time_slot_id,
                candidate.room_id,
            )

            if not solver.Value(variables[key]):
                continue

            session = session_lookup[candidate.session_id]

            block_id = candidate.time_slot_id.split("_")[1]

            entry = TimetableEntry(
                session_id=session.id,
                course_id=session.course_id,
                section_id=session.section_id,
                teacher_ids=session.teacher_ids,
                weekday=candidate.weekday,
                block_id=block_id,
                room_id=candidate.room_id,
            )

            entries.append(entry)

        return Timetable(entries=entries)