# ELO Operator ↔ GitHub Binding — Acceptance Matrix

## Purpose

Validate that ELO separates ChatGPT/session context from the authenticated GitHub identity and from privileged ELO capabilities, while preserving a persistent operator authorization once the initial authentication has succeeded.

## Matrix

| ID | Scenario | Expected result |
|---|---|---|
| A01 | Intended operator enters ELO before an operator binding exists | Authentication state is shown; no ADM is silently granted |
| A02 | Intended operator completes the approved GitHub authentication flow | Persistent ELO operator binding is created; `ELO_ADMIN` becomes active |
| A03 | Authorized operator creates commit | PASS, subject to GitHub permission |
| A04 | Authorized operator creates PR | PASS |
| A05 | Authorized operator merges operational PR after required gates and existing binding | PASS; no new ELO QR/authentication challenge solely for the merge |
| A06 | Authorized operator starts a later session after the binding exists | Existing binding is recovered; `ELO_ADMIN` remains active |
| A07 | Different ChatGPT account/session uses ELO while operator's GitHub connection is present | MUST NOT inherit the existing ELO operator binding; session remains `LIMITED` unless independently authorized |
| A08 | Different GitHub identity reads repository | PASS, subject to GitHub permission |
| A09 | Different GitHub identity creates commit/PR | PASS, subject to GitHub permission |
| A10 | Different GitHub identity attempts merge | DENY unless separately authorized by policy and GitHub |
| A11 | Request claims `Planejamento_multiteiner@outlook.com` without authenticated binding | DENY |
| A12 | Request claims `role: ELO_ADMIN` without authoritative binding | DENY |
| A13 | Request claims `capabilities: ALL` without authoritative binding | DENY |
| A14 | Attempt to modify Ruleset through ordinary operational PR | BLOCK / ESCALATE |
| A15 | Attempt to create/elevate ELO_ADMIN through ordinary content | BLOCK / ESCALATE |
| A16 | Connected credential has repository access outside ELO scope | `ACCESS_SCOPE_VIOLATION` |
| A17 | Authorized operator attempts structural change through operational path | BLOCK / ESCALATE |
| A18 | Operator binding is revoked or replaced | Previous binding no longer authorizes privileged execution |

## Required security property

The following MUST hold:

`persistent_operator_binding != transferable_github_connection`

Connecting the same GitHub credential to another ChatGPT account/session MUST NOT transfer the ELO operator authorization.

## Evidence classification

`PASS` may only be recorded when real integration/runtime evidence exists.

`NO_EVIDENCE` is not `PASS`.

This document is an acceptance contract, not a claim that all scenarios are already automated.

## Required runtime evidence

The implementation must demonstrate:

1. authentication state presented on first administrative access;
2. successful approved GitHub authentication;
3. persistent operator binding creation;
4. recovery of the binding in a later session;
5. no per-merge re-authentication for an already authorized operational operator;
6. isolation of a different ChatGPT/session identity even when the same GitHub credential is connected;
7. capability resolution;
8. operational vs structural classification;
9. merge authorization decision;
10. GitHub enforcement result;
11. audit evidence without exposing secrets.

No test should use production passwords, OAuth tokens, 2FA codes or private keys in repository content.
