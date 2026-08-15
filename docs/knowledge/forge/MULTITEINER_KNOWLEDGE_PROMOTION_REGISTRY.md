# Multiteiner Knowledge Promotion Registry

**Issue:** #101 / ELO-014  
**Source:** `04-knowledge-handbook/MULTITEINER_ORGANIZATIONAL_CONTEXT.md`  
**Method:** `04-knowledge-handbook/MULTITEINER_ELO_CONTEXT_GAPS_AND_STRUCTURE_PLAN.md`

Este registro é uma seleção governada do conteúdo do Forge. Ele não replica a fonte.

| ID | Conteúdo | Classificação | Destino ELO | Condição |
|---|---|---|---|---|
| MT-001 | Fluxo Comercial → Engenharia → Orçamento → PCP → Compras → Almoxarifado → Produção → Expedição → Locação/Retorno | REUSE | CorporateSystemicModel | já coberto; manter referência à fonte |
| MT-002 | Demanda/AF, modalidade venda x locação, escopo, prazo e alterações | EXTEND | Commercial Faculty | validar contratos e autoridade antes de promover regras |
| MT-003 | Projeto, versão, BOM/LM, aprovação e liberação técnica | EXTEND | Engineering/Project Faculty | exigir vínculo projeto → BOM → SO |
| MT-004 | Capacidade, sequenciamento, prioridade, planejamento e planejado × realizado | EXTEND | PCP Faculty | exigir evidência de capacidade/tempos |
| MT-005 | Cotação, pedido, fornecedor, lead time e material crítico | EXTEND | Procurement Faculty | validar fonte operacional |
| MT-006 | Etapas produtivas, capacidade, WIP, gargalo, retrabalho e liberação | EXTEND | Production Faculty | não transformar gargalo histórico em regra universal |
| MT-007 | Expedição, conformidade, carregamento, liberação e retorno | EXTEND | Logistics/Expedition Faculty | validar critérios e registros |
| MT-008 | Retorno, inspeção, avaria, reparo e liberação ao estoque | EXTEND | AfterSales/Asset Lifecycle Faculty | separar fato, custo, causa e decisão |
| MT-009 | Information Gap Framework | EXTEND | Knowledge Governance | registrar lacunas sem invenção |
| MT-010 | Perguntas de esclarecimento vinculadas a gaps | EXTEND | Reasoning/Decision Support | pergunta deve ser verificável e ter evidência esperada |
| MT-011 | Diagnóstico de maturidade 0–5 | EXTEND | Governance/Assessment | nota somente com evidência; caso contrário NÃO AVALIADO |
| MT-012 | KPIs por setor | ROADMAP | Analytics | referência para desenho de indicadores; não promover como verdade operacional sem validação |
| MT-013 | Gargalo histórico de pintura | ROADMAP | Production Knowledge | evidência histórica; não regra universal |
| MT-014 | Componentes complementares críticos | ROADMAP | Production/Procurement Knowledge | validar atualidade e contexto |
| MT-015 | Reprogramações e dispersão de informação | ROADMAP | Process/Risk Knowledge | tratar como hipótese histórica até validação |
| MT-016 | Najason, CAD e planilhas | ROADMAP | Integration Sources | adapters, nunca dependência do Core |
| MT-017 | Regras de provenance, tenant, need-to-know, confidencialidade e human-in-the-loop | REUSE | Governance | alinhar com contratos canônicos existentes |

## Regra de promoção

Somente itens `EXTEND` podem virar candidatos à faculdade lógica após validação. Itens `ROADMAP` permanecem como conhecimento de referência/teste. `REUSE` não deve criar duplicação.

## Regra de conflito

Se outra fonte apresentar regra incompatível com um item deste registro, criar `CONFLICT` e manter ambas as versões/proveniências até decisão governada.

## Regra de remoção

A remoção do documento fonte não pode apagar itens já promovidos e validados. Itens específicos devem permanecer identificados como overlays ou conhecimento dependente da fonte.

## Proveniência mínima

Cada promoção deve guardar:

`source_path + source_version/commit + registry_id + domain + scope + evidence_refs + promotion_decision + promoted_at`.
