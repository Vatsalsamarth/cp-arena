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
  created_at: string;
}