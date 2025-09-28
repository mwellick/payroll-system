from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class SalaryPaymentEmployee(BaseModel):
    full_name: str
    tab_number: int
    payment_date: date
    amount_paid: Decimal
    penalty: Decimal


class DepartmentSalaryPaymentReportCreated(BaseModel):
    department_name: str
    employees: list[SalaryPaymentEmployee]
    total_paid: Decimal
    total_penalty: Decimal

    class Config:
        from_attributes = True
