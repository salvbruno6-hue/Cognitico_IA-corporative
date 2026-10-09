# Hermes Model Capability Metadata — governed candidate

## Purpose
Capture model capability, context-window, pricing and training-tier metadata as evidence for the existing canonical ModelSelector.

## Reused owner
The existing `src/elo/cognitive/routing/model_selection.py` remains the sole canonical model selection owner. This contract does not replace or duplicate it.

## Scope
The candidate records model identifier, capabilities, context-window capacity, input/output cost metadata, training-tier classification and provenance. Unknown, experimental or unverified training tiers generate a policy-review warning. Invalid or incomplete metadata is blocked.

## Symbiont boundary
The Simbionte may observe and compare this metadata as candidate evidence. It may not route from it, promote it, or convert one observation into generalized learning. Any future operational use remains subject to Governed Learning and Evolution Gate.

## Governance
This contract is deterministic and has no provider I/O. It does not select a model, route a request, call a provider, expose credentials, or authorize execution. `routing_permitted` is always false.

No new router, selector, provider authority, credential store, memory, Evolution Gate, or promotion mechanism is introduced.

## Promotion boundary
CI/Evolution Gate success means technical governance validation only. It does not constitute production outcome evidence or authorize autonomous promotion.
