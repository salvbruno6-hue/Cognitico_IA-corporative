import assert from "node:assert/strict";
import { test } from "node:test";

import { mergeGrantResource as validate } from "../src/lib/authorization-resource.ts";
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
