from fastapi import FastAPI
from department.routers import departments_router

app = FastAPI(title="Salary System API")

app.include_router(departments_router)
