from app.projects.application.commands.create_project_command import CreateProjectCommand
from app.projects.domain.models.project_model import Project


class CreateProject:
    
    def __init__(self, project_repository):
        self.project_repository = project_repository

    def execute(self, command: CreateProjectCommand):
        new_project = Project(
            id=None,
            name=command.name,
            budget=command.budget,
            status=command.status
        )
        created_project = self.project_repository.save(new_project)
        return created_project
