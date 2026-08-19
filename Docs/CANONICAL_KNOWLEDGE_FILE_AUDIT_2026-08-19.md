# ELO — Auditoria Arquivo a Arquivo para Consolidação Canônica

## Status
AUDIT BASELINE — 2026-08-19

## Objetivo
Transformar a decisão de consolidação PT/EN em uma migração verificável, sem assumir equivalência apenas pelo nome dos diretórios.

## Critério profissional

- `DUPLICADO_EQUIVALENTE`: mesmo conceito, finalidade e conteúdo materialmente equivalente.
- `COMPLEMENTAR`: mesmo domínio, informação adicional sem substituição segura.
- `CONFLITANTE`: mesma finalidade, regras ou arquitetura incompatíveis.
- `EXCLUSIVO`: conteúdo sem equivalente seguro.
- `HISTÓRICO`: registro de evolução que deve permanecer rastreável.
- `SCAFFOLDING`: placeholder sem conteúdo de domínio relevante.

O nome do arquivo nunca é evidência suficiente. São considerados propósito, conteúdo, autoridade, referências, versão, proveniência e consumidores.

## Evidências confirmadas

### 00 — Manifesto
`00-empresa-manifesto/` possui missão, objetivos, capacidades, cadeia de valor, modelo operacional, stakeholders e regras estratégicas. `00-enterprise-manifest/` possui README estratégico, mas não os equivalentes de conteúdo.

**Decisão:** não é duplicação direta. Conteúdo PT = `EXCLUSIVO/COMPLEMENTAR`; deve receber identidade e ser migrado individualmente. O README EN permanece contrato estrutural.

### 01 — Meta Arquitetura
`01-meta-arquitetura/` possui Inteligência de Demanda, Mapa de Domínios, Glossário, Modelo Conceitual, Entidades, Relacionamentos, Regras de Negócio, framework de arquitetura e `ELO_ARCHITECTURE_MASTER.md`. `01-meta-architecture/` possui README e uma subárvore `cognitive-architecture` com artefatos atuais de aceitação, orçamento, evolução cognitiva, execução, supervisão, Forge e IA externa.

**Decisão:** `COMPLEMENTAR + CONFLITO POTENCIAL DE AUTORIDADE`. Não fundir automaticamente. O conteúdo PT deve ser preservado e os artefatos atuais EN permanecem canônicos quando já governados pelo mapa/ADR.

### 05 — Cognitive Platform
`05-cognitivo-plataforma/` contém fundamentos cognitivos, filosofia, recursos estratégicos, inteligência de demanda, modelo de conhecimento e RAG. `05-cognitive-platform/` contém engine cognitivo, decision engine, memory/reasoning, especialistas e contratos Multiteiner.

**Decisão:** `COMPLEMENTAR + POSSÍVEL CONFLITO DE VERSÃO`. Exigir classificação por artefato e autoridade antes de qualquer consolidação.

### 07 — Data Engineering
`07-engenharia-de dados/` possui modelo lógico, dicionário, SQLite, APIs, eventos e `DATA_ENGINEERING_MASTER.md`. `07-data-engineering/` possui scaffolding/README/AGENTS.

**Decisão:** conteúdo PT = `EXCLUSIVO/COMPLEMENTAR` até prova em contrário. Migrar para o proprietário estrutural EN; não apagar.

### 11 — Models
`11-modelos/MODELS_LIBRARY_MASTER.md` é substantivo; `11-models-library/` contém somente `.gitkeep`.

**Decisão:** `MODELS_LIBRARY_MASTER.md` = `EXCLUSIVO` no estado auditado. Migrar para o proprietário canônico antes de remover a árvore histórica.

### 12 — System Engineering
`12-sistemas/SYSTEMS_ENGINEERING_MASTER.md` é substantivo; `12-system-engineering/` contém somente `.gitkeep`.

**Decisão:** `SYSTEMS_ENGINEERING_MASTER.md` = `EXCLUSIVO` no estado auditado. Migrar antes da remoção.

### 14 — Roadmap
`14-roteiros/ROADMAP_MASTER.md` é substantivo; `14-roadmap/` contém somente `.gitkeep`.

