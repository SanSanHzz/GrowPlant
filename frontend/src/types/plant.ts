export interface PlantType {
  id: string;
  name: string;
  description: string;
  preview_image: string;
}

export interface Plant {
  id: string;
  plant_type: string;
  current_stage: number;
  current_stage_name: string;
  total_drops: number;
  drops_to_next_stage: number;
  name: string | null;
  is_active: boolean;
  created_at: string;
}

export interface DropItem {
  id: string;
  event_type: string;
  source_repo: string;
  committed_at: string;
  created_at: string;
}

export interface PlantState {
  id: string;
  plant_type: string;
  current_stage: number;
  current_stage_name: string;
  total_drops: number;
  drops_in_stage: number;
  drops_to_next_stage: number;
  stage_progress_pct: number;
  max_stage_reached: boolean;
}

export interface DashboardData {
  plant: PlantState | null;
  recent_drops: DropItem[];
  stats: {
    total_commits: number;
    total_pr_merges: number;
    repositories_contributing: string[];
    first_drop_at: string | null;
    last_drop_at: string | null;
  };
}

export interface DropHistory {
  drops: DropItem[];
  next_cursor: string | null;
  has_more: boolean;
  total_drops: number;
}

export interface PlantList {
  plants: Plant[];
  active_plant_id: string | null;
}
