from decimal import Decimal
from datetime import timedelta, date
from fastapi import HTTPException
from starlette import status
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from app.dependencies import db_dependency
from database.models import Payroll, Employee
from .helpers import check_min_wage, calculate_payroll_amounts
from .schemas import PayrollCreate, PayrollCreated


def check_payroll_exists(payroll_id: int, db: db_dependency):
    """
    This function checks if specific payroll exists
    """
    query = select(Payroll).where(
        Payroll.id == payroll_id
    ).options(
        joinedload(Payroll.employee)
    )
    result = db.execute(query)
    payroll_instance = result.scalars().first()

    if not payroll_instance:
        raise HTTPException(
            detail="Payroll not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return payroll_instance


def payroll_create(db: db_dependency, payroll: PayrollCreate):
    check_min_wage(payroll.base_salary)
    gross_salary, tax, net_salary = calculate_payroll_amounts(
        payroll.base_salary,
        payroll.overtime_salary,
        payroll.holiday_salary,
    )

    query = select(Employee).where(
        Employee.id == payroll.employee_id
    )
    result = db.execute(query)
    employee_instance = result.scalars().one_or_none()

    if not employee_instance or not employee_instance.is_active:
        raise HTTPException(
            detail="Employee resigned",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    payroll_instance = Payroll(
        employee_id=payroll.employee_id,
        start_period=payroll.start_period,
        end_period=payroll.end_period,
        base_salary=payroll.base_salary,
        overtime_salary=payroll.overtime_salary,
        holiday_salary=payroll.holiday_salary,
        gross_salary=gross_salary,
        net_salary=net_salary,
        tax=tax,
    )
    db.add(payroll_instance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create payroll"
        )
    db.refresh(payroll_instance)

    return PayrollCreated.model_validate(payroll_instance)


def get_list_payrolls(db: db_dependency):
    query = select(Payroll).options(
        joinedload(Payroll.employee)
    )

    result = db.execute(query)
    return result.scalars().all()


def payroll_delete(payroll_id: int, db: db_dependency):
    payroll_instance = check_payroll_exists(payroll_id, db)

    db.delete(payroll_instance)
    db.commit()


def get_total_year_earnings(db: db_dependency, employee_id: int, vacation_start: date):
    year_ago = vacation_start - timedelta(days=365)

    query = (
        select(func.sum(Payroll.gross_salary))
        .where(Payroll.employee_id == employee_id)
        .where(Payroll.end_period >= year_ago)
        .where(Payroll.end_period <= vacation_start)
    )
    result = db.execute(query)
    total = result.scalars().one_or_none()
    return total or Decimal("0.0")
