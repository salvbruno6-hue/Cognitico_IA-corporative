# 09 — Governance Contracts

Owner canônico dos contratos, padrões, políticas e protocolos que
governam o comportamento do ELO e de seus agentes externos.

## Estrutura

| Subpasta | Conteúdo |
|---|---|
| `standards/` | Padrões normativos (`*_STANDARD.md`) |
| `policies/` | Políticas de acesso, autorização e uso (`*_POLICY.md`) |
| `protocols/` | Protocolos operacionais (`*_PROTOCOL.md`) |

## Hierarquia

1. `standards/` — definem o como normativo
2. `policies/` — definem o quem pode o quê
3. `protocols/` — definem o fluxo operacional

Em caso de conflito: `policy` > `standard` > `protocol`.

## Regra

Nenhum contrato pode existir fora desta pasta. Stubs na raiz são
redirects temporários que serão removidos após o próximo ciclo
de consolidação.