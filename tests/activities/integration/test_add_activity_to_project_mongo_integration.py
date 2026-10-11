import pytest
from bson import ObjectId

from app.activities.application.commands.create_activity_command import (
    CreateActivityCommand,
)
from app.activities.application.usecases.add_activity_to_project import (
    AddActivityToProject,
)
from app.activities.infrastructure.persistence.mongo.mongo_activity_repository import (
    MongoActivityRepository,
)
from app.lib.exceptions.not_found_exception import NotFoundException
from app.projects.infrastructure.persistence.mongo_project_repository import (
    MongoProjectRepository,
)


PROJECT_ID = "64b000000000000000000001"
MISSING_PROJECT_ID = "64b000000000000000000099"


def test_create_activity_persists_it_with_project_reference(db):
    activity_repository = MongoActivityRepository(db)
    use_case = AddActivityToProject(
        activity_repository=activity_repository,
        project_repository=MongoProjectRepository(db),
    )

    activity = use_case.execute(
        CreateActivityCommand(
            title="Review",
            hours=2.5,
            completed=False,
            project_id=PROJECT_ID,
        )
    )

    assert activity.id is not None
    stored_document = db.activities.find_one({"_id": ObjectId(activity.id)})
    assert stored_document == {
        "_id": ObjectId(activity.id),
        "title": "Review",
        "hours": 2.5,
        "completed": False,
        "project_id": PROJECT_ID,
    }
    assert activity in activity_repository.list_by_project(PROJECT_ID)


def test_create_activity_rejects_a_missing_project_without_saving(db):
    initial_activity_count = db.activities.count_documents({})
    use_case = AddActivityToProject(
        activity_repository=MongoActivityRepository(db),
        project_repository=MongoProjectRepository(db),
    )

    with pytest.raises(NotFoundException):
        use_case.execute(
            CreateActivityCommand(
                title="Review",
                hours=2.5,
                completed=False,
                project_id=MISSING_PROJECT_ID,
            )
        )

    assert db.activities.count_documents({}) == initial_activity_count
