import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  ProblemListResponse,
} from "@/types/problem";

interface ProblemParams {
  page?: number;
  size?: number;
  search?: string;
  difficulty?: string;
}

export async function getProblems(
  params?: ProblemParams,
): Promise<ProblemListResponse> {
  const response =
    await apiClient.get<ProblemListResponse>(
      API_ENDPOINTS.problems.list,
      {
        params,
      },
    );

  return response.data;
}