import { useSubmissions } from "@/hooks/useSubmissions";


function statusStyle(status: string) {
  switch (status) {
    case "accepted":
      return "text-green-500";

    case "wrong_answer":
      return "text-red-500";

    case "running":
      return "text-yellow-500";

    default:
      return "text-muted-foreground";
  }
}


export function SubmissionsPage() {
  const {
    data,
    isLoading,
  } = useSubmissions();


  if (isLoading) {
    return (
      <div>
        Loading submissions...
      </div>
    );
  }


  return (
    <div className="space-y-6">

      <h1 className="text-3xl font-bold">
        Submissions
      </h1>


      <div className="overflow-hidden rounded-2xl border border-border">

        <table className="w-full">

          <thead className="bg-muted">
            <tr>
              <th className="p-4 text-left">
                ID
              </th>

              <th className="p-4 text-left">
                Language
              </th>

              <th className="p-4 text-left">
                Status
              </th>

              <th className="p-4 text-left">
                Date
              </th>
            </tr>
          </thead>


          <tbody>
            {data?.items.map(
              (submission) => (
                <tr
                  key={submission.id}
                  className="border-t border-border"
                >
                  <td className="p-4">
                    {submission.id}
                  </td>

                  <td className="p-4">
                    {submission.language}
                  </td>

                  <td
                    className={`p-4 font-medium ${statusStyle(
                      submission.status,
                    )}`}
                  >
                    {submission.status}
                  </td>

                  <td className="p-4 text-sm text-muted-foreground">
                    {new Date(
                      submission.created_at,
                    ).toLocaleString()}
                  </td>

                </tr>
              ),
            )}
          </tbody>

        </table>

      </div>

    </div>
  );
}