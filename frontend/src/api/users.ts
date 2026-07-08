import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  User,
  UserStats,
} from "@/types/user";


export async function getCurrentUser(): Promise<User> {
  const response =
    await apiClient.get<User>(
      API_ENDPOINTS.users.me,
    );

  return response.data;
}


export async function getUserStats(): Promise<UserStats> {
  const response =
    await apiClient.get<UserStats>(
      API_ENDPOINTS.users.stats,
    );

  return response.data;
}