from unittest.mock import Mock

from app.projects.application.commands.create_project_command import (
    CreateProjectCommand,
)
from app.projects.application.use_cases.create_project import CreateProject
from app.projects.domain.models.project_model import Project
from app.projects.domain.repositories.project_repository import ProjectRepository


def test_create_project_saves_a_project_without_an_id_and_returns_saved_project():
    saved_project = Project(
        id="64b000000000000000000010",
        name="New project",
        budget=12000.0,
        status="active",
    )
    project_repository = Mock(spec=ProjectRepository)
    project_repository.save.return_value = saved_project
    use_case = CreateProject(project_repository)

    result = use_case.execute(
        CreateProjectCommand(name="New project", budget=12000.0)
    )

    project_to_save = project_repository.save.call_args.args[0]
    assert project_to_save.id is None
    assert project_to_save.name == "New project"
    assert project_to_save.budget == 12000.0
    assert project_to_save.status == "active"
    assert result is saved_project
