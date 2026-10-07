---
artifact_id: ELO-SO-DOSSIER-PROTOCOL
title: ELO SO Dossier Protocol
family: 09-governance
layer: governance
type: protocol
status: normative
authority: protocol
owner: ELO Governance
version: 1.0.0
related:
  - ELO_ARTIFACT_METADATA_STANDARD
  - ELO_CONTEXT_ASSEMBLY_CONTRACT
  - ELO_EXTERNAL_AI_AUTHORITY_CONTRACT
  - ADR-0014-cognitive-runtime-loop
---

# ELO SO Dossier Protocol

## 1. Propósito

Definir o que é o Dossiê de Solicitação de Orçamento (SO) no ELO, o que ele contém, o que ele NÃO contém, e como ele se relaciona com as fontes existentes.

## 2. Definição

O Dossiê SO é um **índice governado** que:

- Declara a identidade canônica de uma SO
- Registra a máscara e a instância
- Referencia as fontes de conteúdo (sem copiá-las)
- Registra proveniência e rastreabilidade
- Declara o estado de maturação

O Dossiê SO **NÃO é**:

- Uma nova memória canônica
- Uma cópia das fontes existentes
- Uma autoridade paralela
- Um armazenamento de conteúdo próprio (exceto resumo contextual que não exista em outro lugar)

## 3. Regra fundamental — referenciar, não duplicar

Conforme `docs/architecture/ELO_CONTEXT_ASSEMBLY_CONTRACT.md`:

> "The assembler does not copy these layers into one persistent store."

O Dossiê SO segue essa regra. Ele referencia:

| Fonte | O que referencia |
|---|---|
| `memory/solicitations_learning/` | Aprendizado textual por SO |
| `08-ai/.../ORCAMENTO/APRENDIZADOS/` | Memória de cálculo e regras |
| `04-knowledge-handbook/` | Conhecimento geral aplicável |
| Supabase `elo_aprendizado_experiencias` | Experiência persistida |
| `memory/solicitations/` | Projeção de memória operacional |

Nenhuma dessas fontes é copiada para dentro do dossiê.

## 4. Identidade da SO

### 4.1 Máscara canônica

Toda SO segue a máscara:

`SO NNN.AA`

onde:

- `NNN` = identificador numérico de três dígitos;
- `AA` = ano em dois dígitos.

A representação interna canônica do resolver é `SO-NNN.AA`.

A chave de armazenamento por arquivo/pasta é `SO_NNN_AA`.

Exemplo:

| Forma | Exemplo |
|---|---|
| Máscara humana | `SO NNN.AA` |
| ID canônico do resolver | `SO-NNN.AA` |
| Chave de armazenamento | `SO_NNN_AA` |

Representações equivalentes devem ser normalizadas antes da resolução.

### 4.1.1 Autoridade de atribuição

O número da SO é atribuído pelo **Analista de Orçamento** antes de sua entrada no ciclo do ELO.

O ELO recebe uma identidade já atribuída e somente:
- valida o formato canônico;
- normaliza a representação textual;
- resolve referências;
- preserva a identidade e sua proveniência.

O ELO não gera, escolhe, incrementa, reserva, reinicia ou substitui o número da SO. O reinício anual de NNN é uma regra da atribuição externa, não um mecanismo do ELO.

Se a identidade recebida for ausente ou inválida, a operação deve ser bloqueada até que a SO atribuída seja fornecida/corrigida pela autoridade responsável.

### 4.2 Identidade

A identidade da SO deve ser estável independentemente da forma textual recebida.

O Dossiê registra:

- `so_id`
- `canonical_key`
- `mask`
- `tenant_id`
- `domain`
- `scope_state`
- `provenance`

`tenant_id` e `domain` estão sempre presentes como campos do dossiê. Podem ter valor nulo quando o contexto não os fornece. O `scope_state` reflete se ambos (`SCOPED`), um (`PARTIAL`) ou nenhum (`UNKNOWN`) está preenchido.

`so_id` sozinho não é uma identidade de escopo suficiente em ambiente multitenant.

O Dossiê não altera a identidade das fontes referenciadas.

