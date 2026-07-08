export interface User {
  id: number;
  username: string;
  email?: string;
  created_at?: string;
}

export interface UserStats {
  solved_count: number;
  submission_count: number;
  accepted_count: number;
  success_rate: number;
}