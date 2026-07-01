from pydantic import BaseModel, ConfigDict

class Subject(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    subject_name:str
    classes_per_week:int

class SubjectCreate(BaseModel):
    subject_name:str
    classes_per_week: int

class SubjectUpdate(BaseModel):
    subject_name:str | None=None
    classes_per_week: int | None=None