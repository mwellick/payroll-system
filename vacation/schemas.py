from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class VacationCreate(BaseModel):
    employee_id: int = Field(gt=0)
    start_date: date
    end_date: date
    total_days: int = Field(gt=0)
    amount: Decimal = Field(gt=0)


class VacationCreated(VacationCreate):
    id: int

    class Config:
        from_attributes = True


class VacationList(VacationCreated):
    class Config:
        from_attributes = True


class VacationUpdate(BaseModel):
    employee_id: int | None = Field(default=None, gt=0)
    start_date: date | None = None
    end_date: date | None = None
    total_days: int | None = Field(default=None, gt=0)
    amount: Decimal | None = Field(default=None, gt=0)
