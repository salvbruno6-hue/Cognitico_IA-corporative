# ELO — Catálogo Governado de Mecanismos Externos

## Finalidade

Registrar mecanismos úteis identificados em repositórios e ZIPs externos para que possam ser avaliados e incorporados ao ELO por meio do ciclo de aprendizagem e do Evolution Gate existentes.

Este catálogo é **evidência de engenharia**, não uma nova fonte de verdade, registry de capacidades, motor de evolução, memória ou autoridade cognitiva.

## Regra de incorporação

```text
FONTE EXTERNA
    ↓
MECANISMO OBSERVADO
    ↓
EVIDÊNCIA + PROVENIÊNCIA
    ↓
COMPARAÇÃO COM ELO EXISTENTE
    ↓
REUSE → STRENGTHEN → REFACTOR → DEPRECATE → CREATE*
    ↓
VALIDAÇÃO
    ↓
EVOLUTION GATE
    ↓
APRENDIZADO / CAPACIDADE EXISTENTE FORTALECIDA
```

`CREATE` somente quando a ausência de equivalente canônico estiver comprovada e o mecanismo for generalizável.

## Mecanismos extraídos

| Fonte | Mecanismo | Destino ELO | Disposição inicial |
|---|---|---|---|
| Ponytail | adaptação por ambiente, propagação contextual, adapters finos | COGNITIVO / Simbionte | STRENGTHEN |
| Caveman | agentes delimitados, contratos de tarefa, evidência e execução bounded | COGNITIVO / execução | STRENGTHEN |
| maida-assert | regressão comportamental, trials isolados, baseline e PASS/FAIL/INCONCLUSIVE | Evolution Gate / Baseline | STRENGTHEN |
| GraphSmith | atestação, proveniência, verificação e reconciliação de evolução | Evolution Gate / evidência | STRENGTHEN |
| TraceGate | contratos de ferramenta, trace JSONL, replay, redaction e side-effect boundary | execução / auditoria existente | STRENGTHEN |
| Trustabl | inventário de agentes, ferramentas, skills e MCP; findings determinísticos | Capability Registry existente | STRENGTHEN |
| SafeAI | detecção de capacidades e escalada de capacidade | Capability/Policy existentes | STRENGTHEN |
| SecureAI-Scan | evidência `proven`, `likely`, `heuristic` e fluxo source→sink | Evidence/knowledge governance | STRENGTHEN |
| Agent Sync Action | uma autoridade canônica + adapters por ambiente | arquitetura de configuração | STRENGTHEN |
| OpenLore | orientação contextual, impacto, stale detection e travessia relacional | Knowledge Graph / Context existentes | STRENGTHEN |

## Regras de segurança

1. O código-fonte externo nunca é promovido diretamente a conhecimento canônico.
2. Leitura da fonte não equivale a aprendizado.
3. Aprendizado não equivale a promoção.
4. Cada mecanismo precisa de evidência e proveniência.
5. Não criar uma segunda Capability Registry, Authorization Engine, Knowledge Graph, Evolution Engine, Audit Log ou Memory Engine.
6. Mecanismos contextualizados devem permanecer contextuais; somente mecanismos generalizáveis podem propor nova habilidade do ELO.
7. Qualquer promoção deve passar pelo `GovernedLearningService` e pelo Evolution Gate existente.
8. O catálogo não concede autoridade de escrita no Core, Forge ou GitHub.

## Contrato de intake

O ponto executável de entrada é `GovernedLearningService.ingest_external_mechanism(...)`.

Ele produz um `ExternalMechanismCandidate` em estado `CANDIDATE` e exige:

- fonte e referência rastreáveis;
- mecanismo identificado;
- capacidade proposta;
- owner canônico existente ou ausência comprovada;
- disposição `REUSE`, `STRENGTHEN`, `REFACTOR`, `DEPRECATE` ou `CREATE`;
- evidências;
- escopo;
- indicação de generalização.

O método **não escreve Core/Forge, não cria capability, não promove conhecimento e não faz merge**.

## Fluxo de evolução

```text
ZIP / repositório
      ↓
extração do mecanismo
      ↓
ExternalMechanismCandidate
      ↓
comparação com capacidade/contrato canônico
      ├── REUSE       → reutilizar
      ├── STRENGTHEN  → fortalecer implementação existente
      ├── REFACTOR    → corrigir arquitetura existente
      ├── DEPRECATE   → retirar duplicidade/conflito
      └── CREATE      → somente com ausência comprovada
      ↓
avaliação + evidência
      ↓
Evolution Gate
      ↓
GovernedLearningService.prepare_knowledge_promotion(...)
      ↓
materialização governada, quando autorizada
```

## Estado atual

A implementação desta estrutura é deliberadamente **candidate-only**. A incorporação definitiva dos mecanismos acima continua dependente de validação no ELO e de evidência de que cada alteração melhora uma capacidade canônica sem introduzir autoridade paralela.
