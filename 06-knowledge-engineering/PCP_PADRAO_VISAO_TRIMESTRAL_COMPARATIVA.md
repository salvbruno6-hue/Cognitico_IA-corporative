# PCP — Padrão de Visão Trimestral Comparativa

**Status:** contrato de apresentação PCP / Diretoria  
**Owner cognitivo:** `SKILL_PLANEJAMENTO_MULTITEINER`  
**Processo associado:** `PCP_COMERCIAL_DEMANDA_RETORNO_ESTOQUE.md`  
**Referência de comparabilidade:** `PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL.md`  
**Read-model executivo primário:** `public.v_elo_diretoria_comercial_estoque`

---

## 1. Finalidade

Padronizar a forma de apresentação das análises comerciais e de estoque do PCP para que toda leitura diretiva seja comparável, repetível e visualmente consistente.

Este padrão **não cria nova fonte de verdade**. Ele organiza a apresentação dos dados já governados pelas estruturas canônicas existentes.

A ordem obrigatória da resposta é:

1. comparação de 3 meses entre anos equivalentes;
2. explicação das mudanças por modelo;
3. tabela executiva de demanda, retorno e estoque;
4. quadro de planejamento com realizado, plano-base e projeção futura quando solicitada.

---

## 2. Janela temporal padrão

A visão deve trabalhar sempre com **3 meses consecutivos**.

### 2.1 Regra padrão

Quando o usuário não informar meses específicos:

- usar os **3 últimos meses completos/fechados**;
- não usar o mês corrente incompleto como realizado;
- comparar cada mês com o **mesmo mês do ano anterior**;
- quando houver previsão/projeção solicitada, apresentar também o **mesmo mês do ano seguinte**.

Exemplo em outubro de 2026:

```text
JUL/2025 ↔ JUL/2026 ↔ JUL/2027 projeção opcional
AGO/2025 ↔ AGO/2026 ↔ AGO/2027 projeção opcional
SET/2025 ↔ SET/2026 ↔ SET/2027 projeção opcional
```

### 2.2 Mês fechado

Para demanda comercial histórica da base atual, o eixo temporal padrão é `Data da Proposta`.

Um mês só deve ser apresentado como `REALIZADO` quando estiver encerrado no calendário da análise e a fonte correspondente estiver disponível.

Mês futuro ou incompleto deve ser explicitamente rotulado como:

- `PREVISAO_BASE`;
- `PROJECAO_INDICATIVA`;
- ou outro status governado aplicável.

Nunca misturar realizado e projeção sem rótulo.

---

## 3. Primeira tabela obrigatória — comparação dos 3 meses

A primeira visualização deve seguir sempre esta estrutura:

| Mês | Família | Ano anterior | Ano atual | Variação | SPOT ano anterior → atual | EVENTO ano anterior → atual | VENDA ano anterior → atual |
|---|---|---:|---:|---:|---:|---:|---:|
| M1 | CONTÊINER | valor | valor | % | valor → valor | valor → valor | valor → valor |
| M1 | MÓDULO | valor | valor | % | valor → valor | valor → valor | valor → valor |
| M2 | CONTÊINER | valor | valor | % | valor → valor | valor → valor | valor → valor |
| M2 | MÓDULO | valor | valor | % | valor → valor | valor → valor | valor → valor |
| M3 | CONTÊINER | valor | valor | % | valor → valor | valor → valor | valor → valor |
| M3 | MÓDULO | valor | valor | % | valor → valor | valor → valor | valor → valor |

Quando os anos forem 2025 e 2026, os cabeçalhos devem aparecer explicitamente como `2025` e `2026`.

### 3.1 Cálculo da variação

```text
YoY_pct = ((valor_ano_atual / valor_ano_anterior) - 1) × 100
```

Se o denominador for zero ou não comparável, apresentar `SEM_BASE_COMPARAVEL` em vez de inventar percentual.

### 3.2 Família

A visão padrão deve apresentar separadamente:

- `CONTÊINER`;
- `MÓDULO`.

Se o usuário filtrar uma única família, respeitar o filtro.

### 3.3 Natureza

O total deve ser aberto, quando disponível, em:

- `SPOT`;
- `EVENTO`;
- `VENDA`.

`EVENTO` não deve ser tratado automaticamente como sazonalidade permanente.

---

## 4. Segunda camada obrigatória — “Quais modelos explicam essas mudanças”

