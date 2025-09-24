from fastapi import FastAPI
from department.routers import departments_router
from position.routers import positions_router

app = FastAPI(title="Salary System API")

app.include_router(departments_router)
app.include_router(positions_router)
