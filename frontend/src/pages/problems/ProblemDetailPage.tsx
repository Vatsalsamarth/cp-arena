import { Link, useParams } from "react-router-dom";

import { useQuery } from "@tanstack/react-query";

import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import { Button } from "@/components/ui/button";

import type { Problem } from "@/types/problem";

async function getProblem(slug: string) {
  const response = await apiClient.get<Problem>(
    API_ENDPOINTS.problems.details(slug),
  );

  return response.data;
}

export function ProblemDetailPage() {
  const { slug } = useParams();

  const {
    data: problem,
    isLoading,
  } = useQuery({
    queryKey: ["problem", slug],

    queryFn: () =>
      getProblem(slug!),

    enabled: Boolean(slug),
  });

  if (isLoading) {
    return (
      <div>
        Loading problem...
      </div>
    );
  }

  if (!problem) {
    return (
      <div>
        Problem not found
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <section className="space-y-4">
        <h1 className="text-3xl font-bold">
          {problem.title}
        </h1>

        <span className="inline-flex rounded-full bg-muted px-3 py-1 text-sm capitalize">
          {problem.difficulty}
        </span>

        <Link to={`/solve/${problem.slug}`}>
          <Button>
            Solve Problem
          </Button>
        </Link>
      </section>

      <section className="rounded-2xl border border-border bg-card p-6">
        <h2 className="mb-4 text-xl font-semibold">
          Description
        </h2>

        <p className="whitespace-pre-wrap text-muted-foreground">
          {problem.description}
        </p>
      </section>
    </div>
  );
}