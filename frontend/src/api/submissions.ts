import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  Submission,
  SubmissionListResponse,
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


export async function getSubmissions(
  page = 1,
  size = 10,
): Promise<SubmissionListResponse> {
  const response =
    await apiClient.get<SubmissionListResponse>(
      API_ENDPOINTS.submissions.list,
      {
        params: {
          page,
          size,
        },
      },
    );

  return response.data;
}


export async function getSubmission(
  id: number,
): Promise<Submission> {
  const response =
    await apiClient.get<Submission>(
      `${API_ENDPOINTS.submissions.list}/${id}`,
    );

  return response.data;
}