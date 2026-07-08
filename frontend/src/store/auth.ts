import { create } from "zustand";

import { tokenStorage } from "@/api/storage";

import type { User } from "@/types/user";

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;

  setToken: (token: string) => void;
  setUser: (user: User) => void;
  logout: () => void;
  initialize: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  isAuthenticated: false,

  setToken: (token) => {
    tokenStorage.set(token);

    set({
      token,
      isAuthenticated: true,
    });
  },

  setUser: (user) => {
    set({
      user,
    });
  },

  logout: () => {
    tokenStorage.clear();

    set({
      token: null,
      user: null,
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