from fastapi import APIRouter, Path
from starlette import status
from app.dependencies import db_dependency
from .schemas import (
    WorkTimeCreate,
    WorkTimeList,
    WorkTimeUpdate
)
from .crud import (
    worktime_create,
    get_list_worktimes,
    worktime_update,
    worktime_delete
)

worktimes_router = APIRouter(prefix="/worktimes", tags=["worktimes"])


@worktimes_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_worktime(db: db_dependency, worktime: WorkTimeCreate):
    worktime_instance = worktime_create(db, worktime)
    return worktime_instance


@worktimes_router.get("", status_code=status.HTTP_200_OK, response_model=list[WorkTimeList])
def list_worktimes(db: db_dependency):
    worktimes = get_list_worktimes(db)
    return worktimes


@worktimes_router.patch("/{worktime_id}/update", status_code=status.HTTP_200_OK)
def update_worktime(
        db: db_dependency,
        worktime: WorkTimeUpdate,
        worktime_id: int = Path(..., gt=0),
):
    worktime_instance = worktime_update(worktime_id, db, worktime)
    return worktime_instance


@worktimes_router.delete("/{worktime_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_worktime(
        db: db_dependency,
        worktime_id: int = Path(..., gt=0)
):
    worktime_delete(worktime_id, db)
