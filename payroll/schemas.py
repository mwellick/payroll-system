from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class PayrollCreate(BaseModel):
    employee_id: int = Field(gt=0)
    start_period: date
    end_period: date
    base_salary: Decimal = Field(gt=0)
    overtime_salary: Decimal = Decimal("0.0")
    holiday_salary: Decimal = Decimal("0.0")


class PayrollCreated(PayrollCreate):
    id: int
    gross_salary: Decimal
    net_salary: Decimal
    tax: Decimal = Decimal("0.2")

    model_config = ConfigDict(from_attributes=True)


class PayrollList(PayrollCreated):
    model_config = ConfigDict(from_attributes=True)
