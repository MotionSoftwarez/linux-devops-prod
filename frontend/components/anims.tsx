"use client";

/**
 * ChapterAnimations — a visual "Watch it run" section embedded in chapter pages.
 * Each chapter gets 1-2 micro-animations explaining its core concept with
 * CSS/state animations (no external deps).
 */

import { useEffect, useState, type FC } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { PlayCircle } from "lucide-react";
import { cn } from "@/lib/utils";

/* ---------------------------------------------------------------- */
/* helpers                                                          */
/* ---------------------------------------------------------------- */

function useLoop(count: number, ms = 1200): number {
  const [i, setI] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setI((v) => (v + 1) % count), ms);
    return () => clearInterval(t);
  }, [count, ms]);
  return i;
}

function MiniTerm({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`mini-terminal font-mono text-[11.5px] leading-relaxed px-3 py-2.5 rounded-lg ${className}`}>
      {children}
    </div>
  );
}

function Chip({
  active,
  done,
  danger,
  children,
  mono = true,
}: {
  active?: boolean;
  done?: boolean;
  danger?: boolean;
  children: React.ReactNode;
  mono?: boolean;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-md border px-2 py-1 text-[11px] leading-none transition-all duration-300",
        mono && "font-mono",
        active
          ? "border-primary/60 bg-primary/10 text-primary shadow-[0_0_12px_hsl(221_83%_53%/_0.35)] scale-[1.04]"
          : done
            ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
            : danger
              ? "border-red-500/40 bg-red-500/10 text-red-600 dark:text-red-400"
              : "border-border bg-muted/40 text-muted-foreground"
      )}
    >
      {children}
    </span>
  );
}

/** Sequentially highlights a list of labeled steps, then restarts. */
function ChainSeq({
  steps,
  ms = 900,
  doneLabel,
}: {
  steps: { label: string; sub?: string; icon?: string }[];
  ms?: number;
  doneLabel?: string;
}) {
  const idx = useLoop(steps.length + (doneLabel ? 1 : 0), ms);
  return (
    <div className="space-y-1.5">
      {steps.map((s, i) => {
        const active = i === idx;
        const done = i < idx && !(doneLabel && idx === steps.length);
        return (
          <div key={i} className="flex items-center gap-2">
            <span
              className={cn(
                "flex h-5 w-5 shrink-0 items-center justify-center rounded-full border text-[9px] font-bold transition-all duration-300",
                active
                  ? "border-primary bg-primary text-primary-foreground scale-110"
                  : done
                    ? "border-emerald-500/60 bg-emerald-500/15 text-emerald-600 dark:text-emerald-400"
                    : "border-border bg-muted/50 text-muted-foreground/60"
              )}
            >
              {done ? "✓" : i + 1}
            </span>
            <Chip active={active} done={done} mono>
              {s.icon && <span className="not-italic">{s.icon}</span>}
              {s.label}
            </Chip>
            {s.sub && (
              <span className={cn("text-[10px] transition-opacity", active ? "text-foreground opacity-100" : "opacity-0")}>
                {s.sub}
              </span>
            )}
          </div>
        );
      })}
      {doneLabel && (
        <div className={cn("pl-7 text-[11px] font-semibold text-emerald-600 transition-opacity duration-300", idx === steps.length ? "opacity-100" : "opacity-0")}>
          {doneLabel}
        </div>
      )}
    </div>
  );
}

/* ---------------------------------------------------------------- */
/* per-chapter animations                                           */
/* ---------------------------------------------------------------- */

/* CH 1 — Where Linux lives: the layer cake */
const OSLayers = () => {
  const idx = useLoop(4, 1100);
  const layers = [
    { name: "Apps & services", sub: "nginx · docker · your tools", cls: "from-emerald-500/20 to-transparent" },
    { name: "Shell & libraries", sub: "bash · printf · libc", cls: "from-amber-500/20 to-transparent" },
    { name: "Linux kernel", sub: "µmang = memory, files, processes, drivers", cls: "from-violet-500/25 to-transparent" },
    { name: "Hardware", sub: "CPU · RAM · disk · NIC", cls: "from-blue-500/20 to-transparent" },
  ];
  return (
    <div className="space-y-1.5">
      {layers.map((l, i) => (
        <div
          key={l.name}
          className={cn(
            "rounded-lg border px-3 py-2 bg-gradient-to-r transition-all duration-500",
            l.cls,
            idx === i ? "border-primary/70 scale-[1.02] shadow-[0_4px_18px_hsl(221_83%_53%/_0.25)]" : "border-border/60"
          )}
        >
          <p className={cn("text-xs font-semibold", idx === i ? "text-foreground" : "text-muted-foreground")}>{l.name}</p>
          <p className="text-[10px] text-muted-foreground font-mono">{l.sub}</p>
        </div>
      ))}
      <p className="text-[10px] text-muted-foreground text-center pt-1">
        Every command you type talks through the <span className="text-violet-500 font-semibold">kernel</span> to the hardware.
      </p>
    </div>
  );
};

