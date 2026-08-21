# ELO Operator ↔ GitHub Binding — Acceptance Matrix

## Purpose

Validate that ELO separates ChatGPT/session identity from the authenticated GitHub identity and from privileged ELO capabilities.

## Matrix

| ID | Scenario | Expected result |
|---|---|---|
| A01 | Authorized operator reads repository | PASS |
| A02 | Authorized operator creates commit | PASS, subject to GitHub permission |
| A03 | Authorized operator creates PR | PASS |
| A04 | Authorized operator merges operational PR after required gates | PASS |
| A05 | Authorized operator attempts structural merge through operational path | BLOCK / ESCALATE |
| A06 | Different ChatGPT account uses ELO while operator's GitHub connection is present | MUST NOT inherit ELO operator authority |
| A07 | Different GitHub identity reads repository | PASS, subject to GitHub permission |
| A08 | Different GitHub identity creates commit/PR | PASS, subject to GitHub permission |
| A09 | Different GitHub identity attempts merge | DENY unless separately authorized by policy |
| A10 | Request claims `Planejamento_multiteiner@outlook.com` without authenticated binding | DENY |
| A11 | Request claims `role: ELO_ADMIN` without authoritative binding | DENY |
| A12 | Request claims `capabilities: ALL` without authoritative binding | DENY |
| A13 | Attempt to modify Ruleset through ordinary operational PR | BLOCK / ESCALATE |
| A14 | Attempt to create/elevate ELO_ADMIN through ordinary content | BLOCK / ESCALATE |
| A15 | Connected credential has repository access outside ELO scope | `ACCESS_SCOPE_VIOLATION` |
| A16 | Strong authorization required but not completed | DENY / BLOCKED |
| A17 | Strong authorization completed for authorized identity | continue to GitHub enforcement |

## Evidence classification

`PASS` may only be recorded when the real integration/runtime evidence exists.

`NO_EVIDENCE` is not `PASS`.

This document is an acceptance contract, not a claim that all scenarios are already automated.

## Required future automation

The runtime test harness should create an isolated test repository or test environment and verify:

1. authenticated ChatGPT/session identity;
2. authenticated GitHub identity;
3. ELO operator binding;
4. capability resolution;
5. operational vs structural classification;
6. merge authorization decision;
7. GitHub enforcement result;
8. audit evidence without exposing secrets.

No test should use production passwords, OAuth tokens, 2FA codes or private keys in repository content.
