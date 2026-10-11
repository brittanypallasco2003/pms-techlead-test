from fastapi import APIRouter, Depends, HTTPException, Path

from app.lib.exceptions.not_found_exception import NotFoundException
from app.projects.application.commands.create_project_command import CreateProjectCommand
from app.projects.application.use_cases.create_project import CreateProject
from app.projects.application.use_cases.generate_project_summary import (
    GenerateProjectSummary,
)
from app.projects.application.use_cases.list_projects import ListProjects
from app.projects.infrastructure.http.dependencies import (
    create_project,
    get_list_projects,
    get_project_summary,
)
from app.projects.infrastructure.http.dtos.request.create_project_request import CreateProjectRequest
from app.projects.infrastructure.http.dtos.response.project_response import ProjectResponse
from app.projects.infrastructure.http.dtos.response.project_summary_response import (
    ProjectSummaryResponse,
)

router = APIRouter(tags=["projects"])

@router.get("/projects", response_model=list[ProjectResponse])
def list_projects(
    status: str | None = None,
    use_case: ListProjects = Depends(get_list_projects),
) -> list[ProjectResponse]:
    projects = use_case.execute(status)
    return [
        ProjectResponse(
            id=project.id,
            name=project.name,
            budget=project.budget,
            status=project.status,
        )
        for project in projects
    ]


@router.get(
    "/projects/{project_id}/summary", response_model=ProjectSummaryResponse
)
def project_summary(
    project_id: str = Path(pattern=r"^[0-9a-fA-F]{24}$"),
    use_case: GenerateProjectSummary = Depends(get_project_summary),
) -> ProjectSummaryResponse:
    try:
        summary = use_case.execute(project_id)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    return ProjectSummaryResponse(
        project_id=summary.project_id,
        name=summary.name,
        activity_count=summary.activity_count,
        completed_count=summary.completed_count,
        total_hours=summary.total_hours,
        completion_rate=summary.completion_rate,
    )

@router.post("/projects", response_model=ProjectResponse)
def new_project(request: CreateProjectRequest, use_case: CreateProject = Depends(create_project))-> ProjectResponse:
    command = CreateProjectCommand(
        name=request.name,
        budget=request.budget,
        status=request.status,
    )
    project = use_case.execute(command)
    return ProjectResponse(
        id=project.id,
        name=project.name,
        budget=project.budget,
        status=project.status,
    )
    
        