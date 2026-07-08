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


export async function deleteProblem(
  id: number,
) {
  const response =
    await apiClient.delete(
      `${API_ENDPOINTS.problems.list}/${id}`,
    );

  return response.data;
}


export async function updateProblem(
  id: number,
  payload: Partial<Problem>,
) {
  const response =
    await apiClient.put<Problem>(
      `${API_ENDPOINTS.problems.list}/${id}`,
      payload,
    );

  return response.data;
}