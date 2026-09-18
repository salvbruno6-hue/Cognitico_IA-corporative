import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const roots = ["src", "README.md", ".env.example"];
const forbidden = [
  /elo_elo/i,
  /eloelo/i,
  /ELO_COGNITIVE_API_URL/,
  /ELO_HERMES_ENDPOINT/,
];
const textExtensions = new Set([".ts",".tsx",".js",".mjs",".md",".json",".example"]);

function collect(path, relative = path) {
  const absolute = join(root, path);
  const stat = statSync(absolute);
  if (stat.isFile()) return [[relative, readFileSync(absolute, "utf8")]];
  const result = [];
  for (const entry of readdirSync(absolute)) {
    const child = path + "/" + entry;
    const childRelative = relative + "/" + entry;
    const childStat = statSync(join(root, child));
    if (childStat.isDirectory()) result.push(...collect(child, childRelative));
    else if (textExtensions.has(entry.includes(".") ? entry.slice(entry.lastIndexOf(".")) : "")) {
      result.push([childRelative, readFileSync(join(root, child), "utf8")]);
    }
  }
  return result;
}

const findings = [];
for (const rootPath of roots) {
  for (const [file, content] of collect(rootPath)) {
    for (const pattern of forbidden) {
      if (pattern.test(content)) findings.push(`${file}: ${pattern}`);
    }
  }
}
if (findings.length) {
  console.error("ELO Web legacy dependency guard failed:");
  console.error(findings.join("\n"));
  process.exit(1);
}
console.log("ELO Web legacy dependency guard: PASS");
