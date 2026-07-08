import { useEffect } from "react";

import { getCurrentUser } from "@/api/users";

import { useAuthStore } from "@/store/auth";

export function useAuth() {
  const {
    token,
    user,
    isAuthenticated,
    initialize,
    setUser,
    setToken,
    logout,
  } = useAuthStore();

  useEffect(() => {
    initialize();
  }, [initialize]);

  useEffect(() => {
    if (!token) return;

    getCurrentUser()
      .then(setUser)
      .catch(() => {
        logout();
      });
  }, [token, setUser, logout]);

  return {
    token,
    user,
    isAuthenticated,
    setToken,
    logout,
  };
}