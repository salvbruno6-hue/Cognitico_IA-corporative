# EXT-MEMPROVIDER-HERMES — Bounded Runtime Promotion — 2026-10-04

Candidate: `EXT-MEMPROVIDER-HERMES`  
Owner: ELO Memory  
Canonical runtime: `ELOKnowledgeProvider.retrieve`

## Change

The existing memory-provider boundary is now fail-closed for two runtime dimensions:

- only `retrieve` operations are admissible;
- at most `8` provenance/source references are accepted per signal.

Signals outside these bounds are rejected before adaptation.

## Authority preservation

No new authority was introduced.

- ELO Memory remains the owner of memory retrieval.
- The adapter remains retrieval-only.
- `canonical_write`, mutation, and promotion remain rejected.
- Provider activation remains explicit.
- Existing `RuntimeOperationalEvidence` remains the evidence mechanism.
- Existing governed implementation loop and Evolution Gate remain the decision path.

## Validation target

The added tests cover:

1. non-retrieval operation rejection;
2. source-reference overflow rejection;
3. acceptance at the exact boundary;
4. preservation of the existing candidate-only controls.

## Evidence status

This change establishes a bounded runtime control and controlled validation.

It does **not** establish production proof, external-provider performance, or canonical promotion. Production outcome remains `production_proven=false` until independently observed through the existing runtime evidence path.
