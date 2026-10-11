import { InjectionToken } from '@angular/core';
import { ProjectsRepository } from './projects.repository';

export const PROJECTS_REPOSITORY = new InjectionToken<ProjectsRepository>('ProjectsRepository');
