from fastapi import APIRouter, Path
from starlette import status
from app.dependencies import db_dependency
from .schemas import PayrollCreate, PayrollList
from .crud import payroll_create, get_list_payrolls, payroll_delete

payroll_router = APIRouter(prefix="/payrolls", tags=["payrolls"])


@payroll_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_payroll(db: db_dependency, payroll: PayrollCreate):
    payroll_instance = payroll_create(db, payroll)
    return payroll_instance


@payroll_router.get("", status_code=status.HTTP_200_OK, response_model=list[PayrollList])
def list_payrolls(db: db_dependency):
    payrolls = get_list_payrolls(db)
    return payrolls


@payroll_router.delete("/{payroll_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_payroll(db: db_dependency, payroll_id: int = Path(..., gt=0)):
    payroll_delete(payroll_id, db)
