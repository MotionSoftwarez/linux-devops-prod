"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";

type Theme = "light" | "dark" | "system";

interface ThemeContextType {
  theme: Theme;
  setTheme: (t: Theme) => void;
  resolved: "light" | "dark";
  toggle: () => void;
}

interface AuthContextType {
  user: any | null;
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<Theme>("system");
  const [resolved, setResolved] = useState<"light" | "dark">("light");

  useEffect(() => {
    if (typeof window === "undefined") return;
    const stored = localStorage.getItem("lt_theme") as Theme | null;
    if (stored) setThemeState(stored);
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const root = window.document.documentElement;
    const resolve = () => {
      let t = theme;
      if (t === "system") {
        t = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      }
      if (t === "dark") {
        root.classList.add("dark");
        setResolved("dark");
        localStorage.setItem("lt_theme", "dark");
      } else {
        root.classList.remove("dark");
        setResolved("light");
        localStorage.setItem("lt_theme", "light");
      }
    };
    resolve();
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    mq.addEventListener("change", resolve);
    return () => mq.removeEventListener("change", resolve);
  }, [theme]);

  const setTheme = (t: Theme) => setThemeState(t);
  const toggle = () => setThemeState((prev) => (prev === "dark" ? "light" : "dark"));

  return (
    <ThemeContext.Provider value={{ theme, setTheme, resolved, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<any | null>(null);
  const [token, setTokenState] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const stored = localStorage.getItem("lt_token");
    if (stored) setTokenState(stored);
  }, []);

  const login = (t: string) => {
    setTokenState(t);
    localStorage.setItem("lt_token", t);
  };

  const logout = () => {
    setUser(null);
    setTokenState(null);
    if (typeof window !== "undefined") {
      localStorage.removeItem("lt_token");
    }
  };

  const isAuthenticated = !!token;

  // Load user profile when a token exists
  useEffect(() => {
    if (!token) return;
    fetch("/api/v1/auth/me", { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => data && setUser(data))
      .catch(() => {});
  }, [token]);

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};

// Combined client provider wrapper for use inside server layouts
export function ClientProviders({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      <ThemeProvider>{children}</ThemeProvider>
    </AuthProvider>
  );
}
