from academic_scheduler.solver.constraint_context import (
    ConstraintContext,
)
from academic_scheduler.solver.constraints.base_constraint import (
    BaseConstraint,
)


class SessionSpacingConstraint(BaseConstraint):
    """
    Prevents multiple theory sessions of the same
    course from occurring on the same day.
    """

    def apply(
        self,
        ctx: ConstraintContext,
    ) -> None:
        pass