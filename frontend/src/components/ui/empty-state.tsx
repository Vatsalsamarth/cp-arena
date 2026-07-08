interface EmptyStateProps {
  title: string;
  description?: string;
}


export function EmptyState({
  title,
  description,
}: EmptyStateProps) {
  return (
    <div className="rounded-2xl border border-border bg-card p-8 text-center">

      <h2 className="text-xl font-semibold">
        {title}
      </h2>

      {description && (
        <p className="mt-2 text-muted-foreground">
          {description}
        </p>
      )}

    </div>
  );
}