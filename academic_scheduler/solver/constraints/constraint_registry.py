from academic_scheduler.solver.constraints.session_assignment_constraint import (
    SessionAssignmentConstraint,
)


class ConstraintRegistry:

    def __init__(self):

        self.constraints = [
            SessionAssignmentConstraint(),
        ]

    def all(self):

        return self.constraints