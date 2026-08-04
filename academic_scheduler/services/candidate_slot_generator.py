from academic_scheduler.models.candidate_slot import CandidateSlot
from academic_scheduler.models.session_instance import SessionInstance
from academic_scheduler.services.time_grid import TimeGridSlot
from academic_scheduler.models.teacher import Teacher


class CandidateSlotGenerator:
    """
    Generates all valid candidate slots for every session.
    """

    def _teacher_available(
        self,
        teacher: Teacher,
        slot: TimeGridSlot,
    ) -> bool:
        """
        Returns True if the teacher is available
        for the given day and time block.
        """

        # No availability defined -> available everywhere
        if not teacher.availability:
            return True

        for availability in teacher.availability:

            if (
                availability.weekday == slot.day
                and availability.block_id == slot.block_id
                and availability.available
            ):
                return True

        return False

    def generate(
        self,
        sessions: list[SessionInstance],
        slots: list[TimeGridSlot],
        teachers: list[Teacher],
    ) -> list[CandidateSlot]:

        teacher_lookup = {
            teacher.id: teacher
            for teacher in teachers
        }

        candidates: list[CandidateSlot] = []

        for session in sessions:

            for slot in slots:

                # ---------------------------------
                # Activity Compatibility
                # ---------------------------------

                if (
                    session.activity_type
                    not in slot.allowed_activity_types
                ):
                    continue

                # ---------------------------------
                # Teacher Availability
                # ---------------------------------

                teacher = teacher_lookup[
                    session.teacher_ids[0]
                ]

                if not self._teacher_available(
                    teacher,
                    slot,
                ):
                    continue

                candidates.append(
                    CandidateSlot(
                        session_id=session.id,
                        time_slot_id=slot.id,
                    )
                )

        return candidates