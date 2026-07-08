import { useState } from "react";

import { toast } from "react-hot-toast";
import { useNavigate } from "react-router-dom";

import { login } from "@/api/auth";
import { useAuthStore } from "@/store/auth";

import { Button } from "@/components/ui/button";

export function LoginPage() {
  const navigate = useNavigate();

  const setToken = useAuthStore(
    (state) => state.setToken,
  );

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    try {
      setLoading(true);

      const response = await login({
        username,
        password,
      });

      setToken(response.access_token);

      toast.success("Login successful");

      navigate("/");
    } catch {
      toast.error("Invalid username or password");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-6">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md space-y-6 rounded-3xl border border-border bg-card p-8 shadow-xl"
      >
        <div className="space-y-2 text-center">
          <h1 className="text-3xl font-bold">
            Welcome Back
          </h1>

          <p className="text-muted-foreground">
            Login to CP Arena
          </p>
        </div>

        <input
          className="w-full rounded-xl border border-border bg-background px-4 py-3"
          placeholder="Username"
          value={username}
          onChange={(event) =>
            setUsername(event.target.value)
          }
        />

        <input
          className="w-full rounded-xl border border-border bg-background px-4 py-3"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(event) =>
            setPassword(event.target.value)
          }
        />

        <Button
          className="w-full"
          disabled={loading}
        >
          {loading ? "Logging in..." : "Login"}
        </Button>
      </form>
    </main>
  );
}