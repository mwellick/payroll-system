from fastapi import APIRouter, Path
from starlette import status
from app.dependencies import db_dependency
from .schemas import PositionCreate, PositionList, PositionUpdate
from .crud import (
    position_create,
    get_list_positions,
    position_update,
    position_delete
)

positions_router = APIRouter(prefix="/positions", tags=["positions"])


@positions_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_position(db: db_dependency, position: PositionCreate):
    position_instance = position_create(db, position)
    return position_instance


@positions_router.get("", status_code=status.HTTP_200_OK, response_model=list[PositionList])
def list_positions(db: db_dependency):
    positions = get_list_positions(db)
    return positions


@positions_router.patch("/{position_id}/update", status_code=status.HTTP_200_OK)
def update_position(
        db: db_dependency,
        position: PositionUpdate,
        position_id: int = Path(..., gt=0),
):
    position_instance = position_update(position_id, db, position)
    return position_instance


@positions_router.delete("/{position_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_position(
        db: db_dependency,
        position_id: int = Path(..., gt=0),
):
    position_delete(position_id, db)
