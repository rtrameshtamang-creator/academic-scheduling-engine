from academic_scheduler.models.candidate_slot import CandidateSlot


class LastPeriodPenalty:

    def apply(
        self,
        candidates: list[CandidateSlot],
    ) -> None:

        for candidate in candidates:

            if candidate.block_id == "T4":

                candidate.penalty += 10