import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import ts from "typescript";

const file = new URL("../src/lib/authorization-resource.ts", import.meta.url);
const source = readFileSync(file, "utf8");
const transpiled = ts.transpileModule(source, {
  compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext },
}).outputText;
const { mergeGrantResource: validate } = await import(`data:text/javascript;base64,${Buffer.from(transpiled).toString("base64")}`);
const sha = "A".repeat(40);

test("validates exact PR/SHA-bound merge grant resource", () => {
  assert.equal(validate("1237", sha), `pr:1237@${sha.toLowerCase()}`);
  assert.equal(validate("0", sha), null);
  assert.equal(validate("-1", sha), null);
  assert.equal(validate("1237", "abc"), null);
  assert.equal(validate("1237", "g".repeat(40)), null);
  assert.equal(validate("1237", "a".repeat(41)), null);
  assert.equal(validate("1237;drop", sha), null);
});
