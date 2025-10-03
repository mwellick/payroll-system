from datetime import date
from fastapi import APIRouter, Path, Query
from starlette import status
from app.dependencies import db_dependency
from .schemas import DepartmentPayrollReportCreated
from .crud import department_payroll_report_create

department_payroll_router = APIRouter(
    prefix="/department_payrolls",
    tags=["department_payrolls_report"]
)


@department_payroll_router.get(
    "/{department_id}/",
    status_code=status.HTTP_200_OK,
    response_model=DepartmentPayrollReportCreated
)
def get_department_payroll_report(
        db: db_dependency,
        department_id: int = Path(..., gt=0),
        start_date: date = Query(...),
        end_date: date = Query(...),

):
    department_payroll = department_payroll_report_create(
        db,
        department_id,
        start_date,
        end_date
    )
    return department_payroll
