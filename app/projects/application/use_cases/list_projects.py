from app.projects.domain.models.project_model import Project
from app.projects.domain.repositories.project_repository import ProjectRepository

class ListProjects:
    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    def execute(self, status: str | None = None) -> list[Project]:
        return self._repository.list(status)