**Decisão:** `ROADMAP_MASTER.md` = `EXCLUSIVO/COMPLEMENTAR`. Migrar antes da remoção.

### 13 e 15
`13-reference-architecture/` e `15-assets/` foram confirmadas como scaffolding. As raízes portuguesas correspondentes ainda precisam de descoberta física precisa antes de qualquer decisão.

**Decisão:** `AUDIT_REQUIRED`; nenhuma movimentação.

## Caso crítico: conhecimento de produtos/contêineres

`ELO_Licitacoes_Conteineres_V2_1.md` e `ELO_Licitacoes_Conteineres_Composicoes_V2_1.md` pertencem ao mesmo domínio, mas têm finalidades diferentes.

- Base técnica: conhecimento consolidado, hierarquia de evidência, modelos e regras de consulta.
- Composições: quantitativos, insumos, curvas A/B/C e composição documental.

**Classificação: COMPLEMENTAR, não DUPLICADO_EQUIVALENTE.**

A base técnica também determina que informação interna, composição, referência externa e pendência sejam distinguidas e que quantitativos não sejam universalizados entre modelos/revisões. Portanto não haverá fusão textual indiscriminada.

## Mapa inicial de migração

| Artefato | Origem | Destino canônico | Classe | Ação |
|---|---|---|---|---|
| `ELO_ARCHITECTURE_MASTER.md` | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | migrar após revisão |
| `01_Inteligencia_de_Demanda.md` | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | migrar preservando PT |
| `01_Mapa_Dominios.md` | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | comparar com arquitetura atual |
| `02_Glossario.md` | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | migrar preservando terminologia |
| `03_Modelo_Conceitual.md` | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | cruzar com modelos |
| `04_Entidades.md` | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | cruzar com dados |
| `05_Relacionamentos.md` | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/COMPLEMENTAR | cruzar com modelo lógico |
| `06_Regras_Negocio.md` | `01-meta-arquitetura/` | `01-meta-architecture/` | EXCLUSIVO/CONFLITO POTENCIAL | revisão obrigatória |
| `DATA_ENGINEERING_MASTER.md` | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO | migrar |
| `01_Modelo_Logico.md` | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO/COMPLEMENTAR | migrar |
| `02_Dicionario_Dados.md` | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO/COMPLEMENTAR | migrar |
| `03_SQLite.md` | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO/COMPLEMENTAR | migrar |
| `04_APIs.md` | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO/COMPLEMENTAR | migrar |
| `05_Eventos.md` | `07-engenharia-de dados/` | `07-data-engineering/` | EXCLUSIVO/COMPLEMENTAR | migrar |
| `MODELS_LIBRARY_MASTER.md` | `11-modelos/` | `11-models-library/` | EXCLUSIVO | migrar |
| `SYSTEMS_ENGINEERING_MASTER.md` | `12-sistemas/` | `12-system-engineering/` | EXCLUSIVO | migrar |
| `ROADMAP_MASTER.md` | `14-roteiros/` | `14-roadmap/` | EXCLUSIVO/COMPLEMENTAR | migrar |

## Impacto na resolução de endereços

Depois da migração, consumidores devem resolver:

`concept_id/artifact_id → índice canônico → canonical_path`

Nunca:

`nome antigo → caminho físico presumido`

Caminhos históricos tornam-se aliases, não autoridade.

## Gate de migração física

Nenhum diretório histórico será removido até que:

1. todos os arquivos tenham classificação;
2. artefatos exclusivos estejam preservados;
3. referências estejam mapeadas;
4. IDs canônicos estejam atribuídos;
5. índices e links estejam atualizados;
6. testes de resolução e regressão estejam verdes;
7. CI confirme integridade;
8. proveniência histórica esteja preservada.

## Próxima sequência

**Lote A:** atribuir `artifact_id` aos masters substantivos.  
**Lote B:** migrar para proprietários EN sem perda.  
**Lote C:** atualizar índices/navegação.  
**Lote D:** validar referências e testes.  
**Lote E:** `DEPRECATED` somente após absorção integral.  
**Lote F:** remoção física somente após gate verde.

Esta auditoria não autoriza exclusão; ela estabelece evidência para a migração controlada.
