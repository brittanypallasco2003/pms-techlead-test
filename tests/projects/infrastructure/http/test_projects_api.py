import pytest

ID = "64b000000000000000000001"
EMPTY = "64b000000000000000000002"
MISSING = "64b000000000000000000099"

def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}

def test_list(client, db):
    db.projects.update_many({}, {"$set": {
        "created_by": "internal-user",
        "metadata": {"source": "internal-test"},
        "internal_note": "This field must not be public",
    }})
    response = client.get("/projects")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 2
    for project in projects:
        assert set(project) == {"id", "name", "budget", "status"}
        assert type(project["budget"]) in (int, float)
    assert sorted(projects, key=lambda project: project["id"]) == [
        {"id": ID, "name": "SAT", "budget": 15000.0, "status": "active"},
        {"id": EMPTY, "name": "Chatbots", "budget": 8000.0, "status": "active"},
    ]


def test_list_empty(client, db):
    db.projects.delete_many({})
    response = client.get("/projects")
    assert response.status_code == 200
    assert response.json() == []


def test_list_status_filter(client, db):
    db.projects.update_one({"name": "Chatbots"}, {"$set": {"status": "paused"}})
    response = client.get("/projects", params={"status": "paused"})
    assert response.status_code == 200
    assert response.json() == [
        {"id": EMPTY, "name": "Chatbots", "budget": 8000.0, "status": "paused"},
    ]

def test_summary(client):
    response = client.get(f"/projects/{ID}/summary")
    assert response.status_code == 200
    assert response.json() == {"project_id": ID, "name": "SAT", "activity_count": 3,
        "completed_count": 2, "total_hours": 35.0, "completion_rate": pytest.approx(2/3)}


def test_summary_does_not_include_another_projects_activities(client, db):
    db.activities.insert_one({
        "project_id": EMPTY,
        "title": "Chatbots activity",
        "hours": 12.0,
        "completed": False,
    })

    response = client.get(f"/projects/{ID}/summary")

    assert response.status_code == 200
    assert response.json() == {
        "project_id": ID,
        "name": "SAT",
        "activity_count": 3,
        "completed_count": 2,
        "total_hours": 35.0,
        "completion_rate": pytest.approx(2 / 3),
    }


def test_missing_summary(client):
    assert client.get(f"/projects/{MISSING}/summary").status_code == 404

def test_empty_summary(client):
    response = client.get(f"/projects/{EMPTY}/summary")
    assert response.status_code == 200
    assert response.json() == {"project_id": EMPTY, "name": "Chatbots", "activity_count": 0,
        "completed_count": 0, "total_hours": 0, "completion_rate": 0}

def test_invalid_id(client):
    assert client.get("/projects/not-an-id/summary").status_code == 422
