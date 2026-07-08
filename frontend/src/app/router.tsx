import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { Button } from "@/components/ui/button";

function HomePage() {
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
              Production routing is now configured.
            </p>

            <Button size="lg">
              Router Ready
            </Button>
          </div>
        </section>
      </div>
    </main>
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}