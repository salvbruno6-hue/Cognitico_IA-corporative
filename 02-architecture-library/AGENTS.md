# ELO Architecture Library — Local Agent Rules

## Scope

This directory contains architecture-level artifacts. Treat explicitly approved baseline artifacts as normative.

## Rules

1. Do not document an implementation as canonical merely because it exists in code.
2. Use ADRs for durable decisions with meaningful alternatives or consequences.
3. Distinguish current state from target state.
4. Label proposed capabilities as PROPOSED/ROADMAP rather than silently presenting them as implemented.
5. Preserve architecture boundaries between cognitive, data, AI, governance, and system layers.
6. Do not create duplicate architecture documents for the same capability; extend the canonical artifact when appropriate.
7. Any architecture change affecting Tenant, identity, security, persistence, decision authority, or autonomous behavior requires explicit review.

## Architecture evidence

When describing implementation maturity, use the repository maturity vocabulary:

0 absent
1 conceptual
2 documented
3 contracted
4 implemented
5 tested
6 verified
7 operationally evidenced

Never claim a higher level without corresponding evidence.
