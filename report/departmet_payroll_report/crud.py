from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database.models import Employee
from department.crud import check_department_exists
from .schemas import DepartmentEmployee, DepartmentPayrollReportCreated


def department_payroll_report_create(db, department_id, start_date, end_date):
    department = check_department_exists(department_id, db)

    query = select(Employee).where(
        Employee.department_id == department_id
    ).options(
        selectinload(Employee.payrolls)
    )
    result = db.execute(query)
    employees = result.scalars().all()

    total_gross = Decimal("0.0")
    total_net = Decimal("0.0")
    total_tax = Decimal("0.0")

    department_employees = []
    for employee in employees:
        for payroll in employee.payrolls:
            if (payroll.start_period <= end_date and
                    payroll.end_period >= start_date):
                full_name = (f"{employee.first_name} {employee.last_name} "
                             f"{employee.middle_name}").strip()

                department_employees.append(
                    DepartmentEmployee(
                        start_period=payroll.start_period,
                        end_period=payroll.end_period,
                        full_name=full_name,
                        tab_number=employee.tab_number,
                        base_salary=payroll.base_salary,
                        overtime_salary=payroll.overtime_salary,
                        holiday_salary=payroll.holiday_salary,
                        gross_salary=payroll.gross_salary,
                        net_salary=payroll.net_salary,
                        tax=payroll.tax
                    )
                )
                total_gross += payroll.gross_salary
                total_net += payroll.net_salary
                total_tax += payroll.tax

    return DepartmentPayrollReportCreated(
        department_name=department.name,
        employees=department_employees,
        total_gross=total_gross,
        total_net=total_net,
        total_tax=total_tax
    )
