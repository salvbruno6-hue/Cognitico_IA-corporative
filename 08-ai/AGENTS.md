# ELO AI Layer — Local Agent Rules

## Scope

This directory governs AI provider architecture, model usage, evaluation, and AI-specific policies.

## Provider boundary

Application and cognitive components should use the AI Gateway/provider contract rather than hard-coding a specific provider where the architecture requires abstraction.

## Model governance

Record, when relevant:

- provider;
- model;
- invocation context;
- purpose;
- limitations;
- evaluation status;
- provenance.

## Data protection

Do not send sensitive enterprise data to external providers without an authorized policy path.

## AI output

AI-generated content is not automatically evidence or organizational truth. It must be classified and, where required, validated against authoritative sources.

## Future capabilities

Do not implement autonomous learning or uncontrolled agent behavior merely because a provider supports it. Such behavior requires explicit ELO architecture and governance approval.
