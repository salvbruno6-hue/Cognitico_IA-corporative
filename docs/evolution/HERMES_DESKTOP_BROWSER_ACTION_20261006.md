# Hermes Desktop Browser Action — governed candidate

## Purpose

Register an ELO-side observational contract for desktop-browser navigation/extraction,
without introducing a browser executor or new authorization authority.

## Canonical owners reused

- ExecutionRouter / computer-use routing for future routing.
- ExecutionBoundary for any future execution.
- Existing MCP/browser capability contracts for browser navigation.
- Existing ELO provenance/evidence controls.

## Candidate scope

Allowed as evidence classification:
- HTTP/HTTPS navigation intended for read-only observation.
- Read-only extraction.

Explicitly blocked in this candidate:
- click
- submit
- write
- authentication or credential injection
- external state-changing operations

## Governance

The assessment is deterministic and has no I/O. It never invokes a browser.
Even a request carrying an authorization reference remains CANDIDATE_ONLY and
execution_permitted=False. Any future execution must pass through the existing
canonical ExecutionBoundary and its mandatory controls.

No Hermes code is modified. No business operation is performed. No credentials
are accepted as browser payload. No new executor, router, authorization authority,
memory, Evolution Gate, or promotion mechanism is introduced.

## Provenance

Every candidate assessment requires a provenance reference and preserves request,
tenant, principal, mission, target URL digest, and scope metadata.

## Promotion boundary

This PR is technical/governed evidence only. A successful CI/Evolution Gate does
not constitute production outcome evidence and does not authorize merge or execution.
