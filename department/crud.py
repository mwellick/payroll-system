from fastapi import HTTPException
from sqlalchemy import select
from starlette import status
from database.models import Department
from .schemas import DepartmentCreated


def check_department_exists(department_id, db):
    """
    This function checks if specific department exists
    """
    query = select(Department).filter(
        Department.id == department_id)

    result = db.execute(query)

    department_instance = result.scalars().first()

    if not department_instance:
        raise HTTPException(
            detail="Departments not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return department_instance


def department_create(db, department):
    department_instance = Department(
        name=department.name,
        code=department.code,
        head_id=department.head_id
    )
    db.add(department_instance)
    db.commit()
    db.refresh(department_instance)

    return DepartmentCreated.model_validate(department_instance)


def get_list_departments(db):
    query = select(Department).order_by(Department.id)
    result = db.execute(query)
    return result.scalars().all()


def department_update(department_id, db, department):
    department_instance = check_department_exists(department_id, db)

    update_data = department.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(department_instance, k, v)

    db.commit()
    db.refresh(department_instance)

    return {"message": f"{department_instance.name} was updated successfully"}


def department_delete(department_id, db):
    department_instance = check_department_exists(department_id, db)

    db.delete(department_instance)
    db.commit()

    return
