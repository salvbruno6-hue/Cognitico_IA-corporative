# ELO ChatGPT Project Adapter — Canonical

## Purpose

Provide a governed source boundary through which ELO can discover and retrieve information from ChatGPT Projects when an authorized connector exposes that capability.

## Important boundary

A normal ChatGPT/GitHub connection does not by itself grant ELO access to the user's private ChatGPT Projects. ELO must never infer, scrape, or fabricate that access. The adapter is considered available only when a supported connector supplies an explicit read capability.

## Required capability

`chatgpt_project.read`

The connector must provide, at minimum:

- project identifier/name;
- semantic search or source retrieval;
- source identity/type/title;
- provenance;
- authorization context;
- tenant/principal isolation.

## Runtime behavior

```text
ELO question
  -> SourceDiscoveryEngine
  -> CHATGPT_PROJECTS candidate
  -> ChatGPTProjectAdapter
  -> authorization check
  -> if connected: semantic search
  -> ProjectSourceRef results
  -> Temporal Conversation Memory
  -> consultant analysis
  -> admission/promotion

if not connected:
  -> report access gap
  -> continue with other authorized sources
```

## No hard-coded paths

The user should not need to provide `project/folder/file` paths. The adapter receives a semantic query and optional project scope. The connected source implementation is responsible for resolving the underlying Project resources.

## Security

No API key, cookie, session token or private ChatGPT credential is stored in the ELO repository. Credentials belong to the connector/runtime secret mechanism.

## Current status

The ELO Core now has the adapter contract and guarded facade. A live private-Project transport is **not claimed** until an official/authorized connector exposes the required capability.
