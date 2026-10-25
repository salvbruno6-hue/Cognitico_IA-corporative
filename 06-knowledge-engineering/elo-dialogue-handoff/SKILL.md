# SKILL — ELO DIALOGUE HANDOFF

**skill_id:** `ELO_DIALOGUE_HANDOFF`
**domain_family:** `PROCESS_ANALYSIS`
**maturity:** `DEFINED`
**version:** `0.1.0`
**owner:** `Forge`
**canonical_authority:** `ELO_COGNITIVO`
**authorization_authority:** `elo-authz`
**runtime_boundary:** `ELO Web`

## 1. Finalidade

Definir o protocolo operacional de handoff entre GPT e ELO para que respostas relacionadas a objetivos governados sejam produzidas a partir do estado real do ELO, sem criar um segundo owner, um segundo orquestrador ou uma autoridade paralela.

A skill é **transporte + validação de contrato**. Ela não decide continuidade, não cria autorização, não promove aprendizado e não altera o núcleo cognitivo.

## 2. Escopo

Fluxo alvo:

`GPT → handoff → ELO Web → elo-authz → Objective Continuity → checkpoint persistente → ELO_RETURN → GPT`

A skill se aplica quando uma interação precisa consultar ou continuar um objetivo governado pelo ELO.

## 3. Fronteiras

A skill NÃO pode:

- decidir `CONTINUE`, `CORRECT`, `REPLAN`, `ESCALATE` ou `COMPLETE` por conta própria;
- emitir autorização;
- tratar texto conversacional como checkpoint;
- inventar `progress_token`, evidência ou `state_version`;
- substituir `Objective Continuity`;
- substituir `elo-authz`;
- executar mais de um replay/ciclo por turno sem novo handoff governado;
- transformar ausência de conexão em sucesso simulado.

## 4. Pré-requisitos

- objetivo e workstream identificados;
- endpoint canônico ELO Web disponível;
- persistência durável disponível;
- autorização verificável pelo `elo-authz`;
- evidência mínima para o ciclo;
- checkpoint válido ao retomar execução existente.

## 5. Entradas autorizadas

- mensagem atual do usuário;
- contexto conversacional necessário;
- `objective_id`;
- `workstream_id`;
- `expected_checkpoint_version`;
- `progress_token` observado;
- `evidence_refs` reais;
- `proposed_next_action`;
- estado retornado por fontes canônicas.

## 6. Fontes autorizadas

1. GitHub canônico `salvbruno6-hue/Cognitico_IA-corporative` para contratos, owners e código;
2. ELO Web para runtime de prefinalização;
3. `elo-authz` para autorização;
4. Supabase apenas como persistência/estado quando atribuído pela arquitetura canônica;
5. ELO-MCP como boundary de integração quando disponível.

## 7. Procedimento obrigatório

1. Identificar se a solicitação pertence a um objetivo governado.
2. Resolver `objective_id` e `workstream_id` sem inventar valores.
3. Ler o checkpoint persistente quando houver execução existente.
4. Exigir `expected_checkpoint_version` ao retomar um checkpoint existente.
5. Montar o pacote `GPT_TO_ELO` conforme `HANDOFF_GPT_TO_ELO.md`.
6. Enviar ao runtime canônico.
7. Receber `ELO_RETURN`.
8. Validar o retorno conforme `HANDOFF_ELO_TO_GPT.md`.
9. Comunicar ao usuário a decisão do ELO sem alterá-la.
10. Se `should_continue_automatically=true`, preparar somente o próximo handoff permitido.
11. Se houver `human_required=true`, interromper a continuidade automática.

## 8. Requisitos de evidência

Toda continuidade exige:

- identidade objetiva/workstream consistente;
- checkpoint monotônico;
- autorização observada e rastreável;
- pelo menos uma referência de evidência;
- progress token não inventado;
- retorno do owner canônico.

## 9. Incerteza

Na ausência de checkpoint, autorização, evidência ou runtime disponível, usar estado explícito de GAP e não inferir sucesso.

## 10. Escalonamento

Escalar quando:

- `elo-authz` negar ou expirar autorização;
- houver checkpoint stale;
- o objetivo estiver em estado terminal;
- a ação sair do escopo autorizado;
- houver risco alto/crítico que requeira humano;
- a evidência for insuficiente;
- o runtime persistente estiver indisponível.

## 11. Saídas

- `ELO_RETURN` validado;
- mensagem GPT baseada no retorno do ELO;
- `next_trigger` somente quando permitido;
- registro explícito de GAP quando o ciclo não puder ser executado.

## 12. Limites de decisão

A autoridade permanece no `ELO_COGNITIVO` e no owner de `Objective Continuity`. O GPT é interface, transporte e apresentação. A skill coordena o protocolo, não governa a decisão.

## 13. Testes de referência

- rejeição de checkpoint stale;
- ausência de autorização → fail-closed;
- ausência de persistência → fail-closed;
- `ESCALATE` → sem próximo trigger;
- `COMPLETE` → sem próximo trigger;
- `CONTINUE/CORRECT/REPLAN` → no máximo um próximo trigger por turno;
- identidade objetivo/workstream preservada.

## 14. Histórico

- `0.1.0` — contrato inicial de handoff GPT↔ELO.

## 15. Contextual parameters

- `max_replays_per_turn = 1`
- `checkpoint_required_on_resume = true`
- `fail_closed = true`

## 16. Learning candidates

Nenhum aprendizado é promovido por esta skill. Observações de uso podem virar candidatos separados somente pelo fluxo governado existente.

## 17. Promotion candidates

Nenhuma promoção automática. Qualquer promoção exige Evolution Gate e evidência executável.