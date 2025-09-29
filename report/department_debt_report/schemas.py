from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class DepartmentEmployee(BaseModel):
    full_name: str
    tab_number: int
    total_debt: Decimal


class DepartmentDebtReport(BaseModel):
    name: str
    employees: list[DepartmentEmployee]
    total_department_debt: Decimal

    model_config = ConfigDict(from_attributes=True)
