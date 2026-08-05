from academic_scheduler.models.room import Room
from academic_scheduler.models.session_instance import SessionInstance


class RoomCompatibilityService:
    """
    Determines whether a room is compatible
    with a teaching session.
    """

    def is_compatible(
        self,
        session: SessionInstance,
        room: Room,
    ) -> bool:

        # Room type must match
        if room.room_type != session.required_room_type:
            return False

        # Room must have enough capacity
        if room.capacity < session.students_per_session:
            return False

        return True