from fastapi import HTTPException
from sqlalchemy import select
from starlette import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.dependencies import db_dependency
from database.models import Department
from .schemas import (
    DepartmentCreate,
    DepartmentCreated,
    DepartmentUpdate,
    DepartmentRetrieve
)


def check_department_exists(department_id: int, db: db_dependency):
    """
    This function checks if specific department exists
    """
    query = select(Department).where(
        Department.id == department_id).options(
        selectinload(Department.employees)
    )

    result = db.execute(query)

    department_instance = result.scalars().first()

    if not department_instance:
        raise HTTPException(
            detail="Departments not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return department_instance


def department_create(db: db_dependency, department: DepartmentCreate):
    existing = db.execute(select(Department).where(
        Department.code == department.code)
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            detail=f"Department with this code: {department.code} already exists",
            status_code=status.HTTP_409_CONFLICT
        )

    department_instance = Department(
        name=department.name,
        code=department.code,
        head_id=department.head_id
    )
    db.add(department_instance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            detail="Failed to create department",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    db.refresh(department_instance)

    return DepartmentCreated.model_validate(department_instance)


def get_list_departments(db: db_dependency):
    query = select(Department).order_by(Department.id)
    result = db.execute(query)
    return result.scalars().all()


def department_retrieve(department_id: int, db: db_dependency):
    department_instance = check_department_exists(department_id, db)
    return DepartmentRetrieve.model_validate(department_instance)


def department_update(department_id: int, db: db_dependency, department: DepartmentUpdate):
    department_instance = check_department_exists(department_id, db)

    update_data = department.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(department_instance, k, v)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Failed to update department due to integrity constraints"
        )
    db.refresh(department_instance)

    return {"message": f"{department_instance.name} was updated successfully"}


def department_delete(department_id: int, db: db_dependency):
    department_instance = check_department_exists(department_id, db)

    db.delete(department_instance)
    db.commit()
