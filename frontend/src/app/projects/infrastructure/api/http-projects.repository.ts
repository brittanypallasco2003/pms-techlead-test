import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { ProjectsRepository } from '../../application/ports/projects.repository';
import { Project } from '../../domain/models/project.model';
import { ProjectSummary } from '../../domain/models/project-summary.model';
import { ProjectResponseDto, ProjectSummaryResponseDto } from './projects-api.dto';

@Injectable()
export class HttpProjectsRepository implements ProjectsRepository {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api';

  list(): Observable<Project[]> {
    return this.http.get<ProjectResponseDto[]>(`${this.baseUrl}/projects`).pipe(
      map(projects => projects.map(project => ({
        id: project.id,
        name: project.name,
        budget: project.budget,
        status: project.status,
      }))),
    );
  }

  summary(projectId: string): Observable<ProjectSummary> {
    return this.http.get<ProjectSummaryResponseDto>(
      `${this.baseUrl}/projects/${encodeURIComponent(projectId)}/summary`,
    ).pipe(
      map(summary => ({
        projectId: summary.project_id,
        name: summary.name,
        activityCount: summary.activity_count,
        completedCount: summary.completed_count,
        totalHours: summary.total_hours,
        completionRate: summary.completion_rate,
      })),
    );
  }
}
