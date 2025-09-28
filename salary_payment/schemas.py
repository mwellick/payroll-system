from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class SalaryPaymentCreate(BaseModel):
    payroll_id: int = Field(gt=0)
    payment_date: date = Field(default_factory=date.today)


class SalaryPaymentCreated(SalaryPaymentCreate):
    id: int
    amount_paid: Decimal
    penalty: Decimal

    model_config = ConfigDict(from_attributes=True)


class SalaryPaymentList(SalaryPaymentCreated):
    model_config = ConfigDict(from_attributes=True)
