from fastapi import APIRouter, Path
from starlette import status
from dependencies import db_dependency
from .schemas import DepartmentDebtReport
from .crud import department_debt_report_create

department_debt_router = APIRouter(
    prefix="/department_debts",
    tags=["department_debts_report"]
)


@department_debt_router.get(
    "{department_id}",
    status_code=status.HTTP_200_OK,
    response_model=DepartmentDebtReport
)
def get_department_debt_report(
        db: db_dependency,
        department_id: int = Path(..., gt=0)):
    department_debt = department_debt_report_create(db, department_id)
    return department_debt
