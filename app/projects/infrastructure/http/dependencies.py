from fastapi import Depends
from pymongo.database import Database

from app.activities.infrastructure.persistence.mongo.mongo_activity_repository import (
    MongoActivityRepository,
)
from app.database import get_db
from app.projects.application.use_cases.create_project import CreateProject
from app.projects.application.use_cases.generate_project_summary import (
    GenerateProjectSummary,
)
from app.projects.application.use_cases.list_projects import ListProjects
from app.projects.infrastructure.persistence.mongo_project_repository import (
    MongoProjectRepository,
)


def get_list_projects(db: Database = Depends(get_db)) -> ListProjects:
    return ListProjects(MongoProjectRepository(db))


def get_project_summary(db: Database = Depends(get_db)) -> GenerateProjectSummary:
    return GenerateProjectSummary(
        MongoProjectRepository(db),
        MongoActivityRepository(db),
    )

def create_project(db: Database = Depends(get_db)) -> CreateProject:
    return CreateProject(MongoProjectRepository(db))
