# ELO Claude Reasoning and Agent Patterns

## Purpose

This document extracts publicly documented architectural patterns from Anthropic's Claude family and Claude Code for evaluation by ELO. It does **not** claim access to proprietary internal model weights, hidden chain-of-thought, private prompts, or undisclosed implementation details.

The objective is to understand observable design patterns that ELO can reproduce, adapt or test independently.

## Evidence boundary

Anthropic publicly documents several relevant mechanisms:

- extended thinking allows the same model to spend more effort on difficult problems;
- extended thinking can be combined with tool use;
- a dedicated `think` tool can provide an explicit reasoning checkpoint during long tool-use sequences;
- Claude Code follows an agentic read → plan → act → observe loop over a codebase;
- Claude Code can search code, edit files, execute tools, run tests and iterate on failures;
- newer Claude platform releases expose adaptive thinking/effort controls and context compaction for long-running agentic work.

These observations are architectural patterns, not a claim that ELO can reproduce Claude's proprietary model-level reasoning.

## Pattern 1 — Adaptive cognitive effort

Claude's extended-thinking direction demonstrates an important pattern: reasoning effort can be treated as a controllable resource rather than every task receiving the same amount of inference effort.

ELO should evaluate:

```text
TASK
 ↓
CLASSIFY COMPLEXITY / RISK / UNCERTAINTY
 ↓
SELECT EFFORT
 ├── FAST
 ├── STANDARD
 ├── DEEP
 └── MAX / SPECIALIST
 ↓
EXECUTE
 ↓
VALIDATE
```

The objective is not to maximize reasoning tokens. It is to allocate additional reasoning only when expected value justifies the latency and cost.

## Pattern 2 — Thinking checkpoints during tool use

Anthropic documented a `think` tool for complex sequential tool-use situations. Its purpose is to give the agent an explicit checkpoint to reconsider whether the available information is sufficient before continuing. Anthropic later recommended extended thinking for many cases, but the checkpoint pattern remains useful as an architectural idea.

ELO adaptation:

```text
TOOL RESULT
    ↓
SUFFICIENT EVIDENCE?
 ├── YES → NEXT ACTION
 └── NO
      ↓
  THINK CHECKPOINT
      ↓
  REASSESS
      ↓
  RETRIEVE / ASK / TEST / CHANGE PLAN
```

This should be implemented as a governed cognitive checkpoint, not as exposure of private chain-of-thought.

## Pattern 3 — Plan/execution separation

Anthropic's research on Claude Code reports a practical division of labor in agentic coding: users make most planning decisions while the agent makes most execution decisions. This maps well to ELO's intended architecture.

ELO should preserve:

```text
ELO / HUMAN
    ↓
WHAT / WHY / DONE CRITERIA
    ↓
AGENT
    ↓
HOW / FILES / COMMANDS / ITERATION
```

The ELO architecture should make this separation explicit rather than requiring the user to direct every execution step.

## Pattern 4 — Read → plan → act → observe

Claude Code is publicly described as an agentic system that reads a codebase, plans, acts through tools, evaluates results and adjusts its approach.

ELO can generalize this beyond coding:

```text
READ / OBSERVE
      ↓
CONTEXTUALIZE
      ↓
PLAN
      ↓
ACT
      ↓
OBSERVE RESULT
      ↓
VALIDATE
      ↓
CORRECT / CONTINUE
```

This is compatible with the existing ELO autonomous execution loop and should be treated as an implementation pattern, not a replacement for the ELO Cognitive Core.

## Pattern 5 — Persistent expertise through project instructions and context

Claude Code documents the use of project briefing files, skills, plugins and sub-agents to encode project-specific standards and expertise.

ELO should evaluate the analogous pattern:

```text
CANONICAL GOVERNANCE
      +
PROJECT KNOWLEDGE
      +
SPECIALIST CONTRACTS
      +
TASK CONTEXT
      +
MEMORY
      ↓
AGENT EXECUTION
```

