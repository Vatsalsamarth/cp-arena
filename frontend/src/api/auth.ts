import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  LoginRequest,
  TokenResponse,
} from "@/types/auth";

export async function login(
  payload: LoginRequest,
): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>(
    API_ENDPOINTS.auth.login,
    payload,
    {
      headers: {
        "Content-Type": "application/json",
      },
    },
  );

  return response.data;
}