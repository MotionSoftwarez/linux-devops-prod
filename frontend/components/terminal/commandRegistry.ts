/**
 * Simulated shell command registry.
 *
 * Every command is a pure function: (args: string[], state: LabState) => CommandResult.
 * It never touches the host — all state lives in the browser. This keeps the lab
 * safe, deterministic, and clearly simulated (labeled as such in the UI).
 */

export interface FileNode {
  type: "file" | "dir";
  content?: string;
  mode?: number;
  owner?: string;
  group?: string;
  size?: number;
  mtime?: string;
  children?: Record<string, FileNode>;
}

export interface ServiceState {
  name: string;
  running: boolean;
  port?: number;
}

export interface LabState {
  cwd: string;
  files: Record<string, FileNode>;
  services: Record<string, ServiceState>;
  ports: Record<number, string>;
  env: Record<string, string>;
  users: Record<string, { groups: string[] }>;
  history: string[];
  lastExitCode: number;
  message?: string;
}

export interface CommandResult {
  output: string;
  state: LabState;
  exitCode: number;
  html?: boolean;
}

function clone<T>(v: T): T {
  return JSON.parse(JSON.stringify(v));
}

function ensureDir(state: LabState, path: string): FileNode {
  const parts = path.split("/").filter(Boolean);
  let node = state.files[""];
  if (!node) {
    node = { type: "dir", children: {}, mode: 0o755, owner: "root", group: "root" };
    state.files[""] = node;
  }
  let cur = node;
  let curPath = "";
  for (const p of parts) {
    curPath += "/" + p;
    if (!cur.children) cur.children = {};
    if (!cur.children[p]) {
      cur.children[p] = { type: "dir", children: {}, mode: 0o755, owner: "root", group: "root" };
    }
    cur = cur.children[p];
  }
  return cur;
}

function getNode(state: LabState, path: string): FileNode | null {
  let abs = path;
  if (!path.startsWith("/")) abs = state.cwd === "/" ? "/" + path : state.cwd + "/" + path;
  abs = normalize(abs);
  const parts = abs.split("/").filter(Boolean);
  let cur: FileNode | null = state.files[""] || null;
  if (!cur) return null;
  for (const p of parts) {
    if (!cur || cur.type !== "dir" || !cur.children?.[p]) return null;
    cur = cur.children[p];
  }
  return cur;
}

function normalize(p: string): string {
  const parts = p.split("/");
  const out: string[] = [];
  for (const part of parts) {
    if (part === "" || part === ".") continue;
    if (part === "..") { out.pop(); continue; }
    out.push(part);
  }
  return "/" + out.join("/");
}

function basename(p: string): string {
  const parts = p.split("/").filter(Boolean);
  return parts[parts.length - 1] || "/";
}

export function initialLabState(): LabState {
  const root: FileNode = {
    type: "dir",
    mode: 0o755,
    owner: "root",
    group: "root",
    children: {
      home: {
        type: "dir",
        mode: 0o755,
        owner: "root",
        group: "root",
        children: {
          learner: {
            type: "dir",
            mode: 0o755,
            owner: "learner",
            group: "learner",
            children: {},
          },
        },
      },
      etc: {
        type: "dir",
        mode: 0o755,
        owner: "root",
        group: "root",
        children: {
          os_release: {
            type: "file",
            content: 'NAME="Ubuntu"\nVERSION="22.04.3 LTS"\nID=ubuntu\n',
            mode: 0o644,
            owner: "root",
            group: "root",
          },
          hostname: {
            type: "file",
            content: "ubuntu\n",
            mode: 0o644,
            owner: "root",
            group: "root",
          },
          passwd: {
            type: "file",
            content: "root:x:0:0:root:/root:/bin/bash\nlearner:x:1000:1000:Learner:/home/learner:/bin/bash\n",
            mode: 0o644,
            owner: "root",
            group: "root",
          },
        },
      },
      var: {
        type: "dir",
        mode: 0o755,
        owner: "root",
        group: "root",
        children: {
          log: {
            type: "dir",
            mode: 0o755,
            owner: "root",
            group: "root",
            children: {},
          },
        },
      },
      tmp: {
        type: "dir",
        mode: 0o777,
        owner: "root",
        group: "root",
        children: {},
      },
    },
  };
  return {
    cwd: "/home/learner",
    files: { "": root },
    services: {},
    ports: {},
    env: { USER: "learner", HOME: "/home/learner", SHELL: "/bin/bash", PATH: "/usr/bin:/bin" },
    users: {
      root: { groups: ["root"] },
      learner: { groups: ["learner"] },
    },
    history: [],
    lastExitCode: 0,
  };
}

