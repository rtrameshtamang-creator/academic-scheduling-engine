from datetime import time
from pydantic import BaseModel, Field

from academic_scheduler.common.enums import ActivityType, DayPart


class SessionTemplate(BaseModel):
    """
    Reusable session definition.

    Example:
        T1 : 07:10–08:45
        L1 : 07:10–09:30

    A SessionTemplate does NOT belong to a day.
    It is reused across all working days.
    """

    id: str = Field(..., description="Unique identifier")
    code: str = Field(..., description="Short code like T1 or L1")
    name: str = Field(..., description="Human readable name")

    display_order: int = Field(..., ge=1)

    start_time: time
    end_time: time

    duration_minutes: int = Field(..., gt=0)

    day_part: DayPart

    allowed_activity_types: list[ActivityType]

    active: bool = True

    description: str | None = None