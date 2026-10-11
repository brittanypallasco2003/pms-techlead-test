from unittest.mock import Mock

import pytest

from app.activities.domain.models.activity_model import Activity
from app.activities.domain.repository.activity_repository import ActivityRepository
from app.lib.exceptions.not_found_exception import NotFoundException
from app.projects.application.read_models.project_summary_result import (
    ProjectSummaryResult,
)
from app.projects.application.use_cases.generate_project_summary import (
    GenerateProjectSummary,
)
from app.projects.domain.models.project_model import Project
from app.projects.domain.repositories.project_repository import ProjectRepository


PROJECT_ID = "64b000000000000000000001"


def test_generate_project_summary_aggregates_activities():
    project = Project(id=PROJECT_ID, name="SAT", budget=15000.0, status="active")
    project_repository = Mock(spec=ProjectRepository)
    project_repository.get_project_by_id.return_value = project
    activity_repository = Mock(spec=ActivityRepository)
    activity_repository.list_by_project.return_value = [
        Activity(title="Planning", hours=1.5, completed=True, project_id=PROJECT_ID),
        Activity(title="Build", hours=2.25, completed=False, project_id=PROJECT_ID),
        Activity(title="Review", hours=0.75, completed=True, project_id=PROJECT_ID),
    ]

    result = GenerateProjectSummary(project_repository, activity_repository).execute(
        PROJECT_ID
    )

    assert result == ProjectSummaryResult(
        project_id=PROJECT_ID,
        name="SAT",
        activity_count=3,
        completed_count=2,
        total_hours=4.5,
        completion_rate=pytest.approx(2 / 3),
    )
    project_repository.get_project_by_id.assert_called_once_with(PROJECT_ID)
    activity_repository.list_by_project.assert_called_once_with(PROJECT_ID)


def test_generate_project_summary_returns_zeros_for_project_without_activities():
    project = Project(id=PROJECT_ID, name="SAT", budget=15000.0, status="active")
    project_repository = Mock(spec=ProjectRepository)
    project_repository.get_project_by_id.return_value = project
    activity_repository = Mock(spec=ActivityRepository)
    activity_repository.list_by_project.return_value = []

    result = GenerateProjectSummary(project_repository, activity_repository).execute(
        PROJECT_ID
    )

    assert result == ProjectSummaryResult(
        project_id=PROJECT_ID,
        name="SAT",
        activity_count=0,
        completed_count=0,
        total_hours=0.0,
        completion_rate=0.0,
    )
    activity_repository.list_by_project.assert_called_once_with(PROJECT_ID)


def test_generate_project_summary_raises_when_project_is_missing():
    project_repository = Mock(spec=ProjectRepository)
    project_repository.get_project_by_id.return_value = None
    activity_repository = Mock(spec=ActivityRepository)

    with pytest.raises(NotFoundException, match=PROJECT_ID):
        GenerateProjectSummary(project_repository, activity_repository).execute(
            PROJECT_ID
        )

    project_repository.get_project_by_id.assert_called_once_with(PROJECT_ID)
    activity_repository.list_by_project.assert_not_called()
