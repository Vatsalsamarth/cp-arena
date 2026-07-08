import {
  useQuery,
} from "@tanstack/react-query";

import {
  getSubmission,
} from "@/api/submissions";


export function useSubmissionStatus(
  id?: number,
) {
  return useQuery({
    queryKey: [
      "submission",
      id,
    ],

    queryFn: () =>
      getSubmission(id!),

    enabled: Boolean(id),

    refetchInterval: 2000,
  });
}