Imediatamente após a tabela comparativa, deve vir a seção:

# Quais modelos explicam essas mudanças

A análise deve ser organizada por **mês e família**.

Formato mínimo:

| Modelo | Ano anterior | Ano atual | Δ absoluto | Δ % quando comparável | SPOT | EVENTO | VENDA | Leitura |
|---|---:|---:|---:|---:|---:|---:|---:|---|

### 4.1 Seleção dos modelos

Priorizar:

1. maiores contribuições positivas para a variação da família;
2. maiores contribuições negativas;
3. modelos com mudança relevante de mix SPOT/EVENTO;
4. modelos cuja natureza explique um pico extraordinário.

Não é obrigatório listar modelos sem impacto material quando a tabela ficar excessivamente longa.

### 4.2 Regra de leitura

A explicação deve distinguir:

```text
variação da família
≠
variação estrutural do SPOT
≠
pico de EVENTO
≠
mudança de mix entre modelos
```

Exemplo de conclusão válida:

```text
A família caiu, mas o SPOT permaneceu estável; a redução veio principalmente de EVENTO.
```

ou:

```text
O crescimento foi estruturalmente SPOT e concentrado nos modelos X e Y.
```

---

## 5. Terceira tabela obrigatória — demanda, retorno e estoque

Depois dos modelos explicativos, apresentar a tabela operacional/executiva nesta ordem de colunas:

| Mês | Família | Demanda total | SPOT | Evento | Venda | MoM | YoY | Retornos previstos | Estoque mínimo SPOT | Segurança | Estoque-alvo | Reserva evento | Proteção comercial | Sinal |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|

### 5.1 Semântica

- `Demanda total`: demanda da família no período;
- `SPOT`: componente não-evento comparável;
- `Evento`: componente EVENTO;
- `Venda`: pressão comercial de venda separada da locação;
- `MoM`: variação contra o mês imediatamente anterior quando comparável;
- `YoY`: variação contra o mesmo mês do ano anterior;
- `Retornos previstos`: retorno derivado ou operacional conforme fonte/status;
- `Estoque mínimo SPOT`: referência P75 V1;
- `Segurança`: diferença P90 − P75 V1;
- `Estoque-alvo`: P90 SPOT V1;
- `Reserva evento`: referência EVENTO governada;
- `Proteção comercial`: estoque-alvo + reserva EVENTO;
- `Sinal`: alta, queda, estabilidade ou sem base comparável.

### 5.2 Fail-closed

Se a unidade estiver em `REGISTRO_EQUIVALENTE`, não apresentar esses valores como quantidade física comprovada.

A indicação deve permanecer explícita:

```text
GAP_QUANTIDADE_FISICA
```

E:

```text
RETORNO PREVISTO != ESTOQUE LIVRE
```

---

## 6. Quarta tabela — planejamento com ano anterior, atual e seguinte

Quando houver pedido de planejamento/projeção, encerrar a visão com:

| Mês | Família | Ano anterior Realizado | Ano atual Realizado/Plano-base | Δ anterior→atual | Tendência histórica usada | Ano seguinte Projeção indicativa | Mín. SPOT | Segurança | Proteção comercial | Leitura do plano |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|

Exemplo de cabeçalho para 2025–2027:

| Mês | Família | **2025 Realizado** | **2026 Realizado/Plano-base** | **Δ 25→26** | **Tendência histórica usada** | **2027 Projeção indicativa** | Mín. SPOT | Segurança | Proteção comercial | Leitura do plano |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|

### 6.1 Projeção futura é opcional

A projeção do ano seguinte só deve aparecer quando:

- o usuário solicitar projeção; ou
- o objetivo declarado for planejamento futuro.

Caso contrário, a visão encerra no comparativo realizado + tabela executiva.

### 6.2 Regra da projeção

A projeção deve respeitar o **mesmo mês do calendário**.

Não usar automaticamente crescimento do mês anterior para projetar o mês seguinte.

A ordem conceitual é:

```text
mesmo mês histórico comparável
→ tendência histórica validada
→ baseline
→ contexto externo quando comprovado
→ projeção indicativa
```

Toda projeção deve informar o método ou tendência usada.

---

## 7. Reconciliação família × modelo

Antes de apresentar projeção empilhada por modelo, aplicar a regra:

```text
Σ projeção dos modelos da família = projeção total da família
```

