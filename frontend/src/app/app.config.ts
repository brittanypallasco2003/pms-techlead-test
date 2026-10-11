import { provideHttpClient } from '@angular/common/http';
import { ApplicationConfig } from '@angular/core';
import { PROJECTS_REPOSITORY } from './projects/application/ports/projects-repository.token';
import { HttpProjectsRepository } from './projects/infrastructure/api/http-projects.repository';


export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    { provide: PROJECTS_REPOSITORY, useClass: HttpProjectsRepository },
  ],
};
