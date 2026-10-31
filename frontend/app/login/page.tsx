"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/providers";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Monitor, AlertCircle, User, KeyRound } from "lucide-react";

const FIRST_LESSON = "/learn/ch01-introduction-to-linux-and-devops";

export default function LoginPage() {
  const router = useRouter();
  const { login, logout, isAuthenticated, user } = useAuth();
  const [mode, setMode] = useState<"signin" | "register">("signin");

  // form fields
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  if (isAuthenticated) {
    return (
      <div className="mx-auto max-w-md px-4 py-16">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm font-semibold">
              <KeyRound className="h-4 w-4" /> You are already signed in
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Signed in as <span className="font-medium text-foreground">{user?.username}</span>.
            </p>
            <Link
              href={FIRST_LESSON}
              className="block w-full rounded-md bg-primary py-2 text-center text-sm font-medium text-primary-foreground hover:bg-primary/90"
            >
              Continue learning — Chapter 1
            </Link>
            <button
              onClick={() => {
                logout();
                setMode("signin");
                setUsername("");
                setPassword("");
                setEmail("");
              }}
              className="block w-full rounded-md border border-input py-2 text-center text-sm font-medium hover:bg-accent"
            >
              Sign out
            </button>
          </CardContent>
        </Card>
      </div>
    );
  }

  async function doGuest() {
    setError(null);
    setBusy("guest");
    try {
      const res = await fetch("/api/v1/auth/guest", { method: "POST" });
      if (!res.ok) throw new Error("Guest sign-in failed (" + res.status + ")");
      const data = await res.json();
      if (!data.access_token) throw new Error("No token received from server");
      login(data.access_token);
      router.push(FIRST_LESSON);
    } catch (e: any) {
      setError(e.message || "Could not sign in as guest");
      setBusy(null);
    }
  }

  async function doSignIn(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy("signin");
    try {
      const res = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail || "Incorrect username or password");
      }
      const data = await res.json();
      login(data.access_token);
      router.push(FIRST_LESSON);
    } catch (e: any) {
      setError(e.message || "Login failed");
      setBusy(null);
    }
  }

  async function doRegister(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy("register");
    try {
      const res = await fetch("/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password, full_name: "", learning_goal: "" }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail || "Registration failed");
      }
      // auto sign-in with the same credentials
      const res2 = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (!res2.ok) throw new Error("Registration succeeded but auto sign-in failed; go back and sign in manually.");
      const data = await res2.json();
      login(data.access_token);
      router.push(FIRST_LESSON);
    } catch (e: any) {
      setError(e.message || "Registration failed");
      setBusy(null);
    }
  }

  return (
    <div className="mx-auto max-w-md px-4 py-12 space-y-6">
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2">
            <Monitor className="h-5 w-5 text-primary" aria-hidden="true" />
            Sign in to Linux for DevOps
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && (
            <div className="flex items-start gap-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700 dark:border-red-800 dark:bg-red-950 dark:text-red-300">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Tabs */}
          <div className="grid grid-cols-2 gap-1 rounded-md border border-border p-1">
            {(["signin", "register"] as const).map((m) => (
              <button
                key={m}
                onClick={() => {
                  setMode(m);
                  setError(null);
                  setBusy(null);
                }}
                className={
                  "rounded px-3 py-1.5 text-sm font-medium transition-colors " +
                  (mode === m ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-accent")
                }
              >
                {m === "signin" ? "Sign in" : "Create account"}
              </button>
            ))}
          </div>

          <form onSubmit={mode === "signin" ? doSignIn : doRegister} className="space-y-3">
            <div>
              <label htmlFor="username" className="mb-1 block text-xs font-medium text-muted-foreground">
                Username
              </label>
              <input
                id="username"
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-ring"
              />
            </div>
            {mode === "register" && (
              <div>
                <label htmlFor="email" className="mb-1 block text-xs font-medium text-muted-foreground">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-ring"
                />
              </div>
            )}
            <div>
              <label htmlFor="password" className="mb-1 block text-xs font-medium text-muted-foreground">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-ring"
              />
            </div>
            <button
              type="submit"
              disabled={!!busy}
              className="w-full rounded-md bg-primary py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:bg-secondary disabled:text-muted-foreground"
            >
              {busy === "signin" && mode === "signin"
                ? "Signing in…"
                : busy === "register"
                  ? "Creating account…"
                  : mode === "signin"
                    ? "Sign in"
                    : "Create account & continue"}
            </button>
          </form>

          <div className="flex items-center gap-3">
            <div className="h-px flex-1 bg-border" />
            <span className="text-xs text-muted-foreground">or</span>
            <div className="h-px flex-1 bg-border" />
          </div>

          <button
            onClick={doGuest}
            disabled={!!busy}
            className="inline-flex w-full items-center justify-center gap-2 rounded-md border border-input py-2 text-sm font-medium hover:bg-accent disabled:bg-secondary disabled:text-muted-foreground"
          >
            <User className="h-4 w-4" />
            {busy === "guest" ? "Creating guest session…" : "Explore as guest (no account needed)"}
          </button>

          <p className="rounded-md bg-muted p-2.5 text-xs text-muted-foreground">
            <span className="font-medium text-foreground">Demo account:</span> username{" "}
            <code className="rounded bg-input px-1 py-0.5">demo</code> · password{" "}
            <code className="rounded bg-input px-1 py-0.5">demo123</code>
          </p>
        </CardContent>
      </Card>

      <p className="text-center text-xs text-muted-foreground">
        Guest progress is stored locally and won&apos;t persist across devices. Creating a free account saves
        your progress on the server.
      </p>
    </div>
  );
}
