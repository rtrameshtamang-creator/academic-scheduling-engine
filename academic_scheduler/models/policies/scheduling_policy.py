from dataclasses import dataclass


@dataclass(slots=True)
class SchedulingPolicy:
    """
    Base class for all scheduling policies.

    Policies describe scheduling requirements
    without changing the core academic models.
    """

    id: str