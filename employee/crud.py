from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload, joinedload
from database.models import Employee
from .schemas import EmployeeCreated


def check_employee_by_passport(db, passport_id, is_active):
    query = select(Employee).where(
        Employee.passport_id == passport_id,
        Employee.is_active == is_active
    )
    result = db.execute(query)
    exists = result.scalar_one_or_none()
    if exists:
        raise HTTPException(
            detail="Active employee  already works in another department",
            status_code=status.HTTP_400_BAD_REQUEST
        )


def check_employee_exists(employee_id, db):
    """
    This function checks if specific employee exists
    """
    query = select(Employee).where(
        Employee.id == employee_id
    ).options(
        joinedload(Employee.department),
        joinedload(Employee.position)
    )
    result = db.execute(query)
    employee_instance = result.scalars().first()

    if not employee_instance:
        raise HTTPException(
            detail="Employee not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return employee_instance


def employee_create(db, employee):
    check_employee_by_passport(db, employee.passport_id, employee.is_active)

    employee_instance = Employee(
        tab_number=employee.tab_number,
        first_name=employee.first_name,
        last_name=employee.last_name,
        middle_name=employee.middle_name,
        birth_date=employee.birth_date,
        address=employee.address,
        passport_id=employee.passport_id,
        passport_issued_by=employee.passport_issued_by,
        passport_issued_day=employee.passport_issued_day,
        is_active=employee.is_active,
        department_id=employee.department_id,
        position_id=employee.position_id
    )
    db.add(employee_instance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            detail="Employee with these credentials already exists",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    db.refresh(employee_instance)

    return EmployeeCreated.model_validate(employee_instance)


def get_list_employees(db):
    query = select(Employee).options(
        selectinload(Employee.department),
        selectinload(Employee.position)
    )
    result = db.execute(query)
    return result.scalars().all()


def employee_update(employee_id, db, employee):
    employee_instance = check_employee_exists(employee_id, db)

    update_data = employee.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(employee_instance, k, v)

    db.commit()
    db.refresh(employee_instance)

    return {"message": f"Employee ID: {employee_instance.id} was updated successfully"}


def employee_delete(employee_id, db):
    employee_instance = check_employee_exists(employee_id, db)

    db.delete(employee_instance)
    db.commit()
