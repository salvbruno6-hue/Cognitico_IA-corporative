# ELO — Baseline de Maturidade e Rastreabilidade

> **Tipo:** framework normativo de governança arquitetural
> **ID:** ELO-GOV-MAT-001
> **Camada:** enterprise / architecture / governance
> **Status:** proposed
> **Autoridade:** proposal — somente se torna normativa após aprovação formal e atualização de status
> **Versão:** 0.1.0
> **Owner:** ELO Architecture & Governance
> **Objetivo:** estabelecer uma base única para medir maturidade, rastrear requisitos até evidências e impedir que documentação, código ou roadmap sejam confundidos com capacidade implementada.

---

## 1. Propósito

Este documento estabelece o mecanismo-base para responder, de forma objetiva, às perguntas:

- O que o ELO possui hoje?
- O que é somente conceito?
- O que está documentado?
- O que possui contrato?
- O que está implementado?
- O que possui testes?
- O que foi verificado?
- O que possui evidência operacional?
- Qual documento é autoridade para cada conceito?
- Qual código implementa cada contrato?
- Qual teste comprova cada comportamento?
- Qual decisão arquitetural autorizou determinada escolha?
- O que ainda é roadmap?
- Quais são as lacunas críticas?
- O que pode ser entregue pelo Codex com baixo risco?
- O que exige revisão arquitetural humana?

O framework existe para criar **rastreabilidade**, não para produzir burocracia.

A unidade de controle do ELO não deve ser a quantidade de arquivos. Deve ser a relação:

```text
INTENÇÃO
  ↓
REQUISITO
  ↓
CAPACIDADE
  ↓
CONTRATO
  ↓
DECISÃO
  ↓
IMPLEMENTAÇÃO
  ↓
TESTE
  ↓
EVIDÊNCIA
  ↓
MATURIDADE
```

---

## 2. Escopo

Aplica-se a:

- arquitetura;
- plataforma cognitiva;
- processos;
- conhecimento;
- engenharia de conhecimento;
- dados;
- IA;
- governança;
- ADRs;
- sistemas;
- código executável;
- testes;
- integrações;
- contratos;
- capacidades cognitivas futuras;
- roadmap técnico;
- artefatos produzidos ou alterados por humanos, ChatGPT, Codex ou outros agentes de IA.

Não substitui políticas de segurança, privacidade, compliance, engenharia de software ou governança corporativa. Ele cria uma camada de rastreabilidade entre esses mecanismos e a evolução do ELO.

---

## 3. Princípios fundamentais

### 3.1 Existência não significa implementação

A presença de um documento não prova que a capacidade existe em runtime.

### 3.2 Implementação não significa verificação

Código que compila não é automaticamente uma capacidade verificada.

### 3.3 Teste não significa validade arquitetural

Um teste pode provar um comportamento local sem provar que a solução está arquiteturalmente correta.

### 3.4 Roadmap não é requisito aprovado

Uma ideia futura não autoriza implementação.

### 3.5 Proposta não é baseline

Um conceito em `status: proposed` deve ser tratado como proposta, mesmo que esteja escrito com alto nível de detalhe.

### 3.6 Evidência precede declaração de maturidade

Quanto maior a maturidade declarada, maior deve ser a evidência correspondente.

### 3.7 Uma autoridade por conceito

Um conceito canônico deve possuir uma fonte normativa principal. Documentos derivados podem explicar ou referenciar, mas não criar uma segunda definição concorrente.

### 3.8 Pasta não define autoridade sozinha

A localização física ajuda a navegar, mas `authority`, `status`, `owner` e referências canônicas determinam como o artefato deve ser interpretado.

### 3.9 Agentes de IA devem obedecer ao contexto do repositório

Uma IA não deve criar, mover, apagar ou promover artefatos somente porque a mudança parece tecnicamente conveniente.

### 3.10 Mudanças irreversíveis exigem decisão explícita

Alterações de arquitetura-base, contratos canônicos, segurança, tenancy, provenance e limites de responsabilidade humana devem passar por revisão apropriada.

---

## 4. Vocabulário canônico

### 4.1 Artefato

Qualquer unidade versionada relevante para compreensão ou execução do ELO: documento, contrato, ADR, código, teste, configuração, modelo, fixture ou ativo reutilizável.

### 4.2 Capacidade

