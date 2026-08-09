from academic_scheduler.models.candidate_slot import CandidateSlot
from academic_scheduler.models.teacher_preference import (
    TeacherPreference,
)
from academic_scheduler.models.session_instance import (
    SessionInstance,
)

class TeacherPreferencePenalty:
    """
    Applies penalties when a candidate slot
    does not match a teacher's preferences.
    """

    def apply(
        self,
        candidates: list[CandidateSlot],
        sessions: list[SessionInstance],
        teacher_preferences: list[TeacherPreference],
    ) -> None:

        session_lookup = {
            session.id: session
            for session in sessions
        }

        preference_lookup = {
            preference.teacher_id: preference
            for preference in teacher_preferences
        }

        for candidate in candidates:

            session = session_lookup.get(candidate.session_id)

            if session is None:
                continue

            if not session.teacher_ids:
                continue

            teacher_id = session.teacher_ids[0]

            preference = preference_lookup.get(teacher_id)

            if preference is None:
                continue

            # Apply weekday preference
            if (
                preference.preferred_weekdays
                and candidate.weekday
                not in preference.preferred_weekdays
            ):
                candidate.penalty += 5

            # Apply block preference
            if (
                preference.preferred_blocks
                and candidate.block_id
                not in preference.preferred_blocks
            ):
                candidate.penalty += 5