import { create } from "zustand";

import { tokenStorage } from "@/api/storage";

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  setToken: (token: string) => void;
  logout: () => void;
  initialize: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,

  isAuthenticated: false,

  setToken: (token) => {
    tokenStorage.set(token);

    set({
      token,
      isAuthenticated: true,
    });
  },

  logout: () => {
    tokenStorage.clear();

    set({
      token: null,
      isAuthenticated: false,
    });
  },

  initialize: () => {
    const token = tokenStorage.get();

    if (token) {
      set({
        token,
        isAuthenticated: true,
      });
    }
  },
}));