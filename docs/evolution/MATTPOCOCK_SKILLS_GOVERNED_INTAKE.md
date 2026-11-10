# Governed external skills intake — mattpocock/skills

Status: CANDIDATE_ONLY — not installed, not activated, not canonical.
Upstream: https://github.com/mattpocock/skills
License: MIT (copyright 2026 Matt Pocock; preserve license on any vendored copies).
Upstream package version observed: 1.3.2 (not an immutable revision pin).

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
