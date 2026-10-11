from app.activities.domain.repository.activity_repository import ActivityRepository
from app.lib.exceptions.not_found_exception import NotFoundException
from app.projects.application.read_models.project_summary_result import (
    ProjectSummaryResult,
)
from app.projects.domain.repositories.project_repository import ProjectRepository

class GenerateProjectSummary:

    def __init__(
        self,
        project_repository: ProjectRepository,
        activity_repository: ActivityRepository,
    ) -> None:
        self._project_repository = project_repository
        self._activity_repository = activity_repository

    def execute(self, project_id: str) -> ProjectSummaryResult:
        project = self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise NotFoundException(f"Project with id {project_id} not found.")

        activities = self._activity_repository.list_by_project(project_id)
        activity_count = len(activities)
        completed_count = sum(activity.completed for activity in activities)
        total_hours = sum(activity.hours for activity in activities)
        completion_rate = (
            completed_count / activity_count if activity_count else 0.0
        )

        return ProjectSummaryResult(
            project_id=project.id,
            name=project.name,
            activity_count=activity_count,
            completed_count=completed_count,
            total_hours=float(total_hours),
            completion_rate=completion_rate,
        )
