import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  Problem,
} from "@/types/problem";


export async function createProblem(
  payload: Partial<Problem>,
) {
  const response =
    await apiClient.post<Problem>(
      API_ENDPOINTS.problems.list,
      payload,
    );

  return response.data;
}