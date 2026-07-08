import { useLeaderboard } from "@/hooks/useLeaderboard";

export function LeaderboardPage() {
  const {
    data,
    isLoading,
  } = useLeaderboard();

  if (isLoading) {
    return (
      <div>
        Loading leaderboard...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">
        Leaderboard
      </h1>

      <div className="rounded-2xl border border-border">
        {data?.items.map((user) => (
          <div
            key={user.user_id}
            className="flex justify-between border-b border-border p-5"
          >
            <span>
              #{user.rank} {user.username}
            </span>

            <span>
              {user.score} solved
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}