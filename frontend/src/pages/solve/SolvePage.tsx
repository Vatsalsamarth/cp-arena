import { useState } from "react";

import toast from "react-hot-toast";

import { CodeEditor } from "@/components/editor/CodeEditor";

import { useSubmission } from "@/hooks/useSubmission";

import { Button } from "@/components/ui/button";

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

export function SolvePage() {
  const [language, setLanguage] =
    useState("python");

  const [code, setCode] =
    useState("");

  const {
    mutate,
    isPending,
  } = useSubmission();

  function handleSubmit() {
    mutate(
      {
        problem_id: 1,
        language,
        source_code: code,
      },
      {
        onSuccess: () => {
          toast.success(
            "Submission created",
          );
        },

        onError: () => {
          toast.error(
            "Submission failed",
          );
        },
      },
    );
  }

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold">
          Solve Problem
        </h1>

        <p className="text-muted-foreground">
          Submit your solution.
        </p>
      </section>

      <div className="flex items-center justify-between">
        <select
          className="rounded-xl border border-border bg-background px-4 py-2"
          value={language}
          onChange={(event) =>
            setLanguage(event.target.value)
          }
        >
          {LANGUAGES.map((item) => (
            <option
              key={item.value}
              value={item.value}
            >
              {item.label}
            </option>
          ))}
        </select>

        <Button
          onClick={handleSubmit}
          disabled={isPending}
        >
          {isPending
            ? "Submitting..."
            : "Submit Solution"}
        </Button>
      </div>

      <CodeEditor
        value={code}
        language={language}
        onChange={setCode}
      />
    </div>
  );
}