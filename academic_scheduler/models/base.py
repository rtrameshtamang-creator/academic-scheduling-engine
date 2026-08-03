from pydantic import BaseModel, ConfigDict


class SchedulerBaseModel(BaseModel):
    """
    Base model for all scheduler domain models.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
        frozen=False,
        str_strip_whitespace=True,
    )
