export interface ProjectSummary {
  readonly projectId: string;
  readonly name: string;
  readonly activityCount: number;
  readonly completedCount: number;
  readonly totalHours: number;
  readonly completionRate: number;
}
