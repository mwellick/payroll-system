from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    name: str
    code: int = Field(gt=0)
    head_id: int | None


class DepartmentCreated(DepartmentCreate):
    id: int

    class Config:
        from_attributes = True


class DepartmentList(DepartmentCreated):
    class Config:
        from_attributes = True


class DepartmentUpdate(BaseModel):
    name: str | None = None
    head_id: int | None
