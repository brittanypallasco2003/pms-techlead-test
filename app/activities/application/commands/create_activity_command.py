from dataclasses import dataclass

@dataclass(frozen=True)
class CreateActivityCommand:
    title: str
    hours: float
    completed: bool
    project_id: str
