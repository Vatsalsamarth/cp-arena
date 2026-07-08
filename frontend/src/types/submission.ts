export type SubmissionStatus =
  | "pending"
  | "running"
  | "accepted"
  | "wrong_answer"
  | "failed";

export interface SubmissionRequest {
  problem_id: number;
  language: string;
  source_code: string;
}

export interface Submission {
  id: number;
  problem_id: number;
  status: SubmissionStatus;
  language: string;
  source_code?: string;
  created_at: string;
}

export interface SubmissionListResponse {
  items: Submission[];
  total: number;
  page: number;
  size: number;
  pages: number;
}