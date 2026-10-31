"use client";

import { useEffect, useMemo, useRef, useState } from "react";

/* ---------------- TypingTerminal: loops through a scripted session ---------------- */
export interface TermLine {
  prompt?: boolean; // render as typed-after-prompt line
  text: string;
  out?: boolean; // output line (no prompt, typed instantly)
  color?: string;
}

export function TypingTerminal({ lines, className = "" }: { lines: TermLine[]; className?: string }) {
  const [progress, setProgress] = useState(0); // typed char count across whole script
  const containerRef = useRef<HTMLDivElement>(null);

  const full = useMemo(() => {
    const seq: { text: string; out: boolean; start: number; end: number }[] = [];
    let cursor = 0;
    for (const l of lines) {
      const len = l.text.length;
      seq.push({ text: l.text, out: !!l.out, start: cursor, end: cursor + len });
      cursor += len + (l.out ? 0 : 10); // output lines appear instantly, commands type
    }
    return { seq, total: cursor + 30 }; // 30 ticks pause before loop restart
  }, [lines]);

  useEffect(() => {
    let raf: number | null = null;
    let prev = performance.now();
    const tick = (now: number) => {
      if (now - prev > 34) {
        prev = now;
        setProgress((p) => (p >= full.total ? 0 : p + 1));
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => {
      if (raf) cancelAnimationFrame(raf);
    };
  }, [full]);

  const caretTail = (visible: string) => (
    <span className="caret-mini">{visible}</span>
  );

  return (
    <div ref={containerRef} className={`mini-terminal font-mono text-[13px] leading-relaxed ${className}`}>
      <div className="t-bar flex items-center gap-1.5 rounded-t-[0.7rem] px-3 py-2">
        <span className="h-2.5 w-2.5 rounded-full bg-red-500/80" />
        <span className="h-2.5 w-2.5 rounded-full bg-amber-400/80" />
        <span className="h-2.5 w-2.5 rounded-full bg-emerald-400/80" />
        <span className="ml-2 text-[10px] uppercase tracking-widest text-slate-400">tutor — bash</span>
      </div>
      <div className="min-h-[168px] px-4 py-3 space-y-0.5">
        {full.seq.map((line, i) => {
          const active = progress >= line.start && progress <= line.end;
          const done = progress > line.end;
          if (!done && !active) return null;
          const visible = done ? line.text : line.text.slice(0, Math.max(0, progress - line.start));
          const showCaret = active && progress < full.seq[full.seq.length - 1]?.end + 25;
          if (line.out) {
            return (
              <div key={i} className="text-slate-400" style={line.color ? { color: line.color } : undefined}>
                {visible}
              </div>
            );
          }
          return (
            <div key={i} className="text-slate-200">
              <span className="text-emerald-400 select-none">$&nbsp;</span>
              {caretTail(visible)}
              {showCaret && <span className="caret-blank" />}
            </div>
          );
        })}
      </div>
      <style jsx global>{`
        .caret-mini { white-space: pre-wrap; }
        span.caret-blank::after {
          content: "▋";
          margin-left: 1px;
          animation: blink-caret 1s step-end infinite;
          color: #a3e635;
        }
      `}</style>
    </div>
  );
}

/* ---------------- Confetti burst ---------------- */
const COLORS = ["#60a5fa", "#a78bfa", "#34d399", "#fbbf24", "#f472b6", "#7dd3fc"];

export function Confetti({ trigger }: { trigger: number }) {
  const [pieces, setPieces] = useState<null | { id: number; style: React.CSSProperties }[]>(null);

  useEffect(() => {
    if (!trigger) return;
    const rnd = (): React.CSSProperties => ({
      "--cx": `${(Math.random() - 0.5) * 360}px`,
      "--cy": `${260 + Math.random() * 380}px`,
      "--cr": `${360 + Math.random() * 720}deg`,
      left: `${46 + (Math.random() - 0.5) * 8}%`,
      top: "40px",
      width: `${6 + Math.random() * 6}px`,
      height: `${10 + Math.random() * 8}px`,
      background: COLORS[Math.floor(Math.random() * COLORS.length)],
      borderRadius: Math.random() > 0.5 ? "50%" : "2px",
      position: "fixed",
      zIndex: 70,
      pointerEvents: "none",
      transform: `rotate(${Math.random() * 360}deg)`,
    } as React.CSSProperties);
    const burst = Array.from({ length: 34 }, (_, i) => ({ id: i, style: rnd() }));
    setPieces(burst);
    const t = setTimeout(() => setPieces(null), 1600);
    return () => clearTimeout(t);
  }, [trigger]);

  if (!pieces) return null;
  return (
    <div aria-hidden="true">
      {pieces.map((p) => (
        <span
          key={p.id}
          style={{
            ...p.style,
            animation: "confetti-fall 1.35s cubic-bezier(0.15, 0.6, 0.4, 1) forwards",
          }}
        />
      ))}
    </div>
  );
}

/* ---------------- ProgressRing ---------------- */
export function ProgressRing({
  percent,
  size = 120,
  label,
  sublabel,
}: {
  percent: number;
  size?: number;
  label?: string;
  sublabel?: string;
}) {
  const r = (size - 12) / 2;
  const c = 2 * Math.PI * r;
  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setMounted(true), 60);
    return () => clearTimeout(t);
  }, []);
  const clamped = Math.max(0, Math.min(100, percent));
  const offset = c - (mounted ? (clamped / 100) * c : 0);

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} strokeWidth={10} fill="none"
          className="stroke-muted" />
        <circle
          cx={size / 2} cy={size / 2} r={r} strokeWidth={10} fill="none"
          strokeLinecap="round"
          stroke="url(#ringGrad)"
          strokeDasharray={c}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 1.1s cubic-bezier(0.2, 0.8, 0.3, 1)" }}
        />
        <defs>
          <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="55%" stopColor="#a78bfa" />
            <stop offset="100%" stopColor="#34d399" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-2xl font-bold tabular-nums">{label ?? `${clamped}%`}</span>
        {sublabel && <span className="text-[10px] uppercase tracking-wider text-muted-foreground">{sublabel}</span>}
      </div>
    </div>
  );
}

