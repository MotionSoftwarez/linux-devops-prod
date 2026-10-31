const fs = require("fs");
const p = "frontend/components/terminal/commandRegistry.ts";
let s = fs.readFileSync(p, "utf8");
const old = `commands.history = wrap((_args, state) => ({
  output: state.history.map((cmd, i) => (i + 1).toString() + "  " + cmd).join("\n") || "(no history)",
  state,
  exitCode: 0,
});`;
const nv = `commands.history = wrap((_args, state) => {
  const lines = state.history.map((cmd, i) => (i + 1).toString() + "  " + cmd);
  return { output: lines.join("\\n") || "(no history)", state, exitCode: 0 };
};`;
if (s.includes(old)) {
  s = s.split(old).join(nv);
  fs.writeFileSync(p, s);
  console.log("replaced history handler");
} else {
  console.log("OLD NOT FOUND");
  const idx = s.indexOf("commands.history");
  console.log(JSON.stringify(s.slice(idx, idx + 200)));
}
