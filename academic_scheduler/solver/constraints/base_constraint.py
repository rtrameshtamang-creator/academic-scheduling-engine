from abc import ABC, abstractmethod

from academic_scheduler.solver.constraint_context import (
    ConstraintContext,
)


class BaseConstraint(ABC):
    """
    Base class for every scheduling constraint.
    """

    @abstractmethod
    def apply(
        self,
        context: ConstraintContext,
    ) -> None:
        pass