Uma competência que o ELO deve possuir ou poderá possuir. Exemplos: Cognitive Interface, Context Resolution, Reasoning, Decision Support, Organizational Health Intelligence.

### 4.3 Requisito

Uma necessidade verificável que determina comportamento, restrição ou propriedade da solução.

### 4.4 Contrato

Uma definição verificável de interface, estrutura, comportamento, evento, entrada, saída ou boundary.

### 4.5 Evidência

Um resultado observável que permite sustentar uma afirmação de maturidade. Exemplos: teste aprovado, workflow, execução reproduzível, fixture, relatório de validação ou evidência operacional autorizada.

### 4.6 Baseline

Estado aprovado contra o qual alterações posteriores são comparadas.

### 4.7 Maturidade

Grau de evidência de que determinada capacidade passou das intenções para uma condição tecnicamente demonstrável.

### 4.8 Rastreabilidade

Relação explícita entre intenção, requisito, capacidade, contrato, implementação, teste, decisão e evidência.

### 4.9 Owner

Responsável conceitual pelo significado e ciclo de vida do artefato/capacidade. Não implica necessariamente uma pessoa específica.

### 4.10 Authority

Nível de autoridade que o artefato possui em caso de conflito.

---

## 5. Escala de maturidade ELO

A escala-base possui oito níveis, alinhada ao vocabulário já estabelecido no padrão de metadados do ELO.

| Nível | Nome | Significado | Evidência mínima |
|---:|---|---|---|
| 0 | ABSENT | Não há capacidade ou definição suficiente | nenhuma |
| 1 | CONCEPTUAL | Existe intenção/conceito | descrição identificável |
| 2 | DOCUMENTED | O conceito está documentado | documento coerente e localizável |
| 3 | CONTRACTED | Existem contratos/limites verificáveis | contrato ou especificação verificável |
| 4 | IMPLEMENTED | Existe implementação correspondente | código/configuração/integração rastreável |
| 5 | TESTED | Implementação possui testes relevantes | testes executáveis e resultados satisfatórios |
| 6 | VERIFIED | A capacidade foi verificada contra critérios definidos | evidência de validação/revisão |
| 7 | OPERATIONALLY EVIDENCED | Existe evidência de uso/execução operacional autorizada | evidência operacional reproduzível ou auditável |

### Regra de promoção

Nenhuma capacidade deve ser promovida de nível sem evidência compatível.

Exemplo incorreto:

```text
"Cognitive Consulting está documentado em 40 páginas.
Logo, está no nível 5."
```

Exemplo correto:

```text
Cognitive Consulting
Nível 2 — DOCUMENTED

Porque existe especificação conceitual,
mas não há contrato executável nem implementação.
```

---

## 6. Estados de lifecycle

O lifecycle do artefato e a maturidade da capacidade são dimensões diferentes.

### 6.1 Lifecycle de artefato

```text
PROPOSED
  ↓
DRAFT
  ↓
NORMATIVE
  ↓
IMPLEMENTED
  ↓
TESTED
  ↓
VERIFIED
```

Possíveis saídas:

```text
DRAFT → DEPRECATED
NORMATIVE → SUPERSEDED
IMPLEMENTED → BLOCKED
EXPERIMENTAL → NORMATIVE
```

### 6.2 Regra de não confusão

Um documento pode ser `NORMATIVE` enquanto a capacidade descrita nele está no nível 2.

Um módulo de código pode estar `IMPLEMENTED` enquanto a capacidade correspondente está no nível 4 e ainda não está no nível 5.

---

## 7. Dimensões independentes de maturidade

A maturidade global não deve esconder deficiências específicas. Para cada capacidade, avaliar separadamente:

1. definição;
2. arquitetura;
3. contrato;
4. implementação;
5. testes;
6. segurança;
7. governança;
8. observabilidade;
9. provenance;
10. isolamento de tenant;
11. qualidade de dados;
12. operação;
13. documentação;
14. reversibilidade;
15. responsabilidade humana.

Uma capacidade pode estar bem implementada e ainda possuir maturidade global baixa por falhas de governança ou testes.

---

## 8. Scorecard recomendado

Para cada capacidade, manter:

