from datetime import date
from pydantic import BaseModel, Field
from department.schemas import DepartmentList
from position.schemas import PositionList
from payroll.schemas import PayrollList


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    is_active: bool
    department_id: int
    position_id: int


class EmployeeCreate(BaseModel):
    tab_number: int = Field(gt=0)
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date = Field(le=date.today())
    address: str
    passport_id: str
    passport_issued_by: str
    passport_issued_day: date
    is_active: bool = True
    department_id: int = Field(gt=0)
    position_id: int = Field(gt=0)


class EmployeeCreated(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True


class EmployeeList(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


class EmployeeRetrieve(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    tab_number: int = Field(gt=0)
    birth_date: date = Field(le=date.today())
    address: str
    passport_id: str
    passport_issued_by: str
    passport_issued_day: date
    is_active: bool = True
    department: "DepartmentList"
    position: "PositionList"
    payrolls: list[PayrollList] = []

    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    tab_number: int | None = Field(default=None, gt=0)
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    birth_date: date | None = Field(default=None, le=date.today())
    address: str | None = None
    passport_id: str | None = None
    passport_issued_by: str | None = None
    passport_issued_day: date | None = None
    is_active: bool | None = None
    department_id: int | None = Field(default=None, gt=0)
    position_id: int | None = Field(default=None, gt=0)
