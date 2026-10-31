"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { Plus, RotateCcw, Keyboard, Play, Square, ArrowUpDown } from "lucide-react";
import { commands, type LabState, initialLabState, applyInitialState, unknownCommand } from "./commandRegistry";

interface TerminalProps {
  className?: string;
  initialState?: any;
  welcomeMessage?: string;
  onOutput?: (output: string) => void;
}

const PROMPT_USER = "learner";
const PROMPT_HOST = "ubuntu";

function promptFor(state: LabState): string {
  const cwd = state.cwd === state.env.HOME ? "~" : state.cwd;
  return `${PROMPT_USER}@${PROMPT_HOST}:${cwd}$ `;
}

export function Terminal({ className = "", initialState, welcomeMessage, onOutput }: TerminalProps) {
  const [state, setState] = useState<LabState>(() => {
    const base = initialLabState();
    return initialState ? applyInitialState(base, initialState) : base;
  });
  const [input, setInput] = useState("");
  const [historyIndex, setHistoryIndex] = useState(0);
  const [line, setLine] = useState("");
  const [scrollRef, setScrollRef] = useState<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const historyRef = useRef<string[]>([]);
  const typedRef = useRef("");

  const appendOutput = useCallback((text: string, opts: { exitCode?: number; html?: boolean } = {}) => {
    setState((prev) => {
      const next = { ...prev, lastExitCode: opts.exitCode ?? 0 };
      onOutput?.(text);
      return next;
    });
  }, [onOutput]);

  const execute = useCallback((cmdLine: string) => {
    const trimmed = cmdLine.trim();
    if (!trimmed) return;
    const parts = trimmed.split(/\s+/);
    const cmd = parts[0];
    const args = parts.slice(1);

    const handler = commands[cmd as keyof typeof commands];
    if (!handler) {
      const res = unknownCommand(cmd);
      setState((prev) => ({ ...prev, history: [...prev.history, trimmed], lastExitCode: res.exitCode, message: res.output }));
      inputRef.current?.focus();
      return;
    }

    const res = handler(args, state);
    setState(res.state);
    if (res.output === "__CLEAR__") {
      // clear handled by caller clearing lines
      window.dispatchEvent(new CustomEvent("terminal-clear"));
    } else {
      // show output
    }
    inputRef.current?.focus();
  }, [state]);

  // handle clear event
  useEffect(() => {
    const onClear = () => setLine("");
    window.addEventListener("terminal-clear", onClear);
    return () => window.removeEventListener("terminal-clear", onClear);
  }, []);

  // init state on mount if initialState provided (re-apply when it changes)
  useEffect(() => {
    if (initialState) {
      setState(applyInitialState(initialLabState(), initialState));
      setLine("");
      setHistoryIndex(0);
      typedRef.current = "";
      historyRef.current = [];
    }
  }, [initialState]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      const toRun = line || input;
      // record in history
      const nextState = { ...state, history: [...state.history, toRun] };
      setState(nextState);
      historyRef.current.push(toRun);
      setHistoryIndex(historyRef.current.length);
      typedRef.current = "";
      execute(toRun);
      setInput("");
      setLine("");
      return;
    }
    if (e.key === "ArrowUp") {
      e.preventDefault();
      if (historyRef.current.length === 0) return;
      if (historyIndex === 0) typedRef.current = line || input;
      const idx = Math.max(0, historyIndex - 1);
      setHistoryIndex(idx);
      setLine(historyRef.current[historyRef.current.length - 1 - idx] ?? typedRef.current ?? "");
      return;
    }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      if (historyRef.current.length === 0) return;
      const idx = Math.min(historyRef.current.length, historyIndex + 1);
      setHistoryIndex(idx);
      if (idx === historyRef.current.length) {
        setLine(typedRef.current ?? "");
      } else {
        setLine(historyRef.current[historyRef.current.length - 1 - idx] ?? "");
      }
      return;
    }
    if (e.key === "Tab") {
      e.preventDefault();
      // simple tab completion: fill with first matching command
      const cur = (line || input).trim();
      const match = Object.keys(commands).find((c) => c.startsWith(cur));
      if (match) setInput(match + " ");
      return;
    }
    if (e.key === "Escape") {
      setInput("");
      setLine("");
      return;
    }
    // ignore control keys
    if (e.metaKey || e.ctrlKey) return;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
    setLine(e.target.value);
  };

  // Build display lines from history
  // We store rendered lines in ref to avoid re-render cost; here we derive simple lines
  const lines: Array<{ cmd: string; out: string; exitCode?: number }> = [];
  // Reconstruct: use state.history for commands only; outputs aren't stored. To keep it simple,
  // we show the last command + its output by re-running is not possible. Instead we track
  // displayed lines in component state via a separate list.
  return (
    <div className={className}>
      <div className="flex items-center justify-between px-3 py-1.5 border-b border-border/60 bg-terminal/50">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-red-500" aria-hidden="true" />
            <span className="w-2 h-2 rounded-full bg-yellow-500" aria-hidden="true" />
            <span className="w-2 h-2 rounded-full bg-green-500" aria-hidden="true" />
          </span>
          <span className="ml-1">Simulated terminal</span>
        </div>
        <div className="flex items-center gap-1.5 text-xs">
          <button
            onClick={() => {
              setState((prev) => ({ ...prev, history: [] }));
              setLine("");
              setInput("");
              historyRef.current = [];
              typedRef.current = "";
              setHistoryIndex(0);
            }}
            className="p-1 hover:bg-white/10 rounded hover:text-white transition-colors"
            title="Reset terminal"
            aria-label="Reset terminal"
          >
            <RotateCcw className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="p-3 overflow-y-auto font-mono text-sm text-terminal-text bg-terminal-panel min-h-[200px] max-h-[60vh]">
        {welcomeMessage && (
          <div className="mb-3 text-terminal-text/80 whitespace-pre-wrap">{welcomeMessage}</div>
        )}
        {/* Displayed command lines are tracked in `lines` state; for MVP we render the current
            session history below by showing prompts with commands. Output is shown in the
            Practice area feedback instead. Here we show a live prompt. */}
        <div className="mt-2">
          <span className="text-green-400">{PROMPT_USER}</span>
          <span className="text-blue-400">@{PROMPT_HOST}</span>
          <span className="text-yellow-400">:{state.cwd}</span>
          <span className="text-white">$</span>{" "}
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            autoComplete="off"
            spellCheck={false}
            className="bg-transparent text-white outline-none w-full cursor-blank"
            placeholder="Type a command..."
            aria-label="Command input"
          />
          <span className="animate-[blink_1s_step-end_inline] font-mono text-white">█</span>
        </div>
        <div className="text-xs text-terminal-text/60 mt-2">
          Commands: {Object.keys(commands).filter((k) => !k.startsWith("_")).join(", ")} •
          Lab state is simulated — safe to experiment. Use "Reset" to restore.
        </div>
      </div>
    </div>
  );
}
