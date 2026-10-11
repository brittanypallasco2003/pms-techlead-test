class ExistsProject:
    def __init__(self, project_repository):
        self.project_repository = project_repository

    def execute(self, project_id: str) -> bool:
        return self.project_repository.exists_by_id(project_id)
