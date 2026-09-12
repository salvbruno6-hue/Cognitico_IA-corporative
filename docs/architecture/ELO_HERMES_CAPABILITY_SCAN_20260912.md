# ELO — Hermes Capability Scan — 2026-09-12

## Purpose

Map the execution and intelligence mechanisms available in Hermes that can be exposed through ELO without making Hermes an ELO authority.

## Findings

Hermes currently exposes entry points including CLI, gateway, API server, ACP, batch runner and Python library. Its execution loop resolves a model/provider, dispatches registered tools, returns the result and persists the session.

The tool registry covers terminal/process execution, file operations, web search/extraction, browser automation, multimodal tools, delegation, code execution, memory/session search, cron automation and integrations. Hermes also supports MCP servers and Skills as extension mechanisms.

Hermes supports seven terminal backends: local, Docker, SSH, Modal, Daytona, Vercel Sandbox and Singularity/Apptainer. Vercel Sandbox is therefore a valid runtime boundary for ELO's current infrastructure direction.

Hermes cron is a first-class agent task mechanism. Jobs can be one-shot or recurring, can attach Skills, can be paused/resumed/edited/triggered/removed and can deliver results. ELO should treat cron jobs as scheduled missions, not as a second governance authority.

MCP is an adapter mechanism for external tool ecosystems. Hermes can discover MCP tools at startup/reload and can filter exposed tools per server. ELO should govern which MCP capability contracts Hermes may receive.

Skills are the preferred Hermes extension mechanism when a capability can be expressed as instructions, shell commands and existing tools. Skills should enter ELO as governed candidates and only become reusable ELO capabilities after evidence and Evolution Gate validation.

## Governed ELO model

```text
User / Automation
      |
      v
ELO Terminal / Web
      |
      v
ELO Cognitive  <-- authority / authorization
      |
      v
Symbiont       <-- connector / translation / provider selection
      |
      +-----------------------------+
      |                             |
      v                             v
 Hermes                        Other providers
      |
 +----+---------+----------+----------+
 |              |          |          |
Tools         Skills      MCP       Cron
 |              |          |          |
 +--------------+----------+----------+
      |
      v
Evidence + Outcome
      |
      v
Evolution Gate
```

## Terminal decision

The ELO Web now provides a dedicated `/terminal` surface. It is intentionally terminal-like but is **not** a raw Hermes shell.

The browser sends only `/api/cognitive` requests. It never receives a Hermes endpoint, runtime token, provider secret or arbitrary command channel.

Initial authorized command:

```text
/probe
```

Aliases:

```text
hermes probe
/hermes probe
```

The terminal also provides read-only local commands:

```text
/help
/capabilities
/status
/clear
```

`/probe` constructs the existing ELO-authorized `hermes_mission` contract with:

- `mission_class: runtime_probe`
- `authorized_capabilities: [hermes:runtime_probe]`
- read-only execution
- bounded execution
- no canonical mutation
- execution and outcome evidence requirements

## Governance invariant

The terminal is an **entry surface**, not an authority.

The intended chain remains:

```text
Terminal -> ELO Cognitive -> Symbiont -> Hermes -> Evidence/Outcome -> Evolution Gate
```

No terminal command may directly call Hermes. No Hermes result may mutate ELO Core or become canonical knowledge without the existing governance path.

## Sources inspected

- Hermes Agent architecture and entry points
- Hermes built-in tool registry
- Hermes MCP integration
- Hermes Skills system
- Hermes cron scheduler
- Hermes terminal backend configuration
- ELO `CognitiveCore` Hermes mission path
- ELO `SymbiontHermesBridge`
- ELO-Hermes `/elo/v1/execute` runtime boundary
