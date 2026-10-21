# PCP — Demanda, Fluxo Produtivo Modular e Disponibilidade de Pátio

**Status:** especialização PCP / planejamento de demanda / produção modular  
**Owner cognitivo:** `SKILL_PLANEJAMENTO_MULTITEINER`  
**Processo de referência:** `03-process-library/MULTITEINER_END_TO_END_PROCESS_FLOW.md`  
**Protocolo do fluxo modular:** `docs/ELO-012_MULTITEINER_FLOW_MODULAR_PROTOCOL.md`  
**Demanda/estoque comercial:** `PCP_COMERCIAL_DEMANDA_RETORNO_ESTOQUE.md`  
**Read-model:** `public.v_elo_pcp_demanda_fluxo_patio`

---

## 1. Objetivo

Estabelecer a relação governada entre:

```text
DEMANDA COMERCIAL / EVENTOS
        ↓
PEDIDO/AF FÍSICO CONFIRMADO
        ↓
PLANO PCP
        ↓
ORDEM DE PRODUÇÃO
        ↓
FLUXO PRODUTIVO MODULAR
        ↓
QUALIDADE / LIBERAÇÃO
        ↓
PÁTIO DISPONÍVEL
        ↕
EXPEDIÇÃO / RETORNO / QUARENTENA / REPARO
```

O objetivo operacional é permitir que o ELO responda, por período e família/modelo:

- quanto foi demandado;
- quanto da demanda é EVENTO;
- quanto está confirmado em quantidade física;
- quanto está planejado em fabricação;
- quanto já foi produzido;
- quanto permanece em aberto nas OPs;
- quanto do fluxo possui telemetria real;
- quantas unidades físicas estão disponíveis para expedição;
- quantas estão confirmadas em local classificado como `PATIO`;
- quais saídas estão planejadas;
- quais retornos/reparos são potenciais;
- qual é o saldo de pátio planejado condicionado aos dados existentes;
- quais GAPs impedem uma resposta precisa.

---

## 2. Regra epistemológica central

A pergunta "quantos módulos teremos no pátio?" não pode ser respondida somando demanda analítica, retornos previstos e fabricação sem rastreabilidade física.

Regras obrigatórias:

```text
REGISTRO_EQUIVALENTE != UNIDADE_FISICA
RETORNO PREVISTO != ESTOQUE LIVRE
REPARO PREVISTO != UNIDADE LIBERADA
OP PLANEJADA != MÓDULO LIBERADO
FLUXO DOCUMENTADO != EXECUÇÃO REAL
```

A resposta física exige, no mínimo:

```text
tenant
+ modelo canônico
+ quantidade física
+ unidade modular rastreável
+ local atual
+ qualidade/liberação
+ OP/execução quando houver fabricação
+ expedições comprometidas
```

Retornos e reparos permanecem componentes potenciais até liberação física.

---

## 3. Fontes e autoridades

### 3.1 Contexto de demanda comercial

`elo_private.pcp_diretoria_comercial_mensal`

Uso:
- tendência;
- SPOT/EVENTO;
- proteção comercial;
- referência analítica.

Enquanto `unidade_medida = REGISTRO_EQUIVALENTE`, essa fonte não alimenta diretamente o saldo físico de pátio.

### 3.2 Demanda física confirmada

`mt_pedidos_venda` + `mt_pedidos_venda_itens`

Para EVENTO:

```text
natureza_demanda = EVENTO
+ modelo_id
+ quantidade
+ data solicitada/entrega
+ tenant_id
```

Essa é a camada que deve receber uma ordem/AF física confirmada antes de o ELO tratá-la como quantidade real de módulos.

### 3.3 Plano e fabricação

```text
mt_planos_pcp
→ mt_linhas_plano_pcp
→ mt_ordens_producao
→ mt_operacoes_ordem_producao
```

A OP fornece quantidade planejada/produzida e horizonte. As operações fornecem evidência de execução.

### 3.4 Fluxo modular de referência

```text
fluxo_produtivo_modular
→ fluxo_produtivo_modular_etapas
```

Sequência de referência atual:

`Triagem → Chassi → Escovação → Pintura de tratamento → Acabamento branco → Estoque de estruturas → Movimentação → Piso → Teto → Colunas → Trilho → Pintura modular → Paredes → Instalações → Acabamento → Testes → Liberação`.

Tempos/capacidades só podem ser utilizados quando validados.

### 3.5 Pátio físico

```text
mt_unidades_modulares
→ mt_locais
```

Uma unidade só conta como `PATIO_CONFIRMADO` quando:

- existe fisicamente em `mt_unidades_modulares`;
- está disponível para expedição;
- não está bloqueada/reprovada em qualidade;
- possui localização classificada explicitamente como `PATIO`.

### 3.6 Saídas

```text
mt_expedicoes
→ mt_expedicao_itens
```

Saídas planejadas reduzem o saldo planejado do pátio quando vinculadas a unidades físicas.

### 3.7 Retorno e reparo

```text
mt_contratos_locacao
→ retorno contratual previsto

mt_devolucoes
→ mt_devolucao_itens
→ retorno real

mt_ordens_reparo
→ unidade_modular_id
→ data/status
```