```yaml
capability_id: ELO-CAP-XXX
name: <nome>
layer: <camada>
owner: <owner>
status: proposed|active|deprecated
maturity_level: 0
architecture_score: 0
contract_score: 0
implementation_score: 0
test_score: 0
security_score: 0
governance_score: 0
observability_score: 0
provenance_score: 0
operational_evidence_score: 0
confidence: low|medium|high
canonical_artifact: <path>
requirements: []
contracts: []
adrs: []
implementations: []
tests: []
evidence: []
open_gaps: []
blocking_gaps: []
last_reviewed: <date>
```

### Regra de score

Os campos de score não devem ser tratados como uma média matemática automática.

Uma capacidade não deve ser considerada madura somente porque a média é alta se houver um bloqueador crítico.

Exemplo:

```text
Implementation = 5
Tests = 5
Security = 1

Resultado: NÃO VERIFICADA.
```

---

## 9. Rastreabilidade mínima

Toda capacidade relevante deve permitir navegar, quando aplicável, por:

```text
Capability
   ↓
Requirement
   ↓
Architecture
   ↓
Contract
   ↓
ADR
   ↓
Implementation
   ↓
Test
   ↓
Evidence
```

Não é obrigatório que todas as capacidades tenham todos os elementos desde o nível 1. A ausência deve ser explícita.

---

## 10. Tipos de relação

Usar relações semânticas claras:

| Relação | Significado |
|---|---|
| `defines` | artefato define conceito |
| `specifies` | artefato especifica comportamento |
| `implements` | código implementa contrato/capacidade |
| `tests` | teste verifica comportamento |
| `verifies` | evidência valida uma afirmação |
| `depends_on` | depende de |
| `constrains` | impõe restrição |
| `supersedes` | substitui |
| `derived_from` | derivado de |
| `related_to` | relação contextual |
| `owned_by` | responsabilidade conceitual |
| `governed_by` | submetido a governança |
| `evidenced_by` | sustentado por evidência |
| `proposed_by` | originado como proposta |

Evitar relações vagas como `connected_to` quando uma relação mais precisa existir.

---

## 11. Hierarquia de autoridade

Quando houver conflito, usar a seguinte ordem inicial, sujeita à baseline oficial do ELO:

```text
CONSTITUTIONAL / ENTERPRISE PRINCIPLES
        ↓
BASELINE ARCHITECTURE
        ↓
ADR APROVADA
        ↓
POLICY / GOVERNANCE
        ↓
CANONICAL CONTRACT
        ↓
IMPLEMENTATION
        ↓
TEST / FIXTURE
        ↓
REFERENCE
        ↓
ROADMAP / PROPOSAL
```

Um documento de implementação não pode redefinir silenciosamente um contrato canônico.

Um roadmap não pode contradizer uma ADR aprovada sem abrir uma nova decisão.

Uma referência externa não pode substituir uma regra interna sem decisão explícita.

---

## 12. Registro de capacidades

O repositório deve manter um inventário único de capacidades. O registro pode começar pequeno e crescer de forma controlada.

Categorias iniciais:

### Enterprise
- Enterprise Manifest
- Organizational Model
- Tenant Boundary
- Governance

### Interface
- Cognitive Interface
- Cognitive Request
- Cognitive Response
- Session

### Cognitive
- Cognitive Core
- Context
- Knowledge
- Memory
- Reasoning
- Evidence
- Decision Support
- Agent Lifecycle
- Autonomy Controls
- Cognitive Consulting Mode
- Organizational Health Intelligence

### Data
- Data Contracts
- Data Quality
- Provenance
- Event Model
- Ingestion

### Integration
- Integration Contracts
- External AI Gateway
- Event Interfaces

### Operations
- Quality
- Observability
- Testing
- Production Readiness

Estas entradas são **inventário inicial**, não declaração de implementação completa.

---

## 13. Estado inicial conhecido do ELO

Com base na estrutura atual do repositório e no histórico de desenvolvimento disponível, há evidências de trabalho já realizado na interface cognitiva, incluindo especificação arquitetural, exposição da API, componente de chat e fixture de resposta de risco. Esses commits existem no histórico do repositório. Isso demonstra atividade de implementação, mas não autoriza concluir que toda a capacidade correspondente esteja no nível 7. Cada capacidade deve ser auditada contra testes e evidências reais.

Referências históricas relevantes:

- `f1138b5` — establish cognitive interface architecture;
- `42eece2` — add cognitive interface specification;
- `63c8e42` — expose interface public API;
- `84ca5e6` — add cognitive frontend chat component;
- `e90ff9a` — add risk response fixture.

