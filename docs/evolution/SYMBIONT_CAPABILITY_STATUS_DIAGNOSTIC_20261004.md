# Simbionte — Diagnóstico, Organização e Orquestração de Capacidades

**Status:** read model governado, somente leitura  
**Owner:** ELO Cognitive / Symbiont  
**Autoridade:** nenhuma nova; reutiliza owners, contratos, evidências, Evolution Gate e runtime boundaries existentes.

## Objetivo

Permitir que a Simbionte organize o estado de uma capability e conecte as habilidades já existentes em uma cadeia única de governança, sem transformar a composição em uma nova autoridade.

A cadeia canônica é:

```text
CAPABILITY REGISTRY
      ↓
CANONICAL OWNER
      ↓
SymbiontImplementationView
      ↓
LoopReadiness / ImplementationEvidence
      ↓
CapabilityEvolutionReview
      ↓
Evolution Gate
      ↓
Governance / Merge
      ↓
Canonical Runtime
      ↓
RuntimeOperationalEvidence
      ↓
EVOLUÇÃO_DE_CAPACIDADES
```

A Simbionte **orquestra a leitura e o encaminhamento**, mas não substitui nenhum desses owners.

## Relações de governança

O módulo `src/elo/cognitive/symbiont_capability_governance.py` materializa relações somente de leitura:

| Origem | Relação | Destino | Autoridade |
|---|---|---|---|
| SIMBIONTE | DIAGNOSES | Capability | read model da Simbionte |
| Capability | OWNED_BY | Canonical Owner | resolução de ownership |
| Capability | DESCRIBED_BY | SymbiontImplementationView | contrato de implementação |
| SymbiontImplementationView | FEEDS | LoopReadiness | readiness/evidence contract |
| LoopReadiness | FEEDS | CapabilityEvolutionReview | implementation/evolution loop |
| CapabilityEvolutionReview | OBSERVES | EVOLUÇÃO_DE_CAPACIDADES | capability evolution |
| CapabilityEvolutionReview | HANDOFF_TO | Evolution Gate | Evolution Gate existente |
| Evolution Gate | GOVERNS | promoção/merge | Evolution Gate existente |
| Canonical Runtime | EMITS | RuntimeOperationalEvidence | boundary de evidência operacional |

Essas relações não concedem autorização.

## Separação de responsabilidades

### 1. Registry

Responde:

- que capability existe;
- qual seu owner;
- qual seu estado registrado;
- quais gaps estão registrados.

### 2. SymbiontImplementationView

Responde:

- onde a implementação está;
- a qual capability pertence;
- quem é o owner;
- qual é o ownership;
- quais contratos/dependências/evidências estão ligados;
- qual o estágio;
- qual o estado de runtime/governança.

### 3. LoopReadiness

Responde:

- se existem condições técnicas mínimas para entrar no Implementation Loop;
- quais condições estão faltando.

Não autoriza implementação.

### 4. CapabilityEvolutionReview

Responde:

- como a capability está evoluindo;
- se há ganho, estabilidade ou regressão;
- qual intervenção deve ser considerada;
- se existe necessidade de continuar o loop.

Não promove a capability.

### 5. Evolution Gate

Continua sendo a autoridade para a decisão de evolução.

### 6. RuntimeOperationalEvidence

Continua sendo a fonte para evidência operacional real.

### 7. Simbionte

Faz a composição:

```text
observar
→ relacionar
→ diagnosticar
→ localizar bloqueio
→ apontar owner
→ indicar próxima intervenção
→ encaminhar ao gate apropriado
```

Ela não executa autorização implícita.

## Estados de leitura

Os estados do diagnóstico são uma **classificação de leitura**, não uma nova escala de maturidade:

- `NOT_IMPLEMENTED`
- `IMPLEMENTED_NOT_TESTED`
- `TESTED_NOT_EVIDENCED`
- `EVIDENCED_NOT_RUNTIME`
- `RUNTIME_INTEGRATED`
- `OPERATIONALLY_EVIDENCED`
- `READY_FOR_EVOLUTION_GATE`
- `PRODUCTION_PROVEN`
- `BLOCKED`

A maturidade oficial continua pertencendo ao Registry/Baseline e aos critérios canônicos existentes.

## Regras de governança

- Reutilizar owner existente.
- Reutilizar contrato existente.
- Reutilizar Evolution Gate existente.
- Reutilizar Implementation Loop existente.
- Reutilizar runtime owner existente.
- Não criar segunda autoridade.
- Não inferir runtime pela existência de código.
- Não inferir produção por testes.
- Não converter evidência de laboratório em produção.
- Não transformar COMPLETED automaticamente em learning.
- Não autorizar a si própria.
- `canonical_mutation=false`.

## Anti-duplicidade

Antes de qualquer nova implementação:

```text
INSPECT
  ↓
REUSE
  ↓
EXTEND
  ↓
RELATE
  ↓
REFACTOR/MIGRATE
  ↓
CREATE ONLY IF INDISPENSABLE
```

Se o owner ou source of truth não puder ser resolvido, o estado é bloqueado/aguarda evidência.

## Resultado esperado

A Simbionte passa a conseguir responder de forma organizada:

```text
O QUE EXISTE?
      ↓
QUEM É O OWNER?
      ↓
ONDE ESTÁ IMPLEMENTADO?
      ↓
ESTÁ TESTADO?
      ↓
QUAL EVIDÊNCIA EXISTE?
      ↓
ESTÁ NO RUNTIME?
      ↓
HÁ EVIDÊNCIA OPERACIONAL?
      ↓
HÁ RESULTADO DE PRODUÇÃO?
      ↓
QUAL GATE É NECESSÁRIO?
      ↓
QUAL É A PRÓXIMA INTERVENÇÃO?
```

Sem criar uma nova skill concorrente.
