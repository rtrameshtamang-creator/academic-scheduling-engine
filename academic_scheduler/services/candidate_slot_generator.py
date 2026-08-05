from academic_scheduler.models.candidate_slot import CandidateSlot
from academic_scheduler.models.session_instance import SessionInstance
from academic_scheduler.services.time_grid import TimeGridSlot
from academic_scheduler.models.teacher import Teacher
from academic_scheduler.models.room import Room
from academic_scheduler.services.room_compatibility import (
    RoomCompatibilityService,
)
from academic_scheduler.services.room_availability_service import (
    RoomAvailabilityService,
)

class CandidateSlotGenerator:
    """
    Generates all valid candidate slots for every session.
    """

    def __init__(self):

        self.room_compatibility = RoomCompatibilityService()

        self.room_availability = RoomAvailabilityService()

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
        rooms: list[Room],
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

                # ---------------------------------
                # Room Compatibility
                # ---------------------------------

                compatible_rooms = []

                for room in rooms:

                    # -----------------------------
                    # Room Compatibility
                    # -----------------------------
                    if not self.room_compatibility.is_compatible(
                        session,
                        room,
                    ):
                        continue

                    # -----------------------------
                    # Room Availability
                    # -----------------------------
                    if not self.room_availability.is_available(
                        room,
                        slot,
                    ):
                        continue

                    compatible_rooms.append(room)

                # No compatible room -> skip
                if not compatible_rooms:
                    continue

                # Create one candidate for each compatible room
                for room in compatible_rooms:

                    candidates.append(
                        CandidateSlot(
                            session_id=session.id,
                            time_slot_id=slot.id,
                            room_id=room.id,
                        )
                    )

        return candidates