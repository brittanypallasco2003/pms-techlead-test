export interface ProjectResponseDto {
  id: string;
  name: string;
  budget: number;
  status: string;
}

export interface ProjectSummaryResponseDto {
  project_id: string;
  name: string;
  activity_count: number;
  completed_count: number;
  total_hours: number;
  completion_rate: number;
}
