import type {
  SubmissionStatus,
} from "@/types/submission";


interface Props {
  status: SubmissionStatus;
}


const labels = {
  pending: "Pending",
  running: "Running",
  accepted: "Accepted",
  wrong_answer: "Wrong Answer",
  failed: "Failed",
};


export function VerdictBadge({
  status,
}: Props) {
  return (
    <span className="rounded-full bg-muted px-4 py-2 text-sm font-medium">
      {labels[status]}
    </span>
  );
}