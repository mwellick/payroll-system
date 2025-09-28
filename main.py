from fastapi import FastAPI
from department.routers import departments_router
from position.routers import positions_router
from employee.routers import employee_router
from worktime.routers import worktimes_router
from vacation.routers import vacations_router
from payroll.routers import payroll_router
from salary_payment.routers import salary_payment_router
from report.departmet_payroll_report.routers import department_payroll_router

app = FastAPI(title="Salary System API")

app.include_router(departments_router)
app.include_router(positions_router)
app.include_router(employee_router)
app.include_router(worktimes_router)
app.include_router(vacations_router)
app.include_router(payroll_router)
app.include_router(salary_payment_router)
app.include_router(department_payroll_router)
