from bson import ObjectId

from app.projects.domain.models.project_model import Project
from app.projects.infrastructure.persistence.mongo_project_repository import (
    MongoProjectRepository,
)


def test_save_without_id_inserts_project_and_returns_mongo_generated_id(db):
    db.projects.delete_many({})
    repository = MongoProjectRepository(db)
    project = Project(
        id=None,
        name="New project",
        budget=12000.0,
        status="active",
    )

    saved_project = repository.save(project)

    assert ObjectId.is_valid(saved_project.id)
    stored_document = db.projects.find_one({"_id": ObjectId(saved_project.id)})
    assert stored_document == {
        "_id": ObjectId(saved_project.id),
        "name": "New project",
        "budget": 12000.0,
        "status": "active",
    }


def test_save_with_id_keeps_upsert_behavior_for_insert_and_update(db):
    db.projects.delete_many({})
    repository = MongoProjectRepository(db)
    project_id = "64b000000000000000000010"

    repository.save(
        Project(
            id=project_id,
            name="First version",
            budget=12000.0,
            status="active",
        )
    )
    repository.save(
        Project(
            id=project_id,
            name="Updated version",
            budget=15000.0,
            status="paused",
        )
    )

    assert db.projects.count_documents({}) == 1
    assert db.projects.find_one({"_id": ObjectId(project_id)}) == {
        "_id": ObjectId(project_id),
        "name": "Updated version",
        "budget": 15000.0,
        "status": "paused",
    }
