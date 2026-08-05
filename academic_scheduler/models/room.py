from pydantic import Field

from academic_scheduler.common.enums import RoomType
from academic_scheduler.models.base import SchedulerBaseModel
from academic_scheduler.models.room_availability import RoomAvailability


class Room(SchedulerBaseModel):
    """
    Physical teaching space.
    """

    id: str = Field(..., min_length=1)

    code: str = Field(..., min_length=1)

    name: str

    room_type: RoomType

    capacity: int = Field(..., ge=1)

    availability: list[RoomAvailability] = Field(
        default_factory=list
    )

    active: bool = True

    description: str | None = None