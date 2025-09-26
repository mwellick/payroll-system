from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field


class SalaryPaymentCreate(BaseModel):
    payroll_id: int = Field(gt=0)
    payment_date: date = Field(default_factory=date.today)


class SalaryPaymentCreated(SalaryPaymentCreate):
    id: int
    amount_paid: Decimal
    penalty: Decimal

    class Config:
        from_attributes = True


class SalaryPaymentList(SalaryPaymentCreated):
    class Config:
        from_attributes = True