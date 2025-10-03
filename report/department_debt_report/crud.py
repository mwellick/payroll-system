from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.dependencies import db_dependency
from database.models import Payroll, Employee
from department.crud import check_department_exists
from .schemas import DepartmentEmployee, DepartmentDebtReport


def department_debt_report_create(db: db_dependency, department_id: int):
    department = check_department_exists(department_id, db)

    query = select(Employee).where(
        Employee.department_id == department_id).options(
        selectinload(Employee.payrolls).joinedload(
            Payroll.salary_payment
        )
    )
    result = db.execute(query)
    employees = result.scalars().all()

    total_department_debt = Decimal("0.0")

    department_employees = []
    for employee in employees:
        total_employee_debt = Decimal("0.0")

        for payroll in employee.payrolls:
            salary_payment = payroll.salary_payment
            if salary_payment:
                debt = (payroll.net_salary - salary_payment.amount_paid) + salary_payment.penalty
                total_employee_debt += debt

        if total_employee_debt > 0:
            department_employees.append(
                DepartmentEmployee(
                    full_name=employee.full_name,
                    tab_number=employee.tab_number,
                    total_debt=total_employee_debt
                )
            )
        total_department_debt += total_employee_debt

    return DepartmentDebtReport(
        name=department.name,
        employees=department_employees,
        total_department_debt=total_department_debt
    )
