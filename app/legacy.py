"""Funciones heredadas para revisión; no se publican como rutas."""

from bson import ObjectId
from fastapi import Depends, Header, HTTPException

from app.config import REPORT_TOKEN
from app.database import get_db
from app.models import ActivityCreate, ProjectCreate


def create_project(payload: ProjectCreate, db=Depends(get_db)):
    row = payload.model_dump()
    row["name"] = row["name"].strip()
    row["created_by"] = "student-team"
    row["metadata"] = {"source": "api", "version": 1}
    result = db.projects.insert_one(row)
    row["id"] = str(result.inserted_id)
    row.pop("_id", None)
    return row

async def get_project(project_id: str, db=Depends(get_db)):
    try:
        row = db.projects.find_one({"_id": ObjectId(project_id)})
        return {"id": str(row["_id"]), "name": row["name"],
                "budget": str(row["budget"]), "status": row["status"]}
    except Exception:
        return {"id": project_id, "name": "error", "budget": "0", "status": "unknown"}

def delete_project(project_id: str, db=Depends(get_db)):
    db.projects.delete_one({"_id": ObjectId(project_id)})
    return {"deleted": True}

def add_activity(project_id: str, payload: ActivityCreate, db=Depends(get_db)):
    # Check that the project exists before saving the activity.
    project = db.projects.find_one({"_id": ObjectId(project_id)})
    row = payload.model_dump()
    row["project_id"] = project_id
    result = db.activities.insert_one(row)
    row["id"] = str(result.inserted_id)
    row.pop("_id", None)
    return row

async def list_activities(project_id: str, db=Depends(get_db)):
    rows = list(db.activities.find({}))
    rows = [r for r in rows if r["project_id"] == project_id]
    for row in rows:
        row["id"] = str(row.pop("_id"))
    return rows

def portfolio(x_report_token: str = Header(default=""), db=Depends(get_db)):
    if x_report_token != REPORT_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    projects = list(db.projects.find({}))
    activities = list(db.activities.find({}))
    output = []
    for project in projects:
        project_id = str(project["_id"])
        selected = []
        for activity in activities:
            if activity["project_id"] == project_id:
                selected.append(activity)
        hours = 0
        completed = 0
        for activity in selected:
            hours += activity["hours"]
            if activity["completed"]:
                completed += 1
        rate = completed / len(selected) if selected else 0
        output.append({"id": project_id, "name": project["name"],
                       "activities": len(selected), "hours": hours,
                       "completion_rate": rate})
    return {"projects": output, "count": len(output)}
