from datetime import date
from pydantic import BaseModel, Field


class WorkTimeCreate(BaseModel):
    employee_id: int = Field(gt=0)
    work_date: date = Field(le=date.today())
    hours_worked: int = Field(gt=0)
    is_weekend: bool = False
    is_holiday: bool = False


class WorkTimeCreated(WorkTimeCreate):
    id: int

    class Config:
        from_attributes = True


class WorkTimeList(WorkTimeCreate):
    class Config:
        from_attributes = True


class WorkTimeUpdate(BaseModel):
    work_date: date | None = Field(default=None, le=date.today())
    hours_worked: int | None = Field(default=None, gt=0)
    is_weekend: bool | None = None
    is_holiday: bool | None = None
