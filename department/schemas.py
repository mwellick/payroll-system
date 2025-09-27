from typing import TYPE_CHECKING
from pydantic import BaseModel, Field

if TYPE_CHECKING: # Solution to avoid circular import
    from employee.schemas import EmployeeList


class DepartmentCreate(BaseModel):
    name: str
    code: int = Field(gt=0)
    head_id: int | None


class DepartmentCreated(DepartmentCreate):
    id: int

    class Config:
        from_attributes = True


class DepartmentList(DepartmentCreated):
    class Config:
        from_attributes = True


class DepartmentRetrieve(DepartmentCreate):
    employees: list["EmployeeList"] = []

    class Config:
        from_attributes = True


class DepartmentUpdate(BaseModel):
    name: str | None = None
    head_id: int | None = None
