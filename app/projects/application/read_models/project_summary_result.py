from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectSummaryResult:

    project_id: str
    name: str
    activity_count: int
    completed_count: int
    total_hours: float
    completion_rate: float
