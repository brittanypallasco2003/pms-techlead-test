
from dataclasses import dataclass

@dataclass
class Activity:
    title: str
    hours: float
    completed: bool
    project_id: str
    id: str | None = None
