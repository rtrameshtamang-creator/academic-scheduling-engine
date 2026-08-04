from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CandidateSlot:
    """
    One possible placement of a session.
    """

    session_id: str
    time_slot_id: str