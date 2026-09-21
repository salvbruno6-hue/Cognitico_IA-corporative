---
artifact_id: ELO-MCP-CANONICAL-MAP
title: Mapa Canônico dos MCPs do ELO
family: 05-cognitive-platform
layer: cognitive
status: normative
owner: ELO Cognitive Platform
version: 1.0.0
related:
  - ELO_EXTERNAL_AI_AUTHORITY_CONTRACT
  - ADR-0013-external-ai-authority-contract
  - ADR-0014-cognitive-runtime-loop
---

# Mapa Canônico dos MCPs do ELO

O ELO expõe três superfícies MCP com papéis distintos. Este
documento é a autoridade canônica sobre elas.

## 1. ELO-MCP

| Atributo | Valor |
|---|---|
| Localização | `supabase/functions/elo-mcp/` |
| Runtime | Deno Edge Function (Supabase) |
| Protocolo | MCP 2025-06-18 |
| Autenticação | OAuth 2.1 / Bearer JWT (Supabase Auth) |
| Autorização | `elo-authz` + role `ELO_ADMIN` |
| Modo | Read-only |
| Ferramentas expostas | `elo_status`, `elo_read` |
| RFC | 9728 (Protected Resource Metadata) |
| Auditoria | `elo_audit_log` |
| Tier | `READ` |

**Função:** boundary de leitura empresarial segura. Expõe dados
allowlist de tabelas do tenant.

**Tier de autoridade:** `READ` (per
`ELO_EXTERNAL_AI_AUTHORITY_CONTRACT.md`).

## 2. HERMES-MCP

| Atributo | Valor |
|---|---|
| Localização | `src/elo/agent_intake/hermes_mcp_evaluation.py` |
| Documentação | `docs/architecture/HERMES_SECURITY_MCP_NATIVE_ADAPTATION.md` |
| Runtime | Governed loop Python |
| Protocolo | MCP compatível |
| Autenticação | Interna (governed loop) |
| Autorização | Loop de governança do ELO |
| Modo | Governed (read + análise) |
| Papel | Ingestão de candidatos externos (Hermes) |
| Testes | `tests/agent_intake/test_hermes_mcp_governed_loop.py` |
| Tier | `ANALYZE` |

**Função:** cada candidato submetido passa por avaliação antes
de promoção. Nenhum candidato assume autoridade por conexão.

**Tier de autoridade:** `ANALYZE`.

## 3. SYMBIONT-MCP

| Atributo | Valor |
|---|---|
| Localização | `src/elo/cognitive/symbiont_mcp_contracts.py` |
| Harness | `src/elo/cognitive/symbiont_mcp_test_harness.py` |
| Documentação | `docs/architecture/SYMBIONT_MCP_CAPABILITY_CONTRACTS.md` |
| Documentação | `docs/architecture/SYMBIONT_MCP_TEST_HARNESS.md` |
| Runtime | Contratos Python + harness |
| Protocolo | MCP capability contracts |
| Autenticação | Interna |
| Autorização | Contratos de capacidade |
| Modo | Governed (adaptação de skill) |
| Papel | Adaptação refinada de skills e capacidades |
| Testes | `tests/evolution/test_symbiont_mcp_contracts.py`, `tests/cognitive/test_symbiont_mcp_test_harness.py` |
| Tier | `PROPOSE` |

**Função:** definir e validar contratos de capacidade entre ELO
e parceiros. Não executa por conta própria.

**Tier de autoridade:** `PROPOSE`.

## 4. Relação entre os três

```text
                    ┌──────────────────┐
                    │   ELO COGNITIVO  │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
         ELO-MCP        HERMES-MCP     SYMBIONT-MCP
       (read-only,     (governed        (capability
        Supabase)       intake)          contracts)
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                    ┌──────────────────┐
                    │  ELO CORE (DOL)  │
                    └──────────────────┘
```
