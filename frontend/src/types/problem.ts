export type Difficulty =
  | "easy"
  | "medium"
  | "hard";

export interface Problem {
  id: number;
  title: string;
  slug: string;
  description?: string;
  difficulty: Difficulty;
  tags?: string[];
  created_at?: string;
}

export interface ProblemListResponse {
  items: Problem[];
  total: number;
  page: number;
  size: number;
  pages: number;
}