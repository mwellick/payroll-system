from pydantic import BaseModel, Field, ConfigDict


class PositionCreate(BaseModel):
    name: str
    hourly_rate: float = Field(gt=0)


class PositionCreated(PositionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PositionList(PositionCreated):
    model_config = ConfigDict(from_attributes=True)


class PositionUpdate(BaseModel):
    name: str | None = None
    hourly_rate: float | None = None
