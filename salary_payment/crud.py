from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from app.dependencies import db_dependency
from database.models import SalaryPayment, Payroll
from payroll.crud import check_payroll_exists
from .helpers import calculate_penalty
from .schemas import SalaryPaymentCreate, SalaryPaymentCreated


def check_salary_payment_exists(salary_payment_id: int, db: db_dependency):
    """
    This function checks if specific salary payment exists
    """
    query = select(SalaryPayment).where(
        SalaryPayment.id == salary_payment_id
    )
    result = db.execute(query)
    salary_payment_instance = result.scalars().first()

    if not salary_payment_instance:
        raise HTTPException(
            detail="Payment not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return salary_payment_instance


def salary_payment_create(db: db_dependency, salary_payment: SalaryPaymentCreate):
    query = select(Payroll).where(
        Payroll.id == salary_payment.payroll_id
    )
    result = db.execute(query)

    payroll_instance = result.scalar_one_or_none()

    check_payroll_exists(payroll_instance.id, db)

    penalty = calculate_penalty(
        payroll_instance.gross_salary,
        payroll_instance.end_period,
        salary_payment.payment_date
    )

    payment_instance = SalaryPayment(
        payroll_id=salary_payment.payroll_id,
        payment_date=salary_payment.payment_date,
        amount_paid=payroll_instance.net_salary + penalty,
        penalty=penalty
    )

    db.add(payment_instance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create salary payment"
        )
    db.refresh(payment_instance)

    return SalaryPaymentCreated.model_validate(payment_instance)


def get_salary_payments_list(db: db_dependency):
    query = select(SalaryPayment).options(
        joinedload(SalaryPayment.payroll)
    )
    result = db.execute(query)
    return result.scalars().all()


def salary_payment_delete(salary_payment_id: int, db: db_dependency):
    salary_payment_instance = check_salary_payment_exists(salary_payment_id, db)

    db.delete(salary_payment_instance)
    db.commit()
