# Governed external skills intake — mattpocock/skills

Status: FULL_CATALOG_VENDORED — manual-only discovery; runtime activation and canonical promotion not authorized.
Upstream: https://github.com/mattpocock/skills
License: MIT (copyright 2026 Matt Pocock; preserve license on any vendored copies).
Upstream package version observed: 1.3.2 (immutable source commit pinned below).

## Existing owners (do not replace)
- ELO Knowledge & Skills / Forge: specialist skills and context.
- Capability Registry / ExecutionRouter / ExecutionBoundary: discovery, routing and execution.
- Symbiont: evidence and candidate evaluation only.
- Evolution Gate: promotion authority.
- Existing PCP skill: `06-knowledge-engineering/SKILL_PLANEJAMENTO_MULTITEINER.md` (unchanged).

## Admission candidates
| Upstream skill | Potential ELO benefit | Required adaptation |
| --- | --- | --- |
| `skills/engineering/tdd` | Behavior-first tests and red/green feedback | Reuse existing ELO test seams and CI; no new test authority |
| `skills/engineering/diagnosing-bugs` | Reproducible bug diagnosis and evidence | Redact secrets; respect production read-only and governance gates |
| `skills/engineering/improve-codebase-architecture` | Identify deepening opportunities | Advisory only; do not auto-refactor or alter canonical boundaries |

## Installation boundary
The upstream README offers `npx skills@latest add mattpocock/skills -a <agent>`, Claude/Codex/Copilot plugin installs, and manual updates. No agent target or sandbox execution contract has been verified for ELO. Do not run an installer or copy all upstream skills into production before verifying supported agent/runtime, transitive references, and duplicated capabilities. Installing both a plugin and copied skills duplicates skills, according to upstream README.

## Gate checklist
1. Resolve exact upstream commit SHA and inventory all skill files, linked references, scripts and hooks.
2. Compare against existing ELO skills/Forge owners and record duplicates.
3. Static security review of commands, network, permissions, secret handling and prompt injection surfaces.
4. Select an ELO-compatible installation path and immutable revision, retaining MIT notice.
5. Run isolated behavioral tests for intended skills and negative tests for authorization/promotion boundaries.
6. Symbiont evidence assessment, existing CI and Evolution Gate; only then activate through canonical routing.

## Observed evidence
- Upstream README, LICENSE, package.json and three candidate SKILL.md files inspected via GitHub connector.
- Existing ELO PCP skill and skill change-awareness/governance paths inspected via GitHub connector.
- No Supabase schema/data mutation, PCP change, spreadsheet change or runtime activation.


## Integral source import — 2026-11-10

Source pinned immutably to `mattpocock/skills@4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`, upstream package v1.3.2 (MIT).
All **114 source files**, including **39 individual SKILL.md** definitions, are present in `vendor/mattpocock-skills/skills/`, with per-file Git blob hashes in `manifest.json`. LICENSE, upstream README and original Claude plugin manifest are preserved. No external installer or script was executed.

The canonical ELO inventory now has **39 namespaced discovery wrappers** at `.agents/skills/mattpocock-*/SKILL.md`; all carry `disable-model-invocation: true` plus Codex `allow_implicit_invocation: false`. The 27 upstream promoted packages are eligible for separate governed assessment; the 12 miscellaneous or in-progress packages stay explicitly non-promoted. Manual invocation is available to inspect source, not to bypass ELO permissions.

Upstream skills are NOT ELO-native by copying. The ELO Core, Forge, PCP skill, Symbiont, existing code-review adapter, Evolution Gate, branch protection and operator authorization remain canonical. Shell, network, new-package, hook or subagent actions requested inside imported instructions require distinct validation and authorization and are never executed during this import. Production and Supabase are unchanged.

### Evidence and boundaries

- `tests/test_mattpocock_skills_vendor_integrity.py` checks the full source inventory against the pinned Git blob SHA-1s and checks 39 manual-only wrappers.
- `VENDOR_PRESENT` is not `RUNTIME_ACTIVATED`, `TESTED`, `MERGED` or `PROMOTED`. These require CI and existing Symbiont/Evolution gates, and the appropriate human decision where applicable.
- No new skills are registered in the cognitive Core or Supabase; the external references remain in a separate, governed repository source namespace.
- The existing PR #1167 remains the ELO-native two-axis reviewer; this import does not replace or shadow it.