/* CH 2 — the filesystem tree fills in */
const FSTree = () => {
  const idx = useLoop(9, 480);
  const reveal = (n: number) => idx >= n;
  return (
    <MiniTerm>
      <div className="text-emerald-400 select-none">/</div>
      <div className="pl-3 space-y-0.5">
        {[
          { n: 1, c: "text-amber-300", t: "etc/", s: "— config files" },
          { n: 2, c: "text-sky-300", t: "home/", s: "— user files" },
          { n: 3, c: "text-rose-300", t: "var/", s: "— logs, spool" },
          { n: 4, c: "text-emerald-300", t: "usr/", s: "— programs" },
          { n: 5, c: "text-muted-foreground", t: "home/alice/", s: "· " },
          { n: 6, c: "text-muted-foreground", t: "var/log/", s: "· " },
          { n: 7, c: "text-muted-foreground", t: "etc/nginx/", s: "· " },
        ].map((r) => (
          <div key={r.t} className={cn("transition-opacity duration-300", reveal(r.n) ? "opacity-100" : "opacity-5")}>
            <span className={r.c}>{r.t}</span> <span className="text-[10px] text-muted-foreground">{r.s}</span>
          </div>
        ))}
      </div>
      <div className={cn("mt-2 text-[10px] transition-all duration-300", reveal(8) ? "opacity-100" : "opacity-0")}>
        <p className="text-slate-400">$ pwd → <span className="text-emerald-300">/home/alice</span></p>
        <p className="text-slate-400">recall: "Everything is a file. It all hangs under /."</p>
      </div>
    </MiniTerm>
  );
};

/* CH 3 — cp / mv / rm lanes */
const CopyLane = () => {
  const i = useLoop(5, 550);
  return (
    <div className="flex items-center gap-2">
      <Chip active={i === 0}>file.txt</Chip>
      <span className={cn("text-primary transition-opacity", i === 1 ? "opacity-100" : "opacity-30")}>cp file.txt file.bak →</span>
      <Chip done={i >= 3} active={i === 2}>{i === 3 || i === 4 ? "file.bak ✓" : "file.bak"}</Chip>
    </div>
  );
};
const MoveLane = () => {
  const i = useLoop(5, 550);
  return (
    <div className="flex items-center gap-2">
      <Chip active={i <= 1 && i !== 0}>notes.md</Chip>
      <span className={cn("text-primary transition-opacity", i === 2 || i === 3 ? "opacity-100" : "opacity-30")}>mv notes.md /tmp →</span>
      <Chip done={i >= 4} active={i === 3}>{i === 4 ? "moved ✓" : "/tmp/notes.md"}</Chip>
    </div>
  );
};
const RmLane = () => {
  const i = useLoop(5, 600);
  return (
    <div className="flex items-center gap-2">
      <Chip danger={i >= 3} active={i <= 1}>temp.log</Chip>
      <span className={cn("text-red-500 transition-opacity", i === 2 ? "opacity-100" : "opacity-30")}>rm temp.log →</span>
      <span className={cn("text-[11px] transition-all", i >= 3 ? "text-red-500 opacity-100" : "opacity-0")}>
        {i === 3 ? "gone — no recycling bin 🗑" : "no trash, no undo"}
      </span>
    </div>
  );
};

/* CH 4 — grep scanning a file */
const GREP_LNS = [
  "INFO  boot complete",
  "INFO  request ok",
  "ERROR db connection refused",
  "INFO  request ok",
  "WARN  slow query 900ms",
  "ERROR connection timeout",
];
const GrepScan = () => {
  const i = useLoop(GREP_LNS.length, 700);
  const matched = GREP_LNS.filter((l) => l.includes("ERROR"));
  return (
    <div className="grid grid-cols-2 gap-2">
      <MiniTerm>
        <p className="text-slate-500 mb-1">$ cat app.log</p>
        {GREP_LNS.map((l, k) => (
          <div
            key={k}
            className={cn(
              "transition-colors duration-200 rounded px-1",
              k === i ? "bg-primary/20 text-foreground" : l.includes("ERROR") ? "text-red-400" : "text-muted-foreground"
            )}
          >
            {l}
          </div>
        ))}
      </MiniTerm>
      <MiniTerm>
        <p className="text-slate-500 mb-1">$ grep ERROR app.log</p>
        <div className="space-y-0.5 text-red-400">
          {matched.map((m, k) => (
            <div key={m} className={cn("transition-opacity duration-500", GREP_LNS.findIndex((x) => x === m) <= i ? "opacity-100" : "opacity-0")}>
              {m}
            </div>
          ))}
        </div>
      </MiniTerm>
    </div>
  );
};

