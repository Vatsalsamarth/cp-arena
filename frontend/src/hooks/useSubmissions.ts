import { useQuery } from "@tanstack/react-query";

import { getSubmissions } from "@/api/submissions";

export function useSubmissions() {
  return useQuery({
    queryKey: [
      "submissions",
    ],

    queryFn: () =>
      getSubmissions(),
  });
}