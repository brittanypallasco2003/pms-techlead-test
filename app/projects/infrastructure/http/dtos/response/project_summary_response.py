from pydantic import BaseModel

class ProjectSummaryResponse(BaseModel):
    project_id: str
    name: str
    activity_count: int
    completed_count: int
    total_hours: float
    completion_rate: float
