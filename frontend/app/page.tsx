"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { useAuth } from "@/components/providers";
import { TypingTerminal, ProgressRing, type TermLine } from "@/components/fx";
import { Card, CardContent } from "@/components/ui/card";
import {
  Monitor,
  Terminal,
  BookOpen,
  Clock,
  ChevronRight,
  Sparkles,
  Rocket,
  CheckCircle2,
  Flame,
} from "lucide-react";

interface OutlineModule {
  key: string;
  title: string;
  stage: string | null;
  description: string | null;
  order: number;
  lessons: { slug: string; title: string }[];
}

const STAGE_META: Record<
  string,
  { label: string; blurb: string; c1: string; c2: string; icon: React.ReactNode }
> = {
  "1": {
    label: "Stage 1 · Linux Foundations",
    blurb: "The filesystem, first commands, reading & editing files",
    c1: "#3b82f6",
    c2: "#22d3ee",
    icon: <BookOpen className="h-5 w-5" />,
  },
  "2": {
    label: "Stage 2 · Linux Administration",
    blurb: "Permissions, users, processes, systemd, disks, SSH",
    c1: "#8b5cf6",
    c2: "#d946ef",
    icon: <Monitor className="h-5 w-5" />,
  },
  "3": {
    label: "Stage 3 · Linux for DevOps",
    blurb: "Bash, cron, secrets, Git, Docker, Nginx",
    c1: "#f59e0b",
    c2: "#ef4444",
    icon: <Terminal className="h-5 w-5" />,
  },
  "4": {
    label: "Stage 4 · Advanced Linux Engineering",
    blurb: "Hardening, troubleshooting, production scripts, boot",
    c1: "#10b981",
    c2: "#22d3ee",
    icon: <Sparkles className="h-5 w-5" />,
  },
  "5": {
    label: "Stage 5 · Production Capstone",
    blurb: "Investigate & repair a broken production app",
    c1: "#ef4444",
    c2: "#f472b6",
    icon: <Rocket className="h-5 w-5" />,
  },
};

const DEMO_SESSION: TermLine[] = [
  { prompt: true, text: "systemctl status nginx" },
  { out: true, text: "● nginx.service — A high performance web server (active)" },
  { prompt: true, text: "journalctl -u nginx --since '30 min ago' | grep -i error" },
  { out: true, text: "0 errors — all requests served in <120ms" },
  { prompt: true, text: "./deploy.sh production --canary" },
  { out: true, text: "✓ image pulled  ✓ migrated  ✓ healthcheck 80/80 — rollout complete" },
];

