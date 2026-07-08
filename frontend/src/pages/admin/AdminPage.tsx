import {
  useForm,
} from "react-hook-form";

import {
  zodResolver,
} from "@hookform/resolvers/zod";

import toast from "react-hot-toast";
import { ProblemManagement } from "@/components/admin/ProblemManagement";
import {
  problemSchema,
  type ProblemFormData,
} from "@/schemas/problem";

import {
  useCreateProblem,
} from "@/hooks/useAdminProblems";


export function AdminPage() {
  const {
    register,
    handleSubmit,
    reset,
  } = useForm<ProblemFormData>({
    resolver:
      zodResolver(problemSchema),
  });


  const {
    mutate,
    isPending,
  } = useCreateProblem();


  function submit(
    data: ProblemFormData,
  ) {
    mutate(
      {
        ...data,
        tags:
          data.tags
            ?.split(",")
            .map((tag) =>
              tag.trim(),
            ),
      },

      {
        onSuccess() {
          toast.success(
            "Problem created",
          );

          reset();
        },

        onError() {
          toast.error(
            "Failed creating problem",
          );
        },
      },
    );
  }


  return (
    <div className="max-w-3xl space-y-6">

      <h1 className="text-3xl font-bold">
        Admin Panel
      </h1>


      <form
        onSubmit={handleSubmit(submit)}
        className="space-y-4 rounded-2xl border border-border bg-card p-6"
      >

        <input
          {...register("title")}
          placeholder="Title"
          className="w-full rounded-xl border p-3"
        />


        <input
          {...register("slug")}
          placeholder="Slug"
          className="w-full rounded-xl border p-3"
        />


        <textarea
          {...register("description")}
          placeholder="Description"
          className="min-h-40 w-full rounded-xl border p-3"
        />


        <select
          {...register("difficulty")}
          className="w-full rounded-xl border p-3"
        >
          <option value="easy">
            Easy
          </option>

          <option value="medium">
            Medium
          </option>

          <option value="hard">
            Hard
          </option>

        </select>


        <input
          {...register("tags")}
          placeholder="Tags comma separated"
          className="w-full rounded-xl border p-3"
        />


        <button
          disabled={isPending}
          className="rounded-xl bg-primary px-6 py-3 text-primary-foreground"
        >
          {isPending
            ? "Creating..."
            : "Create Problem"}
        </button>

      </form>
      <ProblemManagement />

    </div>

  );
}