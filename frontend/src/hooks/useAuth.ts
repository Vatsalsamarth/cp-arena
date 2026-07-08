import { useEffect } from "react";

import { useAuthStore } from "@/store/auth";

export function useAuth() {
  const {
    token,
    isAuthenticated,
    initialize,
    setToken,
    logout,
  } = useAuthStore();

  useEffect(() => {
    initialize();
  }, [initialize]);

  return {
    token,
    isAuthenticated,
    setToken,
    logout,
  };
}