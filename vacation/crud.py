from fastapi import HTTPException
from starlette import status
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from database.models import Vacation, Employee
from .schemas import VacationCreated



# TODO: implement calculate_vacation_amount()
#  function which will generate amount for specific vacation
#  - calculate S = M / (365 - C) * N
#  - M: total salary of employee in last 12 months
#  - C: number of holidays
#  - N: vacation duration in calendar days
#  - set vacation.amount = S

def check_vacation_exists(vacation_id, db):
    """
    This function checks if specific vacation exists
    """
    query = select(Vacation).where(
        Vacation.id == vacation_id
    ).options(
        joinedload(
            Vacation.employee)
    )
    result = db.execute(query)
    vacation_instance = result.scalars().first()

    if not vacation_instance:
        raise HTTPException(
            detail="Vacation not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return vacation_instance


def check_vacation_limit(vacation, db):
    """
    This function checks if employee is able to
    go in vacation and ensure that no more than 15% of department
    employees are on a vacation
    """

    # Get employee
    employee_query = select(Employee).where(
        Employee.id == vacation.employee_id
    )
    result = db.execute(employee_query)
    employee_instance = result.scalar_one_or_none()

    department_id = employee_instance.department_id

    # Total amount of employees in department
    total_employees_query = select(func.count(Employee.id)).where(
        Employee.department_id == department_id
    )
    employees_res = db.execute(total_employees_query)
    total_employees = employees_res.scalar_one()

    # Find and count number of vacations in this period of time
    num_vacations_query = select(func.count(Vacation.id)).join(
        Employee).where(
        Employee.department_id == department_id
    ).where(
        (Vacation.start_date <= vacation.end_date)
        &
        (Vacation.end_date >= vacation.start_date)
    )
    vacations_res = db.execute(num_vacations_query)

    num_vacations = vacations_res.scalar_one()

    allowed_vacations = max(1, int(total_employees * 0.15))
    if (num_vacations + 1) / allowed_vacations:
        raise HTTPException(
            detail="There are more than 15% of department employees in a vacation",
            status_code=status.HTTP_400_BAD_REQUEST
        )


def vacation_create(db, vacation):
    check_vacation_limit(vacation, db)

    vacation_instance = Vacation(
        employee_id=vacation.employee_id,
        start_date=vacation.start_date,
        end_date=vacation.end_date,
        total_days=vacation.total_days,
        amount=vacation.amount
    )
    db.add(vacation_instance)
    db.commit()
    db.refresh(vacation_instance)

    return VacationCreated.model_validate(vacation_instance)


def get_list_vacations(db):
    query = select(Vacation).options(
        joinedload(Vacation.employee)
    )
    result = db.execute(query)
    return result.scalars().all()


def vacation_update(vacation_id, db, vacation):
    vacation_instance = check_vacation_exists(vacation_id, db)

    update_data = vacation.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(vacation_instance, k, v)

    db.commit()
    db.refresh(vacation_instance)

    return {
        "message": f"Vacation of employee ID: "
                   f"{vacation_instance.employee_id} "
                   f"was updated successfully"
    }


def vacation_delete(vacation_id, db):
    vacation_instance = check_vacation_exists(vacation_id, db)

    db.delete(vacation_instance)
    db.commit()

    return
