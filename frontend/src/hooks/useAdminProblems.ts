import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import {
  createProblem,
  deleteProblem,
  updateProblem,
} from "@/api/admin";


export function useCreateProblem() {
  const queryClient =
    useQueryClient();

  return useMutation({
    mutationFn:
      createProblem,

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: [
          "problems",
        ],
      });
    },
  });
}


export function useDeleteProblem() {
  const queryClient =
    useQueryClient();

  return useMutation({
    mutationFn:
      deleteProblem,

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: [
          "problems",
        ],
      });
    },
  });
}


export function useUpdateProblem() {
  const queryClient =
    useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      payload,
    }: {
      id: number;
      payload: object;
    }) =>
      updateProblem(
        id,
        payload,
      ),

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: [
          "problems",
        ],
      });
    },
  });
}