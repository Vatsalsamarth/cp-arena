import { Button } from "@/components/ui/button";

function App() {
  return (
    <main className="dark min-h-screen bg-background text-foreground">
      <div className="mx-auto flex min-h-screen max-w-7xl items-center justify-center px-6">
        <section className="w-full max-w-xl rounded-3xl border border-border bg-card p-10 shadow-2xl">
          <div className="space-y-6 text-center">
            <span className="inline-flex rounded-full border border-border bg-muted px-3 py-1 text-xs font-medium tracking-wide">
              CP Arena
            </span>

            <h1 className="text-5xl font-bold tracking-tight">
              Competitive Programming,
              <br />
              Reimagined.
            </h1>

            <p className="text-muted-foreground">
              A premium competitive programming platform built for speed,
              learning, contests, and developer experience.
            </p>

            <Button size="lg">
              Frontend Foundation Complete
            </Button>
          </div>
        </section>
      </div>
    </main>
  );
}

export default App;