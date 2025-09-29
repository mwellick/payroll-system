from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database.models import Employee, Payroll
from department.crud import check_department_exists
from .schemas import (
    SalaryPaymentEmployee,
    DepartmentSalaryPaymentReportCreated
)


def department_salary_payment_report_create(db, department_id, start_date, end_date):
    department = check_department_exists(department_id, db)

    query = select(Employee).where(
        Employee.department_id == department_id
    ).options(
        selectinload(Employee.payrolls).selectinload(Payroll.salary_payment)
    )

    result = db.execute(query)
    employees = result.scalars().all()

    total_paid = Decimal("0.0")
    total_penalty = Decimal("0.0")

    department_employees = []
    for employee in employees:
        for payroll in employee.payrolls:
            salary_payment = payroll.salary_payment
            if (salary_payment and
                    start_date <= salary_payment.payment_date <= end_date):

                department_employees.append(
                    SalaryPaymentEmployee(
                        full_name=employee.full_name,
                        tab_number=employee.tab_number,
                        payment_date=salary_payment.payment_date,
                        amount_paid=salary_payment.amount_paid,
                        penalty=salary_payment.penalty
                    )
                )
                total_paid += salary_payment.amount_paid
                total_penalty += salary_payment.penalty

    return DepartmentSalaryPaymentReportCreated(
        department_name=department.name,
        employees=department_employees,
        total_paid=total_paid,
        total_penalty=total_penalty
    )
