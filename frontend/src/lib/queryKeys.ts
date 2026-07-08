export const queryKeys = {
  problems: {
    all: ["problems"] as const,

    list: (params: unknown) =>
      ["problems", "list", params] as const,

    detail: (slug: string) =>
      ["problems", "detail", slug] as const,
  },

  submissions: {
    all: ["submissions"] as const,
  },

  user: {
    stats: ["user", "stats"] as const,
  },
};