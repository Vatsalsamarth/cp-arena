export type Difficulty = number;

export interface Problem {
  id: number;
  title: string;
  slug: string;

  // Backend contract
  statement: string;
  difficulty: Difficulty;

  // Optional fields for future compatibility
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