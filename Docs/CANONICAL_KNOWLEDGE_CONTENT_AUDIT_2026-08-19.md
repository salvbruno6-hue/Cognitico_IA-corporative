# ELO — Auditoria de Conteúdo e Consolidação Canônica

**Data:** 2026-08-19  
**Status:** AUDITORIA EM EXECUÇÃO  
**Regra:** nenhuma exclusão física ocorre sem classificação, migração, validação de referências e gate de consumidores.

## 1. Objetivo

Auditar as árvores PT/EN e os artefatos semanticamente próximos antes da consolidação física, determinando se cada conteúdo é equivalente, complementar, conflitante, exclusivo, histórico ou estrutural.

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

### 3.1 Família 00 — manifesto empresarial — CONSOLIDADA NO OWNER CANÔNICO

Na árvore anterior, `00-enterprise-manifest` continha apenas `.gitkeep` e `README.md`, enquanto `00-empresa-manifesto` continha os artefatos substantivos de missão, objetivos, capacidades, cadeia de valor, modelo operacional, stakeholders e regras estratégicas.

A classificação foi **COMPLEMENTAR/CONSOLIDAR**. O conteúdo substantivo foi migrado para `00-enterprise-manifest/`, preservando a proveniência individual dos oito artefatos:

- `01_Missao.md`;
- `02_Objetivos.md`;
- `03_Capacidades.md`;
- `04_Cadeia_de_Valor.md`;
- `05_Modelo_Operacional.md`;
- `06_Stakeholders.md`;
- `07_Regras_Estrategicas.md`;
- `ENTERPRISE_MANIFESTO.md`.

A pasta física `00-empresa-manifesto/` foi removida somente depois da criação dos owners canônicos e atualização do README/registro de migração. O caminho antigo passa a ser **legacy_path**, não autoridade documental.

A remoção física ainda requer a validação automatizada final de consumidores, referências e aliases para que a família seja marcada como encerrada também no gate de runtime.

### 3.2 Família 01 — meta-arquitetura

Existem `01-meta-architecture` e `01-meta-arquitetura`. A árvore inglesa possui estrutura operacional e a árvore portuguesa possui conteúdo histórico/substantivo. **Decisão: CONTENT_REVIEW_REQUIRED.** Não remover por tradução de nome.

### 3.3 Família 05 — plataforma cognitiva

Existem `05-cognitive-platform` e `05-cognitivo-plataforma`, ambas com conteúdo. **Decisão: COMPLEMENTAR / CONTENT_REVIEW_REQUIRED.** A família exige classificação arquivo-a-arquivo.

### 3.4 Família 06 — engenharia do conhecimento

`06-knowledge-engineering` permanece como owner operacional sem uma árvore portuguesa paralela equivalente identificada nesta etapa. Não executar renomeação por tradução.

### 3.5 Família 07 — engenharia de dados

`07-data-engineering` e `07-engenharia-de dados` permanecem em revisão. O master legado já foi removido, mas o conteúdo restante da árvore portuguesa ainda precisa de classificação arquivo-a-arquivo. O espaço no nome português também constitui risco adicional para consumidores e scripts.

## 4. Impacto na resolução de endereços

A migração não deve usar caminhos físicos como identidade de conhecimento. O fluxo canônico permanece:

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

Caminhos antigos devem ser tratados como aliases temporários quando ainda houver consumidores:

```text
legacy_path → artifact_id → canonical_path
```

## 5. Regras de decisão

1. Nunca excluir porque nomes parecem iguais.
2. Nunca substituir conteúdo conflitante silenciosamente.
3. Nunca usar tradução de nome como prova de equivalência semântica.
4. Um conceito pode possuir múltiplos artefatos históricos, mas apenas um proprietário canônico.
5. Complementares devem ser consolidados sem perda de proveniência.
6. Conflitantes exigem decisão explícita de governança.
7. Arquivos históricos permanecem recuperáveis quando houver valor de proveniência.
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
| Família 00 — conteúdo | CONSOLIDADO |
| Família 00 — owner canônico | CONSOLIDADO |
| Família 00 — referências/consumidores/runtime | GATE FINAL |
| Mapa de dependências | PRÓXIMO |
| Reconciliação de conflitos | PENDENTE |
| Migração de referências | EM EXECUÇÃO |
| Migração física das demais famílias | BLOQUEADA ATÉ GATES |
| Exclusão das demais famílias | BLOQUEADA |

## 7. Próximo gate

Completar a matriz arquivo-a-arquivo das famílias `01`, `05` e `07`, gerar `artifact_id` após classificação e produzir o mapa de impacto para cada consumidor. A remoção física somente poderá ocorrer depois de referências, aliases, testes e runtime comprovarem a resolução canônica.