## 5. Estrutura mínima do índice

O índice deve conter, no mínimo:

```yaml
so_id: SO-NNN.AA
canonical_key: SO_NNN_AA
mask: "SO NNN.AA"
maturation_state: REFERENCED
source_refs:
  - source_type: solicitations_learning
    path: memory/solicitations_learning/SO-NNN.AA.md
  - source_type: budget_learning
    path: 08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/...
  - source_type: knowledge_handbook
    path: 04-knowledge-handbook/...
  - source_type: supabase_experience
    table: elo_aprendizado_experiencias
  - source_type: operational_memory
    path: memory/solicitations/SO_NNN_AA/index.json
provenance:
  resolver: ELO SOResolver
```

Os campos de referência identificam localização e natureza da fonte. Não transportam o conteúdo da fonte.

## 6. Escopo e aplicabilidade

O ELO já exige isolamento por tenant e domínio. O Dossiê deve transportar o escopo conhecido da resolução, sem inventá-lo.

O `tenant_id` e o `domain` estão sempre presentes como campos do dossiê. Podem ter valor nulo quando o contexto não os fornece. O `scope_state` reflete se ambos (`SCOPED`), um (`PARTIAL`) ou nenhum (`UNKNOWN`) está preenchido.

`UNKNOWN` não significa equivalência entre tenants ou domínios. Uma referência histórica sem escopo verificável permanece consultiva e não pode ser promovida automaticamente para a SO atual.

As referências possuem `applicability: CONSULTIVE` por padrão. A classificação de uma fonte como aplicável à SO atual exige evidência explícita da fonte ou decisão governada; presença física do arquivo não basta.

## 7. Estado de maturação

O Dossiê registra o estado da agregação por referência, não promove conhecimento.

Estados previstos para a infraestrutura:

- `IDENTIFIED` — identidade reconhecida;
- `REFERENCED` — uma ou mais fontes foram localizadas/referenciadas;
- `VALIDATED` — estado de validação explicitamente fornecido por uma fonte governada.

O resolver não deve inferir `VALIDATED` apenas pela existência de uma fonte. `REFERENCED` significa somente que uma referência foi localizada; não significa que o conteúdo seja aplicável, correto ou aprovado.

## 8. Proveniência e autoridade

Cada referência deve preservar:

- tipo da fonte;
- localização;
- autoridade da fonte quando conhecida;
- existência/localização observada;
- origem da resolução.

A autoridade permanece na fonte canônica.

O Dossiê não promove:

- PRECEDENT;
- LEARNING_CANDIDATE;
- VALIDATED_LEARNING;
- regra corporativa;
- conhecimento global.

## 9. Isolamento e escopo

O Dossiê deve preservar o contexto da SO e nunca cruzar silenciosamente tenant, domínio ou escopo.

A existência de uma referência em uma SO não autoriza sua reutilização em outra SO.

Referências históricas são consultivas e devem ser avaliadas pelo contexto vigente.

## 10. Integração

A infraestrutura do Dossiê integra-se de forma aditiva:

`SOResolver → SODossier → CONTEXTUALIZE`

O CRL continua responsável somente pela orquestração. Nenhum novo estágio do CRL é criado.

O Dossiê não modifica:

- Cognitive Core;
- CRL;
- workflows existentes;
- memória canônica;
- fontes de conhecimento;
- Supabase.

## 11. Regra de não duplicação

Se uma informação já possui fonte canônica, o Dossiê deve armazenar uma referência, não uma cópia.

Qualquer evolução futura que transforme o Dossiê em armazenamento de conteúdo deve ser tratada como mudança arquitetural independente e submetida à governança.

## 12. Limites de implementação

A implementação inicial fornece:

- contrato normativo;
- README operacional;
- modelo `SODossier`;
- extensão aditiva do `SOResolver`;
- exposição no estágio `CONTEXTUALIZE`;
- testes de identidade, referências e integração.

Não fornece:

- nova persistência;
- consulta direta ao Supabase;
- novo workflow;
- novo estágio do CRL;
- alteração das fontes referenciadas.
