import { useAuth } from "@/hooks/useAuth";
import { useUserStats } from "@/hooks/useUserStats";

export function ProfilePage() {
  const { user } = useAuth();

  const { data: stats } = useUserStats();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold">Profile</h1>

        <p className="text-muted-foreground">
          {user?.username}
        </p>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        <div className="rounded-2xl border border-border bg-card p-6">
          <p className="text-sm text-muted-foreground">
            Accepted
          </p>

          <p className="mt-3 text-3xl font-bold">
            {stats?.accepted ?? 0}
          </p>
        </div>

        <div className="rounded-2xl border border-border bg-card p-6">
          <p className="text-sm text-muted-foreground">
            Total Submissions
          </p>

          <p className="mt-3 text-3xl font-bold">
            {stats?.total_submissions ?? 0}
          </p>
        </div>

        <div className="rounded-2xl border border-border bg-card p-6">
          <p className="text-sm text-muted-foreground">
            Acceptance Rate
          </p>

          <p className="mt-3 text-3xl font-bold">
            {stats?.acceptance_rate ?? 0}%
          </p>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-2">
        <div className="rounded-2xl border border-border bg-card p-6">
          <p className="text-sm text-muted-foreground">
            Wrong Answers
          </p>

          <p className="mt-3 text-3xl font-bold">
            {stats?.wrong_answer ?? 0}
          </p>
        </div>

        <div className="rounded-2xl border border-border bg-card p-6">
          <p className="text-sm text-muted-foreground">
            Runtime / Compilation Errors
          </p>

          <p className="mt-3 text-3xl font-bold">
            {(stats?.runtime_error ?? 0) + (stats?.compilation_error ?? 0)}
          </p>
        </div>
      </section>
    </div>
  );
}