Retorno contratual ou reparo com data não significa disponibilidade. O módulo ainda precisa passar por recebimento, quarentena/inspeção quando aplicável, qualidade e liberação.

---

## 4. Relação com a demanda de fabricação para EVENTOS até janeiro/2027

Foi relatada a existência de uma ordem/necessidade de fabricação que se estende até janeiro de 2027 para atendimento de eventos.

Essa informação é relevante para planejamento, porém **não veio acompanhada nesta interação de quantidade física, modelo, tenant, número da AF/pedido ou OP**.

Portanto o ELO deve tratá-la como:

`NECESSIDADE OPERACIONAL RELATADA / A RECONCILIAR`

Não criar quantidade, modelo ou OP por inferência.

A reconciliação correta é:

```text
necessidade EVENTO relatada
→ localizar AF/pedido
→ confirmar quantidade física por modelo
→ registrar/relacionar tenant
→ gerar/relacionar linha PCP
→ relacionar OP
→ acompanhar operações reais
→ registrar unidades produzidas
→ qualidade/liberação
→ localização em pátio
```

Só depois disso a quantidade planejada pode ser confrontada com disponibilidade física.

---

## 5. Read-model

A view canônica desta relação é:

```sql
public.v_elo_pcp_demanda_fluxo_patio
```

Ela não cria nova autoridade. Apenas relaciona autoridades existentes.

### 5.1 Campos de demanda

- `demanda_referencia`;
- `demanda_evento_referencia`;
- `unidade_demanda_referencia`;
- `demanda_fisica_confirmada`;
- `demanda_evento_fisica_confirmada`.

### 5.2 Campos de produção

- `ordens_producao`;
- `producao_planejada`;
- `producao_produzida`;
- `producao_em_aberto`;
- `ordens_sem_fim_planejado`;
- `operacoes_registradas`;
- `operacoes_concluidas`.

### 5.3 Campos de pátio

- `unidades_cadastradas`;
- `unidades_disponiveis_expedicao`;
- `unidades_patio_confirmadas`;
- `unidades_disponiveis_sem_local`;
- `expedicoes_planejadas`;
- `saldo_patio_planejado_condicional`.

### 5.4 Componentes potenciais, separados do saldo

- `retornos_contratuais_previstos`;
- `reparos_previstos_conclusao`.

Eles não entram automaticamente no saldo de pátio livre.

### 5.5 Readiness do fluxo

- `etapas_fluxo_referencia`;
- `etapas_com_tempo`;
- `etapas_com_capacidade`;
- `lead_time_fluxo_dias`;
- `capacidade_fluxo_referencia`;
- `operacoes_roteiro_cadastradas`;
- `evidencias_tempo_estrutura_20_pes`;
- `tempo_estrutura_20_pes_min`.

---

## 6. Fórmula do saldo planejado condicionado

Quando houver tenant e estoque físico de pátio:

```text
SALDO_PATIO_PLANEJADO_CONDICIONAL =
  PATIO_CONFIRMADO_ATUAL
  + Σ PRODUCAO_EM_ABERTO_COM_FIM_PLANEJADO
  - Σ EXPEDICOES_PLANEJADAS
```

A fórmula é uma visão de planejamento, não uma afirmação de que a produção futura já foi liberada.

Por isso:

- produção futura permanece condicionada à execução/qualidade;
- retorno contratual não é somado automaticamente;
- reparo previsto não é somado automaticamente;
- ausência de localização física gera GAP.

---

## 7. Estados e GAPs

### 7.1 Demanda

- `DEMANDA_FISICA_CONFIRMADA`;
- `REFERENCIA_NAO_FISICA`;
- `REFERENCIA_ANALITICA`;
- `SEM_DEMANDA_REGISTRADA`.

### 7.2 Disponibilidade de pátio

- `GAP_TENANT`;
- `GAP_UNIDADES_MODULARES`;
- `GAP_LOCAL_PATIO`;
- `PATIO_FISICO_RASTREAVEL`.

### 7.3 Fluxo produtivo

- `GAP_ROTEIRO_PRODUTIVO`;
- `GAP_TEMPO_FLUXO`;
- `GAP_CAPACIDADE_FLUXO`;
- `GAP_EXECUCAO_FLUXO`;
- `FLUXO_RASTREAVEL`.

### 7.4 Flags adicionais

- `gap_quantidade_fisica`;
- `gap_modelo_canonico`;
- `gap_tenant`;
- `gap_unidades_modulares`;
- `gap_local_patio`;
- `gap_execucao_fluxo`;
- `gap_roteiro_produtivo`;
- `gap_tempo_fluxo`;
- `gap_capacidade_fluxo`;
- `gap_reparo_sem_unidade`.

---

## 8. Evidência atual em 21/10/2026

Estado observado no Supabase:

| Fonte | Situação atual |
|---|---:|
| `mt_tenants` | 0 registros |
| `mt_previsoes_demanda` | 0 |
| `mt_planos_pcp` | 0 |
| `mt_linhas_plano_pcp` | 0 |
| `mt_ordens_producao` | 0 |
| `mt_operacoes_ordem_producao` | 0 |
| `mt_operacoes_roteiro` | 0 |
| `mt_unidades_modulares` | 0 |
| `mt_expedicoes` | 0 |
| `mt_devolucoes` | 0 |
| `mt_ordens_reparo` | 133 |
| reparos vinculados a unidade modular | 0 |
| `fluxo_produtivo_modular` | 1 fluxo de referência |
| `fluxo_produtivo_modular_etapas` | 17 etapas |
| etapas com tempo parametrizado | 0 |
| etapas com capacidade parametrizada | 0 |
| `mt_tempo_fabricacao_estrutura_modular` | 9 evidências parciais |

As 9 evidências de tempo somam 138 minutos de operações registradas para partes da **estrutura modular de 20 pés**. Isso é evidência parcial de corte/dobra/estrutura e **não** é lead time total do módulo nem capacidade diária da linha.

As 133 ordens de reparo atuais não estão reconciliadas com `mt_unidades_modulares`; portanto não podem ser somadas ao pátio disponível.

A baseline Comercial entre outubro/2026 e janeiro/2027 permanece em `REGISTRO_EQUIVALENTE` e sem tenant/modelo físico reconciliado. Ela serve como contexto de pressão de demanda, não como quantidade física de módulos.

---

## 9. Por que hoje não existe resposta precisa de pátio

O problema não é somente falta de uma fórmula. A cadeia física ainda não está alimentada.

Hoje existem simultaneamente:

```text
DEMANDA ANALÍTICA
+ FLUXO DOCUMENTADO
+ REPAROS NÃO RECONCILIADOS
```

mas faltam:

```text
TENANT
+ PEDIDOS/AFs FÍSICOS
+ OPs
+ EXECUÇÃO DE OPs
+ UNIDADES MODULARES
+ LOCAIS/PÁTIO
+ EXPEDIÇÕES
+ DEVOLUÇÕES FÍSICAS
```

Por isso qualquer número atual de "módulos disponíveis em janeiro" seria inventado se apresentado como físico.

---

## 10. Sequência mínima para fechar a resposta até jan/2027

1. **Estabelecer tenant** operacional da Multiteiner.
2. **Reconciliar a ordem de EVENTO** até jan/2027 com AF/pedido, quantidade e modelo.
3. **Cadastrar pedido físico** em `mt_pedidos_venda` / `mt_pedidos_venda_itens`.
4. **Gerar/relacionar plano PCP e OPs**.
5. **Cadastrar roteiro operacional por modelo** em `mt_operacoes_roteiro`.
6. **Relacionar execução** em `mt_operacoes_ordem_producao`.
7. **Criar/rastrear unidades físicas** em `mt_unidades_modulares`.
8. **Classificar locais de pátio** em `mt_locais`.
9. **Registrar compromissos de expedição**.
10. **Reconciliar contratos/retornos**.
11. **Vincular reparos a unidades físicas** e datas de conclusão/liberação.
12. Consultar `v_elo_pcp_demanda_fluxo_patio` por mês/família/modelo aplicável.

---

## 11. Contrato de resposta do ELO

Quando solicitado algo como:

- "Quantos módulos teremos disponíveis em janeiro?"
- "A fabricação para os eventos cobre a necessidade?"
- "Quanto vai entrar no pátio em dezembro?"
- "Qual será o saldo de módulo disponível depois das expedições?"

O ELO deve responder nesta ordem:

1. **demanda de referência** e sua unidade;
2. **demanda física confirmada**;
3. **OPs e produção em aberto**;
4. **execução do fluxo**;
5. **pátio físico confirmado agora**;
6. **expedições planejadas**;
7. **retornos/reparos potenciais separados**;
8. **saldo planejado condicionado**, quando calculável;
9. **GAPs que limitam precisão**;
10. **próxima evidência mínima**.

Nunca responder somente com um número se o número depende de hipótese não explicitada.

---

## 12. Relação com o fluxo canônico PCP

Esta especialização reutiliza o processo existente:

```text
Comercial/Locação
→ AF
→ PCP
→ materiais/capacidade
→ produção modular
→ qualidade/liberação
→ pátio
→ expedição
→ cliente/campo
→ retorno
→ quarentena/reparo
→ pátio
```

Não cria nova arquitetura de processo e não substitui `v_elo_pcp_cobertura_demanda_externa`.

A diferença é de pergunta:

- `v_elo_pcp_cobertura_demanda_externa` responde cobertura/necessidade adicional por demanda;
- `v_elo_pcp_demanda_fluxo_patio` responde rastreabilidade do caminho da demanda até produção e disponibilidade física de pátio.

---

## 13. Regra de evolução

Quando os dados físicos forem alimentados:

```text
GAP
→ evidência operacional
→ cálculo reproduzível
→ confronto planejado × realizado
→ erro/desvio
→ ajuste de planejamento
→ Evolution Gate
```

Não promover tempos, capacidades ou regras de liberação com base apenas em um caso isolado.