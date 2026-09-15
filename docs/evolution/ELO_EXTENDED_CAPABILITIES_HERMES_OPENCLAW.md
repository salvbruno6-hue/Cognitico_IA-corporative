# ELO — Capacidades Estendidas Hermes + OpenClaw

**Status:** EVOLUTION LAB / CANDIDATE-ONLY
**Owner:** ELO Cognitivo
**Governance:** Core + Evolution_Gate
**Natureza:** extensões de capacidades ELO existentes
**Version:** 1.0

## 1. Finalidade

Este documento registra as extensões evolutivas derivadas de mecanismos observados em Hermes e OpenClaw.

As extensões **não criam novas capacidades-raiz**. Cada uma é associada a uma capacidade já existente no ELO e somente pode ser incorporada quando sua adaptação demonstrar ganho mensurável dentro do fluxo existente.

Regra estrutural:

`capacidade ELO existente → extensão Hermes/OpenClaw → adaptação pela Simbionte → teste → ganho → refinamento → Evolution_Gate`

Hermes e OpenClaw são fontes de experiência, mecanismo, implementação de referência e/ou execução controlada. Nenhum deles é autoridade canônica do ELO.

## 2. Modelo de capacidade estendida

Cada extensão possui:

- `extension_id`
- `source_provider`
- `extends_capability`
- `existing_owner`
- `mechanism`
- `structural_relation`
- `flow_relation`
- `adapted_skill`
- `baseline`
- `expected_gain`
- `evidence`
- `promotion_state`

A unidade de aprendizado é a **extensão aplicada à capacidade existente**, e não o sistema externo isoladamente.

## 3. Matriz das extensões

| ID | Fonte | Capacidade ELO existente | Extensão proposta | Relação estrutural | Relação de fluxo |
|---|---|---|---|---|---|
| `EXT-MEM-HERMES` | Hermes | ELO Memory | memória escopada e operações reutilizáveis | Memory → scoped state | Contexto → Memory → recuperação → decisão |
| `EXT-MEM-OPENCLAW` | OpenClaw | ELO Memory | recall/search autorizado + promoção controlada de memória de curto prazo | Memory → search/flush/promotion | interação → recall → contexto → decisão → retenção |
| `EXT-SKILL-HERMES` | Hermes | ELO Skills | registro de skill executável e reutilizável | Skills → named capability | necessidade → skill → execução → resultado |
| `EXT-SKILL-OPENCLAW` | OpenClaw | ELO Skills | plugin/skill discovery e carregamento controlado | Skills → plugin skill | contexto → seleção → carregamento → execução |
| `EXT-TOOL-HERMES` | Hermes | ELO Toolset Resolution | resolução por allowlist e escopo | Toolset → policy boundary | intenção → capability → autorização → ferramenta |
| `EXT-TOOL-OPENCLAW` | OpenClaw | ELO Toolset Resolution | política explícita de ferramentas e deny-by-default | Toolset → tool policy | pedido → policy → allow/deny → execução |
| `EXT-CONTEXT-HERMES` | Hermes | ELO Context | composição hierárquica com precedência explícita | Context → hierarchy | entrada → contexto pai → contexto filho → decisão |
| `EXT-CONTEXT-OPENCLAW` | OpenClaw | ELO Context | lifecycle de montagem de contexto | Context → lifecycle | evento → preparação → montagem → execução |
| `EXT-DELEG-HERMES` | Hermes | ELO Delegation | handoff delimitado a worker | Delegation → bounded worker | decisão → payload autorizado → worker → resultado |
| `EXT-DELEG-OPENCLAW` | OpenClaw | ELO Delegation | spawn de subagente com escopo | Delegation → subagent scope | objetivo → spawn → execução → retorno |
| `EXT-AUTO-HERMES` | Hermes | ELO Automation | registro explícito de automação repetível | Automation → schedule | condição → registro → disparo → evidência |
| `EXT-AUTO-OPENCLAW` | OpenClaw | ELO Automation | identidade e lifecycle de schedule/cron | Automation → schedule identity | evento/tempo → schedule → execução → resultado |
| `EXT-MCP-HERMES` | Hermes | ELO External Capability Gateway | gateway externo por allowlist | Gateway → external capability | necessidade → gateway → autorização → capability |
| `EXT-MCP-OPENCLAW` | OpenClaw | ELO External Capability Gateway | servidores MCP stdio/HTTP sob política | Gateway → MCP boundary | request → policy → MCP → evidence |
| `EXT-STATE-HERMES` | Hermes | ELO State Recovery | snapshot/restauração de estado escopado | State → checkpoint | execução → checkpoint → falha/interrupção → restore |
| `EXT-STATE-OPENCLAW` | OpenClaw | ELO State Recovery | reparo/recuperação de sessão | State → session recovery | sessão → detecção → reparo → retomada |

