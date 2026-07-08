import axios from "axios";

import { ENV } from "@/config/env";

import { tokenStorage } from "./storage";

export const apiClient = axios.create({
  baseURL: ENV.apiBaseUrl,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

apiClient.interceptors.request.use((config) => {
  const token = tokenStorage.get();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      tokenStorage.clear();
    }

    return Promise.reject(error);
  },
);