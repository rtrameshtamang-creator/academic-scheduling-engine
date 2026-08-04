from dataclasses import dataclass

from academic_scheduler.models.session_requirement import SessionRequirement
from academic_scheduler.models.teaching_assignment import TeachingAssignment
from academic_scheduler.models.time_slot import TimeSlot


@dataclass(slots=True)
class SampleDataset:
    """
    Holds all sample data required
    to run the scheduling engine.
    """

    teaching_assignments: list[TeachingAssignment]

    session_requirements: list[SessionRequirement]

    time_slots: list[TimeSlot]