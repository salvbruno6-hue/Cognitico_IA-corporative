---
artifact_id: ADR-0013-cognitive-runtime-loop
title: Cognitive Runtime Loop — consolidação do ciclo decisório
family: 10-adr
status: proposed
owner: ELO Architecture Board
date: 2026-09-19
related:
  - 10-adr/ADR-0012-decision-outcome-loop.md
  - 01-meta-architecture/cognitive-architecture/ELO_COGNITIVE_EXECUTION_CONTRACT.md
  - ELO_AUTHORIZATION_ENFORCEMENT_STANDARD.md
---

# ADR-0013 — Cognitive Runtime Loop

## Contexto

O ELO já possui contratos e runtimes para entrada de IA, contexto, decisão, autorização, execução, outcome, aprendizado, Evolution Gate, agentes, Symbiont/Hermes e observabilidade.

O risco atual não é ausência de mecanismos isolados, mas a existência de múltiplos caminhos parcialmente sobrepostos. O Cognitive Runtime Loop (CRL) deve, portanto, consolidar os componentes existentes sem criar uma segunda autoridade.

## Decisão

O CRL será uma **composição governada** dos componentes canônicos existentes:

`entrada → contexto → análise → DecisionLifecycle → autorização/mandato → execução → observação → outcome → atribuição → aprendizado → calibração/precedente → novo contexto`

### Autoridades

- **ELO Cognitivo:** autoridade semântica, arquitetural e de decisão.
- **ELO Core:** materialização dos mecanismos canônicos.
- **GitHub:** ledger durável de execução, versionamento, Issue/PR e evidências.
- **Supabase:** memória/estado estruturado já estabelecido, quando o contrato existente determinar sua utilização.
- **elo-authz:** autoridade de autorização.
- **Evolution Gate:** autoridade exclusiva de evolução/promoção.
- **Symbiont/Hermes/Agentes:** execução e especialização sob autorização.
- **Automations/Eventos:** adaptadores determinísticos; não podem ultrapassar a governança do ELO.

## Decision Ledger

O CRL não cria uma nova tabela ou banco denominado `decision_ledger`.

O **Decision Ledger é um contrato/projeção do ciclo decisório sobre o ledger durável já existente**, principalmente GitHub Issue/PR, mantendo referência ao `DecisionRecord`, transições do `DecisionLifecycle`, evidências, actor, request/correlation IDs e referências de execução.

O Core expõe somente a porta contratual necessária para registrar e consultar essa projeção. A implementação durável permanece fora do Core e deve reutilizar o conector/controle de execução existente.

Consequentemente:

- não criar uma segunda memória de decisões;
- não criar `memory/ledger/`;
- não criar tabela paralela de decisões sem evidência de necessidade;
- não permitir que o ledger substitua o `DecisionLifecycle`;
- não permitir que o ledger autorize, promova ou execute;
- não aceitar registros sem identidade da decisão e rastreabilidade;
- gravações devem ser idempotentes por identidade do evento/transição.

## Próximas integrações

1. ligar a porta do Decision Ledger ao ledger durável GitHub existente;
2. expor leitura governada através do `elo-mcp`, sem conceder escrita genérica;
3. integrar observers ao `DecisionLifecycle`;
4. consolidar Event/Trigger com o workflow/automação existente;
5. fechar o caminho CRL ponta a ponta;
6. somente depois avaliar lacunas residuais.

## Critérios de aceitação

- nenhuma nova autoridade cognitiva é criada;
- `DecisionRecord` e `DecisionLifecycle` permanecem canônicos;
- decisões e transições podem ser correlacionadas de forma idempotente;
- evidências permanecem referenciadas;
- autorização e Evolution Gate permanecem nos seus proprietários atuais;
- GitHub continua sendo o ledger durável de execução/versionamento;
- nenhum componente novo executa ação empresarial por conta própria.
