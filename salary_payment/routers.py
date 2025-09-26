from fastapi import APIRouter, Path
from starlette import status
from dependencies import db_dependency
from .schemas import SalaryPaymentCreate, SalaryPaymentList
from .crud import (
    salary_payment_create,
    get_salary_payments_list,
    salary_payment_delete
)

salary_payment_router = APIRouter(prefix="/salary_payments", tags=["salary_payments"])


@salary_payment_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_salary_payment(db: db_dependency, salary_payment: SalaryPaymentCreate):
    salary_payment_instance = salary_payment_create(db, salary_payment)
    return salary_payment_instance


@salary_payment_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[SalaryPaymentList]
)
def list_salary_payments(db: db_dependency):
    salary_payments = get_salary_payments_list(db)
    return salary_payments


@salary_payment_router.delete(
    "/{salary_payment_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_salary_payment(
        db: db_dependency,
        salary_payment_id: int = Path(..., gt=0)
):
    salary_payment_delete(salary_payment_id, db)