export default function Dashboard() {
  const { user, isAuthenticated } = useAuth();
  const [outline, setOutline] = useState<OutlineModule[]>([]);
  const [summary, setSummary] = useState<{ completed: number; total: number } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    api
      .get("/curriculum/outline")
      .then((d: OutlineModule[]) => !cancelled && setOutline(Array.isArray(d) ? d : []))
      .catch(() => {});
    if (isAuthenticated) {
      api
        .get("/progress/summary")
        .then((d: any) => !cancelled && setSummary(d))
        .catch(() => !cancelled && setSummary(null))
        .finally(() => !cancelled && setLoading(false));
    } else {
      setLoading(false);
    }
    return () => {
      cancelled = true;
    };
  }, [isAuthenticated]);

  const chapters = outline.length;
  const totalMinutes = chapters * 30;
  const completed = summary?.completed ?? 0;
  const percent = summary?.total ? Math.round((completed / summary.total) * 100) : 0;

  // next chapter to continue: completed + 1
  const nextIdx = Math.min(chapters - 1, completed);
  const nextChapter = outline[nextIdx]?.lessons[0];

  const stages = Array.from(new Set(outline.map((m) => String(m.stage ?? "0"))));

  return (
    <div className="space-y-10">
      {/* ================= HERO ================= */}
      <section className="hero-mesh border-b border-border">
        <div className="mx-auto max-w-6xl px-4 py-12 grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
          <div className="space-y-5">
            <div className="animate-fade-up inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
              <Flame className="h-3.5 w-3.5" />
              {chapters > 0 ? `${chapters} chapters · 5 stages · Completely hands-on` : "Loading course…"}
            </div>
            <h1 className="animate-fade-up delay-1 text-4xl sm:text-5xl font-extrabold tracking-tight leading-[1.08]">
              Master <span className="gradient-text">Linux for DevOps</span>
              <br />
              from zero to production
            </h1>
            <p className="animate-fade-up delay-2 max-w-xl text-muted-foreground text-base sm:text-lg">
              Not a wall of docs — a mission-driven course. Solve real incidents, run guided terminal
              workflows, and finish with a full production capstone. Every chapter is loaded with
              runnable commands, case studies, and assignments.
            </p>
            <div className="animate-fade-up delay-3 flex flex-wrap items-center gap-3">
              <Link
                href={nextChapter ? `/learn/${nextChapter.slug}` : "/learn/ch01-introduction-to-linux-and-devops"}
                className="group inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-blue-500 to-violet-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/25 transition-transform hover:scale-[1.03] active:scale-[0.98]"
              >
                {completed > 0 ? (
                  <>
                    <Rocket className="h-4 w-4" /> Continue · Chapter {nextChapter?.slug?.slice(2, 4) ?? "01"}
                  </>
                ) : (
                  <>
                    <Terminal className="h-4 w-4" /> Start Chapter 1 — it&apos;s free
                  </>
                )}
                <ChevronRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Link>
              <Link
                href="/reference"
                className="inline-flex items-center gap-2 rounded-lg border border-border px-5 py-2.5 text-sm font-medium hover:bg-accent transition-colors"
              >
                <BookOpen className="h-4 w-4" /> Cheat sheets
              </Link>
              {!isAuthenticated && (
                <Link href="/login" className="text-sm text-muted-foreground underline-offset-4 hover:text-foreground hover:underline">
                  or create an account →
                </Link>
              )}
            </div>
            <div className="animate-fade-up delay-4 flex flex-wrap gap-x-6 gap-y-2 pt-2 text-xs text-muted-foreground">
              <span className="inline-flex items-center gap-1.5">
                <Clock className="h-3.5 w-3.5" /> ~{Math.round(totalMinutes / 60)} hours of material
              </span>
              <span className="inline-flex items-center gap-1.5">
                <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> Track progress chapter by chapter
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Sparkles className="h-3.5 w-3.5 text-amber-500" /> Real-world case studies in every chapter
              </span>
            </div>
          </div>

          {/* Animated terminal */}
          <div className="animate-fade-up delay-2 animate-float">
            <TypingTerminal lines={DEMO_SESSION} />
            <p className="mt-3 text-center text-xs text-muted-foreground">
              What DevOps work looks like — you&apos;ll write every line of it yourself.
            </p>
          </div>
        </div>
      </section>

      {/* ================= PROGRESS + STAGES ================= */}
      <section className="mx-auto max-w-6xl px-4 space-y-8">
        {/* Progress row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="glass hover-lift md:col-span-1">
            <CardContent className="flex items-center gap-5 p-6">
              <ProgressRing
                percent={percent}
                label={isAuthenticated ? `${percent}%` : "—"}
                sublabel={isAuthenticated ? "Course" : "Guest"}
              />
              <div className="space-y-1.5">
                <p className="text-sm font-semibold">
                  {isAuthenticated ? "Your progress" : "You're browsing as guest"}
                </p>
                <p className="text-xs text-muted-foreground">
                  {isAuthenticated
                    ? `${completed} of ${summary?.total ?? chapters} chapters completed`
                    : "Sign in or go guest to start tracking progress"}
                </p>
                {!isAuthenticated && (
                  <Link href="/login" className="inline-block text-xs font-medium text-primary hover:underline">
                    Log in →
                  </Link>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Stat chips */}
          <Card className="glass hover-lift md:col-span-2">
            <CardContent className="p-6 grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
              {[
                { v: chapters || "—", l: "Chapters", icon: <BookOpen className="h-4 w-4 text-blue-500" /> },
                { v: "5", l: "Stages", icon: <Rocket className="h-4 w-4 text-violet-500" /> },
                { v: `${Math.round(totalMinutes / 60)}h`, l: "Material", icon: <Clock className="h-4 w-4 text-amber-500" /> },
                { v: completed > 0 ? `+${completed}` : "0", l: "Completed", icon: <CheckCircle2 className="h-4 w-4 text-emerald-500" /> },
              ].map((s, i) => (
                <div key={i} className="animate-fade-up rounded-xl border border-border/70 bg-background/40 p-4 hover-lift" style={{ animationDelay: `${i * 80}ms` }}>
                  <div className="flex items-center justify-center gap-1.5 text-2xl font-bold">
                    {s.icon}
                    {s.v}
                  </div>
                  <div className="mt-1 text-[11px] uppercase tracking-wider text-muted-foreground">{s.l}</div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Stage cards */}
        <div>
          <h2 className="text-lg font-bold tracking-tight mb-4 flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-amber-500" /> Your learning roadmap
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {stages.map((stage, i) => {
              const meta = STAGE_META[stage] ?? STAGE_META["1"];
              const stageChapters = outline.filter((m) => String(m.stage ?? "0") === stage);
              const first = stageChapters[0]?.lessons[0];
              return (
                <Link key={stage} href={first ? `/learn/${first.slug}` : "/"} className="group animate-fade-up" style={{ animationDelay: `${i * 90}ms` }}>
                  <Card className={cn2("h-full border-transparent", "hover-lift")}>
                    <CardContent className="p-5 relative overflow-hidden">
                      <div
                        className="absolute -right-10 -top-10 h-28 w-28 rounded-full opacity-20 blur-2xl transition-opacity group-hover:opacity-40"
                        style={{ background: `linear-gradient(135deg, ${meta.c1}, ${meta.c2})` }}
                      />
                      <div className="flex items-start gap-3">
                        <span
                          className="stage-badge flex h-10 w-10 shrink-0 items-center justify-center rounded-xl"
                          style={{ ["--s1" as any]: meta.c1, ["--s2" as any]: meta.c2 }}
                        >
                          {meta.icon}
                        </span>
                        <div>
                          <p className="text-sm font-semibold leading-tight">{meta.label}</p>
                          <p className="mt-1 text-xs text-muted-foreground">{meta.blurb}</p>
                        </div>
                      </div>
                      <div className="mt-4 flex items-center justify-between text-xs">
                        <span className="rounded-full bg-muted px-2.5 py-1 font-medium tabular-nums">
                          Chapters {stageChapters.map((m) => m.key.replace("chapter-", "")).join(", ")}
                        </span>
                        <ChevronRight className="h-4 w-4 text-muted-foreground transition-transform group-hover:translate-x-1 group-hover:text-foreground" />
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Chapter grid */}
        <div>
          <h2 className="text-lg font-bold tracking-tight mb-4 flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-blue-500" /> All chapters
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {outline.map((m, i) => {
              const no = m.key?.replace("chapter-", "") ?? String(i + 1);
              const lesson = m.lessons[0];
              if (!lesson) return null;
              const stageMeta = STAGE_META[String(m.stage ?? "0")] ?? STAGE_META["1"];
              const isNext = nextChapter?.slug === lesson.slug && completed > 0;
              return (
                <Link key={m.key} href={`/learn/${lesson.slug}`} className="group animate-fade-up" style={{ animationDelay: `${Math.min(i, 12) * 50}ms` }}>
                  <div
                    className={cn2(
                      "hover-lift flex items-center gap-3 rounded-xl border border-border bg-card p-3.5",
                      isNext && "animate-glow border-primary/50"
                    )}
                  >
                    <span
                      className="flex h-8 min-w-8 items-center justify-center rounded-lg text-xs font-bold text-white tabular-nums"
                      style={{ background: `linear-gradient(135deg, ${stageMeta.c1}, ${stageMeta.c2})` }}
                    >
                      {no}
                    </span>
                    <div className="min-w-0">
                      <p className="truncate text-sm font-medium group-hover:text-primary transition-colors">
                        {lesson.title}
                      </p>
                      <p className="text-[11px] text-muted-foreground">{stageMeta.label.split("·")[1]?.trim()}</p>
                    </div>
                    {isNext && <span className="ml-auto shrink-0 rounded-full bg-primary/10 px-2 py-0.5 text-[10px] font-semibold text-primary">NEXT</span>}
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>
    </div>
  );
}

function cn2(...cls: (string | false | undefined)[]) {
  return cls.filter(Boolean).join(" ");
}
