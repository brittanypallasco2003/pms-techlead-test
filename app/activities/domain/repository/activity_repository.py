from __future__ import annotations

from abc import ABC, abstractmethod

from app.activities.domain.models.activity_model import Activity


class ActivityRepository(ABC):

    @abstractmethod
    def list(self, status: str | None = None) -> list[Activity]:
        raise NotImplementedError

    @abstractmethod
    def list_by_project(self, project_id: str) -> list[Activity]:
        raise NotImplementedError

    @abstractmethod
    def save(self, activity: Activity) -> Activity:
        raise NotImplementedError
