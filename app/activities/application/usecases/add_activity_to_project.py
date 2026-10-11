from app.activities.application.commands.create_activity_command import (
    CreateActivityCommand,
)
from app.activities.domain.models.activity_model import Activity
from app.activities.domain.repository.activity_repository import ActivityRepository
from app.lib.exceptions.not_found_exception import NotFoundException
from app.projects.domain.repositories.project_repository import ProjectRepository


class AddActivityToProject:

    def __init__(
        self,
        activity_repository: ActivityRepository,
        project_repository: ProjectRepository,
    ) -> None:
        self._activity_repository = activity_repository
        self._project_repository = project_repository

    def execute(self, command: CreateActivityCommand) -> Activity:
        project = self._project_repository.get_project_by_id(command.project_id)
        if project is None:
            raise NotFoundException(
                f"Project with id {command.project_id} does not exist."
            )

        activity = Activity(
            title=command.title,
            hours=command.hours,
            completed=command.completed,
            project_id=project.id,
        )
        return self._activity_repository.save(activity)
