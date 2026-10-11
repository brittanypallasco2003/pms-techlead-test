import { Observable } from 'rxjs';
import { Project } from '../../domain/models/project.model';
import { ProjectSummary } from '../../domain/models/project-summary.model';

export interface ProjectsRepository {
  list(): Observable<Project[]>;
  summary(projectId: string): Observable<ProjectSummary>;
}
