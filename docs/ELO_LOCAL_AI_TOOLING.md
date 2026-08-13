# ELO Local AI Tooling — Capability Discovery

## Source
Workstation diagnostic provided by the user on 2026-08-13.

## Detected capabilities

| Capability | Version / state | ELO relevance |
|---|---|---|
| Node.js | 24.15.0 | scripts, local tooling |
| npm | 11.12.1 | package/tool discovery |
| npx | 11.12.1 | ephemeral CLI execution |
| Git | 2.54.0.windows.1 | repository operations |
| Python | 3.14.5 | ELO runtime/tooling |
| pip | 26.1.1 | Python dependencies |
| Ollama | 0.30.10 | local model provider; no models installed at scan time |
| OpenAI Codex CLI | 0.144.6 | local coding/engineering agent |
| GitHub CLI | 2.92.0 | repository/issue/PR operations |
| Claude Code | not installed | provider/tool unavailable locally at scan time |
| Gemini CLI | not installed | provider/tool unavailable locally at scan time |
| Docker | not installed | container runtime unavailable locally at scan time |
| API keys | none detected in tested scopes | provider credentials not exposed |
| npm global | @openai/codex 0.144.6 | confirms Codex installation |

## Canonical interpretation

The workstation is a capability pool for ELO Source Discovery. It is not a fixed architecture dependency.

ELO should choose a tool/source according to intent, authorization, availability, cost and evidence requirements. The user should not have to specify a technical path when the system can discover an appropriate source itself.

## Security invariant

Never persist secret values. Store only non-sensitive capability state such as installed/not installed, version and provider availability.

## Future discovery targets

The ELO Source Discovery layer should be able to inspect and use, when authorized and available:

- GitHub repository, issues, pull requests and commits;
- local Codex CLI;
- Ollama and installed local models;
- Python scripts and packages;
- Node/npm tools;
- future Claude/Gemini CLIs;
- project/document stores exposed through authorized connectors.

## Relationship to Temporal Memory

Results obtained from local tools/providers during an `elo` session should enter Temporal Conversation Memory first. Promotion to Evolution Memory, Evidence, Knowledge or Decision remains governed.
