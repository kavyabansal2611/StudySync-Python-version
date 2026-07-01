from datetime import datetime
from pydantic import BaseModel,ConfigDict

class Attendance(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    subject_id: int
    date: datetime
    present: bool

class AttendanceUpdate(BaseModel):
    date:datetime | None = None
    present:bool | None=None

class AttendanceCreate(BaseModel):
    date:datetime
    present:bool
