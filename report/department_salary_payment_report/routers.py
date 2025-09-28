from datetime import date
from fastapi import APIRouter, Path, Query
from starlette import status
from dependencies import db_dependency
from .schemas import DepartmentSalaryPaymentReportCreated
from .crud import department_salary_payment_report_create

department_salary_payment_router = APIRouter(
    prefix="/department_salary_payments",
    tags=["salary_payment_report"]
)


@department_salary_payment_router.get(
    "/{department_id}/",
    status_code=status.HTTP_200_OK,
    response_model=DepartmentSalaryPaymentReportCreated
)
def get_department_salary_payment_report(
        db: db_dependency,
        department_id: int = Path(..., gt=0),
        start_date: date = Query(...),
        end_date: date = Query(...)
):
    department_salary_payment = department_salary_payment_report_create(
        db,
        department_id,
        start_date,
        end_date
    )
    return department_salary_payment
