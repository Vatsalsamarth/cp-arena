export interface User {
  id: number;
  username: string;
  email?: string;
  created_at?: string;
}

export interface UserStats {
  total_submissions: number;
  accepted: number;
  wrong_answer: number;
  runtime_error: number;
  compilation_error: number;
  acceptance_rate: number;
}

export interface LeaderboardUser {
  rank: number;
  user_id: number;
  username: string;
  score: number;
}

export interface LeaderboardResponse {
  items: LeaderboardUser[];
  total: number;
  limit: number;
  offset: number;
  has_next: boolean;
}