/* ---------------- ReadingProgress (scroll-linked top bar) ---------------- */
export function ReadingProgress() {
  const [pct, setPct] = useState(0);
  useEffect(() => {
    const main = document.querySelector("main");
    if (!main) return;
    const update = () => {
      const el = main as HTMLElement;
      const scrollable = el.scrollHeight - el.clientHeight;
      setPct(scrollable > 40 ? Math.min(100, Math.max(0, (el.scrollTop / scrollable) * 100)) : 0);
    };
    update();
    main.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    return () => {
      main.removeEventListener("scroll", update);
      window.removeEventListener("resize", update);
    };
  }, []);
  if (pct <= 0) return null;
  return (
    <div
      className="fixed left-0 right-0 top-0 z-50 h-1 origin-left reading-progress"
      style={{ width: `${pct}%` }}
      role="progressbar"
      aria-label="Reading progress"
    />
  );
}

/* ---------------- CodeCopy (adds copy buttons to every <pre> in a container) ---------------- */
export function CodeCopyButtons({ containerClass = ".lesson-content" }: { containerClass?: string }) {
  useEffect(() => {
    const container = document.querySelector(containerClass);
    if (!container) return;
    const pres = Array.from(container.querySelectorAll("pre"));
    const cleanups: (() => void)[] = [];
    pres.forEach((pre) => {
      if (pre.dataset.copyInstalled === "yes") return;
      pre.dataset.copyInstalled = "yes";
      pre.style.position = "relative";
      const btn = document.createElement("button");
      btn.textContent = "Copy";
      btn.className =
        "absolute right-2 top-2 rounded-md border border-white/10 bg-white/10 px-2 py-1 text-[11px] font-medium text-slate-200 opacity-0 transition-opacity hover:bg-white/20";
      const click = async () => {
        try {
          await navigator.clipboard.writeText(pre.textContent || "");
          btn.textContent = "Copied!";
          setTimeout(() => (btn.textContent = "Copy"), 1200);
        } catch {}
      };
      btn.addEventListener("click", click);
      const show = () => (btn.style.opacity = "1");
      const hide = () => (btn.style.opacity = "0");
      pre.addEventListener("mouseenter", show);
      pre.addEventListener("mouseleave", hide);
      pre.appendChild(btn);
      cleanups.push(() => {
        btn.removeEventListener("click", click);
        pre.removeEventListener("mouseenter", show);
        pre.removeEventListener("mouseleave", hide);
        btn.remove();
      });
    });
    return () => cleanups.forEach((c) => c());
  }, [containerClass]);
  return null;
}
