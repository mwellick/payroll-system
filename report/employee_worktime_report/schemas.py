from pydantic import BaseModel, ConfigDict


class EmployeeWorktimeReportCreated(BaseModel):
    full_name: str
    department: str
    position: str
    hourly_rate: float
    hours_worked: int

    model_config = ConfigDict(from_attributes=True)
