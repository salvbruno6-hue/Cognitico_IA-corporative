# ELO Cognitive Context, Knowledge and Memory v1.0

**Status:** Documento canônico subordinado à baseline
**Escopo:** camada cognitiva do ELO
**Finalidade:** fixar contratos de Context, Knowledge e Memory sem redefinir suas fronteiras canônicas.

## 1. Objetivo

Este documento consolida os contratos de contexto, conhecimento e memória do ELO para suportar raciocínio, decisão, recuperação e rastreabilidade sem duplicar responsabilidades de outros domínios.

## 2. Responsabilidades

### Context
Context representa informação situacional de curta duração necessária para interpretar uma tarefa, interação, consulta ou evento. Context é transitório e deve refletir o estado relevante no momento do uso.

### Knowledge
Knowledge representa conteúdo corporativo persistente, governado e recuperável, derivado de fontes identificáveis e sujeito a versionamento, classificação e provenance.

### Memory
Memory representa registro cognitivo governado derivado de experiências, interações, decisões ou resultados. Memory pode referenciar Context e Knowledge, mas não os substitui nem os redefine.

## 3. Limites

- Context não é repositório permanente.
- Knowledge não é memória de sessão.
- Memory não é conhecimento bruto.
- Nenhum dos três deve assumir responsabilidades de Reasoning, Decision, Agent ou Provenance.

## 4. Modelo conceitual

### Context object
- context_id
- tenant_id
- domain
- source
- scope
- ttl / expiration policy quando aplicável
- created_at
- updated_at
- provenance_ref

### Knowledge object
- knowledge_id
- tenant_id
- domain
- source_ref
- classification
- version
- validity
- owner
- provenance_ref
- created_at
- updated_at

### Memory object
- memory_id
- tenant_id
- domain
- context_ref
- knowledge_ref
- version
- source
- confidence
- owner
- retention_class
- status
- provenance_ref
- created_at
- updated_at

## 5. Lifecycle

### Context lifecycle
Capture -> normalize -> use -> expire or refresh.

### Knowledge lifecycle
Ingest -> validate -> classify -> version -> publish -> update or retire.

### Memory lifecycle
Create -> evaluate -> store -> retrieve -> update -> archive -> expire.

## 6. Interfaces

Entradas esperadas:
- Session layer
- Cognitive request pipeline
- Knowledge ingestion pipeline
- Agent outputs when validated

Saídas esperadas:
- Reasoning Engine
- Decision Engine
- Search and retrieval utilities
- Audit and provenance services

## 7. Regras de governança

1. Toda criação de Memory deve manter referência a sua origem ou ao mecanismo de geração.
2. Toda Knowledge entry deve possuir owner, version and classification.
3. Context com TTL ou validade deve ser tratado como conteúdo transitório.
4. Nenhum registro pode ser promovido de Context para Knowledge sem validação e política aplicável.
5. Nenhum resultado de IA deve ser tratado como conhecimento até passar por validação governada quando a criticidade exigir.

## 8. Eventos

- ContextCreated
- ContextRefreshed
- ContextExpired
- KnowledgeIngested
- KnowledgeValidated
- KnowledgeVersioned
- KnowledgeRetired
- MemoryCreated
- MemoryUpdated
- MemoryArchived
- MemoryExpired

## 9. Observabilidade

Métricas recomendadas:
- tempo de criação de contexto
- taxa de expiração de contexto
- taxa de validação de conhecimento
- volume de memória por tenant e domain
- taxa de recuperação de memória
- incidência de conteúdos sem provenance

## 10. Compatibilidade

Este documento não redefine as entidades canônicas. Ele apenas detalha os contratos operacionais que derivam da baseline.

---

**Dependência principal:** ELO Core Architecture Baseline v1.0
**Categoria:** Cognitive Platform