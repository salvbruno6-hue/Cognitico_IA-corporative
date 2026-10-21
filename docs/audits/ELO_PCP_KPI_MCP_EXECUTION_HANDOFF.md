# Execution handoff — PCP / Comercial / Demanda / Estoque

## 1. Regra geral

Use `docs/prompts/CODEX_ELO_PCP_KPI_E2E_IMPLEMENTATION.md` para implementações E2E de KPI PCP quando aplicável.

Não promover nova autoridade, fórmula ou decisão sem implementação, testes, evidência, validação e gate correspondente.

## 2. Processo associado à Skill PCP

O processo especializado de Comercial → Demanda → Retorno → Estoque está documentado em:

`06-knowledge-engineering/PCP_COMERCIAL_DEMANDA_RETORNO_ESTOQUE.md`

Owner cognitivo/metodológico:

`06-knowledge-engineering/SKILL_PLANEJAMENTO_MULTITEINER.md`

Governança superior:

- `06-knowledge-engineering/PCP_INSTRUCOES_GERAIS_GOVERNANCA.md`;
- `06-knowledge-engineering/PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL.md`.

A especialização não redefine os gates de demanda comparável. Ela começa na evidência Comercial classificada e estende a análise para retorno, disponibilidade, estoque mínimo/segurança e impacto no PCP.

## 3. Fluxo do handoff

```text
Comercial
→ classificar família/modelo/natureza/período
→ reconstruir referência histórica comparável
→ calcular crescimento/redução somente entre dimensões equivalentes
→ produzir previsão-base identificada
→ confrontar contexto externo com fonte/hipótese explícita
→ consolidar demanda por mês/família/modelo
→ derivar retorno somente quando data/período forem semanticamente válidos
→ separar retorno de disponibilidade
→ quarentena/inspeção/reparo/liberação
→ confrontar estoque mínimo + segurança + reserva EVENTO
→ medir cobertura/déficit somente em unidade física comparável
→ emitir alerta cognitivo
→ SWOT quando houver evidências suficientes
→ decisão governada
→ 5W2H
→ PCP
→ realizado
→ erro/aprendizado
→ Evolution Gate
```

## 4. Estruturas implantadas

### Read-model executivo

`public.v_elo_diretoria_comercial_estoque`

### Baseline analítica privada

`elo_private.pcp_diretoria_comercial_mensal`

### Cobertura operacional PCP

`public.v_elo_pcp_cobertura_demanda_externa`

A view executiva deve ser usada para leitura de Comercial/demanda/estoque. A view de cobertura operacional deve ser confrontada quando tenant, modelo e unidade física estiverem reconciliados.

## 5. Indicadores no handoff

O pacote de evidência para Diretoria/PCP pode conter:

- família `MODULO` / `CONTEINER`;
- modelo;
- ano/mês;
- demanda total;
- SPOT;
- EVENTO;
- venda;
- participação percentual por natureza;
- sazonalidade validada, quando demonstrada;
- crescimento MoM/YoY;
- retorno previsto;
- cobertura do retorno;
- estoque mínimo SPOT;
- estoque de segurança SPOT;
- estoque-alvo SPOT;
- reserva EVENTO;
- proteção comercial;
- estoque livre;
- reparos liberáveis;
- produção programada;
- necessidade adicional;
- estado de estoque;
- alerta cognitivo;
- orientação PCP;
- checklist de contexto externo;
- ferramenta de qualidade recomendada.

## 6. Política de estoque V1

```text
ESTOQUE_MINIMO_SPOT = ceil(P75(demanda mensal SPOT histórica))
ESTOQUE_SEGURANCA_SPOT = max(ceil(P90) - ceil(P75), 0)
ESTOQUE_ALVO_SPOT = ceil(P90)
RESERVA_EVENTO = ceil(P90(demanda mensal EVENTO histórica))
PROTECAO_COMERCIAL = ESTOQUE_ALVO_SPOT + RESERVA_EVENTO
```

EVENTO permanece separado do estoque permanente. P75/P90 são parâmetros V1 e devem ser recalibrados com nível de serviço, lead time e dados físicos validados.

## 7. Regras de retorno

Para locações com período comprovadamente em meses:

```text
DATA_RETORNO_PREVISTA = DATA_PREVISTA_SAIDA + PERIODO_MESES
```

Não aplicar automaticamente a EVENTO enquanto a semântica de `Período` não estiver validada.

Regra obrigatória:

```text
RETORNO PREVISTO != ESTOQUE LIVRE
```

O retorno precisa passar por quarentena, inspeção, reparo quando necessário e liberação antes de compor oferta operacional.

## 8. Alertas cognitivos

O handoff ao ELO deve separar:

- **FATO**;
- **RISCO**;
- **IMPACTO**;
- **AÇÃO/ANÁLISE RECOMENDADA**.

Quando houver crescimento, queda ou cobertura crítica, validar contexto externo como:

- perdas de contrato;
- renovações frágeis/confirmadas;
- campanhas comerciais;
- eventos;
- concorrência;
- preço;
- mudanças de mercado.

Não declarar causalidade sem evidência.

SWOT é análise de cenário; 5W2H é transformação de uma decisão governada em plano de ação.

## 9. Estado validado em 2026-10-21

Supabase:

- `elo_private.pcp_diretoria_comercial_mensal`: 600 linhas;
- `public.v_elo_diretoria_comercial_estoque`: 600 linhas;
- 24 linhas de FAMÍLIA;
- 576 linhas de MODELO;
- horizonte inicial: out/2026–set/2027.

GitHub:

- implementação executiva anterior consolidada em `6aaf73370cf4d0e0698c2c6bfc0c816d218931de`;
- documentação/evidência: `docs/pcp/PCP_VISAO_DIRETORIA_COMERCIAL_ESTOQUE_20261021.md` e `docs/pcp/PCP_DIRETORIA_COMERCIAL_ESTOQUE_EVIDENCE_20261021.md`.

## 10. GAPs que devem sobreviver ao handoff

- fonte Comercial sem quantidade física explícita por linha;
- baseline em `REGISTRO_EQUIVALENTE`;
- tenant canônico ainda não estabelecido para a carga;
- modelos de CONTÊINER ainda não integralmente reconciliados com o catálogo canônico;
- semântica de `Período` para EVENTO não validada para derivação mensal de retorno;
- backfill histórico mensal linha a linha ainda pendente no read-model;
- previsão-base não substitui `mt_previsoes_demanda`;
- saldo físico contra estoque mínimo deve permanecer fail-closed enquanto as unidades não forem comparáveis.

## 11. Próxima sequência recomendada

```text
BACKFILL HISTÓRICO
→ RECONCILIAR MODELOS
→ ESTABELECER TENANT
→ INCORPORAR QUANTIDADE FÍSICA
→ RECONCILIAR DEVOLUÇÃO REAL
→ INTEGRAR QUARENTENA/REPARO/LIBERAÇÃO
→ CALIBRAR NÍVEL DE SERVIÇO/LEAD TIME
→ MEDIR ERRO DA PREVISÃO
→ VALIDAR APRENDIZADO
```

## 12. Critério de encerramento do handoff

O processo está pronto para decisão operacional somente quando a dimensão analisada possuir evidência suficiente para a próxima ação.

A ausência de dado complementar não bloqueia toda a análise; a ausência de dado essencial bloqueia apenas a conclusão/ação que depende dele.

Nunca converter `REGISTRO_EQUIVALENTE`, previsão-base ou hipótese externa em quantidade física ou causa operacional sem validação.