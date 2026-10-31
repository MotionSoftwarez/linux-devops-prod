"use client";

import Link from "next/link";
import { useTheme, useAuth } from "@/components/providers";
import {
  Sun,
  Moon,
  Monitor,
  Search,
  Menu,
  LogOut,
  User,
  ChevronRight,
  AlertCircle,
} from "lucide-react";
import { useState } from "react";
import { useRouter } from "next/navigation";

export function Navbar() {
  const { theme, setTheme, resolved, toggle } = useTheme();
  const { user, login, logout, isAuthenticated } = useAuth();
  const router = useRouter();
  const [search, setSearch] = useState("");
  const [mobileMenu, setMobileMenu] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);
  const [loggingIn, setLoggingIn] = useState(false);

  function handleSearch(e?: React.FormEvent) {
    e?.preventDefault();
    const q = search.trim();
    if (!q) return;
    router.push(`/reference?q=${encodeURIComponent(q)}`);
    setSearch("");
  }

  function handleLogin() {
    setLoginError(null);
    setLoggingIn(true);
    fetch("/api/v1/auth/guest", { method: "POST" })
      .then((r) => {
        if (!r.ok) throw new Error("Guest login failed: " + r.status);
        return r.json();
      })
      .then((data) => {
        if (!data.access_token) throw new Error("No token received from server");
        login(data.access_token);
        router.push("/learn/ch01-introduction-to-linux-and-devops");
      })
      .catch((err: any) => {
        setLoginError(err.message || "Guest login failed. Please try again.");
        setLoggingIn(false);
      });
  }

  function handleLogout() {
    logout();
    router.push("/");
  }

  return (
    <header className="sticky top-0 z-20 border-b border-border bg-background/85 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-3">
          <button
            onClick={() => {
              document.documentElement.classList.toggle("sidebar-open");
            }}
            className="md:hidden p-2 text-muted-foreground hover:bg-accent rounded-md"
            aria-label="Toggle navigation"
          >
            <Menu className="h-5 w-5" />
          </button>
          <Link href="/" className="flex items-center gap-2">
            <Monitor className="h-6 w-6 text-primary" aria-hidden="true" />
            <span className="font-semibold tracking-tight">Linux<span className="text-muted-foreground">Tutor</span></span>
          </Link>
        </div>

        <div className="hidden md:flex items-center gap-1">
          <form onSubmit={handleSearch} className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" aria-hidden="true" />
            <input
              type="search"
              placeholder="Search commands…"
              className="pl-9 pr-3 py-1.5 text-sm border border-input rounded-md bg-input focus:ring-1 focus:ring-ring focus:border-transparent transition-colors w-64"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </form>
          <button
            onClick={toggle}
            className="p-2 text-muted-foreground hover:bg-accent rounded-md"
            aria-label={resolved === "dark" ? "Switch to light theme" : "Switch to dark theme"}
          >
            {resolved === "dark" ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            )}
          </button>
        </div>

        <div className="hidden md:flex items-center gap-3">
          {isAuthenticated ? (
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-secondary text-secondary-foreground text-sm">
              <User className="h-4 w-4" aria-hidden="true" />
              <span>{user?.username || "Guest"}</span>
              <button
                onClick={handleLogout}
                className="ml-2 p-1 text-muted-foreground hover:text-destructive"
                aria-label="Log out"
              >
                <LogOut className="h-4 w-4" />
              </button>
            </div>
          ) : (
            <>
              <Link
                href="/login"
                className="px-4 py-1.5 text-sm font-medium rounded-md border border-primary bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
              >
                Log in
              </Link>
              <button
                onClick={handleLogin}
                disabled={loggingIn}
                className={`px-4 py-1.5 text-sm font-medium rounded-md border border-input transition-colors ${
                  loggingIn ? "bg-secondary cursor-not-allowed" : "hover:bg-accent"
                }`}
              >
                {loggingIn ? "Signing in…" : "Explore as guest"}
              </button>
              {loginError && (
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-md border border-red-200 bg-red-50 text-red-700 text-sm">
                  <AlertCircle className="h-4 w-4" aria-hidden="true" />
                  <span>{loginError}</span>
                </div>
              )}
            </>
          )}
        </div>

        <button
          onClick={() => {
            document.documentElement.classList.toggle("sidebar-open");
          }}
          className="md:hidden p-2 text-muted-foreground hover:bg-accent rounded-md"
          aria-label="Toggle navigation"
        >
          <Menu className="h-5 w-5" />
        </button>
      </div>

      {mobileMenu && (
        <div className="fixed inset-0 z-[60] bg-background/95 backdrop-blur" onClick={() => setMobileMenu(false)}>
          <div className="absolute top-4 right-4">
            <button onClick={() => setMobileMenu(false)} className="p-2 text-muted-foreground hover:bg-accent rounded-md">
              <LogOut className="h-5 w-5" />
            </button>
          </div>
        </div>
      )}
    </header>
  );
}

