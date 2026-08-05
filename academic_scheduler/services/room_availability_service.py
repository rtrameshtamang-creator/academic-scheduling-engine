from academic_scheduler.models.room import Room
from academic_scheduler.services.time_grid import TimeGridSlot


class RoomAvailabilityService:
    """
    Checks whether a room is available for a
    particular time slot.
    """

    def is_available(
        self,
        room: Room,
        slot: TimeGridSlot,
    ) -> bool:

        # No availability defined -> available everywhere
        if not room.availability:
            return True

        for availability in room.availability:

            if (
                availability.weekday == slot.day
                and availability.block_id == slot.block_id
            ):
                return availability.available

        return False