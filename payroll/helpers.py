from decimal import Decimal
from datetime import date
from fastapi import HTTPException
from starlette import status

PENALTY = Decimal("0.001")
MIN_WAGE = Decimal("8000.00")
TAX = Decimal("0.2")


def calculate_penalty(
        gross_salary: Decimal,
        end_period: date,
        payment_date: date | None = None
):
    if payment_date is None:
        payment_date = date.today()

    if end_period.month == 12:
        due_date = date(end_period.year + 1, 1, 10)
    else:
        due_date = date(end_period.year, end_period.month + 1, 10)

    if payment_date <= due_date:
        return Decimal("0.0")

    overdue_days = (payment_date - due_date).days

    penalty = Decimal(overdue_days) * PENALTY * gross_salary

    return penalty.quantize(Decimal("0.001"))


def check_min_wage(base_salary: Decimal):
    if base_salary < MIN_WAGE:
        raise HTTPException(
            detail="Base salary can't be less than minimum wage.",
            status_code=status.HTTP_400_BAD_REQUEST
        )


def calculate_payroll_amounts(
        base_salary: Decimal,
        overtime_salary: Decimal,
        holiday_salary: Decimal,
        end_period: date
):
    gross_salary = base_salary + overtime_salary + holiday_salary
    tax = gross_salary * TAX
    net_salary = gross_salary - tax
    penalty = calculate_penalty(gross_salary, end_period)

    return gross_salary, tax, net_salary, penalty
