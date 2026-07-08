import { useState } from "react";

import { useProblems } from "@/hooks/useProblems";

export function ProblemsPage() {
  const [search, setSearch] = useState("");

  const {
    data,
    isLoading,
  } = useProblems({
    search,
    page: 1,
    size: 10,
  });

  if (isLoading) {
    return (
      <div>
        Loading problems...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold">
          Problems
        </h1>

        <p className="text-muted-foreground">
          Practice competitive programming.
        </p>
      </section>

      <input
        className="w-full rounded-xl border border-border bg-background px-4 py-3"
        placeholder="Search problems..."
        value={search}
        onChange={(event) =>
          setSearch(event.target.value)
        }
      />

      <div className="space-y-4">
        {data?.items?.map((problem) => (
          <div
            key={problem.id}
            className="rounded-2xl border border-border bg-card p-5"
          >
            <h2 className="text-xl font-semibold">
              {problem.title}
            </h2>

            <p className="mt-2 text-sm capitalize text-muted-foreground">
              {problem.difficulty}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}