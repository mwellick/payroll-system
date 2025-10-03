from fastapi import FastAPI
from sqlalchemy import text

from app.dependencies import db_dependency
from department.routers import departments_router
from position.routers import positions_router
from employee.routers import employee_router
from worktime.routers import worktimes_router
from vacation.routers import vacations_router
from payroll.routers import payroll_router
from salary_payment.routers import salary_payment_router
from report.departmet_payroll_report.routers import department_payroll_router
from report.department_salary_payment_report.routers import department_salary_payment_router
from report.employee_worktime_report.routers import employee_worktime_router
from report.department_debt_report.routers import department_debt_router

from .config import settings


def setup_system_endpoints(app: FastAPI):
    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": f"{settings.app_name}"}

    @app.get("/db-health")
    def db_health_check(db: db_dependency):
        try:
            db.execute(text("SELECT 1"))
            return {"status": "ok"}
        except Exception as e:
            return {"status": "not ok", "detail": str(e)}

    return app


def setup_routers(app: FastAPI):
    domains = [
        departments_router,
        positions_router,
        employee_router,
        worktimes_router,
        vacations_router,
        payroll_router,
        salary_payment_router,
        department_payroll_router,
        department_salary_payment_router,
        employee_worktime_router,
        department_debt_router
    ]
    for domain in domains:
        app.include_router(domain)

    return app


def create_app():
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        debug=settings.debug,
        docs_url="/"
    )

    setup_system_endpoints(app)
    setup_routers(app)

    return app
