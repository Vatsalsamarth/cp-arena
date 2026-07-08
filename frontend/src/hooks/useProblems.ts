import {
  useQuery,
} from "@tanstack/react-query";

import { getProblems } from "@/api/problems";

export function useProblems(params?: {
  page?: number;
  size?: number;
  search?: string;
  difficulty?: string;
}) {
  return useQuery({
    queryKey: [
      "problems",
      params,
    ],

    queryFn: () =>
      getProblems(params),
  });
}