Essas referências devem ser tratadas como evidência histórica de evolução, não como substitutas de testes atuais.

---

## 14. Gate de promoção

### Gate G0 — Existência

Perguntas:

- Existe definição suficiente?
- Existe owner?
- Existe localização canônica?

### Gate G1 — Documentação

Perguntas:

- O propósito está documentado?
- Escopo e não escopo estão definidos?
- Dependências conhecidas estão registradas?

### Gate G2 — Arquitetura

Perguntas:

- Boundary está definido?
- Responsabilidades estão separadas?
- Não existe duplicidade conhecida?

### Gate G3 — Contrato

Perguntas:

- Entradas estão definidas?
- Saídas estão definidas?
- Erros estão definidos?
- Identidade, tenant e provenance são tratados quando aplicável?

### Gate G4 — Implementação

Perguntas:

- Existe código correspondente?
- O código respeita o contrato?
- A implementação está localizada no owner correto?

### Gate G5 — Testes

Perguntas:

- Happy path existe?
- Casos de erro existem?
- Limites relevantes existem?
- Testes são executáveis?

### Gate G6 — Verificação

Perguntas:

- Critérios de aceite foram verificados?
- Revisão arquitetural foi realizada quando necessária?
- Evidência está registrada?

### Gate G7 — Operação

Perguntas:

- Existe execução real autorizada?
- Observabilidade existe?
- Falhas são detectáveis?
- Provenance/auditoria são adequados?
- Há evidência de comportamento operacional?

---

## 15. Bloqueadores de promoção

Uma capacidade não pode avançar quando existir qualquer bloqueador crítico não tratado em:

- segurança;
- isolamento entre tenants;
- integridade de dados;
- contratos incompatíveis;
- perda de provenance;
- violação de autoridade arquitetural;
- ausência de responsabilidade humana em decisão de alto impacto;
- testes inexistentes quando o gate exigir testes;
- comportamento destrutivo sem mecanismo de reversão;
- exposição indevida de dados;
- contradição com ADR aprovada.

---

## 16. Matriz de evidências

Cada afirmação importante deve apontar para evidência.

| Afirmação | Evidência aceitável |
|---|---|
| API existe | código + teste/execução |
| contrato é válido | schema/validação + teste |
| tenant é obrigatório | contrato + teste de rejeição |
| session é criada | código + teste |
| response é canônica | contrato + teste |
| erro é consistente | testes de erro |
| componente está integrado | teste de integração |
| arquitetura foi aprovada | ADR/revisão |
| segurança está adequada | análise/teste/evidência correspondente |
| operação é observável | logs/metrics/traces/teste |
| capacidade é operacional | evidência operacional autorizada |

---

## 17. Regra de evidência negativa

Ausência de evidência não deve ser convertida em afirmação positiva.

Exemplo:

```text
Não encontramos teste.
```

não significa:

```text
O componente não funciona.
```

Significa:

```text
A capacidade não pode ser promovida ao nível que exige teste
até que exista evidência suficiente.
```

---

## 18. Auditoria de duplicidade

Antes de criar um artefato:

1. procurar pelo conceito;
2. procurar sinônimos;
3. procurar versões em português e inglês;
4. verificar pastas paralelas;
5. verificar ADRs;
6. verificar contratos;
7. verificar `src/elo`;
8. verificar roadmap;
9. determinar owner;
10. classificar como `REUSE`, `EXTEND`, `NEW`, `DUPLICATE`, `CONFLICT` ou `ROADMAP`.

### Regra

`DUPLICATE` não deve ser criado.

`CONFLICT` deve gerar análise/ADR antes de implementação.

`EXTEND` deve atualizar a fonte canônica ou criar uma extensão explicitamente vinculada.

---

## 19. Matriz de decisão para novas mudanças

| Situação | Ação |
|---|---|
| Apenas documentação explicativa | documentação |
| Nova definição normativa | revisão arquitetural |
| Nova capacidade | registro + arquitetura |
| Mudança de contrato | ADR/revisão + testes |
| Nova implementação sob contrato existente | implementação + testes |
| Correção local sem alteração arquitetural | patch + testes |
| Mudança de segurança | revisão obrigatória |
| Mudança de tenancy | revisão obrigatória |
| Mudança de provenance | revisão obrigatória |
| Novo comportamento autônomo | revisão de autonomia |
| Nova integração externa | contrato + segurança + testes |
| Exclusão/movimentação de conteúdo canônico | ADR ou decisão explícita |

