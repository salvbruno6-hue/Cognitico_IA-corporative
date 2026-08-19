# ELO — Família 05: Reconciliação Estrutural — 2026-08-19

## Objetivo

Registrar a reconciliação estrutural inicial da família 05 sem alterar o conceito do ELO e sem presumir que as árvores PT/EN sejam equivalentes.

## Contexto

A família 05 conecta conhecimento cognitivo e estrutura operacional. A árvore histórica `05-cognitivo-plataforma/` contém material substantivo, incluindo fundamentos cognitivos, filosofia, recursos estratégicos, inteligência de demanda, modelo de conhecimento e RAG. A árvore `05-cognitive-platform/` contém estrutura operacional efetiva, incluindo engine cognitivo, decision engine, memória/raciocínio, especialistas e contratos Multiteiner.

A evidência de árvore confirma arquivos como:

- `05-cognitive-platform/ELO_COGNITIVE_ENGINE.md`
- `05-cognitive-platform/ELO_DECISION_ENGINE.md`
- `05-cognitive-platform/ELO_MEMORY_ENGINE.md`
- `05-cognitive-platform/ELO_REASONING_ENGINE.md`
- `05-cognitive-platform/ELO_ESPECIALISTAS_ESTRUTURA_OPERACIONAL.md`
- `05-cognitive-platform/ELO-018-GOVERNED-CYCLE-MEMORY.md`
- `05-cognitive-platform/MULTITEINER_CORE_FORGE_REGULATORY_APPLICATION.md`

A árvore histórica contém, entre outros:

- `05-cognitivo-plataforma/COGNITIVE_FUNDAMENTALS.md`
- `05-cognitivo-plataforma/CORE-004_Filosofia_do_ELO.md`
- `05-cognitivo-plataforma/CORE-007_Recursos_Estrategicos.md`
- `05-cognitivo-plataforma/INTELIGENCIA_DE_DEMANDA.md`
- `05-cognitivo-plataforma/KNOWLEDGE_MODEL.md`
- `05-cognitivo-plataforma/RAG.md`

## Conclusão estrutural

Não há evidência suficiente para classificar a família 05 como simples duplicação PT/EN.

A hipótese mais segura é:

```text
05-cognitivo-plataforma
        │
        ├── conhecimento/fundamentos
        ├── filosofia
        ├── recursos estratégicos
        ├── inteligência de demanda
        ├── modelo de conhecimento
        └── RAG

                ↓ reconciliação por função

05-cognitive-platform
        │
        ├── engine cognitivo
        ├── decision engine
        ├── memory/reasoning
        ├── especialistas
        ├── ciclo governado
        └── contratos operacionais
```

A relação deve ser tratada como **potencialmente complementar**, não como duplicação automática.

## Regra de evolução estrutural

A evolução desta família deve:

1. preservar o conhecimento histórico;
2. manter uma autoridade clara por conceito;
3. separar fundamento conceitual de implementação/estrutura operacional quando essa distinção for real;
4. conectar referências entre as partes quando comprovadas;
5. evitar cópia textual apenas para uniformizar idioma;
6. não criar novo conceito apenas para justificar a organização;
7. não alterar `src/elo` nesta fase;
8. não remover arquivos históricos enquanto consumidores e equivalência não forem comprovados.

## Modelo de conexão

```text
fundamentos
    ↓
princípios cognitivos
    ↓
modelo de conhecimento
    ↓
arquitetura cognitiva
    ↓
engines / especialistas / memória / raciocínio
    ↓
contratos operacionais
    ↓
implementação
    ↓
testes e evidência
```

As setas são um modelo estrutural de auditoria. Uma seta somente se torna dependência operacional após evidência de referência/consumidor.

## Classificação atual

```text
FAMILY_05 = CONTENT_RECONCILIATION_REQUIRED
PT_TREE    = CONTENT_RICH
EN_TREE    = OPERATIONAL_STRUCTURE_PRESENT
RELATION   = POTENTIALLY_COMPLEMENTARY
EQUIVALENCE = NOT_PROVEN
MIGRATION  = BLOCKED
REMOVAL    = BLOCKED
```

## Próxima evidência

O próximo lote deve parear artefatos por função e conceito, não apenas por nome. Para cada par/candidato:

```text
identidade
→ conteúdo
→ função
→ referências
→ consumidor
→ autoridade
→ conexão
→ decisão
```

Nenhuma remoção ou fusão física é autorizada por este documento.

## Gate

```text
STRUCTURAL_CONTEXT = CONFIRMED
SEMANTIC_EQUIVALENCE = NOT_PROVEN
CONSUMER_MAPPING = PENDING
MIGRATION = BLOCKED
REMOVAL = BLOCKED
```
