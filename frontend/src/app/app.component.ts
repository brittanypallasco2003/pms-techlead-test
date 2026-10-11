import { ChangeDetectionStrategy, Component } from '@angular/core';
import { ProjectsDashboardComponent } from './projects/presentation/dashboard/projects-dashboard.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ProjectsDashboardComponent],
  template: '<app-projects-dashboard />',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppComponent {}
