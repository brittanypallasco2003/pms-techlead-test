from pydantic import BaseModel

class ProjectResponse(BaseModel):
    id: str
    name: str
    budget: float
    status: str = "active"
