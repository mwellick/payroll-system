from pydantic import BaseModel, Field


class PositionCreate(BaseModel):
    name: str
    hourly_rate: float = Field(gt=0)


class PositionCreated(PositionCreate):
    id: int

    class Config:
        from_attributes = True


class PositionList(PositionCreated):
    class Config:
        from_attributes = True


class PositionUpdate(BaseModel):
    name: str | None = None
    hourly_rate: float | None = None