/* CH 5 — chmod mode calculator */
const DEMO_MODES = ["755", "644", "777", "600", "664"];
const ChmodCalc = () => {
  const i = useLoop(DEMO_MODES.length, 1300);
  const mode = DEMO_MODES[i];
  const digits = mode.split("").map((d) => parseInt(d, 10));
  const who = ["User", "Group", "Other"];
  const perms = ["r", "w", "x"];
  return (
    <div className="space-y-2">
      <div className="flex items-baseline gap-3">
        <span className="font-mono text-sm text-primary">chmod {mode} file.sh</span>
        <span className="text-[10px] text-muted-foreground">one octal digit per user class</span>
      </div>
      <div className="grid grid-cols-3 gap-2">
        {who.map((w, gi) => {
          const val = digits[gi] || 0;
          return (
            <div key={w} className="rounded-lg border border-border/60 p-2">
              <p className="text-[10px] font-semibold text-muted-foreground mb-1.5">
                {w} <span className="font-mono text-primary">{val}</span>
              </p>
              <div className="flex gap-1">
                {perms.map((p, pi) => {
                  const on = (val & (1 << (2 - pi))) !== 0;
                  return (
                    <span
                      key={p}
                      className={cn(
                        "flex h-6 w-6 items-center justify-center rounded border font-mono text-[11px] transition-all duration-300",
                        on
                          ? "border-emerald-500/60 bg-emerald-500/20 text-emerald-600 dark:text-emerald-300"
                          : "border-border bg-muted/30 text-muted-foreground/40"
                      )}
                      title={`${p} = ${1 << (2 - pi)}`}
                    >
                      {p}
                    </span>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
      <p className="text-[10px] text-muted-foreground">{mode === "777" ? "⚠ 777 = world-writable — almost always wrong" : mode === "600" ? "600 = only the owner reads it — private keys live here" : "r=4 · w=2 · x=1 — add the bits you want"}</p>
    </div>
  );
};

/* CH 6 — sudo elevation */
const SudoFlow = () => {
  const i = useLoop(5, 1000);
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <Chip active={i === 0}>👤 bob</Chip>
        <span className="text-[10px] text-muted-foreground">member of group <span className="text-primary font-mono">sudo</span></span>
      </div>
      <div className={cn("flex items-center gap-2 transition-all duration-300", i === 1 ? "opacity-100" : "opacity-40")}>
        <Chip active={i === 1}>🔒 password?</Chip>
        <span className="text-[10px] text-muted-foreground">asked once, cached 15 min</span>
      </div>
      <div className="flex items-center gap-2">
        <Chip active={i === 2} done={i >= 3}>⚡ sudo systemctl restart nginx</Chip>
        {i >= 3 && <Chip done>root privileges ✓</Chip>}
      </div>
      <div className={cn("text-[10px] text-muted-foreground transition-opacity", i === 4 ? "opacity-100" : "opacity-0")}>
        sudo = "do this once as root" — the session stays bob.
      </div>
    </div>
  );
};

/* CH 7 — process lifecycle */
const ProcCycle = () => {
  const i = useLoop(5, 900);
  const states = [
    { name: "fork() — created", icon: "🌱" },
    { name: "READY — waiting for CPU", icon: "⏳" },
    { name: "RUNNING — on the CPU", icon: "🔥" },
    { name: "sleeping — waiting for I/O", icon: "💤" },
  ];
  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between">
        <span className="font-mono text-[11px] text-muted-foreground">
          PID <span className="text-primary">1234</span>
        </span>
        <span className={cn("font-mono text-[10.5px] transition-opacity duration-300", i === 4 ? "text-red-500 opacity-100" : "opacity-0")}>
          kill 1234 → zombie → reaped
        </span>
      </div>
      {states.map((s, k) => (
        <div
          key={s.name}
          className={cn(
            "rounded-lg border px-2.5 py-1.5 text-[11px] font-mono flex items-center gap-2 transition-all duration-300",
            k === i % 4 ? "border-primary/60 bg-primary/10 text-primary" : "border-border/50 bg-muted/30 text-muted-foreground"
          )}
        >
          <span>{s.icon}</span> {s.name}
        </div>
      ))}
      <div className="h-4 text-center font-mono text-[10.5px] text-muted-foreground">
        {i >= 2 && i < 4 ? "top shows: %CPU 99.7 — that's us at this stage" : ""}
      </div>
    </div>
  );
};

/* CH 8 — packet journey: DNS + HTTP */
const PacketJourney = () => {
  const i = useLoop(6, 800);
  const stops = ["Client", "DNS", "Server"];
  const pos = i === 0 ? 0 : i === 1 ? 0.5 : i === 2 ? 0.15 : i === 3 ? 1 : i === 4 ? 1 : 0;
  const captions = [
    "1  where is api.example.com?",
    "2  ← 203.0.113.7",
    "3  SYN → SYN/ACK → ACK (TCP handshake)",
    "4  GET /health HTTP/1.1",
    "5  ← 200 OK (45ms)",
    "done — connection reused next time",
  ];
  return (
    <div className="space-y-2.5">
      <div className="relative h-8">
        <div className="absolute left-0 right-0 top-3 h-0.5 bg-border rounded" />
        <div
          className="absolute top-1 h-3.5 w-3.5 rounded-full bg-gradient-to-r from-blue-500 to-violet-500 shadow-[0_0_10px_hsl(221_83%_53%/.7)] transition-all duration-700"
          style={{ left: `calc(${pos * 88}% + 6px)` }}
        />
        {stops.map((s, k) => (
          <div key={s} className="absolute top-0" style={{ left: `${k * 44}%` }}>
            <div className="h-6 w-px bg-border" />
            <span className={cn("text-[10px] font-mono", i >= k && "text-muted-foreground")}>{s}</span>
          </div>
        ))}
      </div>
      <p className="font-mono text-[11px] text-foreground">{captions[i]}</p>
    </div>
  );
};

/* CH 9 — apt install flow */
const APT_CHAIN = [
  { label: "apt install nginx", sub: "you type it" },
  { label: "resolve dependencies", sub: "nginx → libssl23 ..." },
  { label: "download .deb files", sub: "from archive.ubuntu.com" },
  { label: "unpack + configure", sub: "postinst scripts run" },
  { label: "service enabled", sub: "systemd starts nginx" },
];
/* CH 10 — systemd dependency chain */
const UNIT_CHAIN = [
  { label: "network.service", sub: "ens100 up" },
  { label: "sshd.service", sub: "listening :22" },
  { label: "postgres.service", sub: "ready on :5432" },
  { label: "nginx.service", sub: "wants: network.target" },
  { label: "multi-user.target", sub: "boot complete" },
];
/* CH 13 — ssh handshake */
const SSH_CHAIN = [
  { label: "TCP connect :22", sub: "SYN → SYN/ACK" },
  { label: "key exchange", sub: "Diffie-Hellman, curve25519" },
  { label: "host fingerprint", sub: "~/.ssh/known_hosts check" },
  { label: "auth: publickey", sub: "id_ed25519 — no password sent" },
  { label: "session", sub: "PTY allocated, $ " },
];
/* CH 22 — troubleshooting loop */
const TTR_CHAIN = [
  { label: "symptom", sub: "what do users see?" },
  { label: "observe", sub: "ps · df · journalctl -xe" },
  { label: "hypothesis", sub: "one change at a time" },
  { label: "test", sub: "measure → confirm/refute" },
  { label: "fix + verify", sub: "and write down the why" },
];
/* CH 23 — CI-style script execution */
const CI_CHAIN = [
  { label: "shellcheck lint", sub: "fail fast, < 1s" },
  { label: "unit tests", sub: "bash bats / pytest" },
  { label: "build artifacts", sub: "docker build -t app:1.3" },
  { label: "deploy --canary", sub: "one server first" },
  { label: "healthcheck", sub: "curl -fsS /healthz" },
];
/* CH 24 — boot sequence */
const BOOT_CHAIN = [
  { label: "firmware (UEFI)", sub: "POST — hardware self-test" },
  { label: "bootloader (GRUB)", sub: "picks kernel + params" },
  { label: "kernel vmlinuz", sub: "drivers probe, mounts /" },
  { label: "initramfs", sub: "disk/crypto drivers, pivot_root" },
  { label: "systemd (PID 1)", sub: "reaches default.target" },
];
/* CH 25 — incident timeline */
const INC_CHAIN = [
  { label: "ALERT", sub: "p99 latency > 2s", icon: "🚨" },
  { label: "triage", sub: "narrow scope: one pod?" },
  { label: "mitigate", sub: "rollback or restart" },
  { label: "recover", sub: "error budget back to 0" },
  { label: "postmortem", sub: "blameless, action items" },
];

const aptMs = 1000;
const aptDone = "installed 3 packages — `systemctl status nginx` to verify";
const APT_ANIM: FC = () => <ChainSeq steps={APT_CHAIN} ms={aptMs} doneLabel={aptDone} />;
const SYSTEMD_ANIM: FC = () => (
  <div>
    <ChainSeq steps={UNIT_CHAIN} ms={900} doneLabel="✅ target reached — system ready for users" />
    <p className="mt-1.5 text-[10px] text-muted-foreground">systemd starts units in parallel as soon as their dependencies are up.</p>
  </div>
);
const SSH_ANIM: FC = () => (
  <div>
    <ChainSeq steps={SSH_CHAIN} ms={900} doneLabel="🔐 encrypted channel established" />
  </div>
);
const TTR_ANIM: FC = () => <ChainSeq steps={TTR_CHAIN} ms={850} />;
const CI_ANIM: FC = () => (
  <div>
    <ChainSeq steps={CI_CHAIN} ms={850} doneLabel="🚀 pipeline green in 42s" />
    <p className="mt-1.5 text-[10px] text-muted-foreground">The same loop runs from cron, CI, or a git hook — the script is the robot.</p>
  </div>
);
const BOOT_ANIM: FC = () => <ChainSeq steps={BOOT_CHAIN} ms={900} doneLabel="login prompt reaches sshd + getty" />;
const INC_ANIM: FC = () => <ChainSeq steps={INC_CHAIN} ms={900} />;

/* CH 11 — journal stream + grep filter */
const LOG_POOL = [
  "sshd: accepted key for alice",
  "nginx: 200 GET /healthz",
  "cron[512]: job ran backup.sh",
  "kernel: TCP retransmit x3",
  "nginx: 502 upstream timeout",
  "docker: container app-1 restarted",
];
const LogStream = () => {
  const [lines, setLines] = useState<string[]>(LOG_POOL.slice(0, 4));
  useEffect(() => {
    const t = setInterval(() => setLines((cur) => [...cur.slice(-5), LOG_POOL[Math.floor(Math.random() * LOG_POOL.length)]]), 900);
    return () => clearInterval(t);
  }, []);
  const errCount = lines.filter((l) => l.includes("502")).length;
  return (
    <div className="grid grid-cols-2 gap-2">
      <MiniTerm>
        <p className="text-slate-500 mb-1">$ journalctl -f</p>
        <div className="space-y-0.5">
          {lines.map((l, k) => (
            <div key={`${k}-${l}`} className={cn("animate-fade-up", l.includes("502") ? "text-red-400" : "text-muted-foreground")}>
              {l}
            </div>
          ))}
        </div>
      </MiniTerm>
      <MiniTerm>
        <p className="text-slate-500 mb-1">$ journalctl -f | grep 502</p>
        <div className="text-red-400 space-y-0.5">
          {lines.filter((l) => l.includes("502")).map((l, k) => (
            <div key={`${k}-${l}`}>{l}</div>
          ))}
        </div>
        <p className="mt-2 text-[10px] text-emerald-400">{errCount > 0 ? `filter caught ${errCount} error line(s)` : "waiting for errors…"}</p>
      </MiniTerm>
    </div>
  );
};

/* CH 12 — disk filling up / df */
const DiskFill = () => {
  const i = useLoop(10, 620);
  const pct = 62 + i * 3;
  return (
    <div className="space-y-2">
      <div>
        <p className="font-mono text-[11px] text-muted-foreground">df -h /</p>
        <div className="mt-1 h-4 w-full rounded bg-muted/60 overflow-hidden border border-border/50">
          <div
            className={cn("h-full rounded transition-all duration-500", pct > 85 ? "bg-gradient-to-r from-red-500 to-red-400" : "bg-gradient-to-r from-blue-500 to-violet-500")}
            style={{ width: `${Math.min(pct, 92)}%` }}
          />
        </div>
        <p className="mt-1 font-mono text-[11px]">{pct > 85 ? <span className="text-red-500">⚠ {pct}% — clean libs first: journalctl --vacuum-size=100M</span> : <span className="text-emerald-600">{pct}% used — healthy</span>}</p>
      </div>
      <p className="text-[10px] text-muted-foreground">Watch how fast the bar re-fills from /var/log + docker images — the usual suspects.</p>
    </div>
  );
};

/* CH 14 — live metric bars */
const METRIC_POOL = ["cpu", "mem", "io wait"];
const LiveMetrics = () => {
  const [vals, setVals] = useState([31, 55, 12]);
  useEffect(() => {
    const t = setInterval(
      () => setVals((v) => v.map((x, k) => Math.max(4, Math.min(97, x + Math.round((Math.random() - (k === 1 ? 0.35 : 0.5)) * 26))))),
      800
    );
    return () => clearInterval(t);
  }, []);
  return (
    <div className="space-y-2">
      <div className="grid grid-cols-3 gap-2 text-center">
        {vals.map((v, k) => (
          <div key={k}>
            <p className="font-mono text-[10px] text-muted-foreground mb-1">{METRIC_POOL[k]}</p>
            <div className="h-14 w-full flex items-end rounded bg-muted/40 border border-border/50 overflow-hidden">
              <div
                className={cn("w-full rounded-t transition-all duration-700", v > 80 ? "bg-gradient-to-t from-red-500/80 to-red-400/60" : "bg-gradient-to-t from-blue-500/80 to-violet-400/50")}
                style={{ height: `${v}%` }}
              />
            </div>
            <p className={cn("font-mono text-[11px]", v > 80 ? "text-red-500" : "text-emerald-600")}>{v}%</p>
          </div>
        ))}
      </div>
      <p className="text-center font-mono text-[10px] text-muted-foreground">{vals.some((v) => v > 80) ? "🚨 set alerts BEFORE this happens — htop / vmstat 1" : "top / htop / vmstat — three tools that read these numbers"}</p>
    </div>
  );
};

/* CH 15 — pipeline tokens */
const Pipeline = () => {
  const i = useLoop(6, 620);
  const stages = [
    { cmd: "cat access.log", n: 5000 },
    { cmd: "grep 404", n: 213 },
    { cmd: "wc -l", n: 213 },
  ];
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-1 font-mono text-[11px]">
        {stages.map((s, k) => (
          <div key={s.cmd} className="flex items-center gap-1">
            {k > 0 && <span className={cn("text-primary transition-opacity", i > k * 2 ? "opacity-100" : "opacity-25")}>|</span>}
            <Chip active={i > k * 2} done={i > k * 2 + 2}>
              {s.cmd}
            </Chip>
          </div>
        ))}
      </div>
      <div className="flex items-center gap-2">
        {stages.map((s, k) => (
          <div key={s.cmd} className="flex items-center gap-1 flex-1">
            {k > 0 && <span className="flex items-center justify-center text-primary font-mono w-4">{"·".repeat(Math.max(1, Math.round(6 - k)))}</span>}
            <div className="flex-1 text-center">
              <span className={cn("font-mono text-xs transition-all", i >= k * 2 + 1 ? "text-foreground opacity-100" : "opacity-30")}>
                {s.n.toLocaleString()}
              </span>
              <p className="text-[9px] text-muted-foreground">tokens</p>
            </div>
          </div>
        ))}
      </div>
      <p className="text-[10px] text-muted-foreground">5,000 lines → 213 with two commands. Each stage is tiny — that's the Unix way.</p>
    </div>
  );
};

/* CH 16 — cron clock */
const CronClock = () => {
  const i = useLoop(12, 500);
  const hand = i * 30;
  const fires = i === 3 || i === 9; // quarter marks
  return (
    <div className="flex items-center gap-4">
      <div className="relative h-20 w-20">
        <div className="absolute inset-0 rounded-full border-2 border-border" />
        {Array.from({ length: 12 }).map((_, k) => (
          <div key={k} className="absolute left-1/2 top-0 h-full w-full" style={{ transform: `rotate(${k * 30}deg)` }}>
            <span className={cn("absolute left-1/2 top-0.5 h-2 w-0.5 -translate-x-1/2", k === 3 || k === 9 ? "bg-primary" : "bg-border")} />
          </div>
        ))}
        <div
          className="absolute left-1/2 top-1/2 h-7 w-0.5 origin-bottom -translate-x-1/2 -translate-y-full bg-gradient-to-t from-red-500 to-orange-400 transition-transform duration-500 ease-linear"
          style={{ transform: `translate(-50%, -100%) rotate(${hand}deg)` }}
        />
        <span className={cn("absolute left-1/2 top-1/2 h-1.5 w-1.5 -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary")} />
      </div>
      <div className="min-w-0 flex-1">
        <p className="font-mono text-[10px] text-muted-foreground">m h dom mon dow</p>
        <p className="font-mono text-[11px] text-foreground mb-1">30 * * * * backup.sh</p>
        <div className={cn("rounded-lg border px-2 py-1.5 font-mono text-[11px] transition-all duration-300", fires ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-600" : "border-border/50 text-muted-foreground/50")}>
          {fires ? "ran backup.sh ✓ (at minute :30 past every hour)" : "tick… waiting for minute 30"}
        </div>
      </div>
    </div>
  );
};

/* CH 17 — export passes vars to children */
const ExportFlow = () => {
  const i = useLoop(5, 900);
  return (
    <div className="space-y-2">
      <div className="rounded-lg border border-primary/40 bg-primary/5 p-2.5">
        <p className="text-[10px] font-semibold text-primary mb-1.5">parent shell</p>
        <div className="flex gap-1 flex-wrap">
          <Chip active={i === 1} done={i >= 2}>DEPLOY_ENV=prod</Chip>
          <Chip active={i === 0 }>PRIVATE=ssh-key 🤫</Chip>
        </div>
        <p className="text-[10px] text-muted-foreground mt-1.5 font-mono">export DEPLOY_ENV</p>
      </div>
      <div className="flex justify-center">
        <span className={cn("text-xs transition-opacity", i === 2 ? "opacity-100" : "opacity-30")}>
          {i === 2 ? "$ ./deploy.sh" : "$"}
        </span>
      </div>
      <div className="rounded-lg border border-border/60 bg-muted/30 p-2.5">
        <p className="text-[10px] font-semibold text-muted-foreground mb-1.5">child process (deploy.sh)</p>
        <div className="flex gap-1 flex-wrap">
          <span className={cn("transition-opacity duration-300", i >= 3 ? "opacity-100" : "opacity-20")}><Chip done>DEPLOY_ENV ✓ inherited</Chip></span>
          <span className={cn("transition-opacity duration-300", i >= 3 ? "opacity-100" : "opacity-20")}><Chip danger>PRIVATE ✗ blocked</Chip></span>
        </div>
      </div>
      <p className="text-[10px] text-muted-foreground">Only <span className="font-mono text-primary">export</span>-ed variables cross the boundary to children.</p>
    </div>
  );
};

/* CH 18 — commit graph */
const COMMITS = ["init", "feat: pg checks", "fix: typo", "docs", "refactor"];
const GitGraph = () => {
  const i = useLoop(COMMITS.length + 2, 750);
  const branchAt = 1; // branch off between idx1..3, merge at 5
  return (
    <div className="space-y-2">
      <div className="relative h-16">
        <div className="absolute left-0 right-0 top-9 h-0.5 bg-border" />
        {COMMITS.map((c, k) => (
          <div
            key={c}
            className={cn(
              "absolute top-9 -translate-y-1/2 h-3.5 w-3.5 rounded-full border-2 transition-all duration-300",
              i >= k ? "border-emerald-500 bg-emerald-400" : "border-border bg-muted"
            )}
            style={{ left: `${6 + k * 22}%` }}
          >
            <span className={cn("absolute top-4 whitespace-nowrap text-[8.5px] font-mono", i >= k ? "text-foreground" : "text-muted-foreground/40", k > 2 && "left-[-14px]")}>{c}</span>
          </div>
        ))}
        <div className={cn("absolute top-0 h-9 border-l-2 border-dashed border-violet-400/70 transition-opacity duration-300", i >= branchAt + 1 && i <= branchAt + 3 ? "opacity-100" : "opacity-40")} style={{ left: `${6 + branchAt * 22 + 8}%` }} />
        <span className={cn("absolute font-mono text-[9px] transition-all", i > branchAt && i < branchAt + 3 ? "text-violet-400 opacity-100" : "opacity-30")} style={{ left: `${6 + branchAt * 22 + 12}%`, top: "2px" }}>
          fix/healthchecks {i > branchAt && i < branchAt + 3 ? "← you are here" : ""}
        </span>
      </div>
      <p className="font-mono text-[10px] text-muted-foreground center" style={{ textAlign: "center" }}>
        {i < branchAt + 3 ? "git branch fix/healthchecks → commit → " : ""}
        {i === COMMITS.length ? "git merge → main now has the fix" : ""}
      </p>
    </div>
  );
};

/* CH 19 — docker layers → container */
const DockerLayers = () => {
  const i = useLoop(8, 650);
  const layers = ["ubuntu:22.04  74MB", "apt install python  22MB", "pip install -r reqs  18MB", "COPY app/  2MB"];
  return (
    <div className="space-y-1.5">
      {layers.map((l, k) => (
        <div
          key={l}
          className={cn(
            "rounded-lg border px-2.5 py-1.5 font-mono text-[10.5px] transition-all duration-500 bg-gradient-to-r from-sky-500/10 to-violet-500/10",
            i > k ? "border-sky-500/50 opacity-100 translate-y-0" : "border-border/40 opacity-20 translate-y-1"
          )}
        >
          ≡ {l}
        </div>
      ))}
      <div
        className={cn(
          "rounded-lg border px-2.5 py-1.5 font-mono text-[10.5px] transition-all duration-500",
          i === 4 || i === 5
            ? "border-emerald-500/60 bg-emerald-500/10 text-emerald-600 opacity-100"
            : i === 6
              ? "border-red-500/50 bg-red-500/5 text-red-500 opacity-100 line-through"
              : "border-border/40 opacity-20"
        )}
      >
        {i === 6 ? "container app-1:1234 —docker rm→ gone" : "🐳 container running · ports 80→8080"}
      </div>
      <p className="text-[10px] text-muted-foreground">Layers are cached and shared — delete the container, the image survives.</p>
    </div>
  );
};

/* CH 20 — nginx round robin upstreams */
const LoadBalanced = () => {
  const i = useLoop(8, 700);
  const target = i % 2; // alternate
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <Chip active={i % 3 !== 2}>🌐 client</Chip>
        <span className="text-[10px] font-mono text-primary">→ nginx :80</span>
        <Chev target={target} />
      </div>
      <div className="grid grid-cols-2 gap-2">
        {["app-1", "app-2"].map((up, k) => (
          <div
            key={up}
            className={cn(
              "rounded-lg border px-2.5 py-2 font-mono text-[11px] transition-all duration-300",
              target === k ? "border-emerald-500/60 bg-emerald-500/10 text-emerald-600" : "border-border/50 text-muted-foreground"
            )}
          >
            {up} {target === k ? "← 200 OK" : "idle"}
          </div>
        ))}
      </div>
      <p className="text-[10px] text-muted-foreground">Round-robin: request {Math.floor(i / 2) + 1} → {target === 0 ? "app-1" : "app-2"}; one dies? the other takes over with `backup`.</p>
    </div>
  );
};
const Chev = ({ target }: { target: number }) => (
  <span className={cn("font-mono text-xs transition-colors duration-300", target === 0 ? "text-emerald-500" : "text-violet-500")}>{target === 0 ? "↖ app-1" : "↗ app-2"}</span>
);

/* CH 21 — hardening: ports close, brute force blocked */
const Hardening = () => {
  const i = useLoop(7, 650);
  const ports = [
    { p: "22 ssh", keep: true },
    { p: "23 telnet", keep: false },
    { p: "21 ftp", keep: false },
    { p: "3306 mysql", keep: false },
  ];
  return (
    <div className="grid grid-cols-2 gap-3">
      <div className="space-y-1.5">
        {ports.map((pt, k) => {
          const closed = !pt.keep && i >= k + 1;
          return (
            <div key={pt.p}>
              <Chip active={pt.keep && i === 0} done={closed} danger={closed}>
                {closed ? "🔒 " : "🔓 "}
                {pt.p}
                {closed ? " closed ✓" : pt.keep ? " — only door left open" : ""}
              </Chip>
            </div>
          );
        })}
        <p className="text-[9.5px] text-muted-foreground mt-1">ufw default deny → allow OpenSSH — every extra port is attack surface.</p>
      </div>
      <MiniTerm>
        <p className="text-slate-500">$ tail -f /var/log/auth.log</p>
        <div className={cn("font-mono text-[10px] text-red-400 transition-all duration-300", i >= 3 ? "opacity-100" : "opacity-30")}>
          Failed password for root from 203.0.113.66 ×412
        </div>
        <div className={cn("font-mono text-[10px] mt-1 transition-all duration-300", i >= 4 ? "text-amber-400 opacity-100" : "opacity-30 text-muted-foreground")}>
          fail2ban: ban 203.0.113.66 → ufw DENY ⛓
        </div>
        <div className={cn("font-mono text-[10px] mt-1 text-emerald-400 transition-all duration-300", i >= 5 ? "opacity-100" : "opacity-0")}>
          brute force stopped — key-only auth from here
        </div>
      </MiniTerm>
    </div>
  );
};

/* ---------------------------------------------------------------- */
/* registry + section                                               */
/* ---------------------------------------------------------------- */

type Anim = { title: string; hint: string; C: FC };

const ANIMS: Record<number, Anim[]> = {
  1: [{ title: "Where Linux lives", hint: "The four layers every command passes through.", C: OSLayers }],
  2: [{ title: "The tree under /", hint: "Everything hangs off / — watch the branches grow.", C: FSTree }],
  3: [
    { title: "cp — duplication", hint: "Original stays.", C: CopyLane },
    { title: "mv & rm", hint: "mv relocates; rm is instant and unrecoverable.", C: MoveLane },
    { title: "rm second look", hint: "No trash bin — learn --flag safety early.", C: RmLane },
  ],
  4: [{ title: "grep scanning a log", hint: "The scanner walks the file; matches stream out.", C: GrepScan }],
  5: [{ title: "chmod digit decoder", hint: "One octal digit per class: r=4, w=2, x=1.", C: ChmodCalc }],
  6: [{ title: "sudo in action", hint: "Group membership → password → root for one command.", C: SudoFlow }],
  7: [{ title: "Life and death of a process", hint: "fork → CPU → I/O wait → kill.", C: ProcCycle }],
  8: [{ title: "A packet's journey", hint: "DNS lookup, TCP handshake, HTTP round trip.", C: PacketJourney }],
  9: [{ title: "What apt does", hint: "From your keystroke to a running service.", C: APT_ANIM }],
  10: [{ title: "systemd dependency dance", hint: "Units start in parallel, honoring what they need.", C: SYSTEMD_ANIM }],
  11: [{ title: "Streaming logs live", hint: "journalctl -f with a grep filter riding on top.", C: LogStream }],
  12: [{ title: "Disk filling up", hint: "Watch df climb and what to reclaim first.", C: DiskFill }],
  13: [{ title: "SSH handshake", hint: "Trust is established before any password — or key.", C: SSH_ANIM }],
  14: [{ title: "Live metrics", hint: "CPU, memory, I/O wait — four tools read these.", C: LiveMetrics }],
  15: [{ title: "5,000 lines → 213", hint: "Pipes pass raw tokens between tiny stages.", C: Pipeline }],
  16: [{ title: "The cron clock", hint: "Five fields decide *when* — watch minute 30 fire.", C: CronClock }],
  17: [{ title: "export: the only gate", hint: "Children inherit exported vars, nothing else.", C: ExportFlow }],
  18: [{ title: "Commits & branches", hint: "Branch, build the fix, merge back into main.", C: GitGraph }],
  19: [{ title: "Docker layers → container", hint: "Layers are cached; containers are disposable.", C: DockerLayers }],
  20: [{ title: "Load balancing live", hint: "Round-robin between two upstreams, request by request.", C: LoadBalanced }],
  21: [{ title: "Hardening day one", hint: "Close ports, ban brute force, allow SSH only.", C: Hardening }],
  22: [{ title: "The troubleshooting loop", hint: "Same loop every time — symptoms to verified fix.", C: TTR_ANIM }],
  23: [{ title: "An automation pipeline", hint: "Script the boring parts; humans review failures.", C: CI_ANIM }],
  24: [{ title: "Boot, step by step", hint: "Firmware → kernel → initramfs → systemd.", C: BOOT_ANIM }],
  25: [{ title: "Incident, minute by minute", hint: "The capstone choreography you practiced.", C: INC_ANIM }],
};

export function ChapterAnimations({ chapter }: { chapter: number }) {
  const anims = ANIMS[chapter];
  if (!anims) return null;
  return (
    <section className="animate-fade-up delay-2">
      <div className="flex items-center gap-2 mb-3">
        <PlayCircle className="h-5 w-5 text-violet-500" />
        <h2 className="text-base font-bold tracking-tight">Watch it run</h2>
        <span className="text-[11px] text-muted-foreground">live visual demos for this chapter</span>
      </div>
      <div className={cn("grid grid-cols-1 gap-3", anims.length > 1 ? "lg:grid-cols-2" : "")}>
        {anims.map((a) => (
          <Card key={a.title} className="hover-lift">
            <CardContent className="p-4">
              <p className="text-sm font-semibold">{a.title}</p>
              <p className="text-xs text-muted-foreground mb-3">{a.hint}</p>
              <a.C />
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
