from dataclasses import dataclass


@dataclass(slots=True)
class FixedRoomAssignment:
    """
    Assigns a specific session to a specific room.
    """

    session_id: str

    room_id: str