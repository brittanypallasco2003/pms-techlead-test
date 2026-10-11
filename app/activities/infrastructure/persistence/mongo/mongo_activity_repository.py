from __future__ import annotations

from pymongo.database import Database

from app.activities.domain.models.activity_model import Activity
from app.activities.domain.repository.activity_repository import ActivityRepository


class MongoActivityRepository(ActivityRepository):
    def __init__(self, database: Database) -> None:
        self._database = database

    def list(self, status: str | None = None) -> list[Activity]:
        documents = self._database.activities.find({})
        return [self._to_activity(document) for document in documents]

    def list_by_project(self, project_id: str) -> list[Activity]:
        documents = self._database.activities.find({"project_id": project_id})
        return [self._to_activity(document) for document in documents]

    def save(self, activity: Activity) -> Activity:
        document = {
            "title": activity.title,
            "hours": activity.hours,
            "completed": activity.completed,
            "project_id": activity.project_id,
        }
        result = self._database.activities.insert_one(document)
        return self._to_activity({**document, "_id": result.inserted_id})

    @staticmethod
    def _to_activity(document: dict) -> Activity:
        return Activity(
            id=str(document["_id"]),
            title=document["title"],
            hours=float(document["hours"]),
            completed=bool(document["completed"]),
            project_id=str(document["project_id"]),
        )
