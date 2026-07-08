import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  Submission,
  SubmissionRequest,
} from "@/types/submission";

export async function createSubmission(
  payload: SubmissionRequest,
): Promise<Submission> {
  const response =
    await apiClient.post<Submission>(
      API_ENDPOINTS.submissions.create,
      payload,
    );

  return response.data;
}