from pydantic import BaseModel


class CreateProjectRequest(BaseModel):
    name: str
    budget: float
    status: str = "active"