## 4. Relação com a Simbionte

A Simbionte atua como camada de adaptação refinada:

`OBSERVE → INTERPRET → DECOMPOSE → EXTRACT_MECHANISM → IDENTIFY_EXISTING_OWNER → CHECK_COMPATIBILITY → ADAPT → TEST → MEASURE → DIAGNOSE → REFINE → RETEST`

Para cada extensão a Simbionte deve registrar:

1. comportamento externo observado;
2. mecanismo útil;
3. capacidade ELO que já possui o owner correto;
4. diferença entre baseline e extensão;
5. adaptação ao contrato ELO;
6. risco/regressão;
7. ganho medido;
8. necessidade de nova iteração.

## 5. Exemplo de aceitação — Memory

A extensão **não** é aceita porque Hermes ou OpenClaw possuem memória.

Ela é aceita somente se:

`ELO Memory atual → adaptação → teste controlado → melhoria comprovada de retenção/recuperação/contexto → ausência de regressão → repetibilidade → Evolution_Gate`

Exemplo conceitual:

`ELO Memory`
→ `EXT-MEM-HERMES`
→ memória escopada por tenant + operação reutilizável
→ teste de isolamento e recuperação
→ medir precisão, recuperação e isolamento

Em paralelo:

`ELO Memory`
→ `EXT-MEM-OPENCLAW`
→ recall/search + flush/promotion adaptados ao contrato ELO
→ teste de recuperação contextual
→ medir relevância, persistência e custo

As duas extensões podem fortalecer a **mesma capacidade ELO Memory**. Não são duas memórias canônicas.

## 6. Regra de integração evolutiva

Uma extensão somente pode sair de `CANDIDATE-ONLY` quando houver:

`proveniência + baseline + hipótese + mecanismo + adaptação + teste + resultado + métricas + regressão + repetibilidade + owner + governança`

A implementação final deve entrar no mecanismo proprietário do ELO correspondente. Código externo não se torna canônico por cópia ou proximidade estrutural.

## 7. Estados

`OBSERVED → EVIDENCED → ASSOCIATED → ADAPTED → TESTED → REFINED → LEARNING_CANDIDATE → GOVERNED_LEARNING → EVOLUTION_GATE → VALIDATED_LEARNING`

Nenhum estado, exceto o fluxo canônico de governança, autoriza promoção.

## 8. Regras de não duplicidade

É proibido criar:

- segunda memória canônica;
- segundo Skill Registry;
- segundo Tool Registry;
- segundo Context Engine;
- segundo Delegation Engine;
- segundo Scheduler/Watcher Authority;
- segundo MCP Gateway Authority;
- segundo State Recovery Authority;
- segundo Core ou Evolution_Gate.

Cada extensão deve ser registrada como `EXTEND(existing_capability)`.

## 9. Critério de evolução positiva

A extensão é considerada evolutivamente útil somente se melhorar pelo menos uma métrica relevante da capacidade existente sem violar suas invariantes.

Resultados possíveis:

- `STRENGTHEN` — melhora mensurável sem mudança de contrato;
- `REFACTOR` — melhora mediante reorganização interna;
- `REUSE` — mecanismo já compatível e aproveitado sem alteração material;
- `REJECT` — ganho insuficiente, regressão ou incompatibilidade;
- `RETEST` — evidência inconclusiva e requer nova iteração.

`CREATE` não é uma saída normal deste laboratório; exige demonstração de ausência de owner existente e aprovação arquitetural separada.

## 10. Princípio final

Hermes e OpenClaw fornecem experiência.

A Simbionte transforma essa experiência em adaptação refinada.

O ELO mede se a adaptação aumenta sua própria capacidade.

O Core e o Evolution_Gate determinam o que pode se tornar aprendizado governado.
