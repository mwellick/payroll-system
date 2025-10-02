from fastapi import HTTPException
from sqlalchemy import select
from starlette import status
from dependencies import db_dependency
from database.models import Position
from .schemas import (
    PositionCreate,
    PositionCreated,
    PositionUpdate
)


def check_position_exists(position_id: int, db: db_dependency):
    """
    This function checks if specific position exists
    """
    query = select(Position).where(
        Position.id == position_id)

    result = db.execute(query)

    position_instance = result.scalars().first()

    if not position_instance:
        raise HTTPException(
            detail="Position not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return position_instance


def position_create(db: db_dependency, position: PositionCreate):
    position_instance = Position(
        name=position.name,
        hourly_rate=position.hourly_rate
    )
    db.add(position_instance)
    db.commit()
    db.refresh(position_instance)

    return PositionCreated.model_validate(position_instance)


def get_list_positions(db: db_dependency):
    query = select(Position).order_by(
        Position.id)
    result = db.execute(query)
    return result.scalars().all()


def position_update(position_id: int, db: db_dependency, position: PositionUpdate):
    position_instance = check_position_exists(position_id, db)

    update_data = position.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(position_instance, k, v)

    db.commit()
    db.refresh(position_instance)

    return {"message": f"{position_instance.name} was updated successfully"}


def position_delete(position_id: int, db: db_dependency):
    position_instance = check_position_exists(position_id, db)

    db.delete(position_instance)
    db.commit()
