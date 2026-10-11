from abc import ABC, abstractmethod

from app.projects.domain.models.project_model import Project


class ProjectRepository(ABC):
    
    @abstractmethod
    def list(self, status: str | None = None) -> list[Project]:
        raise NotImplementedError

    @abstractmethod
    def exists_by_id(self, project_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save(self, project: Project) -> Project:
        raise NotImplementedError

    @abstractmethod
    def get_project_by_id(self, id: str) -> Project | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError
