# ELO Forge → ELO Cognitivo — Matriz de Consolidação

**Status:** DRAFT
**Origem:** `salvbruno6-hue/ELO-Forge`
**Destino canônico:** `salvbruno6-hue/Cognitico_IA-corporative`
**Objetivo:** identificar o que foi construído no Forge que pertence ao ELO Cognitivo, sem promover o Forge a autoridade arquitetural independente.

## 1. Princípio

O `Cognitico_IA-corporative` é tratado como o repositório canônico do ecossistema ELO. O conteúdo do `ELO-Forge` é tratado como material de implementação, conhecimento, experimentação e especialização que deve ser avaliado e, quando pertinente, incorporado ao ELO Cognitivo.

Nenhum artefato é promovido automaticamente por cópia. A incorporação deve preservar autoridade, contratos, rastreabilidade, versionamento e testes definidos pelo Cognitico.

## 2. Classificação

- **INCORPORAR** — conteúdo pertence conceitualmente ao ELO Cognitivo e deve ser integrado.
- **RECONCILIAR** — conteúdo é útil, mas precisa ser comparado com contratos/arquitetura existentes antes da integração.
- **EXTRAIR** — o conhecimento é válido, mas a forma atual não deve ser mantida.
- **IMPLEMENTAR** — código/schema/migration pode ser aproveitado após aprovação arquitetural.
- **PRESERVAR COMO EVIDÊNCIA** — manter histórico/origem, sem torná-lo canônico.
- **NÃO INCORPORAR** — conteúdo operacional, temporário ou fora da arquitetura cognitiva.
- **CONFLITO** — existe autoridade ou conceito concorrente; exige ADR antes de integração.

## 3. Matriz inicial

| Artefato Forge | Natureza | Destino Cognitico | Decisão | Tratamento |
|---|---|---|---|---|
| `AGENTS.md` | Regras de agentes/governança | Regras oficiais de agentes | RECONCILIAR | Extrair princípios e alinhar às regras canônicas |
| `ELO_Blueprint_v1.0.md` | Blueprint operacional | Arquitetura de domínio/operacional | EXTRAIR | Preservar conhecimento; não substituir arquitetura cognitiva |
| `agents/ELO_ANALISAR_DIRETRIZ_ESPECIALISTA_ORCAMENTO.md` | Contrato comportamental de especialista | Agents / Specialist Capabilities / Decision Support | INCORPORAR | Transformar em contrato formal versionado |
| `agents/PLANILHA_ORCAMENTO_BASE_ELO.md` | Conhecimento operacional/comercial | Domain Knowledge / Commercial / Budgeting | INCORPORAR | Normalizar taxonomia, regras e proveniência |
| `schemas/elo_governanca.md` | Contrato de governança | Governance / Contracts | RECONCILIAR | Comparar com contratos existentes |
| `sql/001_create_schemas.sql` | Infraestrutura SQL | Data / Persistence | RECONCILIAR | Não copiar sem validar modelo canônico |
| `sql/010_elo_governanca.sql` | Implementação de governança | Governance Data Layer | IMPLEMENTAR | Reconciliar regras, tabelas e autoridade |
| `supabase/migrations/20260521_001_create_elo_governanca.sql` | Migration | Persistence / Governance | RECONCILIAR | Verificar duplicidade com implementação atual |
| `supabase/migrations/20260525_009_kanban_setorial.sql` | Workflow/coordenação | Task/Work orchestration | RECONCILIAR | Determinar se pertence ao ELO ou a aplicação |
| `automation/` | Automação | Agent Orchestration / Execution | RECONCILIAR | Separar decisão ELO de execução técnica |
| `prompts/` | Instruções | Agent Contracts / Prompt Assets | INCORPORAR | Normalizar, versionar e definir autoridade |
| `docs/fase_1_governanca.md` | Roadmap/documentação | Governance roadmap | EXTRAIR | Fundir com roadmap oficial |
| `api/` | Integração | Integration Layer / API contracts | RECONCILIAR | Só incorporar APIs com contrato canônico |
| `dashboards/` | Interface/visualização | Observability/UI | RECONCILIAR | Incorporar somente se houver capacidade oficial |
| diretórios `.gitkeep`/workspace | Estrutura auxiliar | — | NÃO INCORPORAR | Sem valor arquitetural |

## 4. Capacidades que devem ser preservadas

### 4.1 Governança

Preservar como capacidade canônica:

- regras de negócio versionadas;
- parâmetros de sistema;
- validações de entrada;
- glossário;
- versionamento de entidades;
- políticas de acesso;
- bloqueio de remoção física quando essa regra for aprovada;
- rastreabilidade de decisões automatizadas.

### 4.2 Especialistas

Preservar a experiência acumulada no especialista de orçamento, especialmente:

- reconstrução de contexto;
- análise documental;
- distinção entre documento, análise, premissa, recomendação e pendência;
- identificação de interfaces e responsabilidades;
- análise de risco e custo;
- continuidade de trabalho;
- questionamento proativo;
- rastreabilidade da conclusão.

### 4.3 Conhecimento comercial

Preservar:

- taxonomias de produtos;
- famílias comerciais;
- composição de orçamento;
- venda versus locação;
- excedentes/customizações;
- serviços e mão de obra;
- regras de preenchimento;
- rastreabilidade da origem de cada informação.

## 5. Limites arquiteturais

O Forge não recebe autoridade sobre:

- definição do ELO;
- arquitetura canônica;
- contratos soberanos;
- governança final;
- decisão de baseline;
- definição do Cognitive Core.

Essas decisões permanecem no `Cognitico_IA-corporative`.

O Codex pode atuar como executor técnico. A execução não deve alterar a autoridade arquitetural do ELO.

## 6. Próxima ordem de implementação

1. Validar esta matriz.
2. Comparar cada artefato contra contratos existentes no Cognitico.
3. Criar ADRs para conflitos ou decisões duráveis.
4. Incorporar primeiro governança e contratos de especialistas.
5. Incorporar conhecimento de orçamento e taxonomias.
6. Reconciliar SQL/migrations com o modelo de dados oficial.
7. Reestruturar automações para separar decisão, orquestração e execução.
8. Validar testes e evidências.
9. Somente depois avaliar o papel definitivo do `ELO-Forge`.

## 7. Critério de conclusão

A consolidação só será considerada concluída quando cada artefato relevante do Forge possuir:

- destino definido;
- autoridade definida;
- contrato identificado;
- status de implementação;
- evidência de teste quando aplicável;
- origem preservada;
- ausência de duplicação ou conflito não resolvido.
