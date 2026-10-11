from dataclasses import dataclass


@dataclass(eq=False)
class Project:
    id: str | None
    name: str
    budget: float
    status: str
