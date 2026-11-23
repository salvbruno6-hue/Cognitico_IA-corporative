# ELO / Multiteiner — Auditoria de reutilização do conhecimento PCP e Fluxo Modular

**Data da verificação:** 2026-11-23  
**Status:** diagnóstico baseado em consultas somente leitura; integração operacional NÃO validada.  
**Natureza:** evidência de GAP e contrato de verificação, não mudança do Core.

## 1. Fontes canônicas existentes
- `03-process-library/MULTITEINER_END_TO_END_PROCESS_FLOW.md` — ELO-PROC-MULTITEINER-001, status draft, referência detalhada do fluxo.
- `docs/ELO-012_MULTITEINER_FLOW_MODULAR_PROTOCOL.md` — protocolo normativo de recuperação e preservação de proveniência.
- `04-knowledge-handbook/MULTITEINER_ORGANIZATIONAL_CONTEXT.md` — contexto organizacional.
- `docs/architecture/ELO_MATURE_MULTITEINER_DATA_GOVERNANCE.md` — mapeamento de dados por setor.
- `docs/MULTITEINER_KPIs_MASTER.md` — definições de indicadores.

Não criar cópias concorrentes dessas autoridades. O ELO deve recuperar primeiro o fluxo detalhado, depois o contexto organizacional, depois documentos especializados, estado operacional e experiências históricas.

## 2. Fluxo modular de referência
Triagem → Chassi → Escovação → Pintura de tratamento → Acabamento branco → Estoque de estruturas → Movimentação → Piso → Teto → Colunas → Trilho → Pintura modular → Paredes → Instalações → Acabamento → Testes → Liberação.

**Limite:** sequência documentada não comprova status real, duração, capacidade ou gargalo atual.

## 3. Evidência do Supabase — consulta somente leitura em 2026-11-23
Projeto conectado: `Elo-forge` (ID `fxbpevjrkwhbicpmecow`).

| Tabela existente | Contagem observada |
|---|---:|
| mt_ordens_producao | 0 |
| mt_eventos_fluxo_modular | 0 |
| mt_planos_pcp | 0 |
| mt_linhas_plano_pcp | 0 |
| mt_capacidade_diaria | 0 |
| mt_necessidades_materiais | 0 |
| mt_gates | 0 |
| mt_proveniencia_registros | 8 |

Contagens representam somente as tabelas consultadas, não todo o banco nem sistemas externos.

Campos observados: `mt_ordens_producao` inclui `tenant_id`, `numero_ordem`, `modelo_id`, `bom_versao_id`, quantidades, status e datas planejadas/reais; `mt_eventos_fluxo_modular` inclui `unidade_modular_id`, `centro_trabalho_id`, `nome_operacao`, `tipo_evento`, `inicio`, `fim`, `quantidade`, `status`, `operador_id`. `mt_proveniencia_registros` preserva referência de origem.

## 4. GAP e decisões de governança
- **GAP-PCP-01:** documentação do fluxo existe, mas não está demonstrado que o mecanismo de recuperação do ELO a utilize em todas as respostas de PCP.
- **GAP-PCP-02:** não há telemetria nas tabelas consultadas para calcular status de ordens, carga x capacidade, lead time, WIP ou aderência à programação.
- **GAP-PCP-03:** não foi demonstrada correspondência entre fontes externas (Najason, CAD, planilhas, documentos) e registros governados no Supabase.
- **GAP-PCP-04:** ausência de evidência de validação end-to-end de análise → recomendação → decisão → resultado.
- **GAP-PCP-05:** dados do estudo acadêmico Vexia Modular Solutions não devem ser tratados automaticamente como telemetria real da Multiteiner, mesmo quando há similaridade operacional.

## 5. Contrato mínimo de análise
1. Identificar tenant, pergunta e período.
2. Recuperar ELO-PROC-MULTITEINER-001 e referências de governança.
3. Distinguir PROCESSO DOCUMENTADO, ESTADO ATUAL, DESVIO, HIPÓTESE e DADO AUSENTE.
4. Buscar registros operacionais existentes antes de propor novas tabelas ou importar dados.
5. Exigir identificação de origem, momento, escopo e validade; marcar conflito como GAP.
6. Correlacionar AF/SO → BOM → materiais → capacidade → operação/etapa → qualidade → expedição apenas com chaves e relações comprovadas.
7. Não gerar datas, capacidades, gargalos quantitativos ou riscos numéricos sem evidência.
8. Apresentar diagnóstico, impacto, alternativas, evidências e pendências para decisão humana.
9. Registrar decisão e resultado em estruturas existentes somente após validação e autorização.

## 6. Critérios de aceite / Evolution Gate
- [x] Fontes canônicas localizadas.
- [x] Estruturas de dados PCP e fluxo modular verificadas por leitura.
- [x] Contagens de registros documentadas.
- [ ] Varredura de todas as fontes operacionais relevantes e classificação de qualidade.
- [ ] Teste de recuperação do fluxo detalhado pela aplicação ELO.
- [ ] Teste de ligação AF/SO, módulo, evento, materiais, capacidade e evidência com registros reais autorizados.
- [ ] Teste de isolamento por tenant e controles de acesso.
- [ ] Teste de decisão humana, registro de resultado e rastreabilidade.
- [ ] Validação por responsável do PCP e governança antes de ativar automação.

**Evolution Gate:** este diagnóstico documental pode ser incorporado ao repositório sem promover regras ao Core. A integração operacional permanece bloqueada até validação dos itens pendentes.

## 7. Próxima execução
Inspecionar inventário de tabelas com contagens e proveniência, identificar fontes operacionais existentes, testar recuperação canônica do fluxo, registrar evidências dos testes e abrir implementação incremental apenas quando os contratos de dados estiverem demonstrados. Não popular tabelas com dados sintéticos apresentados como reais.
