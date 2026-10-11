from app.activities.domain.models.activity_model import Activity
from app.lib.exceptions.not_found_exception import NotFoundException


class ListActivitiesByProject:
    def __init__(self, activity_repository, project_repository):
        self.activity_repository = activity_repository
        self.project_repository = project_repository

    def execute(self, project_id: str) -> list[Activity]:
        if not self.project_repository.exists_by_id(project_id):
            raise NotFoundException(f"Project with id {project_id} does not exist.")

        return self.activity_repository.list_by_project(project_id)
