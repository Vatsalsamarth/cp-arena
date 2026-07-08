
import { useState } from "react";

import { CodeEditor } from "@/components/editor/CodeEditor";

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

  const [code, setCode] = useState(
    "# Write your solution here",
  );

  function handleSubmit() {
    console.log({
      language,
      code,
    });
  }

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold">
          Solve Problem
        </h1>

        <p className="text-muted-foreground">
          Write your solution and submit.
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

        <Button onClick={handleSubmit}>
          Submit Solution
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