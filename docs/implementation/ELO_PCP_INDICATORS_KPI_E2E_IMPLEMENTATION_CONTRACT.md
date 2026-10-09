# Contrato de Implementação E2E — PCP → Indicadores → KPI → API → MCP

Status: implementação pendente de código/migration/testes  
Autoridade: complementa a auditoria `docs/audits/ELO_PCP_KPI_MCP_E2E_AUDIT_20261009.md` sem criar autoridade paralela.

## 1. Resultado esperado

A implementação deve provar, sem inferência de dados ausentes:

`registro operacional → relação canônica → read-model → indicador → KPI governado (quando existir) → interpretação → evidência → CognitiveResponse → ELO-MCP → resposta ELO`

Rastreabilidade inversa obrigatória:

`resposta ELO → evidence_ref → indicador/KPI → read-model → fórmula/campo → tabela → registro de origem`.

## 2. Regra central

Um **indicador calculável em uma view** não é automaticamente um **KPI corporativo governado**.

Para promover um indicador a KPI operacional devem existir, no mínimo:

- `codigo_kpi` estável;
- nome;
- domínio;
- unidade;
- fórmula canônica;
- fonte(s) autorizada(s);
- janela temporal;
- numerador/denominador quando aplicável;
- baseline e target quando o objetivo exigir;
- política de dados ausentes;
- proveniência;
- definição ativa em `mt_definicoes_kpi`;
- snapshot em `mt_snapshots_kpi` quando houver evidência suficiente.

Enquanto `mt_definicoes_kpi` e `mt_snapshots_kpi` estiverem vazias, resultados de views devem ser apresentados como **indicadores/read-models observados**, nunca como KPI operacional registrado.

## 3. Fontes que devem entrar no catálogo governado

Adicionar por nova migration, sem alterar migration histórica:

### 3.1 `v_elo_pcp_carga_capacidade_periodo`

Domínio: `planejamento_pcp`  
Tipo: `read_model_carga_capacidade`  
Somente leitura: `true`  
Preservar proveniência: `true`

Indicadores disponíveis:

- quantidade planejada;
- carga planejada em horas;
- capacidade padrão;
- capacidade de recuperação;
- capacidade bloqueada;
- capacidade disponível;
- folga em horas;
- utilização percentual;
- excesso de carga.

Regra fail-closed já existente: `folga_horas`, `utilizacao_pct` e `excesso_carga` só são calculados quando a unidade do centro de trabalho é compatível com horas.

### 3.2 `v_elo_pcp_indicadores_montagem_externa`

Domínio: `operacoes_externas`  
Tipo: `read_model_indicadores_montagem_externa`  
Somente leitura: `true`  
Preservar proveniência: `true`

Indicadores disponíveis:

- ordens totais;
- ordens abertas;
- ordens atrasadas;
- módulos;
- colaboradores alocados;
- funções ativas;
- horas planejadas;
- horas realizadas;
- horas planejadas de equipe;
- horas reais de mão de obra;
- aderência de horas (%).

## 4. Forge — extensão obrigatória

Arquivo: `elo-virtual-core/integracoes/supabase_elo_forge.py`

### 4.1 Descoberta

Adicionar termos de descoberta sem criar segunda allowlist:

- `capacidade` → `planejamento_pcp`
- `carga` → `planejamento_pcp`
- `utilização` / `utilizacao` → `planejamento_pcp`
- `indicador` / `indicadores` → `planejamento_pcp`, `operacoes_externas`
- `kpi` → `planejamento_pcp`, `operacoes_externas`, `gestao`

A autoridade continua sendo `elo_aprendizado_fontes`.

### 4.2 Escopo global seguro

Adicionar a `global_tables` apenas as views read-only governadas:

- `v_elo_pcp_carga_capacidade_periodo`
- `v_elo_pcp_indicadores_montagem_externa`

Não adicionar tabelas operacionais brutas ao escopo global só para facilitar consultas.

### 4.3 Retorno do contexto

`governed_demand_context()` deve incluir, de forma tipada/explicável:

- `capacity_records`;
- `external_indicator_records`;
- resumo de excesso de carga apenas a partir de linhas que tenham `excesso_carga` não nulo;
- indicadores de montagem externa observados;
- indicação explícita de que `formal_kpi_registry_available` é falsa quando `mt_definicoes_kpi` não possuir definição governada pertinente.

Não calcular ICAC ou outro KPI mestre dentro do adapter.

## 5. Humanizer / resposta cognitiva

Arquivo: `src/elo/cognitive/runtime/humanization/humanizer.py`

No escopo `cross_domain_demand_and_impacts`, incluir se houver evidência:

### Capacidade

- centros/dias observados;
- carga planejada;
- capacidade disponível;
- folga;
- utilização;
- excesso de carga.

Texto obrigatório quando não houver dados:

`Capacidade operacional: não comprovada para este escopo; faltam registros governados de centro/roteiro/plano/capacidade.`

### Operação externa

- ordens abertas/atrasadas;
- horas planejadas/realizadas;
- aderência de horas.

### KPI

Se não houver definição/snapshot formal:

`Os valores acima são indicadores operacionais derivados de read-models governados; não foram promovidos a KPI corporativo registrado.`

## 6. API

Não criar API paralela se o resultado puder trafegar pelo contrato canônico existente.

Reutilizar:

- `POST /cognitive`;
- `CognitiveResponse`;
- `Provenance.evidence_refs`;
- `SourceReference`;
- `validation_status` / metadata quando aplicável.

Critério: cada indicador apresentado na resposta deve possuir evidence ref recuperável no `EvidenceRepository` ou referência equivalente já canônica.

## 7. ELO-MCP

Arquivo: `supabase/functions/elo-mcp/index.ts`

Adicionar uma tool read-only específica, sem ampliar `elo_read` para tabelas operacionais brutas:

`elo_pcp_indicadores_status`

Resultado mínimo:

- `status`: `OBSERVADO`, `PARCIAL`, `BLOQUEADO_POR_DADOS`;
- `capacity`: registros/resumo de `v_elo_pcp_carga_capacidade_periodo`;
- `external_operations`: `v_elo_pcp_indicadores_montagem_externa`;
- `coverage`: resumo da cobertura já governada;
- `decision`: resumo decisório já governado;
- `kpi_registry`: contagem/estado de `mt_definicoes_kpi` e `mt_snapshots_kpi`, sem promover ausência a zero operacional;
- `sources`: lista explícita de views/tabelas consultadas;
- `read_only: true`;
- `guessed: false`.

A tool deve ser auditada em `elo_audit_log` e usar o mesmo `authenticate()` / `authorizeRead()` existente.

## 8. Persistência de KPI

Não popular automaticamente `mt_definicoes_kpi` a partir de Markdown.

Primeira promoção candidata somente após prova E2E. Candidatos mais próximos de fonte executável:

- utilização de capacidade;
- excesso de carga;
- aderência de horas de montagem externa;
- gap/cobertura por modelo.

ICAC deve permanecer `NÃO_COMPROVADO` enquanto todos os seus termos não possuírem fontes canônicas e regras de comprometimento/bloqueio/perda suficientemente definidas.

## 9. Testes obrigatórios

### Forge

1. Consulta contendo `capacidade` descobre `v_elo_pcp_carga_capacidade_periodo` quando a view estiver governada.
2. Consulta contendo `indicadores de montagem externa` descobre a view correspondente.
3. Views não governadas continuam bloqueadas.
4. Ausência de registros não gera valor inventado.
5. Unidade incompatível não gera utilização/folga falsa.

### Orquestrador/Humanizer

6. Resposta inclui capacidade observada quando a evidência existe.
7. Resposta explicita ausência quando não existe.
8. Indicador não é chamado de KPI quando registro formal está ausente.
9. Evidence refs apontam para as fontes usadas.
10. Consulta sem modelo continua funcionando.

### MCP

11. `tools/list` inclui `elo_pcp_indicadores_status`.
12. Chamada não autenticada permanece 401/RFC9728.
13. Chamada sem autorização permanece 403.
14. Tool é read-only e auditada.
15. KPI registry vazio retorna estado de ausência, não KPI com valor zero.

### Regressão

16. Tools existentes continuam disponíveis.
17. Nenhuma nova escrita operacional é adicionada.
18. Nenhuma autoridade paralela é criada.

## 10. Condição de merge

Merge só é elegível quando:

- migration nova criada pelo fluxo oficial de migrations;
- testes acima passam;
- schema/read-models verificados;
- documentação MCP coincide com runtime;
- `main` não recebeu alteração direta;
- ausência de dados continua fail-closed;
- revisão confirma que nenhum KPI parcial foi promovido a fato operacional.

A aprovação desta especificação não equivale a autorização de merge.
