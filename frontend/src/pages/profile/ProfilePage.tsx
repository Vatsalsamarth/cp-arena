import { useAuth } from "@/hooks/useAuth";
import { useUserStats } from "@/hooks/useUserStats";


export function ProfilePage() {
  const {
    user,
  } = useAuth();

  const {
    data: stats,
  } = useUserStats();


  return (
    <div className="space-y-6">

      <section>
        <h1 className="text-3xl font-bold">
          Profile
        </h1>

        <p className="text-muted-foreground">
          {user?.username}
        </p>
      </section>


      <section className="grid gap-6 md:grid-cols-3">

        <div className="rounded-2xl border border-border bg-card p-6">
          Solved
          <p className="mt-3 text-3xl font-bold">
            {stats?.solved_count ?? 0}
          </p>
        </div>


        <div className="rounded-2xl border border-border bg-card p-6">
          Submissions
          <p className="mt-3 text-3xl font-bold">
            {stats?.submission_count ?? 0}
          </p>
        </div>


        <div className="rounded-2xl border border-border bg-card p-6">
          Success Rate
          <p className="mt-3 text-3xl font-bold">
            {stats?.success_rate ?? 0}%
          </p>
        </div>

      </section>

    </div>
  );
}