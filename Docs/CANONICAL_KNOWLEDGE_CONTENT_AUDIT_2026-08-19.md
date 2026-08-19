# ELO — Auditoria de Conteúdo e Consolidação Canônica

**Data:** 2026-08-19  
**Status:** AUDITORIA EM EXECUÇÃO  
**Regra:** nenhuma exclusão física nesta fase

## 1. Objetivo

Auditar as árvores PT/EN e os artefatos semanticamente próximos antes da consolidação física, determinando se cada conteúdo é equivalente, complementar, conflitante, exclusivo ou histórico.

## 2. Critério profissional de classificação

| Código | Classificação | Ação |
|---|---|---|
| EQUIVALENTE | Mesmo conceito e finalidade, sem perda material | um proprietário canônico + alias |
| COMPLEMENTAR | Mesmo domínio, informações diferentes úteis | consolidar conteúdo sob um proprietário |
| CONFLITANTE | Mesmo conceito, afirmações/regras divergentes | preservar ambos e abrir decisão de governança |
| EXCLUSIVO | Não existe equivalente funcional | manter como autoridade própria |
| HISTÓRICO | Evidência de evolução, decisão ou legado | preservar como histórico; não usar como autoridade |
| ESTRUTURAL | Diretório/placeholder sem conteúdo conceitual próprio | não transformar em conhecimento |

## 3. Evidências verificadas

### 3.1 Família 00 — manifesto empresarial

Existem simultaneamente `00-empresa-manifesto` e `00-enterprise-manifest`.

`00-enterprise-manifest` contém apenas `.gitkeep` e `README.md`, enquanto `00-empresa-manifesto` contém os artefatos substantivos de missão, objetivos, capacidades, cadeia de valor, modelo operacional, stakeholders e regras estratégicas. Portanto, **não são duas autoridades de conteúdo equivalentes**. A árvore inglesa é estrutural/placeholder nesta evidência. fileciteturn572file0

Dentro de `00-empresa-manifesto`, existem duplicidades de conteúdo em português:

- `01_Missao.md` e `MISSAO.md`: ambos definem a missão do ELO, com redação parcialmente divergente. A primeira fala em integração, conhecimento e execução; a segunda em integração, conhecimento e suporte à decisão. Isso é **CONFLITANTE/COMPLEMENTAR**, não duplicado seguro. fileciteturn578file0turn579file0
- `02_Objetivos.md` e `OBJETIVOS_ESTRATEGICOS.md`: ambos tratam dos objetivos estratégicos, mas possuem listas diferentes. Classificação: **CONFLITANTE/COMPLEMENTAR**. fileciteturn580file0turn581file0

**Decisão:** não apagar nenhum dos quatro arquivos. O conceito deve receber um único `concept_id`, mas as versões devem ser reconciliadas antes da escolha do texto canônico.

### 3.2 Família 01 — meta-arquitetura

Existem `01-meta-architecture` e `01-meta-arquitetura`. A árvore inglesa atualmente contém apenas `.gitkeep`, `README.md` e um diretório `cognitive-architecture`, enquanto a árvore portuguesa contém os artefatos substantivos de inteligência de demanda, mapa de domínios, glossário, modelo conceitual, entidades, relacionamentos, regras de negócio e frameworks arquiteturais. fileciteturn573file0turn574file0

**Decisão:** classificar a árvore inglesa como **ESTRUTURAL/LEGACY CANDIDATE**, não como duplicado de conteúdo. A consolidação deve preservar o conteúdo português.

### 3.3 Família 05 — plataforma cognitiva

Existem `05-cognitive-platform` e `05-cognitivo-plataforma`. Ambas possuem conteúdo. A árvore inglesa contém, entre outros, `ELO-018-GOVERNED-CYCLE-MEMORY.md`, `ELO_COGNITIVE_ENGINE.md`, `ELO_MEMORY_ENGINE.md`, `ELO_REASONING_ENGINE.md`, documentação de especialistas e contratos Multiteiner/NR24. fileciteturn575file0

A árvore portuguesa contém artefatos diferentes, como `COGNITIVE_FUNDAMENTALS.md`, `CORE-004_Filosofia_do_ELO.md`, `CORE-007_Recursos_Estrategicos.md`, `INTELIGENCIA_DE_DEMANDA.md`, `KNOWLEDGE_MODEL.md` e `RAG.md`. fileciteturn576file0

**Decisão:** **COMPLEMENTAR**, não duplicado. Não consolidar por simples equivalência de nome. A família exige classificação arquivo-a-arquivo.

### 3.4 Família 06 — engenharia do conhecimento

`06-knowledge-engineering` contém `KNOWLEDGE_ENGINEERING_MASTER.md`, índices e masters regulatórios da Multiteiner, NR24 e documentação de agentes. fileciteturn577file0

Não foi encontrada, nesta etapa de evidência, uma árvore portuguesa paralela equivalente. **Não executar renomeação por tradução sem evidência.**

### 3.5 Família 07 — engenharia de dados

A raiz apresenta `07-data-engineering` e `07-engenharia-de dados`. A existência simultânea confirma uma colisão estrutural de nomenclatura PT/EN e o espaço no nome português é um risco adicional para scripts e consumidores. A classificação de conteúdo depende da auditoria dos arquivos internos antes da remoção.

**Decisão preliminar:** `07-data-engineering` é candidato a proprietário canônico pela convenção estrutural vigente; `07-engenharia-de dados` permanece legado até conteúdo auditado.

## 4. Impacto na resolução de endereços

A migração não deve alterar diretamente os consumidores para caminhos novos em massa. O consumidor deve passar progressivamente por identidade lógica:

```text
consulta
  ↓
concept_id / artifact_id
  ↓
Canonical Knowledge Index
  ↓
canonical_path
  ↓
conteúdo
```

Caminhos antigos devem ser tratados como aliases temporários:

```text
legacy_path → artifact_id → canonical_path
```

O `SourceResolver` já existente deve permanecer como fronteira de resolução autorizada; não será criada uma segunda autoridade de resolução no Core. A implementação atual já valida tenant, domínio, principal, sessão, requisição, correlação, autorização e proveniência antes de registrar material recuperado na memória temporal. 

## 5. Regras de decisão para a próxima fase

1. Nunca excluir porque nomes parecem iguais.
2. Nunca substituir conteúdo conflitante silenciosamente.
3. Nunca usar tradução de nome como prova de equivalência semântica.
4. Um conceito pode possuir múltiplos artefatos históricos, mas apenas um proprietário canônico.
5. Complementares devem ser consolidados sem perda de proveniência.
6. Conflitantes exigem decisão explícita de governança.
7. Arquivos históricos permanecem recuperáveis.
8. O caminho físico é endereço; `artifact_id` é identidade.
9. O consumidor novo deve preferir identidade lógica.
10. A remoção física somente ocorre após zero dependências e validação de conteúdo.

## 6. Estado atual

| Frente | Estado |
|---|---|
| Ponto primário | CONCLUÍDO |
| Modelo de identidade | CONCLUÍDO |
| Inventário estrutural | EM EXECUÇÃO |
| Auditoria semântica | EM EXECUÇÃO |
| Mapa de dependências | PRÓXIMO |
| Reconciliação de conflitos | PENDENTE |
| Migração de referências | PENDENTE |
| Migração física | BLOQUEADA ATÉ GATES |
| Exclusão | BLOQUEADA |

## 7. Próximo gate

Completar a matriz arquivo-a-arquivo das famílias restantes, gerar `artifact_id` somente após classificação e produzir o mapa de impacto para cada consumidor. Depois disso será possível iniciar a migração controlada de aliases e referências.
