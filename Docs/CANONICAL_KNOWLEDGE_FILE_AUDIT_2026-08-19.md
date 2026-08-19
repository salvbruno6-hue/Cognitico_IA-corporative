# ELO — Auditoria Arquivo a Arquivo para Consolidação Canônica

## Status
AUDIT BASELINE — 2026-08-19

## Objetivo
Transformar a decisão de consolidação PT/EN em uma migração verificável, sem assumir equivalência apenas pelo nome dos diretórios.

## Evidências confirmadas

### 01 — Meta Arquitetura
`01-meta-arquitetura/` possui conteúdo substantivo: Inteligência de Demanda, Mapa de Domínios, Glossário, Modelo Conceitual, Entidades, Relacionamentos, Regras de Negócio, framework de arquitetura de domínio e `ELO_ARCHITECTURE_MASTER.md`.

`01-meta-architecture/` possui `README.md`, `.gitkeep` e uma subárvore `cognitive-architecture` com artefatos atuais de aceitação, orçamento, evolução cognitiva, execução, supervisão, Forge e IA externa.

**Decisão:** NÃO tratar como duplicação direta. Classificar a família como `COMPLEMENTAR + CONFLITO POTENCIAL DE AUTORIDADE`. O conteúdo histórico português deve ser preservado e os artefatos atuais em inglês permanecem canônicos quando já governados pelo mapa/ADR.

### 07 — Data Engineering
`07-engenharia-de dados/` possui modelo lógico, dicionário de dados, SQLite, APIs, eventos e `DATA_ENGINEERING_MASTER.md`.

`07-data-engineering/` possui pelo menos `README.md` e scaffolding.

**Decisão:** conteúdo português é `EXCLUSIVO/COMPLEMENTAR` até prova em contrário. Não apagar. A árvore inglesa permanece proprietária e deve receber migração controlada.

### 11 — Models
`11-modelos/MODELS_LIBRARY_MASTER.md` é substantivo. `11-models-library/` contém somente `.gitkeep`.

**Decisão:** `MODELS_LIBRARY_MASTER.md` = `EXCLUSIVO` na árvore histórica no estado auditado. Migrar para o proprietário canônico antes de remover a árvore histórica.

### 12 — System Engineering
`12-sistemas/SYSTEMS_ENGINEERING_MASTER.md` é substantivo. `12-system-engineering/` contém somente `.gitkeep`.

**Decisão:** `SYSTEMS_ENGINEERING_MASTER.md` = `EXCLUSIVO` na árvore histórica no estado auditado. Migrar para o proprietário canônico antes de remoção.

### 05 — Cognitive Platform
O ADR confirma que `05-cognitivo-plataforma/` contém fundamentos cognitivos, filosofia, recursos estratégicos, inteligência de demanda, modelo de conhecimento e RAG, enquanto `05-cognitive-platform/` contém estrutura operacional mais recente, incluindo engine cognitivo, decision engine, memory/reasoning, especialistas e contratos Multiteiner.

**Decisão:** `COMPLEMENTAR + POSSÍVEL CONFLITO DE VERSÃO`. Não fazer merge textual automático. Exigir classificação por artefato e autoridade.

## Regras de classificação

- `DUPLICADO_EQUIVALENTE`: mesmo conceito, finalidade e conteúdo materialmente equivalente.
- `COMPLEMENTAR`: mesmo domínio, informação adicional sem substituição segura.
- `CONFLITANTE`: mesma finalidade, regras ou arquitetura incompatíveis.
- `EXCLUSIVO`: conteúdo sem equivalente seguro.
- `HISTÓRICO`: registro de evolução que deve permanecer rastreável.

## Regra de decisão
O nome do arquivo nunca é evidência suficiente para marcar duplicidade. Devem ser considerados: propósito, conteúdo, autoridade, referências, versão, proveniência e consumidores.

## Mapa inicial de migração

| Artefato | Origem | Destino canônico | Classe | Ação |
|---|---|---|---|---|
| ELO_ARCHITECTURE_MASTER.md | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | migrar após revisão |
| 01_Inteligencia_de_Demanda.md | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | migrar preservando PT |
| 01_Mapa_Dominios.md | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | comparar com arquitetura atual |
| 02_Glossario.md | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | migrar e preservar terminologia |
| 03_Modelo_Conceitual.md | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | comparar com modelos canônicos |
| 04_Entidades.md | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | cruzar com dados |
| 05_Relacionamentos.md | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | cruzar com modelo lógico |
| 06_Regras_Negocio.md | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/CONFLITO POTENCIAL | revisão obrigatória |
| DATA_ENGINEERING_MASTER.md | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO | migrar |
| 01_Modelo_Logico.md | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO/COMPLEMENTAR | migrar |
| 02_Dicionario_Dados.md | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO/COMPLEMENTAR | migrar |
| 03_SQLite.md | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO/COMPLEMENTAR | migrar |
| 04_APIs.md | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO/COMPLEMENTAR | migrar |
| 05_Eventos.md | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO/COMPLEMENTAR | migrar |
| MODELS_LIBRARY_MASTER.md | `11-modelos/` | `11-models-library/` | EXCLUSIVO | migrar |
| SYSTEMS_ENGINEERING_MASTER.md | `12-sistemas/` | `12-system-engineering/` | EXCLUSIVO | migrar |

## Impacto na resolução de endereços

Após a migração, consumidores devem resolver:

`concept_id/artifact_id → índice canônico → canonical_path`

Nunca:

`nome antigo → caminho físico presumido`

Caminhos históricos devem ser aliases, não autoridade.

## Gate para migração física

Nenhum diretório histórico será removido até que:

1. todos os arquivos tenham classificação;
2. todos os artefatos exclusivos estejam preservados;
3. referências tenham sido mapeadas;
4. IDs canônicos estejam atribuídos;
5. links/índices tenham sido atualizados;
6. testes de resolução e regressão estejam verdes;
7. CI confirme a integridade;
8. proveniência histórica esteja preservada.

## Próximo lote

Prioridade: `01-meta-arquitetura`, `07-engenharia-de dados`, `11-modelos`, `12-sistemas`.

Depois: `05-cognitivo-plataforma`, `13-referências`, `14-roteiros`, `15-ativos`, `00-empresa-manifesto`.

## Limites

Esta auditoria não autoriza exclusão. Ela estabelece evidência para a próxima etapa de migração controlada.
