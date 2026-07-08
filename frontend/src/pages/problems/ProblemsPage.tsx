import { useState } from "react";

import { Link } from "react-router-dom";

import { useProblems } from "@/hooks/useProblems";

const difficulties = [
  "all",
  "easy",
  "medium",
  "hard",
];

export function ProblemsPage() {
  const [search, setSearch] = useState("");

  const [difficulty, setDifficulty] = useState("all");

  const [page, setPage] = useState(1);

  const {
    data,
    isLoading,
  } = useProblems({
    search,
    difficulty:
      difficulty === "all"
        ? undefined
        : difficulty,
    page,
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
      </section>

      <div className="flex flex-col gap-4 md:flex-row">
        <input
          className="flex-1 rounded-xl border border-border bg-background px-4 py-3"
          placeholder="Search problems..."
          value={search}
          onChange={(event) =>
            setSearch(event.target.value)
          }
        />

        <select
          className="rounded-xl border border-border bg-background px-4 py-3"
          value={difficulty}
          onChange={(event) => {
            setDifficulty(event.target.value);
            setPage(1);
          }}
        >
          {difficulties.map((item) => (
            <option
              key={item}
              value={item}
            >
              {item}
            </option>
          ))}
        </select>
      </div>

      <div className="grid gap-4">
        {data?.items.map((problem) => (
          <Link
            key={problem.id}
            to={`/problems/${problem.slug}`}
            className="rounded-2xl border border-border bg-card p-6 transition hover:bg-muted"
          >
            <div className="flex justify-between">
              <h2 className="text-xl font-semibold">
                {problem.title}
              </h2>

              <span className="rounded-full bg-muted px-3 py-1 text-sm capitalize">
                {problem.difficulty}
              </span>
            </div>

            {problem.tags?.length ? (
              <p className="mt-3 text-sm text-muted-foreground">
                {problem.tags.join(", ")}
              </p>
            ) : null}
          </Link>
        ))}
      </div>

      <div className="flex justify-center gap-4">
        <button
          className="rounded-xl border px-4 py-2"
          disabled={page <= 1}
          onClick={() =>
            setPage((current) => current - 1)
          }
        >
          Previous
        </button>

        <span className="px-4 py-2">
          Page {page}
        </span>

        <button
          className="rounded-xl border px-4 py-2"
          disabled={page >= (data?.pages ?? 1)}
          onClick={() =>
            setPage((current) => current + 1)
          }
        >
          Next
        </button>
      </div>
    </div>
  );
}