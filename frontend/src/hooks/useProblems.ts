import { useQuery } from "@tanstack/react-query";

import { getProblems } from "@/api/problems";
import { queryKeys } from "@/lib/queryKeys";

export function useProblems(params?: {
  page?: number;
  size?: number;
  search?: string;
  difficulty?: string;
}) {
  return useQuery({
    queryKey: queryKeys.problems.list(params),

    queryFn: () =>
      getProblems(params),
  });
}