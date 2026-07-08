import { useProblems } from "@/hooks/useProblems";
import {
  useDeleteProblem,
} from "@/hooks/useAdminProblems";


export function ProblemManagement() {
  const {
    data,
  } = useProblems({
    page: 1,
    size: 20,
  });


  const {
    mutate: remove,
  } = useDeleteProblem();


  return (
    <div className="space-y-4">

      <h2 className="text-xl font-semibold">
        Manage Problems
      </h2>


      {data?.items.map(
        (problem) => (
          <div
            key={problem.id}
            className="flex items-center justify-between rounded-xl border border-border bg-card p-4"
          >

            <div>
              <p className="font-semibold">
                {problem.title}
              </p>

              <p className="text-sm text-muted-foreground">
                {problem.difficulty}
              </p>
            </div>


            <button
              className="rounded-lg border px-3 py-2 text-sm"
              onClick={() =>
                remove(problem.id)
              }
            >
              Delete
            </button>

          </div>
        ),
      )}

    </div>
  );
}