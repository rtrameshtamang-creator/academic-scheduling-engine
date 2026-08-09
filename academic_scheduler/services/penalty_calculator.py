from academic_scheduler.services.penalties.last_period_penalty import (
    LastPeriodPenalty,
)
from academic_scheduler.services.penalties.teacher_preference_penalty import (
    TeacherPreferencePenalty,
)


class PenaltyCalculator:

    def __init__(self):

        self.rules = [

            LastPeriodPenalty(),

            TeacherPreferencePenalty(),

        ]

    def calculate(
        self,
        candidates,
        sessions,
        teacher_preferences,
    ):

        # Reset penalties
        for candidate in candidates:

            candidate.penalty = 0

        # Apply every penalty rule
        for rule in self.rules:

            if isinstance(rule, TeacherPreferencePenalty):

                rule.apply(
                    candidates,
                    sessions,
                    teacher_preferences,
                )

            else:

                rule.apply(candidates)