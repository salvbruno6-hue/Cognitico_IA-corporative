# Hermes → ELO — Skill inventory change awareness (2026-10-12)

## Source observation

Upstream Hermes commits inspected on 2026-10-12 include `c098b2bf1ddad46c24c6ec01f5d8754555d23f6d`, which makes a skill written by another process visible to a running process by adding skill-file signatures to the index cache key, and `097fcaa1deec1903ece5abce8919c9937a57f3f4`, which announces skill changes once per turn. The current upstream also contains scanner hardening (`4e03f4581a0a19a08213f81f91e8e79c487fb556`) and catalog changes; these are observations, not ELO promotions.

## Candidate selected by the Symbiont filter

`EXT-SKILL-CHANGE-AWARENESS-HERMES` reuses **ELO Knowledge & Skills**. The ELO-side adaptation accepts governed skill-name/signature metadata and produces deterministic added/removed/changed evidence. It performs no filesystem scan, skill activation, tool execution, memory mutation, business operation, or Hermes mutation.

The mechanism is intentionally narrower than Hermes runtime behavior: it imports the useful invariant (external inventory changes must become observable) without importing Hermes cache, prompt, plugin, or activation authority.

## Controlled evidence

Baseline: externally changed inventory is not detected by the candidate fixture (`0.0`).

Adapted: deterministic delta identifies one added and one changed skill (`1.0`) and reproduces the same result across repeated evaluation.

This is controlled evidence only. It is not production proof.

## Mechanisms not introduced in this cycle

- Plugin catalog additions/updates: already covered by `EXT-PLUGIN-CATALOG-HERMES`; no new ELO owner is justified.
- Scanner false-positive hardening: useful upstream implementation detail, but no independent ELO capability was demonstrated; retain as observation for future admission-safety evaluation.
- Optional individual skills/plugins: content/catalog additions are not architectural capabilities and are not promoted by discovery.

## Governance

The candidate remains non-mutating and subordinate to the existing ELO Knowledge & Skills owner. Symbiont deep filtering, Evolution Gate, and existing learning governance remain authoritative. No SO instance is used as an architectural reference.
