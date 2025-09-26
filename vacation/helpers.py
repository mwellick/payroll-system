from decimal import Decimal

HOLIDAY_DAYS = 11


def calculate_vacation_amount(total_year_earnings, start_date, end_date):
    """
    S = M / (365 - C) * N

    S- vacation amount
    M - total year earnings
    C - Holiday days
    N - vacation duration (days)
    """

    vacation_days = (end_date - start_date).days + 1
    amount = Decimal(total_year_earnings / (365 - HOLIDAY_DAYS)) * vacation_days
    return amount.quantize(Decimal("0.01"))
