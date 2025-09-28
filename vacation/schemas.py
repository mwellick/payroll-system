from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class VacationCreate(BaseModel):
    employee_id: int = Field(gt=0)
    start_date: date
    end_date: date


class VacationCreated(VacationCreate):
    id: int
    amount: Decimal
    total_days: int

    model_config = ConfigDict(from_attributes=True)


class VacationList(VacationCreated):
    model_config = ConfigDict(from_attributes=True)


class VacationUpdate(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    total_days: int | None = Field(default=None, gt=0)
    amount: Decimal | None = Field(default=None, gt=0)
