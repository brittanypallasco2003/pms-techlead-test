from pydantic import BaseModel


class ActivityResponse(BaseModel):
    id: str
    title: str
    hours: float
    completed: bool