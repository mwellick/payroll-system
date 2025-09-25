from fastapi import APIRouter, Path
from starlette import status
from dependencies import db_dependency
from .schemas import (
    VacationCreate,
    VacationList,
    VacationUpdate
)
from .crud import (
    vacation_create,
    get_list_vacations,
    vacation_update,
    vacation_delete
)

vacations_router = APIRouter(prefix="/vacations", tags=["vacations"])


@vacations_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_vacation(db: db_dependency, vacation: VacationCreate):
    vacation_instance = vacation_create(db, vacation)
    return vacation_instance


@vacations_router.get("", status_code=status.HTTP_200_OK, response_model=list[VacationList])
def list_vacations(db: db_dependency):
    vacations = get_list_vacations(db)
    return vacations


@vacations_router.patch("/{vacation_id}/update", status_code=status.HTTP_200_OK)
def update_vacation(
        db: db_dependency,
        vacation: VacationUpdate,
        vacation_id: int = Path(..., gt=0)
):
    vacation_instance = vacation_update(vacation_id, db, vacation)
    return vacation_instance


@vacations_router.delete("/{vacation_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_vacation(
        db: db_dependency,
        vacation_id: int = Path(..., gt=0)
):
    vacation_delete(vacation_id, db)
    return
