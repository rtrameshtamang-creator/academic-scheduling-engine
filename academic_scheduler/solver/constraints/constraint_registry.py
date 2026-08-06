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
from academic_scheduler.solver.constraints.teacher_daily_workload_constraint import (
    TeacherDailyWorkloadConstraint,
)
from academic_scheduler.solver.constraints.teacher_weekly_workload_constraint import (
    TeacherWeeklyWorkloadConstraint,
)
from academic_scheduler.solver.constraints.session_spacing_constraint import (
    SessionSpacingConstraint,
)
from academic_scheduler.solver.constraints.fixed_room_constraint import (
    FixedRoomConstraint,
)
from academic_scheduler.solver.constraints.same_course_same_day_constraint import (
    SameCourseSameDayConstraint,
)

class ConstraintRegistry:

    def __init__(self):

        self.constraints = [
            SessionAssignmentConstraint(),
            TeacherOverlapConstraint(),
            SectionOverlapConstraint(),
            RoomOverlapConstraint(),
            TeacherDailyWorkloadConstraint(),
            TeacherWeeklyWorkloadConstraint(),
            SessionSpacingConstraint(),
            FixedRoomConstraint(),
            SameCourseSameDayConstraint(),
        ]

    def all(self):

        return self.constraints