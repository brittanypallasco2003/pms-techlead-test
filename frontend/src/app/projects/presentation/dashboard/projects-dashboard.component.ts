import {
  ChangeDetectionStrategy,
  Component,
  computed,
  DestroyRef,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { DecimalPipe, PercentPipe } from '@angular/common';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Subscription } from 'rxjs';
import { PROJECTS_REPOSITORY } from '../../application/ports/projects-repository.token';
import { Project } from '../../domain/models/project.model';
import { ProjectSummary } from '../../domain/models/project-summary.model';

@Component({
  selector: 'app-projects-dashboard',
  standalone: true,
  imports: [DecimalPipe, PercentPipe],
  templateUrl: './projects-dashboard.component.html',
  styleUrl: './projects-dashboard.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProjectsDashboardComponent implements OnInit {
  private readonly repository = inject(PROJECTS_REPOSITORY);
  private readonly destroyRef = inject(DestroyRef);
  private summaryRequest?: Subscription;

  readonly projects = signal<Project[]>([]);
  readonly selectedId = signal('');
  readonly summary = signal<ProjectSummary | null>(null);
  readonly loadingProjects = signal(true);
  readonly loadingSummary = signal(false);
  readonly error = signal('');


  readonly message = computed(() => {
    if (this.loadingProjects()) return 'Cargando proyectos…';
    if (this.loadingSummary()) return 'Cargando resumen del proyecto…';
    if (this.error()) return '';
    if (this.projects().length === 0) return 'No hay proyectos disponibles.';
    if (!this.selectedId()) return 'Seleccione un proyecto para consultar sus indicadores.';
    if (this.summary()?.activityCount === 0) return 'Este proyecto todavía no tiene actividades.';
    return 'Resumen del proyecto cargado.';
  });

  ngOnInit(): void {
    this.repository.list().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: projects => {
        this.projects.set(projects);
        this.loadingProjects.set(false);
      },
      error: () => {
        this.projects.set([]);
        this.summary.set(null);
        this.selectedId.set('');
        this.loadingProjects.set(false);
        this.error.set('No se pudo cargar la lista de proyectos.');
      },
    });
  }

  selectProject(projectId: string): void {
    this.summaryRequest?.unsubscribe();
    this.selectedId.set(projectId);
    this.summary.set(null);
    this.error.set('');
    this.loadingSummary.set(false);

    if (!projectId) return;

    this.loadingSummary.set(true);
    this.summaryRequest = this.repository.summary(projectId)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: summary => {
          this.summary.set(summary);
          this.loadingSummary.set(false);
        },
        error: () => {
          this.summary.set(null);
          this.loadingSummary.set(false);
          this.error.set('No se pudo cargar el resumen del proyecto seleccionado.');
        },
      });
  }
}
