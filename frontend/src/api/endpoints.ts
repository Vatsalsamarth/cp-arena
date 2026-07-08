export const API_ENDPOINTS = {
  auth: {
    login: "/auth/login",
  },

  users: {
    create: "/users",
    me: "/users/me",
    stats: "/users/me/stats",
    solved: "/users/me/solved",
    leaderboard: "/users/leaderboard",
  },

  problems: {
    list: "/problems",
    details: (slug: string) => `/problems/${slug}`,
  },

  submissions: {
    list: "/submissions",
    create: "/submissions",
  },

  health: {
    live: "/live",
    ready: "/ready",
    health: "/health",
  },
} as const;