---

## 20. Protocolo para Codex e agentes de IA

Antes de alterar código:

```text
1. Ler AGENTS.md
2. Ler ELO_REPOSITORY_NAVIGATION_RULES.md
3. Identificar owner
4. Identificar artefato canônico
5. Identificar status e authority
6. Procurar duplicidades
7. Ler contratos relacionados
8. Ler ADRs relacionadas
9. Determinar gate atual
10. Implementar somente o escopo autorizado
11. Executar testes
12. Registrar evidência
13. Atualizar rastreabilidade
14. Relatar gaps
15. Não promover maturidade sem evidência
```

### Regra para agentes

Se o agente não conseguir determinar:

- qual é a autoridade;
- qual contrato deve ser usado;
- qual capacidade está sendo alterada;
- qual é o critério de aceite;
- qual é o risco;

ele deve parar e reportar a lacuna em vez de inventar contexto.

---

## 21. Template de capacidade

```yaml
capability_id: ELO-CAP-XXX
name: <nome>
description: <descrição objetiva>
layer: <enterprise|architecture|process|knowledge|cognitive|data|ai|governance|system>
owner: <owner>
status: proposed
maturity_level: 1
authority: proposal
canonical_artifact: <path>
requirements: []
contracts: []
adrs: []
implementations: []
tests: []
evidence: []
dependencies: []
constraints: []
security_controls: []
open_gaps: []
blocking_gaps: []
confidence: low
last_reviewed: <YYYY-MM-DD>
```

---

## 22. Template de requisito

```yaml
requirement_id: ELO-REQ-XXX
statement: <requisito verificável>
type: functional|non-functional|security|governance|data|operational
priority: critical|high|medium|low
owner: <owner>
status: proposed|approved|implemented|verified|superseded
source: <document/issue/decision>
acceptance_criteria:
  - <critério>
related_capabilities: []
contracts: []
tests: []
evidence: []
```

---

## 23. Template de evidência

```yaml
evidence_id: ELO-EVD-XXX
type: test|workflow|execution|review|benchmark|audit|operational
subject: <capability/requirement/contract>
claim: <o que a evidência sustenta>
source: <path/url/commit/workflow>
result: pass|fail|partial|inconclusive
observed_at: <timestamp>
reviewer: <owner/reviewer>
limitations:
  - <limitação>
```

---

## 24. Template de gap

```yaml
gap_id: ELO-GAP-XXX
subject: <capability/requirement>
type: architecture|contract|implementation|test|security|governance|observability|data|provenance|operations
severity: blocker|critical|high|medium|low
description: <lacuna>
impact: <impacto>
required_action: <ação>
owner: <owner>
status: open|planned|in_progress|resolved|accepted_risk
related_evidence: []
```

---

## 25. Definition of Done de uma capacidade

Uma capacidade não deve ser considerada concluída somente porque o código foi escrito.

### DoD mínimo para nível 4

- definição canônica;
- owner;
- contrato;
- implementação;
- documentação de execução relevante.

### DoD mínimo para nível 5

Tudo do nível 4 +:

- testes happy path;
- testes de erro;
- testes de boundary relevantes;
- resultados registrados.

### DoD mínimo para nível 6

Tudo do nível 5 +:

- critérios de aceite revisados;
- arquitetura verificada quando aplicável;
- provenance suficiente;
- gaps críticos resolvidos ou formalmente aceitos.

### DoD mínimo para nível 7

Tudo do nível 6 +:

- execução operacional autorizada;
- observabilidade;
- evidência de comportamento real;
- mecanismo de detecção de falhas;
- revisão de segurança/governança quando aplicável.

---

## 26. Rastreabilidade do Cognitive Interface Vertical Slice

O vertical slice ELO-001 deve ser rastreado conceitualmente como:

```text
ELOChat
  ↓
Cognitive API
  ↓
CognitiveRequest
  ↓
Tenant Validation
  ↓
Session
  ↓
Cognitive Core
  ↓
CognitiveResponse
  ↓
Provenance / Timing / IDs
```

Critérios conhecidos do slice:

