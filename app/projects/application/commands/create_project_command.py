from dataclasses import dataclass


@dataclass(frozen=True)
class CreateProjectCommand:
   name: str
   budget: float
   status: str = "active"