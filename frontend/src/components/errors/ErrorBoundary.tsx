import {
  Component,
  type ErrorInfo,
  type ReactNode,
} from "react";

import { Button } from "@/components/ui/button";


interface Props {
  children: ReactNode;
}


interface State {
  hasError: boolean;
}


export class ErrorBoundary extends Component<
  Props,
  State
> {
  state: State = {
    hasError: false,
  };


  static getDerivedStateFromError() {
    return {
      hasError: true,
    };
  }


  componentDidCatch(
    error: Error,
    info: ErrorInfo,
  ) {
    console.error(
      "Application error:",
      error,
      info,
    );
  }


  render() {
    if (this.state.hasError) {
      return (
        <main className="flex min-h-screen items-center justify-center p-6">
          <section className="space-y-4 rounded-2xl border border-border bg-card p-8 text-center">

            <h1 className="text-3xl font-bold">
              Something went wrong
            </h1>

            <p className="text-muted-foreground">
              Please refresh and try again.
            </p>

            <Button
              onClick={() =>
                window.location.reload()
              }
            >
              Reload
            </Button>

          </section>
        </main>
      );
    }


    return this.props.children;
  }
}