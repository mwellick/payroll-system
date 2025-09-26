from decimal import Decimal
from datetime import date

PENALTY = Decimal("0.001")


def calculate_penalty(
        gross_salary: Decimal,
        end_period: date,
        payment_date: date
):
    if end_period.month == 12:
        due_date = date(end_period.year + 1, 1, 10)
    else:
        due_date = date(end_period.year, end_period.month + 1, 10)

    if payment_date <= due_date:
        return Decimal("0.0")

    overdue_days = (payment_date - due_date).days

    penalty = Decimal(overdue_days) * PENALTY * gross_salary

    return penalty.quantize(Decimal("0.001"))
