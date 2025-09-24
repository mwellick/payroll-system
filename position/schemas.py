from pydantic import BaseModel, Field


class PositionCreate(BaseModel):
    name: str
    hourly_rate: float = Field(gt=0)


class PositionCreated(BaseModel):
    id: int
    name: str
    hourly_rate: float

    class Config:
        from_attributes = True


class PositionList(BaseModel):
    id: int
    name: str
    hourly_rate: float

    class Config:
        from_attributes = True


class PositionUpdate(BaseModel):
    name: str
    hourly_rate: float