Se a baseline por modelo e a baseline por família tiverem sido calculadas independentemente e não fecharem:

- não somar como se fossem reconciliadas;
- não construir barra empilhada enganosa;
- sinalizar `GAP_RECONCILIACAO_FAMILIA_MODELO`;
- usar a família como total diretivo;
- apresentar modelos como sinais explicativos até a reconciliação.

A evolução recomendada é:

```text
PREVISÃO DA FAMÍLIA
→ define total mensal
→ MIX PREVISTO POR MODELO
→ distribui o total da família
→ SPOT + EVENTO por modelo
```

---

## 8. Ordem visual obrigatória da resposta

Toda solicitação PCP/Diretoria relacionada a comparação de demanda e estoque deve, quando os dados existirem, seguir:

```text
1. TABELA COMPARATIVA — 3 MESES × ANO ANTERIOR/ATUAL

2. QUAIS MODELOS EXPLICAM ESSAS MUDANÇAS
   ├─ mês 1 / CONTÊINER
   ├─ mês 1 / MÓDULO
   ├─ mês 2 / CONTÊINER
   ├─ mês 2 / MÓDULO
   ├─ mês 3 / CONTÊINER
   └─ mês 3 / MÓDULO

3. TABELA DEMANDA / RETORNO / ESTOQUE

4. PLANO ANO ANTERIOR → ATUAL → SEGUINTE
   └─ somente quando houver projeção solicitada/aplicável
```

---

## 9. Convenção de status

Usar explicitamente:

- `REALIZADO` — período fechado com evidência histórica;
- `PREVISAO_BASE` — baseline estatística existente;
- `PROJECAO_INDICATIVA` — extrapolação para planejamento, ainda não previsão Comercial governada;
- `PREVISAO_COMERCIAL_GOVERNADA` — somente quando houver processo/evidência correspondente;
- `GAP_DADOS` — dado necessário ausente;
- `GAP_RECONCILIACAO_FAMILIA_MODELO` — total de modelos não fecha com família;
- `GAP_QUANTIDADE_FISICA` — registro-equivalente não reconciliado com unidade física.

---

## 10. Regras de apresentação

1. Sempre comparar **mesmo mês contra mesmo mês**.
2. Sempre usar **3 meses consecutivos** na visão padrão.
3. Preferir **3 últimos meses completos** quando nenhum período for indicado.
4. Sempre mostrar `CONTÊINER` e `MÓDULO`, salvo filtro explícito.
5. Sempre abrir o total em `SPOT`, `EVENTO` e `VENDA` quando os dados existirem.
6. Sempre explicar quais modelos causaram a mudança.
7. Sempre apresentar retorno/estoque depois da explicação dos modelos.
8. Projeção futura é opcional e deve ser rotulada.
9. Não transformar EVENTO em estoque permanente sem análise.
10. Não afirmar causalidade externa sem evidência.
11. Não comparar `REGISTRO_EQUIVALENTE` com estoque físico.
12. Não usar soma de modelos projetados quando ela não estiver reconciliada com a família.

---

## 11. Exemplo de solicitação interpretada

Pedido:

```text
Mostre a visão PCP comercial.
```

Interpretação padrão:

```text
- localizar os 3 últimos meses completos;
- comparar com os mesmos 3 meses do ano anterior;
- montar tabela de família/natureza;
- identificar modelos que explicam as mudanças;
- apresentar demanda/retorno/estoque;
- não projetar o ano seguinte, salvo se o objetivo ou pedido incluir planejamento futuro.
```

Pedido:

```text
Mostre a visão PCP comercial e projete o próximo ano.
```

Interpretação:

```text
- executar toda a visão padrão;
- acrescentar o mesmo trimestre do ano seguinte como PROJECAO_INDICATIVA;
- informar método/tendência;
- reconciliar família × modelo ou registrar GAP.
```

---

## 12. Contrato de integração

Este documento deve ser recuperado em conjunto com:

1. `PCP_INSTRUCOES_GERAIS_GOVERNANCA.md`;
2. `PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL.md`;
3. `PCP_COMERCIAL_DEMANDA_RETORNO_ESTOQUE.md`;
4. `public.v_elo_diretoria_comercial_estoque`;
5. fontes operacionais de devolução, estoque, reparo e produção quando aplicáveis.

Ele define a **forma padrão de resposta**, não uma nova autoridade operacional.