1. frontend envia `CognitiveRequest` válido;
2. API valida entrada;
3. `tenant_id` é obrigatório no backend;
4. `session_id` é criado ou recuperado;
5. `domain` é preservado;
6. core recebe request tipado;
7. resposta usa `CognitiveResponse` canônico;
8. `response_id`/`request_id` existem;
9. `processing_time_ms` é calculado;
10. erros usam contrato consistente;
11. testes cobrem happy path e erros;
12. execução local é documentada.

A presença desses critérios no documento não significa que todos estejam verificados neste momento. A matriz deve ser preenchida com evidências reais.

---

## 27. Rastreabilidade do novo Cognitive Consulting

O conceito de `Cognitive Consulting Mode` deve permanecer inicialmente como proposta até que sua arquitetura seja aprovada.

Modelo inicial:

```text
Signal
 ↓
Context Resolution
 ↓
Relevance Scope
 ↓
Information Gaps
 ↓
Clarification Questions
 ↓
Knowledge Retrieval
 ↓
Experience Retrieval
 ↓
Evidence Assessment
 ↓
Reasoning
 ↓
Scenario Analysis
 ↓
Recommendation
 ↓
Human Decision
 ↓
Outcome
 ↓
Governed Learning
```

Não criar um `ConsultantEngine` monolítico apenas para implementar esse fluxo.

A responsabilidade deve ser distribuída entre capacidades existentes ou explicitamente aprovadas.

---

## 28. Rastreabilidade de Organizational Health Intelligence

O ELO pode analisar:

```text
EVENTS
 ↓
PATTERNS
 ↓
HYPOTHESES
 ↓
EVIDENCE
 ↓
PROCESS / SYSTEM / TEAM / PERSON CONTEXT
 ↓
CAPABILITY GAP
 ↓
INTERVENTION OPTIONS
 ↓
HUMAN DECISION
```

A avaliação deve evitar inferências automáticas de culpa ou incompetência.

Uma lacuna observada deve inicialmente ser classificada como hipótese até existir evidência suficiente.

---

## 29. Exemplo de rastreabilidade — Financeiro / RH

Hipótese:

```text
Movimentação financeira
→ notificação
→ disponibilidade de recurso
→ diferença identificada na folha
```

O ELO deve registrar:

- sinais observados;
- fontes;
- relações temporais;
- hipóteses;
- evidências confirmatórias;
- evidências contraditórias;
- setores relacionados;
- decisões humanas;
- resultado.

Não registrar automaticamente:

```text
"Financeiro cometeu erro por incompetência."
```

A forma correta é algo como:

```text
Foi detectada uma inconsistência potencial entre eventos financeiros
que merece investigação. A causa ainda não foi determinada.
```

---

## 30. Exemplo de rastreabilidade — Empilhadeiras / Pátio

Hipótese:

```text
Condição do piso
+
rotas
+
frequência de movimentação
+
características das cargas
+
falhas recorrentes
→ possível aumento do custo operacional
```

O ELO deve separar:

### Observação

O custo/manutenção apresenta determinado padrão.

### Hipótese

A condição operacional pode contribuir para o padrão.

### Investigação

Buscar dados de manutenção, rotas, carga, frequência, layout e segurança.

### Alternativas

- manutenção/pavimentação;
- alteração de rota;
- alteração de horários;
- rota dedicada;
- solução alternativa de movimentação;
- combinação.

### Decisão

Humana e tecnicamente validada.

Uma solução física sugerida pelo contexto deve permanecer como hipótese até validação de engenharia, segurança e operação.

---

## 31. Métricas de governança

### Cobertura de rastreabilidade

```text
requisitos com evidência rastreável
-----------------------------------
requisitos relevantes
```

### Cobertura de contratos

```text
capacidades implementadas com contrato
--------------------------------------
capacidades implementadas
```

### Cobertura de testes

```text
requisitos verificáveis com testes
----------------------------------
requisitos verificáveis
```

### Debt de documentação

Número de capacidades implementadas sem documentação canônica suficiente.

### Debt de arquitetura

Número de implementações que não possuem decisão/boundary claro quando isso é necessário.

### Debt de provenance

Número de resultados relevantes cuja origem não pode ser reconstruída.

### Debt de governança

Número de capacidades sem owner, política ou controle necessário.

---

## 32. Métrica de confiança

