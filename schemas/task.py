from datetime import datetime
from pydantic import BaseModel,Field,ConfigDict

from typing import Literal

class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    title:str
    description:str
    date:datetime
    deadline:datetime
    status:Literal["pending","completed","cancelled"]=Field(default="pending")
    priority:int=Field(...,ge=1,le=3)

class TaskCreate(BaseModel):

    title:str
    description:str
    deadline:datetime
    status:Literal["pending","completed","cancelled"]=Field(default="pending")
    priority: int = Field(..., ge=1, le=3)

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None
    status: Literal["pending", "completed","cancelled"] | None = None
    priority: int | None=Field(default=None, ge=1, le=3)