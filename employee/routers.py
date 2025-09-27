from fastapi import APIRouter, Path
from starlette import status
from dependencies import db_dependency
from department.schemas import DepartmentRetrieve
from .schemas import (
    EmployeeCreate,
    EmployeeList,
    EmployeeUpdate
)
from .crud import (
    employee_create,
    get_list_employees,
    employee_retrieve,
    employee_update,
    employee_delete
)

# TODO: 1) Add pagination in Employees list

DepartmentRetrieve.model_rebuild() # Updating schema after forward reference
employee_router = APIRouter(prefix="/employees", tags=["employees"])


@employee_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_employee(db: db_dependency, employee: EmployeeCreate):
    employee_instance = employee_create(db, employee)
    return employee_instance


@employee_router.get("", status_code=status.HTTP_200_OK, response_model=list[EmployeeList])
def list_employees(db: db_dependency):
    employees = get_list_employees(db)
    return employees


@employee_router.get("/{employee_id}/", status_code=status.HTTP_200_OK)
def retrieve_employee(db: db_dependency, employee_id: int = Path(..., gt=0)):
    employee_instance = employee_retrieve(employee_id, db)
    return employee_instance


@employee_router.patch("/{employee_id}/update", status_code=status.HTTP_200_OK)
def update_employee(
        db: db_dependency,
        employee: EmployeeUpdate,
        employee_id: int = Path(..., gt=0)
):
    employee_instance = employee_update(employee_id, db, employee)
    return employee_instance


@employee_router.delete("/{employee_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
        db: db_dependency,
        employee_id: int = Path(..., gt=0),
):
    employee_delete(employee_id, db)
