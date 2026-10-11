from unittest.mock import Mock

import pytest

from app.activities.application.commands.create_activity_command import (
    CreateActivityCommand,
)
from app.activities.application.usecases.add_activity_to_project import (
    AddActivityToProject,
)
from app.activities.domain.models.activity_model import Activity
from app.activities.domain.repository.activity_repository import ActivityRepository
from app.lib.exceptions.not_found_exception import NotFoundException
from app.projects.domain.models.project_model import Project
from app.projects.domain.repositories.project_repository import ProjectRepository


PROJECT_ID = "64b000000000000000000001"


def test_add_activity_saves_it_for_an_existing_project():
    project_repository = Mock(spec=ProjectRepository)
    project_repository.get_project_by_id.return_value = Project(
        id=PROJECT_ID,
        name="SAT",
        budget=15000.0,
        status="active",
    )
    activity_repository = Mock(spec=ActivityRepository)
    saved_activity = Activity(
        id="64b000000000000000000011",
        title="Review",
        hours=2.5,
        completed=False,
        project_id=PROJECT_ID,
    )
    activity_repository.save.return_value = saved_activity

    result = AddActivityToProject(
        activity_repository=activity_repository,
        project_repository=project_repository,
    ).execute(
        CreateActivityCommand(
            title="Review",
            hours=2.5,
            completed=False,
            project_id=PROJECT_ID,
        )
    )

    project_repository.get_project_by_id.assert_called_once_with(PROJECT_ID)
    activity_repository.save.assert_called_once_with(
        Activity(
            id=None,
            title="Review",
            hours=2.5,
            completed=False,
            project_id=PROJECT_ID,
        )
    )
    assert result is saved_activity


def test_add_activity_does_not_save_when_project_is_missing():
    project_repository = Mock(spec=ProjectRepository)
    project_repository.get_project_by_id.return_value = None
    activity_repository = Mock(spec=ActivityRepository)

    with pytest.raises(NotFoundException, match=PROJECT_ID):
        AddActivityToProject(
            activity_repository=activity_repository,
            project_repository=project_repository,
        ).execute(
            CreateActivityCommand(
                title="Review",
                hours=2.5,
                completed=False,
                project_id=PROJECT_ID,
            )
        )

    project_repository.get_project_by_id.assert_called_once_with(PROJECT_ID)
    activity_repository.save.assert_not_called()
