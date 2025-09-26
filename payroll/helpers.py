from decimal import Decimal
from fastapi import HTTPException
from starlette import status

MIN_WAGE = Decimal("8000.00")
TAX = Decimal("0.2")


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
):
    gross_salary = base_salary + overtime_salary + holiday_salary
    tax = gross_salary * TAX
    net_salary = gross_salary - tax

    return gross_salary, tax, net_salary