A confiança deve representar a qualidade da evidência, não a confiança subjetiva do modelo.

### LOW

- conceito;
- informação incompleta;
- ausência de evidência independente.

### MEDIUM

- documentação consistente;
- contrato definido;
- alguma evidência executável.

### HIGH

- contrato;
- implementação;
- testes;
- verificação;
- evidência consistente;
- ausência de gaps críticos conhecidos.

Mesmo `HIGH` não significa certeza absoluta.

---

## 33. Regra para afirmações do ELO

Toda afirmação relevante deve poder ser classificada como:

```text
FACT
INFERENCE
HYPOTHESIS
RECOMMENDATION
DECISION
UNKNOWN
```

Isso é especialmente importante para o futuro modo consultor.

Exemplo:

```text
FACT:
A manutenção da empilhadeira aumentou.

INFERENCE:
O aumento coincide com maior frequência de movimentação.

HYPOTHESIS:
A condição do trajeto pode estar contribuindo.

RECOMMENDATION:
Investigar rotas e componentes afetados.

DECISION:
Gestão autoriza estudo de rota dedicada.

UNKNOWN:
Ainda não sabemos se a intervenção reduzirá o custo.
```

---

## 34. Regra de reversibilidade

Toda mudança deve ser classificada como:

- reversível;
- parcialmente reversível;
- difícil de reverter;
- irreversível.

Quanto menor a reversibilidade, maior a exigência de revisão.

---

## 35. Regra de escopo

Uma mudança deve declarar:

```text
IN SCOPE
OUT OF SCOPE
DEPENDENCIES
RISKS
ASSUMPTIONS
ACCEPTANCE CRITERIA
EVIDENCE REQUIRED
```

Isso reduz o risco de uma tarefa do Codex transformar uma pequena solicitação em refatoração arquitetural.

---

## 36. Registro de decisão

Toda decisão significativa deve responder:

1. Qual problema foi resolvido?
2. Qual era o estado anterior?
3. Quais alternativas foram consideradas?
4. Por que a alternativa escolhida foi selecionada?
5. Quais consequências foram aceitas?
6. Quais riscos permanecem?
7. Como a decisão será verificada?
8. Como poderá ser revertida ou substituída?

Quando isso tiver impacto arquitetural, usar ADR.

---

## 37. Baseline operacional

Quando este framework for aprovado, a primeira atividade deverá ser produzir uma fotografia do ELO:

```text
CAPABILITY
STATUS
MATURITY
OWNER
CANONICAL ARTIFACT
CONTRACT
IMPLEMENTATION
TEST
EVIDENCE
GAPS
RISK
NEXT ACTION
```

Essa fotografia será denominada:

**ELO Baseline Maturity Snapshot v1.0**

Ela deve registrar o estado real naquele momento e não ser alterada retroativamente sem histórico.

---

## 38. Regra de congelamento da baseline

Uma baseline pode ser congelada quando:

- conceitos canônicos estão identificados;
- duplicidades críticas estão conhecidas;
- owners estão definidos;
- contratos críticos estão identificados;
- capacidades principais estão classificadas;
- gaps críticos estão registrados;
- evidências disponíveis estão vinculadas;
- alterações futuras podem ser comparadas contra esse estado.

Congelar baseline não significa congelar desenvolvimento.

Significa congelar o **referencial de comparação**.

---

## 39. Processo de auditoria

### Auditoria inicial

1. inventariar diretórios;
2. inventariar documentos;
3. inventariar código;
4. inventariar testes;
5. inventariar ADRs;
6. identificar capacidades;
7. identificar contratos;
8. identificar duplicidades;
9. atribuir owners;
10. atribuir maturidade;
11. registrar evidências;
12. registrar gaps;
13. produzir snapshot.

### Auditoria incremental

Para cada PR:

```text
O que mudou?
→ qual capacidade?
→ qual requisito?
→ qual contrato?
→ qual risco?
→ quais testes?
→ qual evidência?
→ muda maturidade?
→ muda baseline?
```

---

## 40. Critério para declarar uma fase concluída

Uma fase somente deve ser declarada concluída quando:

- escopo foi executado;
- critérios de aceite foram atendidos ou exceções foram formalizadas;
- testes exigidos foram executados;
- documentação necessária foi atualizada;
- evidências foram registradas;
- gaps residuais foram classificados;
- não há bloqueador oculto conhecido;
- o status foi atualizado sem exagerar a maturidade.

