from academic_scheduler.solver.constraints.session_assignment_constraint import (
    SessionAssignmentConstraint,
)
from academic_scheduler.solver.constraints.teacher_overlap_constraint import (
    TeacherOverlapConstraint,
)
from academic_scheduler.solver.constraints.section_overlap_constraint import (
    SectionOverlapConstraint,
)
from academic_scheduler.solver.constraints.room_overlap_constraint import (
    RoomOverlapConstraint,
)


class ConstraintRegistry:

    def __init__(self):

        self.constraints = [
            SessionAssignmentConstraint(),
            TeacherOverlapConstraint(),
            SectionOverlapConstraint(),
            RoomOverlapConstraint(),
        ]

    def all(self):

        return self.constraints