import { useState } from "react";

import { Link } from "react-router-dom";

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
          Solve competitive programming challenges.
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
          <Link
            key={problem.id}
            to={`/problems/${problem.slug}`}
            className="block rounded-2xl border border-border bg-card p-5 transition hover:bg-muted"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">
                {problem.title}
              </h2>

              <span className="rounded-full bg-muted px-3 py-1 text-sm capitalize">
                {problem.difficulty}
              </span>
            </div>

            <p className="mt-2 text-sm text-muted-foreground">
              {problem.tags?.join(", ")}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}