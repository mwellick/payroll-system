from fastapi import APIRouter, Path
from starlette import status
from dependencies import db_dependency
from .schemas import DepartmentCreate, DepartmentList, DepartmentUpdate
from .crud import (
    department_create,
    get_list_departments,
    department_retrieve,
    department_update,
    department_delete
)

departments_router = APIRouter(prefix="/departments", tags=["departments"])


@departments_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_department(db: db_dependency, department: DepartmentCreate):
    department_instance = department_create(db, department)
    return department_instance


@departments_router.get("", status_code=status.HTTP_200_OK, response_model=list[DepartmentList])
def list_departments(db: db_dependency):
    departments = get_list_departments(db)
    return departments


@departments_router.get("/{department_id}/", status_code=status.HTTP_200_OK)
def retrieve_department(db: db_dependency, department_id: int = Path(..., gt=0)):
    department_instance = department_retrieve(department_id, db)
    return department_instance


@departments_router.patch("/{department_id}/update", status_code=status.HTTP_200_OK)
def update_department(
        db: db_dependency,
        department: DepartmentUpdate,
        department_id: int = Path(..., gt=0),
):
    department_instance = department_update(department_id, db, department)
    return department_instance


@departments_router.delete("/{department_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
        db: db_dependency,
        department_id: int = Path(..., gt=0),
):
    department_delete(department_id, db)
