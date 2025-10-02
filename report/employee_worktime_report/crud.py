from datetime import date
from dependencies import db_dependency
from employee.crud import check_employee_exists
from .schemas import EmployeeWorktimeReportCreated


def employee_worktime_report_create(
        db: db_dependency,
        employee_id: int,
        start_date: date,
        end_date: date
):
    employee = check_employee_exists(employee_id, db)

    total_hours = 0
    for work_time in employee.work_times:
        if start_date <= work_time.work_date <= end_date:
            total_hours += work_time.hours_worked

    return EmployeeWorktimeReportCreated(
        full_name=employee.full_name,
        department=employee.department.name,
        position=employee.position.name,
        hourly_rate=employee.position.hourly_rate,
        hours_worked=total_hours
    )
