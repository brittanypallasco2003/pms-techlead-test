from app.lib.exceptions.not_found_exception import NotFoundException


class FindProjectById:
    def __init__(self, project_repository):
        self.project_repository = project_repository

    def execute(self, id: str):
        project = self.project_repository.get_project_by_id(id)
        if project is None:
            raise NotFoundException(f"Project with id {id} not found.")
        return project
