from bson import ObjectId
from pymongo.database import Database

from app.projects.domain.models.project_model import Project
from app.projects.domain.repositories.project_repository import ProjectRepository


class MongoProjectRepository(ProjectRepository):
    def __init__(self, database: Database) -> None:
        self._database = database

    def list(self, status: str | None = None) -> list[Project]:
        query = {"status": status} if status else {}
        projection = {"_id": 1, "name": 1, "budget": 1, "status": 1}
        documents = self._database.projects.find(query, projection)
        return [self._to_project(document) for document in documents]

    def save(self, project: Project) -> Project:
        document = {
            "name": project.name,
            "budget": project.budget,
            "status": project.status,
        }

        if project.id is None:
            result = self._database.projects.insert_one(document)
            return self._to_project({**document, "_id": result.inserted_id})

        self._database.projects.replace_one(
            {"_id": ObjectId(project.id)},
            document,
            upsert=True,
        )
        return project

    def get_project_by_id(self, id: str) -> Project | None:
        if not ObjectId.is_valid(id):
            return None

        document = self._database.projects.find_one({"_id": ObjectId(id)})
        if document is None:
            return None

        return self._to_project(document)

    def delete(self, id: str) -> None:
        if ObjectId.is_valid(id):
            self._database.projects.delete_one({"_id": ObjectId(id)})

    def exists_by_id(self, project_id: str) -> bool:
        if not ObjectId.is_valid(project_id):
            return False

        document = self._database.projects.find_one({"_id": ObjectId(project_id)})
        return document is not None

    @staticmethod
    def _to_project(document: dict) -> Project:
        return Project(
            id=str(document["_id"]),
            name=document["name"],
            budget=float(document["budget"]),
            status=document["status"],
        )
