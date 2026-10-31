"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ChevronRight, BookOpen, Terminal, CheckCircle2 } from "lucide-react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

interface OutlineLesson {
  slug: string;
  title: string;
  order: number;
}

interface OutlineModule {
  key: string;
  title: string;
  stage: string | null;
  description: string | null;
  order: number;
  lessons: OutlineLesson[];
}

const STAGE_LABELS: Record<string, string> = {
  "1": "Stage 1 · Linux Foundations",
  "2": "Stage 2 · Linux Administration",
  "3": "Stage 3 · Linux for DevOps",
  "4": "Stage 4 · Advanced Linux Engineering",
  "5": "Stage 5 · Production Capstone",
};

export function Sidebar({ currentSlug }: { currentSlug?: string }) {
  const [modules, setModules] = useState<OutlineModule[]>([]);
  const [openStages, setOpenStages] = useState<Set<string>>(new Set(["1", "2", "3", "4", "5"]));
  const [mobileOpen, setMobileOpen] = useState(false);

  // Follow the navbar hamburger which toggles `sidebar-open` on <html>
  useEffect(() => {
    const check = () => setMobileOpen(document.documentElement.classList.contains("sidebar-open"));
    check();
    const observer = new MutationObserver(check);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    let cancelled = false;
    api
      .get("/curriculum/outline")
      .then((data: OutlineModule[]) => {
        if (!cancelled) setModules(Array.isArray(data) ? data : []);
      })
      .catch(() => {});

    // Ensure the stage containing the current lesson is expanded
    if (currentSlug) {
      const mod = modules.find((m) => m.lessons.some((l) => l.slug === currentSlug));
      if (mod?.stage) {
        setOpenStages((prev) => new Set(prev).add(mod.stage as string));
      }
    }
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Expand stage of current slug when it changes
  useEffect(() => {
    if (!currentSlug) return;
    const mod = modules.find((m) => m.lessons.some((l) => l.slug === currentSlug));
    if (mod?.stage) {
      setOpenStages((prev) => (prev.has(mod.stage as string) ? prev : new Set(prev).add(mod.stage as string)));
    }
  }, [currentSlug, modules]);

  const toggleStage = (stage: string) => {
    setOpenStages((prev) => {
      const next = new Set(prev);
      if (next.has(stage)) next.delete(stage);
      else next.add(stage);
      return next;
    });
  };

  const stages = Array.from(new Set(modules.map((m) => m.stage || "0")));

  return (
    <aside
      className={cn(
        "fixed left-0 top-16 bottom-0 w-64 border-r border-border bg-card z-40 transform transition-transform duration-200 ease-in-out md:relative md:translate-x-0 md:flex md:flex-col",
        mobileOpen ? "translate-x-0" : "-translate-x-full"
      )}
      aria-label="Syllabus navigation"
    >
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        <div className="flex items-center gap-2 px-2 py-2 text-xs font-medium text-muted-foreground uppercase tracking-wider">
          <BookOpen className="h-4 w-4" aria-hidden="true" />
          Syllabus · 25 chapters
        </div>

        {stages.map((stage) => {
          const stageModules = modules.filter((m) => (m.stage || "0") === stage);
          const isOpen = openStages.has(stage);
          return (
            <div key={stage} className="space-y-1">
              <button
                onClick={() => toggleStage(stage)}
                className="flex w-full items-center gap-2 px-2 py-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground hover:text-foreground transition-colors"
                aria-expanded={isOpen}
              >
                <ChevronRight
                  className={cn("h-3.5 w-3.5 transition-transform duration-200", isOpen ? "rotate-90" : "")}
                  aria-hidden="true"
                />
                {STAGE_LABELS[stage] || `Stage ${stage}`}
              </button>
              {isOpen && (
                <div className="space-y-0.5">
                  {stageModules.map((m) => {
                    const lesson = m.lessons[0];
                    if (!lesson) return null;
                    const chapNo = m.key.replace("chapter-", "");
                    const isActive = lesson.slug === currentSlug;
                    return (
                      <Link
                        key={m.key}
                        href={`/learn/${lesson.slug}`}
                        onClick={() => {
                          document.documentElement.classList.remove("sidebar-open");
                        }}
                        className={cn(
                          "flex items-start gap-2 px-2 py-1.5 text-sm rounded-md transition-colors",
                          isActive
                            ? "bg-primary text-primary-foreground font-medium"
                            : "text-muted-foreground hover:bg-accent hover:text-foreground"
                        )}
                      >
                        <span
                          className={cn(
                            "mt-0.5 inline-flex h-5 min-w-5 shrink-0 items-center justify-center rounded text-[10px] font-mono",
                            isActive ? "bg-primary-foreground/20" : "bg-muted"
                          )}
                        >
                          {chapNo}
                        </span>
                        <span className="leading-snug">
                          {lesson.title}
                        </span>
                        {isActive && (
                          <CheckCircle2 className="h-3.5 w-3.5 ml-auto mt-1 shrink-0" aria-hidden="true" />
                        )}
                      </Link>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}

        <div className="pt-3 border-t border-border">
          <Link
            href="/reference"
            className="flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-primary hover:bg-accent rounded-lg transition-colors"
          >
            <Terminal className="h-4 w-4" aria-hidden="true" />
            Cheat Sheets
          </Link>
        </div>
      </div>
    </aside>
  );
}
