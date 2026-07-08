export function DashboardPage() {
  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold">
          Dashboard
        </h1>

        <p className="mt-2 text-muted-foreground">
          Welcome to CP Arena. Track your progress,
          solve problems, and improve your ranking.
        </p>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        <div className="rounded-2xl border border-border bg-card p-6">
          <h2 className="text-sm text-muted-foreground">
            Problems Solved
          </h2>

          <p className="mt-3 text-4xl font-bold">
            0
          </p>
        </div>

        <div className="rounded-2xl border border-border bg-card p-6">
          <h2 className="text-sm text-muted-foreground">
            Submissions
          </h2>

          <p className="mt-3 text-4xl font-bold">
            0
          </p>
        </div>

        <div className="rounded-2xl border border-border bg-card p-6">
          <h2 className="text-sm text-muted-foreground">
            Rank
          </h2>

          <p className="mt-3 text-4xl font-bold">
            -
          </p>
        </div>
      </section>
    </div>
  );
}