from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    budget: float
    status: str = "active"

class ActivityCreate(BaseModel):
    title: str
    hours: float
    completed: bool = False
