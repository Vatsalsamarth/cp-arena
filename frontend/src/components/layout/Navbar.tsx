import { LogOut } from "lucide-react";

import { useAuth } from "@/hooks/useAuth";

import { Button } from "@/components/ui/button";

export function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-card px-6">
      <div>
        <h1 className="text-xl font-bold">
          CP Arena
        </h1>
      </div>

      <div className="flex items-center gap-4">
        <span className="text-sm text-muted-foreground">
          {user?.username ?? "User"}
        </span>

        <Button
          variant="outline"
          size="sm"
          onClick={logout}
        >
          <LogOut className="mr-2 h-4 w-4" />
          Logout
        </Button>
      </div>
    </header>
  );
}