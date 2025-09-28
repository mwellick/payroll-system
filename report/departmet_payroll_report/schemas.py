from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class DepartmentEmployee(BaseModel):
    start_period: date
    end_period: date
    full_name: str
    tab_number: int
    base_salary: Decimal
    overtime_salary: Decimal
    holiday_salary: Decimal
    gross_salary: Decimal
    net_salary: Decimal
    tax: Decimal


class DepartmentPayrollReportCreated(BaseModel):
    department_name: str
    employees: list[DepartmentEmployee]
    total_gross: Decimal
    total_net: Decimal
    total_tax: Decimal

    class Config:
        from_attributes = True