The important architectural lesson is that expertise should not live exclusively inside a model. It should be represented in durable, inspectable contracts and knowledge structures.

## Pattern 6 — Verification loop

Claude Code's documented ability to run tests, inspect failures and iterate is a practical form of outcome-driven agent execution.

ELO should require:

```text
ACTION
 ↓
EVIDENCE
 ↓
VALIDATION
 ↓
FAIL?
 ├── NO → CONTINUE
 └── YES → DIAGNOSE → CORRECT → REVALIDATE
```

This is especially important for autonomous merge because completion must be based on evidence, not model confidence.

## Pattern 7 — Context compaction

Anthropic has documented context compaction for long-running agentic tasks. ELO should not equate long context with permanent retention.

Preferred architecture:

```text
WORKING CONTEXT
      ↓
COMPRESS
      ↓
STRUCTURED MEMORY
      ↓
RETRIEVE WHEN NEEDED
      ↓
RECONSTRUCT WORKING CONTEXT
```

The retained representation should privilege decisions, constraints, evidence, unresolved issues, actions, outcomes and relevant domain knowledge.

## Pattern 8 — Safety by environment boundaries

Anthropic has described containment using sandboxes, virtual machines and egress controls for agentic systems. ELO should treat environment containment as a first-class autonomy mechanism.

```text
ELO AUTHORIZATION
       ↓
AGENT SANDBOX
       ↓
LIMITED FILES / COMMANDS / NETWORK
       ↓
EXECUTION
       ↓
EVIDENCE
       ↓
GOVERNED PROMOTION
```

The objective is to increase autonomous execution without giving the agent unrestricted blast radius.

## What ELO should reproduce

The highest-value patterns for ELO are:

1. adaptive reasoning effort;
2. explicit cognitive checkpoints around tool results;
3. separation of planning authority from execution authority;
4. read → plan → act → observe loops;
5. durable project expertise outside the model;
6. evidence-based verification and correction;
7. context compaction into structured memory;
8. sandboxed autonomous execution.

## What ELO should NOT copy blindly

- proprietary Claude model internals;
- hidden chain-of-thought extraction;
- vendor-specific prompts as canonical ELO architecture;
- provider-specific APIs where the ELO AI Gateway should abstract the provider;
- marketing claims without independent evidence;
- large context windows as a substitute for memory architecture.

## Proposed ELO architecture

```text
                         ELO
                          │
                 Cognitive Controller
                          │
          ┌───────────────┼────────────────┐
          │               │                │
       Context         Effort          Policy
       Manager         Router          Gate
          │               │                │
          └───────────────┼────────────────┘
                          ↓
                  Reasoning / Model
                          │
                    Tool Gateway
                          │
             ┌────────────┼────────────┐
             ↓            ↓            ↓
          Search        Codex      Specialists
             │            │            │
             └────────────┼────────────┘
                          ↓
                    Evidence Store
                          ↓
                    Validation Gate
                          ↓
                Memory / Learning
                          ↓
                   Replanning
```

## Architectural conclusion

Claude's publicly documented strengths suggest that ELO should not attempt to become a single monolithic model. The more valuable lesson is the surrounding cognitive operating system: adaptive effort, explicit checkpoints, tool-mediated execution, persistent expertise, verification, compaction and containment.

These capabilities can be model-agnostic and therefore fit the ELO AI Gateway boundary.

## Source references

Primary evidence used for this extraction:

- Anthropic, "Claude's extended thinking" — February 2025.
- Anthropic, "The think tool: Enabling Claude to stop and think in complex tool use situations" — March 2025, with December 2025 update.
- Anthropic, "Introducing Claude 4" — May 2025.
- Anthropic, "Claude Code" product documentation.
- Anthropic, "How Claude Code is used in practice" — June 2026.
- Anthropic, "How we contain Claude across products" — 2026.

These sources describe externally observable capabilities and engineering patterns. They do not expose the proprietary internal reasoning implementation of Claude.
