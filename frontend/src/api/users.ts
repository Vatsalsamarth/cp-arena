import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  LeaderboardResponse,
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


export async function getLeaderboard(): Promise<LeaderboardResponse> {
  const response =
    await apiClient.get<LeaderboardResponse>(
      API_ENDPOINTS.users.leaderboard,
    );

  return response.data;
}