---

## 41. Critério para Codex abrir PR

O Codex pode preparar PR quando:

- escopo está definido;
- arquivos afetados são conhecidos;
- mudança está dentro da autoridade da tarefa;
- testes foram executados ou a limitação foi explicitada;
- nenhuma alteração arquitetural não autorizada foi introduzida;
- documentação de impacto está disponível.

O Codex deve interromper e pedir revisão quando:

- contrato canônico precisa mudar;
- tenancy muda;
- segurança muda significativamente;
- provenance muda;
- nova autonomia é introduzida;
- arquitetura-base muda;
- duplicidade não pode ser resolvida com segurança;
- a alteração exige decisão de negócio.

---

## 42. Critério para merge

Merge não deve ser tratado como sinônimo de conclusão.

Antes do merge:

```text
Scope ✓
Authority ✓
Tests ✓
Review ✓
Security ✓ quando aplicável
Traceability ✓
Evidence ✓
Risk classified ✓
```

Depois do merge:

- atualizar snapshot quando a mudança altera maturidade;
- registrar nova evidência;
- atualizar ADR quando aplicável;
- manter histórico.

---

## 43. O que este framework NÃO faz

Não:

- cria automaticamente novas capacidades;
- substitui arquitetura;
- substitui testes;
- autoriza autonomia;
- define políticas corporativas;
- toma decisões trabalhistas;
- garante qualidade por si só;
- transforma documentos em software;
- elimina necessidade de revisão humana.

Ele cria o mecanismo para que essas coisas sejam avaliadas de forma rastreável.

---

## 44. Relação com o Cognitive Core

O Cognitive Core deve ser entendido como orquestrador de capacidades cognitivas, e não como depósito de toda a lógica do ELO.

O framework de maturidade deve permitir rastrear componentes como:

```text
Cognitive Core
 ├── Context
 ├── Knowledge
 ├── Memory
 ├── Reasoning
 ├── Evidence
 ├── Decision Support
 ├── Agent Lifecycle
 └── Consulting Mode
```

O `Consulting Mode` deve utilizar essas capacidades sem criar um segundo núcleo monolítico.

---

## 45. Roadmap de aplicação

### Fase A — Governança

- aprovar framework;
- estabelecer registry;
- validar owners;
- validar autoridade.

### Fase B — Snapshot

- inventariar capacidades atuais;
- classificar maturidade;
- registrar evidências;
- registrar gaps.

### Fase C — Contratos

- rastrear capacidades implementadas para contratos;
- identificar contratos ausentes;
- testar contratos críticos.

### Fase D — Implementação

- fechar gaps de código;
- melhorar testes;
- documentar execução.

### Fase E — Verificação

- executar gates;
- produzir evidências;
- atualizar maturidade.

### Fase F — Baseline

- revisar snapshot;
- congelar baseline;
- abrir roadmap pós-baseline.

---

## 46. Resultado esperado

Ao final da adoção deste framework, qualquer pessoa ou agente autorizado deverá conseguir responder:

> "O que o ELO realmente possui hoje?"

sem depender apenas de interpretação subjetiva da documentação.

Deve ser possível navegar:

```text
CAPACIDADE
  ↓
DEFINIÇÃO
  ↓
REQUISITO
  ↓
CONTRATO
  ↓
CÓDIGO
  ↓
TESTE
  ↓
EVIDÊNCIA
  ↓
MATURIDADE
  ↓
GAP
  ↓
PRÓXIMA AÇÃO
```

Esse é o objetivo central desta base.

---

## 47. Condição de aprovação deste documento

Este documento permanece `proposed` até revisão.

Para promovê-lo a `normative` devem ser confirmados:

- nomenclatura;
- escala de maturidade;
- hierarquia de autoridade;
- gates;
- critérios de evidência;
- relação com `ELO_ARTIFACT_METADATA_STANDARD.md`;
- relação com `ELO_REPOSITORY_NAVIGATION_RULES.md`;
- compatibilidade com ADRs existentes;
- compatibilidade com a arquitetura-base vigente.

Após aprovação, alterar o bloco de metadados para:

```yaml
status: normative
authority: baseline
version: 1.0.0
```

somente quando essa promoção tiver sido efetivamente decidida.
