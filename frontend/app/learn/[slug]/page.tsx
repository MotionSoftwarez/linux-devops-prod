"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { useParams } from "next/navigation";
import { useAuth } from "@/components/providers";
import { Card, CardContent } from "@/components/ui/card";
import { Confetti, ReadingProgress, CodeCopyButtons } from "@/components/fx";
import { ChapterAnimations } from "@/components/anims";
import {
  CheckCircle2,
  Clock,
  ChevronLeft,
  ChevronRight,
  BookOpen,
  AlertCircle,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface OutlineModule {
  key: string;
  title: string;
  stage: string | null;
  description?: string | null;
  order: number;
  lessons: { slug: string; title: string }[];
}

const STAGE_LABELS: Record<string, string> = {
  "1": "Stage 1 · Linux Foundations",
  "2": "Stage 2 · Linux Administration",
  "3": "Stage 3 · Linux for DevOps",
  "4": "Stage 4 · Advanced Linux Engineering",
  "5": "Stage 5 · Production Capstone",
};

interface NavEntry {
  slug: string;
  title: string;
  chapter: string;
  stage: string;
}

export default function LessonPage() {
  const params = useParams<{ slug: string }>();
  const slug = params?.slug as string;
  const { user, isAuthenticated } = useAuth();
  const [lesson, setLesson] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [chapterList, setChapterList] = useState<NavEntry[]>([]);
  const [markDone, setMarkDone] = useState(false);
  const [confettiTick, setConfettiTick] = useState(0);
  const [feedback, setFeedback] = useState<{ ok: boolean; text: string } | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setNotFound(false);
    setMarkDone(false);
    setFeedback(null);

    api
      .get(`/curriculum/lessons/${slug}`)
      .then((data: any) => {
        if (!cancelled) setLesson(data);
      })
      .catch(() => {
        if (!cancelled) setNotFound(true);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    api
      .get("/curriculum/outline")
      .then((mods: OutlineModule[]) => {
        if (cancelled || !Array.isArray(mods)) return;
        const entries: NavEntry[] = [];
        mods
          .slice()
          .sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
          .forEach((m) => {
            const no = m.key?.replace("chapter-", "") ?? "?";
            m.lessons.forEach((l) =>
              entries.push({ slug: l.slug, title: l.title, chapter: no, stage: m.stage || "" })
            );
          });
        setChapterList(entries);
      })
      .catch(() => {});

    // If logged in, fetch existing progress for this lesson
    if (localStorage.getItem("lt_token")) {
      api
        .get(`/curriculum/lessons/${slug}/progress`)
        .then((p: any) => {
          if (!cancelled && p && p.status === "completed") setMarkDone(true);
        })
        .catch(() => {});
    }

    return () => {
      cancelled = true;
    };
  }, [slug]);

  const idx = chapterList.findIndex((c) => c.slug === slug);
  const prev = idx > 0 ? chapterList[idx - 1] : null;
  const next = idx >= 0 && idx < chapterList.length - 1 ? chapterList[idx + 1] : null;

  const markComplete = () => {
    if (!isAuthenticated) {
      setFeedback({ ok: false, text: "Log in (guest works too) to save your progress." });
      return;
    }
    api
      .post(`/progress/lessons/${slug}`, { status: "completed" })
      .then(() => {
        setMarkDone(true);
        setConfettiTick((t) => t + 1);
        setFeedback({ ok: true, text: "🎉 Progress saved — chapter marked as completed!" });
      })
      .catch(() => {
        setFeedback({ ok: false, text: "Could not save progress. Try again." });
      });
  };

  // ---- early returns (all hooks above) ----
  if (loading) {
    return <div className="p-8 text-muted-foreground">Loading chapter…</div>;
  }
  if (notFound || !lesson) {
    return (
      <div className="p-8 space-y-3">
        <h1 className="text-xl font-semibold">Chapter not found</h1>
        <p className="text-muted-foreground">
          This chapter does not exist. Open{" "}
          <Link href="/learn/ch01-introduction-to-linux-and-devops" className="text-primary underline">
            Chapter 1
          </Link>{" "}
          to return to the course.
        </p>
      </div>
    );
  }

  let sections: any[] = [];
  try {
    const parsed = typeof lesson.content === "string" ? JSON.parse(lesson.content) : lesson.content;
    sections = parsed?.sections || [];
  } catch {
    sections = [];
  }

  const stageLabel =
    STAGE_LABELS[chapterList[idx]?.stage ?? ""] ?? "";

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 space-y-6">
      <ReadingProgress />
      <Confetti trigger={confettiTick} />
      {/* Header */}
      <header className="space-y-2 animate-fade-up">
        <div className="flex items-center gap-2 text-xs uppercase tracking-wider text-muted-foreground">
          <BookOpen className="h-3.5 w-3.5" aria-hidden="true" />
          {stageLabel && <span>{stageLabel}</span>}
          <span className="inline-flex items-center gap-1 rounded border border-border px-1.5">
            <Clock className="h-3 w-3" /> {lesson.estimated_minutes} min
          </span>
          <span className="rounded border border-border px-1.5 capitalize">{lesson.difficulty}</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight">{lesson.title}</h1>
        {lesson.summary && <p className="text-muted-foreground">{lesson.summary}</p>}
      </header>

      {/* Progress bar */}
      <div className="flex items-center gap-3">
        {markDone ? (
          <span className="inline-flex items-center gap-1.5 text-sm text-green-600 dark:text-green-400 font-medium">
            <CheckCircle2 className="h-4 w-4" /> Chapter completed
          </span>
        ) : (
          <button
            onClick={markComplete}
            className="inline-flex items-center gap-1.5 rounded-md border border-border px-3 py-1.5 text-sm font-medium hover:bg-accent transition-colors"
          >
            <CheckCircle2 className="h-4 w-4" /> Mark chapter as complete
          </button>
        )}
      </div>
      {feedback && (
        <div
          className={cn(
            "rounded-md border p-3 text-sm",
            feedback.ok
              ? "border-green-200 bg-green-50 text-green-800 dark:border-green-800 dark:bg-green-950 dark:text-green-300"
              : "border-amber-200 bg-amber-50 text-amber-800 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-300"
          )}
        >
          {feedback.text}
        </div>
      )}

      {/* Imported rich chapter content */}
      <Card className="animate-fade-up delay-1">
        <CardContent className="pt-6">
          {sections.map((section, i) =>
            section.type === "html" ? (
              <div
                key={i}
                className="lesson-content"
                dangerouslySetInnerHTML={{ __html: section.content }}
              />
            ) : (
              <div key={i} className="whitespace-pre-wrap text-sm">
                {section.content}
              </div>
            )
          )}
        </CardContent>
      </Card>
      <CodeCopyButtons />

      {/* Animated concept demos for this chapter */}
      <ChapterAnimations chapter={Number((slug.match(/^ch(\d+)/) || [])[1] || 0)} />

      {/* Prev / Next */}
      <div className="flex items-center justify-between border-t border-border pt-4">
        {prev ? (
          <Link
            href={`/learn/${prev.slug}`}
            className="flex items-center gap-1 text-sm hover:text-primary max-w-[45%]"
          >
            <ChevronLeft className="h-4 w-4 shrink-0" />
            <span className="truncate">
              <span className="text-muted-foreground">Chapter {prev.chapter}: </span>
              {prev.title}
            </span>
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link
            href={`/learn/${next.slug}`}
            className="flex items-center gap-1 text-sm hover:text-primary max-w-[45%] text-right"
          >
            <span className="truncate ml-auto">
              <span className="text-muted-foreground">Chapter {next.chapter}: </span>
              {next.title}
            </span>
            <ChevronRight className="h-4 w-4 shrink-0" />
          </Link>
        ) : (
          <span className="text-sm text-muted-foreground">End of course 🎉</span>
        )}
      </div>

      {user && (
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <AlertCircle className="h-3 w-3" /> Progress is saved for {user.username}.
        </div>
      )}
    </div>
  );
}
