# ELO SO Dossiers

## Finalidade

`forge/dossiers/` contém a infraestrutura operacional do **Dossiê SO**.

O Dossiê SO é um **índice governado por referência**. Ele identifica uma SO e aponta para as fontes existentes. Não é uma nova memória nem uma cópia dos documentos.

## Regra operacional

> **Referenciar, não duplicar.**

As fontes permanecem em seus owners canônicos:

| Fonte | Responsabilidade |
|---|---|
| `memory/solicitations_learning/` | aprendizado textual por SO |
| `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/` | aprendizados e memória documental de orçamento |
| `04-knowledge-handbook/` | conhecimento corporativo reutilizável |
| Supabase `elo_aprendizado_experiencias` | experiência persistida |
| `memory/solicitations/` | projeção operacional de solicitações |

O Dossiê não copia o conteúdo dessas fontes.

## Identidade

A convenção é:

```text
SO NNN.AA     # máscara humana
SO-NNN.AA     # ID canônico do resolver
SO_NNN_AA     # chave de armazenamento
```

## Índice lógico

A implementação do índice está em:

```text
src/elo/cognitive/runtime/knowledge/so_dossier.py
```

O módulo produz referências para:

- identidade da SO;
- aprendizado textual;
- aprendizado de orçamento;
- handbook;
- experiência persistida no Supabase;
- memória operacional;
- proveniência;
- estado de maturação.

## Relação com o resolver

```text
SO
 ↓
SOResolver
 ↓
SODossier
 ↓
CONTEXTUALIZE
```

A integração é aditiva. Os campos existentes de `SOResolver.resolve()` permanecem disponíveis.

## Não fazer

Não usar `forge/dossiers/` para:

- armazenar cópias de TR;
- copiar PTS Técnica;
- copiar orçamento;
- copiar PTS Pós;
- copiar memória quantitativa do Supabase;
- promover aprendizado;
- criar autoridade paralela;
- substituir `memory/`, `04-knowledge-handbook/` ou Supabase.

## Validação

A infraestrutura deve ser validada pelos testes em:

```text
tests/cognitive/runtime/test_so_dossier.py
tests/cognitive/runtime/test_so_resolver.py
```

O dossiê é uma camada de índice e referência, não uma camada adicional de autoridade.


## Escopo e aplicabilidade

O identificador da SO não substitui o escopo cognitivo. Quando disponível, o resolver transporta `tenant_id` e `domain` para o dossiê.

- `SCOPED`: tenant e domínio conhecidos;
- `PARTIAL`: apenas parte do escopo conhecida;
- `UNKNOWN`: escopo não fornecido.

`UNKNOWN` nunca autoriza mistura entre tenants ou domínios.

As referências do dossiê são `CONSULTIVE` por padrão. Encontrar um arquivo não significa que seu conteúdo foi aplicado à SO atual. A promoção para aplicável ou validado depende da evidência e da governança da fonte.

## Descoberta de fontes

Índices e metadados canônicos têm precedência sobre convenções de nomes de arquivo. A busca por padrão de filename existe apenas como fallback para registros históricos que ainda não possuem referência indexada.

Isso evita que o nome físico do arquivo se torne uma segunda autoridade.

## Compatibilidade

A máscara operacional do resolver é `SO NNN.AA`. O parser de linguagem natural continua tolerante na entrada, mas delega a normalização final ao `SOResolver`. Assim, somente IDs conformes entram no contexto cognitivo.
