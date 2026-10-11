import { HttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { appConfig } from '../../../app.config';
import { ProjectsRepository } from '../../application/ports/projects.repository';
import { PROJECTS_REPOSITORY } from '../../application/ports/projects-repository.token';
import { Project } from '../../domain/models/project.model';
import { ProjectSummary } from '../../domain/models/project-summary.model';
import { ProjectResponseDto, ProjectSummaryResponseDto } from '../../infrastructure/api/projects-api.dto';
import { ProjectsDashboardComponent } from './projects-dashboard.component';

const projects: ProjectResponseDto[] = [
  { id: '64b000000000000000000001', name: 'SAT', budget: 15000, status: 'active' },
  { id: '64b000000000000000000002', name: 'Chatbots', budget: 8000, status: 'active' },
];
const satSummary: ProjectSummaryResponseDto = {
  project_id: projects[0].id,
  name: 'SAT',
  activity_count: 3,
  completed_count: 2,
  total_hours: 35,
  completion_rate: 2 / 3,
};
const emptySummary: ProjectSummaryResponseDto = {
  project_id: projects[1].id,
  name: 'Chatbots',
  activity_count: 0,
  completed_count: 0,
  total_hours: 0,
  completion_rate: 0,
};

describe('ProjectsDashboardComponent con el adaptador HTTP', () => {
  let fixture: ComponentFixture<ProjectsDashboardComponent>;
  let http: HttpTestingController;
  let element: HTMLElement;

  beforeEach(() => {
    // Solo las pruebas sustituyen la red; el componente utiliza el servicio real.
    TestBed.configureTestingModule({
      imports: [ProjectsDashboardComponent],
      providers: [...appConfig.providers, provideHttpClientTesting()],
    });
    http = TestBed.inject(HttpTestingController);
    fixture = TestBed.createComponent(ProjectsDashboardComponent);
    element = fixture.nativeElement;
    fixture.detectChanges();
  });

  afterEach(() => http.verify());

  function loadProjects(): void {
    http.expectOne({ method: 'GET', url: '/api/projects' }).flush(projects);
    fixture.detectChanges();
  }

  function select(projectId: string): void {
    const selector = element.querySelector('select')!;
    selector.value = projectId;
    selector.dispatchEvent(new Event('change'));
    fixture.detectChanges();
  }

  function summaryUrl(projectId: string): string {
    return `/api/projects/${projectId}/summary`;
  }

  function indicators(): string[] {
    return Array.from(element.querySelectorAll('article strong'), card => card.textContent!.trim());
  }

  it('anuncia la carga de la lista y distingue una lista vacía de un error', () => {
    expect(element.querySelector('[role="status"]')?.textContent).toContain('Cargando proyectos');
    expect(element.querySelector('select')!.disabled).toBe(true);

    http.expectOne('/api/projects').flush([]);
    fixture.detectChanges();

    expect(element.querySelector('[role="status"]')?.textContent).toContain('No hay proyectos disponibles.');
    expect(element.querySelector('[role="alert"]')).toBeNull();
    expect(element.querySelector('select')!.disabled).toBe(true);
    expect(indicators()).toEqual([]);
  });

  it('muestra un error visible cuando falla la lista', () => {
    http.expectOne('/api/projects').flush('Unavailable', { status: 503, statusText: 'Service Unavailable' });
    fixture.detectChanges();

    expect(element.querySelector('[role="alert"]')?.textContent).toBe('No se pudo cargar la lista de proyectos.');
    expect(element.querySelector('[role="status"]')?.textContent).toBe('');
    expect(element.querySelector('select')!.disabled).toBe(true);
    expect(indicators()).toEqual([]);
  });

  it('consulta el resumen seleccionado y muestra el nombre y los cuatro indicadores', () => {
    loadProjects();
    select(projects[0].id);

    expect(element.querySelector('[role="status"]')?.textContent).toContain('Cargando resumen');
    expect(element.querySelector('#project-summary')?.getAttribute('aria-busy')).toBe('true');
    expect(indicators()).toEqual([]);

    http.expectOne({ method: 'GET', url: summaryUrl(projects[0].id) }).flush(satSummary);
    fixture.detectChanges();

    expect(element.querySelector('#summary-title')?.textContent).toBe('SAT');
    expect(indicators()).toEqual(['3', '2', '35', '66.7%']);
    expect(element.querySelector('#project-summary')?.getAttribute('aria-busy')).toBe('false');
  });

  it('presenta ceros y 0% cuando el proyecto no tiene actividades', () => {
    loadProjects();
    select(projects[1].id);
    http.expectOne(summaryUrl(projects[1].id)).flush(emptySummary);
    fixture.detectChanges();

    expect(element.querySelector('#summary-title')?.textContent).toBe('Chatbots');
    expect(indicators()).toEqual(['0', '0', '0', '0%']);
    expect(element.querySelector('[role="status"]')?.textContent).toContain('todavía no tiene actividades');
  });

  it('retira los indicadores anteriores en cuanto cambia el proyecto', () => {
    loadProjects();
    select(projects[0].id);
    http.expectOne(summaryUrl(projects[0].id)).flush(satSummary);
    fixture.detectChanges();

    select(projects[1].id);

    expect(indicators()).toEqual([]);
    expect(element.querySelector('#summary-title')).toBeNull();
    expect(element.querySelector('[role="status"]')?.textContent).toContain('Cargando resumen');

    http.expectOne(summaryUrl(projects[1].id)).flush(emptySummary);
    fixture.detectChanges();
    expect(element.querySelector('#summary-title')?.textContent).toBe('Chatbots');
  });

  it('limpia las tarjetas ante un error de resumen y permite otra selección', () => {
    loadProjects();
    select(projects[0].id);
    http.expectOne(summaryUrl(projects[0].id)).flush(satSummary);
    fixture.detectChanges();

    select(projects[1].id);
    http.expectOne(summaryUrl(projects[1].id)).flush('Unavailable', { status: 503, statusText: 'Service Unavailable' });
    fixture.detectChanges();

    expect(indicators()).toEqual([]);
    expect(element.querySelector('[role="alert"]')?.textContent).toContain('No se pudo cargar el resumen');
    expect(fixture.componentInstance.loadingSummary()).toBe(false);

    select(projects[0].id);
    expect(element.querySelector('[role="alert"]')).toBeNull();
    http.expectOne(summaryUrl(projects[0].id)).flush(satSummary);
    fixture.detectChanges();
    expect(indicators()).toEqual(['3', '2', '35', '66.7%']);
  });

  it('deselecciona un proyecto cargado sin hacer otra petición', () => {
    loadProjects();
    select(projects[0].id);
    http.expectOne(summaryUrl(projects[0].id)).flush(satSummary);
    fixture.detectChanges();

    select('');

    expect(indicators()).toEqual([]);
    expect(element.querySelector('[role="status"]')?.textContent).toContain('Seleccione un proyecto');
    expect(fixture.componentInstance.selectedId()).toBe('');
    http.expectNone(request => request.url.includes('/summary'));
  });

  it('cancela un resumen pendiente al deseleccionar', () => {
    loadProjects();
    select(projects[0].id);
    const request = http.expectOne(summaryUrl(projects[0].id));

    select('');

    expect(request.cancelled).toBe(true);
    expect(fixture.componentInstance.loadingSummary()).toBe(false);
    expect(indicators()).toEqual([]);
    expect(element.querySelector('[role="status"]')?.textContent).toContain('Seleccione un proyecto');
  });

  it('cancela las peticiones al destruir el componente', () => {
    loadProjects();
    select(projects[0].id);
    const request = http.expectOne(summaryUrl(projects[0].id));

    fixture.destroy();

    expect(request.cancelled).toBe(true);
  });
});

describe('ProjectsDashboardComponent con un repositorio independiente de HTTP', () => {
  it('renderiza el resumen del puerto sin usar HttpClient', () => {
    const domainProjects: Project[] = [
      { id: 'local-project', name: 'Proyecto del puerto', budget: 1000, status: 'active' },
    ];
    const domainSummary: ProjectSummary = {
      projectId: domainProjects[0].id,
      name: domainProjects[0].name,
      activityCount: 4,
      completedCount: 1,
      totalHours: 12,
      completionRate: 0.25,
    };
    const summary = vi.fn(() => of(domainSummary));
    const repository: ProjectsRepository = {
      list: () => of(domainProjects),
      summary,
    };
    const httpClientFactory = vi.fn(() => {
      throw new Error('La vista no debe depender de HttpClient.');
    });

    // La vista recibe modelos del puerto: no necesita el adaptador ni DTO de la API.
    TestBed.configureTestingModule({
      imports: [ProjectsDashboardComponent],
      providers: [
        { provide: PROJECTS_REPOSITORY, useValue: repository },
        { provide: HttpClient, useFactory: httpClientFactory },
      ],
    });
    const fixture = TestBed.createComponent(ProjectsDashboardComponent);
    const element: HTMLElement = fixture.nativeElement;
    fixture.detectChanges();

    const selector = element.querySelector('select')!;
    selector.value = domainProjects[0].id;
    selector.dispatchEvent(new Event('change'));
    fixture.detectChanges();

    expect(summary).toHaveBeenCalledExactlyOnceWith(domainProjects[0].id);
    expect(element.querySelector('#summary-title')?.textContent).toBe(domainSummary.name);
    expect(Array.from(element.querySelectorAll('article strong'), card => card.textContent!.trim()))
      .toEqual(['4', '1', '12', '25%']);
    expect(httpClientFactory).not.toHaveBeenCalled();
  });
});
