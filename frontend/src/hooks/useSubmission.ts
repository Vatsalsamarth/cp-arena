import {
  useMutation,
} from "@tanstack/react-query";

import { createSubmission } from "@/api/submissions";

export function useSubmission() {
  return useMutation({
    mutationFn: createSubmission,
  });
}