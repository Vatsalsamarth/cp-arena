import { useUserStats } from "@/hooks/useUserStats";

export function DashboardPage() {
  const {
    data: stats,
    isLoading,
  } = useUserStats();


  if (isLoading) {
    return (
      <div>
        Loading dashboard...
      </div>
    );
  }


  return (
    <div className="space-y-8">

      <section>
        <h1 className="text-3xl font-bold">
          Dashboard
        </h1>

        <p className="mt-2 text-muted-foreground">
          Track your competitive programming progress.
        </p>
      </section>


      <section className="grid gap-6 md:grid-cols-4">

        <div className="rounded-2xl border border-border bg-card p-6">
          <p className="text-sm text-muted-foreground">
            Problems Solved
          </p>

          <p className="mt-3 text-4xl font-bold">
            {stats?.solved_count ?? 0}
          </p>
        </div>


        <div className="rounded-2xl border border-border bg-card p-6">
          <p className="text-sm text-muted-foreground">
            Submissions
          </p>

          <p className="mt-3 text-4xl font-bold">
            {stats?.submission_count ?? 0}
          </p>
        </div>


        <div className="rounded-2xl border border-border bg-card p-6">
          <p className="text-sm text-muted-foreground">
            Accepted
          </p>

          <p className="mt-3 text-4xl font-bold">
            {stats?.accepted_count ?? 0}
          </p>
        </div>


        <div className="rounded-2xl border border-border bg-card p-6">
          <p className="text-sm text-muted-foreground">
            Success Rate
          </p>

          <p className="mt-3 text-4xl font-bold">
            {stats?.success_rate ?? 0}%
          </p>
        </div>

      </section>


      <section className="rounded-2xl border border-border bg-card p-6">
        <h2 className="text-xl font-semibold">
          Recent Activity
        </h2>

        <p className="mt-3 text-muted-foreground">
          Submission history and activity tracking will appear here.
        </p>
      </section>

    </div>
  );
}