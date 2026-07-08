import { useState } from "react";

import { useParams } from "react-router-dom";
import toast from "react-hot-toast";

import { useQuery } from "@tanstack/react-query";

import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import { CodeEditor } from "@/components/editor/CodeEditor";
import { VerdictBadge } from "@/components/submission/VerdictBadge";

import { useSubmission } from "@/hooks/useSubmission";
import { useSubmissionStatus } from "@/hooks/useSubmissionStatus";

import { Button } from "@/components/ui/button";

import type { Problem } from "@/types/problem";

const LANGUAGES = [
  {
    label: "Python",
    value: "python",
  },
  {
    label: "C++",
    value: "cpp",
  },
  {
    label: "Java",
    value: "java",
  },
];

async function getProblem(
  slug: string,
): Promise<Problem> {
  const response =
    await apiClient.get<Problem>(
      API_ENDPOINTS.problems.details(slug),
    );

  return response.data;
}

export function SolvePage() {
  const { slug } = useParams();

  const [language, setLanguage] =
    useState("python");

  const [code, setCode] =
    useState("");

  const [submissionId, setSubmissionId] =
    useState<number>();

  const {
    data: problem,
    isLoading,
  } = useQuery({
    queryKey: [
      "problem",
      slug,
    ],

    queryFn: () =>
      getProblem(slug!),

    enabled: Boolean(slug),
  });


  const {
    mutate,
    isPending,
  } = useSubmission();


  const {
    data: submission,
  } = useSubmissionStatus(
    submissionId,
  );


  function handleSubmit() {
    if (!problem) return;

    mutate(
      {
        problem_id: problem.id,
        language,
        source_code: code,
      },
      {
        onSuccess(data) {
          setSubmissionId(data.id);

          toast.success(
            "Submission started",
          );
        },

        onError() {
          toast.error(
            "Submission failed",
          );
        },
      },
    );
  }


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
    <div className="grid gap-6 lg:grid-cols-2">

      <section className="space-y-6 rounded-2xl border border-border bg-card p-6">

        <div>
          <h1 className="text-3xl font-bold">
            {problem.title}
          </h1>

          <span className="mt-3 inline-flex rounded-full bg-muted px-3 py-1 text-sm capitalize">
            {problem.difficulty}
          </span>
        </div>


        <div>
          <h2 className="mb-3 text-xl font-semibold">
            Problem Statement
          </h2>

          <p className="whitespace-pre-wrap text-muted-foreground">
            {problem.description}
          </p>
        </div>


        {submission && (
          <div className="space-y-2">
            <h3 className="font-semibold">
              Verdict
            </h3>

            <VerdictBadge
              status={submission.status}
            />
          </div>
        )}

      </section>


      <section className="space-y-4">

        <div className="flex items-center justify-between">

          <select
            className="rounded-xl border border-border bg-background px-4 py-2"
            value={language}
            onChange={(event) =>
              setLanguage(
                event.target.value,
              )
            }
          >
            {LANGUAGES.map(
              (item) => (
                <option
                  key={item.value}
                  value={item.value}
                >
                  {item.label}
                </option>
              ),
            )}
          </select>


          <Button
            onClick={handleSubmit}
            disabled={isPending}
          >
            {isPending
              ? "Submitting..."
              : "Submit"}
          </Button>

        </div>


        <CodeEditor
          value={code}
          language={language}
          onChange={setCode}
        />

      </section>

    </div>
  );
}