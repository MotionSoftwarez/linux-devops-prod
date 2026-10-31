"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Copy, Search, Check } from "lucide-react";
import { cn } from "@/lib/utils";

export default function ReferencePage() {
  return (
    <Suspense fallback={<div className="p-8 text-muted-foreground">Loading reference…</div>}>
      <ReferenceContent />
    </Suspense>
  );
}

function ReferenceContent() {
  const [sheets, setSheets] = useState<any[]>([]);
  const [topics, setTopics] = useState<string[]>([]);
  const [filter, setFilter] = useState({ topic: "", search: "" });
  const [copied, setCopied] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const searchParams = useSearchParams();
  const qParam = searchParams.get("q") ?? "";

  // Prefill the filter when the navbar search navigates here with ?q=…
  useEffect(() => {
    if (qParam) setFilter((f) => ({ ...f, search: qParam }));
  }, [qParam]);

  useEffect(() => {
    Promise.all([api.get("/cheatsheets"), api.get("/cheatsheets/topics")])
      .then(([s, t]) => {
        setSheets(s);
        setTopics(t);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = sheets
    .map((s: any) => {
      if (!s.__parsed) {
        try {
          s.__parsed = typeof s.content === "string" ? JSON.parse(s.content) : s.content || {};
        } catch {
          s.__parsed = {};
        }
      }
      const q = filter.search.trim().toLowerCase();
      let entries: any[] = s.__parsed.entries || [];
      if (filter.topic && s.topic !== filter.topic) return null;
      if (q) {
        const matchesTitle =
          s.title.toLowerCase().includes(q) || s.topic.toLowerCase().includes(q);
        const matched = entries.filter(
          (e: any) =>
            (e.cmd || "").toLowerCase().includes(q) ||
            (e.what || "").toLowerCase().includes(q)
        );
        entries = matched.length > 0 ? matched : matchesTitle ? entries : [];
      }
      return { sheet: s, entries };
    })
    .filter(Boolean)
    .filter((x: any) => x.entries.length > 0);

  const totalShown = filtered.reduce((n: number, x: any) => n + x.entries.length, 0);

  const copyCmd = async (cmd: string) => {
    try {
      await navigator.clipboard.writeText(cmd);
      setCopied(cmd);
      setTimeout(() => setCopied((c) => (c === cmd ? null : c)), 1200);
    } catch {}
  };

  if (loading) return <div className="p-8 text-muted-foreground">Loading reference…</div>;

  return (
    <div className="mx-auto max-w-7xl px-3 py-5 space-y-4">
      {/* Compact sticky header */}
      <div className="sticky top-14 z-10 glass rounded-lg border border-border px-3 py-2 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3">
        <div className="flex items-baseline gap-2 shrink-0">
          <h1 className="text-lg font-bold tracking-tight">Cheat Sheets</h1>
          <span className="text-[11px] text-muted-foreground tabular-nums">
            {totalShown} commands
          </span>
        </div>
        <div className="flex gap-2 sm:ml-auto">
          <select
            value={filter.topic === "all" ? "" : filter.topic}
            onChange={(e) => setFilter({ ...filter, topic: e.target.value || "" })}
            className="h-8 text-xs border border-input rounded-md bg-background px-2 focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option value="">All topics</option>
            {topics.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
          <div className="relative">
            <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
            <Input
              placeholder="Filter commands…"
              value={filter.search}
              onChange={(e) => setFilter({ ...filter, search: e.target.value })}
              className="h-8 w-full sm:w-56 text-xs pl-7"
            />
          </div>
        </div>
      </div>

      {filtered.length === 0 && (
        <p className="text-sm text-muted-foreground p-6 text-center">No commands match your filters.</p>
      )}

      {/* Multi-column dense layout */}
      {filtered.map(({ sheet, entries }: any) => (
        <section key={sheet.key}>
          <div className="flex items-center gap-2 mb-2">
            <h2 className="text-xs font-bold uppercase tracking-wider text-foreground">
              {sheet.title}
            </h2>
            <span className="text-[10px] text-muted-foreground tabular-nums">
              {entries.length}
            </span>
            <div className="h-px flex-1 bg-border" />
          </div>
          <div className="columns-1 sm:columns-2 lg:columns-3 2xl:columns-4 gap-2.5">
            {entries.map((entry: any, i: number) => {
              const flagged = entry.safety && entry.safety.toLowerCase() !== "safe.";
              return (
                <div
                  key={i}
                  className={cn(
                    "group mb-2.5 break-inside-avoid rounded-lg border px-2.5 py-2 transition-colors",
                    flagged
                      ? "border-red-500/25 bg-red-500/[0.04]"
                      : "border-border/60 bg-muted/25 hover:border-primary/40 hover:bg-accent/50"
                  )}
                >
                  <div className="flex items-start gap-1.5">
                    <code
                      className={cn(
                        "text-[12px] font-mono leading-tight break-all",
                        flagged ? "text-red-600 dark:text-red-400" : "text-primary"
                      )}
                    >
                      {entry.cmd}
                    </code>
                    <button
                      onClick={() => copyCmd(entry.cmd)}
                      className="ml-auto shrink-0 p-0.5 text-muted-foreground hover:text-primary opacity-0 group-hover:opacity-100 transition-opacity"
                      title="Copy command"
                      aria-label={`Copy ${entry.cmd}`}
                    >
                      {copied === entry.cmd ? (
                        <Check className="h-3 w-3 text-emerald-500" />
                      ) : (
                        <Copy className="h-3 w-3" />
                      )}
                    </button>
                  </div>
                  <p className="mt-1 text-[11px] leading-snug text-muted-foreground">
                    {entry.what}
                  </p>
                  {(flagged || (entry.distro && entry.distro !== "All")) && (
                    <div className="mt-1 flex items-center gap-2 flex-wrap">
                      {flagged && (
                        <span className="text-[10px] font-medium text-red-600/90 dark:text-red-400/90 leading-tight">
                          ⚠ {entry.safety}
                        </span>
                      )}
                      {entry.distro && entry.distro !== "All" && (
                        <span className="text-[9px] uppercase tracking-wide text-muted-foreground/80 border border-border rounded px-1">
                          {entry.distro}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      ))}

      <p className="text-center text-[10px] text-muted-foreground pt-2 pb-4">
        Source: phoenixNAP Linux Commands Cheat Sheet + platform foundation sheets.
      </p>
    </div>
  );
}
