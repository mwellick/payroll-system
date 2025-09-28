from typing import TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict

if TYPE_CHECKING:  # Solution to avoid circular import
    from employee.schemas import EmployeeList


class DepartmentCreate(BaseModel):
    name: str
    code: int = Field(gt=0)
    head_id: int | None


class DepartmentCreated(DepartmentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class DepartmentList(DepartmentCreated):
    model_config = ConfigDict(from_attributes=True)


class DepartmentRetrieve(DepartmentCreate):
    employees: list["EmployeeList"] = []

    model_config = ConfigDict(from_attributes=True)


class DepartmentUpdate(BaseModel):
    name: str | None = None
    head_id: int | None = None
