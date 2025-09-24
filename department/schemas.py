from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    name: str
    code: int = Field(gt=0)
    head_id: int | None


class DepartmentCreated(BaseModel):
    id: int
    name: str
    code: int
    head_id: int | None

    class Config:
        from_attributes = True


class DepartmentList(BaseModel):
    id: int
    name: str
    code: int
    head_id: int | None

    class Config:
        from_attributes = True


class DepartmentUpdate(BaseModel):
    name: str | None = None
    head_id: int | None