export function applyInitialState(base: LabState, initial: any): LabState {
  const state = clone(base);
  if (initial.cwd) state.cwd = initial.cwd;
  if (initial.files) {
    for (const [path, node] of Object.entries(initial.files)) {
      const dir = path.split("/").slice(0, -1).join("/");
      ensureDir(state, dir);
      state.files[path] = node as FileNode;
    }
  }
  if (initial.services) state.services = { ...state.services, ...initial.services };
  if (initial.ports) state.ports = { ...state.ports, ...initial.ports };
  if (initial.env) state.env = { ...state.env, ...initial.env };
  return state;
}

type CommandHandler = (args: string[], state: LabState) => CommandResult;
export const commands: Record<string, CommandHandler> = {};

function wrap(fn: CommandHandler): CommandHandler {
  return (args, state) => {
    const res = fn(args, state);
    res.state.history = [...state.history, args.join(" ")];
    return res;
  };
}

commands.pwd = wrap((_args, state) => ({
  output: state.cwd,
  state,
  exitCode: 0,
}));

commands.clear = wrap((_args, state) => ({
  output: "__CLEAR__",
  state,
  exitCode: 0,
}));

commands.history = wrap((_args, state) => {
  const lines: string[] = [];
  for (let i = 0; i < state.history.length; i++) {
    lines.push((i + 1).toString() + "  " + state.history[i]);
  }
  return { output: lines.join("\n") || "(no history)", state, exitCode: 0 };
});

commands.echo = wrap((args, state) => {
  const out: string[] = [];
  for (const a of args) {
    if (a.startsWith("$")) out.push(state.env[a.slice(1)] ?? "");
    else out.push(a);
  }
  return { output: out.join(" "), state, exitCode: 0 };
});

commands.ls = wrap((args, state) => {
  const target = args[0] ?? ".";
  const node = getNode(state, target);
  if (!node) {
    return { output: "ls: cannot access '" + target + "': No such file or directory", state, exitCode: 2 };
  }
  if (node.type === "file") return { output: basename(target), state, exitCode: 0 };
  const names: string[] = [];
  if (node.children) {
    for (const k of Object.keys(node.children)) names.push(k);
    names.sort();
  }
  return { output: names.join("  "), state, exitCode: 0 };
});

commands.cd = wrap((args, state) => {
  const target = args[0] ?? state.env.HOME ?? "/";
  let abs = target;
  if (!target.startsWith("/")) abs = state.cwd === "/" ? "/" + target : state.cwd + "/" + target;
  abs = normalize(abs);
  const node = getNode(state, abs);
  if (!node || node.type !== "dir") {
    return { output: "cd: " + target + ": No such directory", state, exitCode: 1 };
  }
  const next = clone(state);
  next.cwd = abs;
  return { output: "", state: next, exitCode: 0 };
});

commands.cat = wrap((args, state) => {
  const target = args[0];
  if (!target) return { output: "cat: missing operand", state, exitCode: 1 };
  const node = getNode(state, target);
  if (!node) return { output: "cat: " + target + ": No such file or directory", state, exitCode: 1 };
  if (node.type === "dir") return { output: "cat: " + target + ": Is a directory", state, exitCode: 1 };
  return { output: node.content ?? "", state, exitCode: 0 };
});

commands.which = wrap((args, state) => {
  const cmd = args[0];
  if (!cmd) return { output: "which: missing operand", state, exitCode: 1 };
  if (commands[cmd]) return { output: "/bin/" + cmd, state, exitCode: 0 };
  return { output: "", state, exitCode: 1 };
});
commands.type = commands.which;

commands.uname = wrap((args, state) => {
  const flag = args[0];
  if (flag === "-a") return { output: "Linux ubuntu 5.15.0-XX-generic #1 SMP GNU/Linux", state, exitCode: 0 };
  if (flag === "-r") return { output: "5.15.0-XX-generic", state, exitCode: 0 };
  return { output: "Linux", state, exitCode: 0 };
});

commands.whoami = wrap((_args, state) => ({ output: "learner", state, exitCode: 0 }));
commands.id = wrap((_args, state) => ({ output: "uid=1000(learner) gid=1000(learner) groups=1000(learner)", state, exitCode: 0 }));

export function unknownCommand(cmd: string): CommandResult {
  return {
    output: "linotutor: " + cmd + ": command not found",
    state: initialLabState(),
    exitCode: 127,
  };
}
