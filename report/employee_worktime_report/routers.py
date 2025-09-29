from datetime import date
from fastapi import APIRouter, Path, Query
from starlette import status
from dependencies import db_dependency
from .schemas import EmployeeWorktimeReportCreated
from .crud import employee_worktime_report_create

employee_worktime_router = APIRouter(
    prefix="/employee_worktimes",
    tags=["employee_worktimes_report"]
)


@employee_worktime_router.get(
    "/{employee_id}/",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeWorktimeReportCreated
)
def get_employee_worktime_report(
        db: db_dependency,
        employee_id: int = Path(..., gt=0),
        start_date: date = Query(...),
        end_date: date = Query(...),

):
    employee_worktime = employee_worktime_report_create(
        db,
        employee_id,
        start_date,
        end_date
    )
    return employee_worktime
