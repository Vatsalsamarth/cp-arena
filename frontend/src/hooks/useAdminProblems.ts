import {
  useMutation,
} from "@tanstack/react-query";

import {
  createProblem,
} from "@/api/admin";


export function useCreateProblem() {
  return useMutation({
    mutationFn:
      createProblem,
  });
}