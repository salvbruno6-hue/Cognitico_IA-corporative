# Hermes Context Engine Plugins -> ELO Boundary - 2026-09-20

## Finding

Hermes context engines are provider plugins. One engine is active at a time, selection is configuration-driven, and plugin engines are not auto-activated. The engine lifecycle includes session start, response updates, compression decisions, compression, and session end/reset.

## ELO adaptation

EXT-CONTEXT-PLUGIN-HERMES is a refinement of the existing ELO context candidate, not a second context authority.

- provenance is mandatory;
- plugin identity and tenant scope are mandatory;
- discovery alone is OBSERVATION;
- explicit activation produces only CANDIDATE;
- activation is never granted by this boundary;
- exclusive-provider semantics are preserved as a constraint;
- lifecycle events are evidence, not authority;
- ELO Context and Evolution Gate remain authoritative.

## Safety boundary

An external engine must not replace canonical ELO context assembly, provenance, authorization, or memory authority merely because Hermes can activate it.

## Non-goals

- no Hermes configuration mutation;
- no automatic engine activation;
- no context compression implementation;
- no replacement of ELO ContextResolution;
- no Core promotion.
