# PCP — Comercial, Demanda, Retorno e Estoque

**Status:** processo especializado PCP / Comercial  
**Owner cognitivo:** `SKILL_PLANEJAMENTO_MULTITEINER`  
**Governança superior:** `PCP_INSTRUCOES_GERAIS_GOVERNANCA.md`  
**Referência de comparabilidade:** `PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL.md`  
**Read-model executivo:** `public.v_elo_diretoria_comercial_estoque`  
**Baseline analítica privada:** `elo_private.pcp_diretoria_comercial_mensal`

---

## 1. Finalidade

Formalizar o processo que transforma evidência Comercial em informação governada para planejamento do PCP, cobrindo:

- demanda por família e modelo;
- separação entre MÓDULO e CONTÊINER;
- SPOT, EVENTO e sazonalidade validada;
- crescimento/redução por mês e ano;
- previsão-base e correção contextual;
- retorno previsto de locações;
- impacto de quarentena, inspeção e reparo;
- estoque mínimo, estoque de segurança e proteção comercial;
- cobertura, déficit e necessidade adicional;
- alerta cognitivo ao ELO/PCP;
- análise de contexto externo;
- SWOT e 5W2H quando aplicáveis;
- confronto previsto × realizado e aprendizado governado.

Este documento **não substitui** a autoridade das tabelas operacionais, da governança PCP nem da Skill. Ele descreve o processo especializado e suas fronteiras.

---

## 2. Cadeia canônica

```text
COMERCIAL
   ↓
classificação e proveniência
   ↓
referência histórica comparável
   ↓
crescimento/redução por dimensão comparável
   ↓
previsão-base
   ↓
contexto externo comprovado / hipóteses explícitas
   ↓
previsão contextual governada
   ↓
demanda por família/modelo/mês
   ↕
retornos previstos por família/modelo/mês
   ↓
quarentena → inspeção → reparo → liberação provável
   ↓
estoque operacional projetado
   ↓
estoque mínimo + segurança + reserva EVENTO
   ↓
cobertura / déficit / excesso
   ↓
alerta cognitivo ELO
   ↓
SWOT / análise de cenário
   ↓
decisão governada
   ↓
5W2H / PCP
   ↓
resultado real
   ↓
erro da previsão / aprendizado
```

---

## 3. Dimensões obrigatórias

Toda análise deve preservar, quando disponíveis e comparáveis:

- ano;
- mês;
- família do produto: `MODULO` ou `CONTEINER`;
- modelo;
- natureza da demanda;
- operação comercial;
- origem/fonte;
- unidade de medida;
- condição de comparabilidade.

### 3.1 Operação comercial × natureza da demanda

A operação da fonte e a natureza analítica não são a mesma dimensão.

Regras iniciais do processo:

- `EVENTO` na fonte → locação com `natureza_demanda = EVENTO`;
- `LOCAÇÃO` não-evento → `tipo_pedido = LOCACAO` e `natureza_demanda = SPOT`;
- `VENDA` → `tipo_pedido = VENDA`; quando não houver evidência de evento/sazonalidade, permanece no grupo não-evento/`SPOT` para análise comercial;
- `SAZONALIDADE` **não é sinônimo de EVENTO**.

`SAZONALIDADE` só pode ser usada quando a recorrência histórica estiver demonstrada e validada.

---

## 4. Família: MÓDULO × CONTÊINER

A apresentação executiva deve permitir filtro explícito por:

```text
familia_produto = MODULO
familia_produto = CONTEINER
```

A família não substitui o modelo. A análise deve existir nos dois níveis:

1. `FAMILIA` — visão diretiva consolidada;
2. `MODELO` — visão operacional/analítica detalhada.

Mobiliário, acessórios e demais famílias não devem ser tratados como modelos de contêiner somente porque aparecem na mesma fonte comercial.

---

## 5. Datas e semântica temporal

### 5.1 Data da proposta

Usar para medir atividade/demanda comercial histórica quando a pergunta for volume de propostas/demanda apresentada.

### 5.2 Data do fechamento

Usar para medir fechamento realizado. Não substituir automaticamente a data de proposta.

### 5.3 Data prevista da saída

Representa a saída/expedição planejada informada pela fonte comercial. Não deve ser reinterpretada como entrega ao cliente sem evidência.

### 5.4 Data prevista de retorno

Para locações cuja unidade de `Período` esteja validada em meses:

```text
DATA_RETORNO_PREVISTA = DATA_PREVISTA_SAIDA + PERIODO_MESES
```

Exemplo de regra:

```text
14/01/2021 + 4 meses = 14/05/2021
```

A fórmula é uma **derivação**. O retorno real deve vir da autoridade operacional de devolução.

### 5.5 EVENTO

O campo `Período` de EVENTO não deve ser tratado automaticamente como meses enquanto sua semântica não estiver validada.

---

## 6. Referência histórica comparável

Antes de aplicar crescimento ou redução, comparar dimensões equivalentes.

A autoridade metodológica é:

`PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL.md`.

A comparação deve respeitar:

```text
mes equivalente
+ familia equivalente
+ modelo equivalente
+ natureza equivalente
+ unidade equivalente
+ chave de comparabilidade quando aplicável
```

Ausência de referência equivalente gera `GAP_COMPARABILIDADE`.

---

## 7. Indicadores de crescimento e queda

### 7.1 Diferença em pontos percentuais

```text
Δpp = participação_atual_pct - participação_anterior_pct
```

### 7.2 Crescimento relativo YoY

```text
YoY_pct = ((valor_atual / valor_ano_anterior) - 1) × 100
```

### 7.3 Crescimento MoM

```text
MoM_pct = ((valor_mes_atual / valor_mes_anterior) - 1) × 100
```

Quando o denominador for zero ou não comparável, não produzir percentual artificial.

### 7.4 Percentual mensal dentro do ano

```text
participacao_mes_pct = demanda_mes / demanda_ano × 100
```

Esse indicador deve ser calculado por dimensão coerente, por exemplo família, modelo e natureza.

---

## 8. Previsão-base e correção contextual

A previsão estatística é uma **baseline**, não decisão operacional.

Ela pode utilizar histórico comparável, tendência e erro observado, mas deve permanecer identificada como `PREVISAO_BASE` até passar pelos gates de validação.

Fatores externos podem alterar cenário/confiança apenas quando houver evidência ou hipótese explicitamente rotulada.

Exemplos a investigar:

- perda de contrato;
- renovação contratual frágil;
- renovação confirmada;
- campanha de novos clientes;
- evento confirmado/cancelado;
- mudança de preço;
- entrada/saída de concorrente;
- aumento de concorrência;
- alterações relevantes de mercado.

O ELO não deve declarar causalidade apenas porque uma variação estatística foi observada.

---

## 9. Retorno previsto e disponibilidade

Regra central:

```text
RETORNO PREVISTO != ESTOQUE LIVRE
```

O fluxo físico esperado é:

```text
retorno previsto
→ quarentena
→ inspeção
→ necessidade de reparo?
→ reparo
→ liberação
→ estoque operacional disponível
```

A análise de cobertura deve considerar separadamente:

- retorno previsto;
- retorno efetivo;
- quarentena;
- reparo pendente;
- reparo recuperável no período;
- compromissos/reservas já existentes;
- estoque livre;
- produção programada.

---

## 10. Política de estoque V1

A política inicial usa a demanda mensal histórica SPOT por família/modelo e mês-calendário.

### 10.1 Estoque mínimo SPOT

```text
ESTOQUE_MINIMO_SPOT = ceil(P75(demanda_mensal_SPOT_historica))
```

### 10.2 Estoque de segurança SPOT

```text
ESTOQUE_SEGURANCA_SPOT = max(ceil(P90) - ceil(P75), 0)
```

### 10.3 Estoque-alvo SPOT

```text
ESTOQUE_ALVO_SPOT = ceil(P90(demanda_mensal_SPOT_historica))
```

### 10.4 Reserva EVENTO

EVENTO não deve inflar silenciosamente o estoque permanente.

A referência inicial é:

```text
RESERVA_EVENTO_REFERENCIA = ceil(P90(demanda_mensal_EVENTO_historica))
```

A reserva pode ser substituída por demanda de evento confirmada quando houver evidência governada mais específica.

### 10.5 Proteção comercial

```text
PROTECAO_COMERCIAL = ESTOQUE_ALVO_SPOT + RESERVA_EVENTO
```

Esses parâmetros devem ser recalibrados com nível de serviço, lead time e histórico físico quando esses dados estiverem disponíveis e validados.

---

## 11. Cobertura e necessidade adicional

Quando todos os valores estiverem na mesma unidade física e período:

```text
OFERTA_PROJETADA =
  ESTOQUE_LIVRE
  + RETORNOS_LIBERAVEIS
  + REPAROS_LIBERAVEIS
  + PRODUCAO_PROGRAMADA
```

```text
NECESSIDADE_ADICIONAL =
  max(PROTECAO_COMERCIAL - OFERTA_PROJETADA, 0)
```

Nunca confrontar `REGISTRO_EQUIVALENTE` com unidade física como se fossem a mesma medida.

---

## 12. Unidade de medida e fail-closed

A baseline atual originada da planilha Comercial não possui quantidade física explícita por linha.

Enquanto não houver reconciliação, usar:

```text
unidade_medida = REGISTRO_EQUIVALENTE
estado_estoque = GAP_QUANTIDADE_FISICA
```

Consequências:

- estoque mínimo/segurança podem ser apresentados como referência estatística;
- não afirmar que o número representa unidades físicas;
- saldo físico contra mínimo deve permanecer bloqueado/nulo;
- a decisão de fabricar/comprar não pode ser disparada somente por essa baseline.

---

## 13. Read-model executivo

A view oficial desta camada é:

```sql
public.v_elo_diretoria_comercial_estoque
```

Ela deve ser consultada antes de propor outra view equivalente.

Filtros principais:

- `nivel_analise`: `FAMILIA` ou `MODELO`;
- `familia_produto`: `MODULO` ou `CONTEINER`;
- ano;
- mês;
- modelo;
- `tipo_registro` quando aplicável.

Indicadores esperados:

- demanda total;
- demanda SPOT;
- demanda EVENTO;
- venda;
- participações percentuais;
- natureza dominante;
- crescimento MoM/YoY;
- retorno previsto;
- cobertura do retorno;
- estoque mínimo;
- estoque de segurança;
- estoque-alvo;
- reserva EVENTO;
- proteção comercial;
- cobertura/necessidade quando fisicamente comparável;
- alerta cognitivo;
- orientação PCP;
- ferramenta de qualidade recomendada.

---

## 14. Baseline privada

A tabela derivada é:

```sql
elo_private.pcp_diretoria_comercial_mensal
```

Ela é uma baseline analítica e **não substitui**:

- `mt_demanda_historico`;
- `mt_previsoes_demanda`;
- `mt_unidades_modulares`;
- `mt_devolucoes`;
- `mt_ordens_reparo`;
- demais autoridades operacionais.

A proveniência deve permanecer ligada a `mt_referencias_fontes` e, quando aplicável, `mt_proveniencia_registros`.

---

## 15. Alerta cognitivo do ELO

O alerta deve separar:

1. **FATO** — evidência localizada;
2. **RISCO** — condição provável ou ameaça explicitamente sustentada;
3. **IMPACTO** — efeito calculado ou cenário;
4. **AÇÃO/ANÁLISE RECOMENDADA** — próximo passo governado.

Níveis possíveis podem incluir:

- `INFORMATIVO`;
- `ATENCAO`;
- `CRITICO`;
- `GAP_DADOS`.

Variação elevada ou baixa cobertura deve orientar investigação, não inventar causa.

---

## 16. SWOT e 5W2H

### SWOT

Pode ser usada como ferramenta de leitura de cenário quando houver evidências externas suficientes.

Cada item deve ser classificado como:

- evidência;
- hipótese a validar.

### 5W2H

Deve ocorrer depois da decisão governada, convertendo a decisão em plano de ação.

```text
WHAT
WHY
WHERE
WHEN
WHO
HOW
HOW MUCH
```

O ELO não deve usar 5W2H para legitimar uma decisão ainda sem evidência.

---

## 17. Contrato com a Skill PCP

Este processo é uma especialização da:

`SKILL_PLANEJAMENTO_MULTITEINER`.

Quando a solicitação envolver demanda Comercial, crescimento, retorno, estoque mínimo/segurança ou cobertura de famílias/modelos, a Skill deve:

1. recuperar a governança PCP vigente;
2. recuperar este documento;
3. consultar `v_elo_diretoria_comercial_estoque`;
4. confrontar com `v_elo_pcp_cobertura_demanda_externa` quando houver unidade física/modelo/tenant reconciliados;
5. registrar GAPs sem inferi-los;
6. produzir orientação PCP somente no limite da evidência;
7. encaminhar evidência elegível pelo fluxo canônico de aprendizado/evolução.

---

## 18. GATES obrigatórios

### Gate A — Classificação

Confirmar família, modelo, operação, natureza, período e unidade.

### Gate B — Comparabilidade

Confirmar referência histórica equivalente.

### Gate C — Previsão

Separar histórico, previsão-base, previsão Comercial e cenário contextual.

### Gate D — Retorno

Confirmar semântica do período e qualidade das datas antes de derivar retorno.

### Gate E — Estoque

Confirmar que demanda e estoque estão na mesma unidade física antes de calcular déficit/excesso operacional.

### Gate F — Contexto externo

Separar evidência de hipótese e registrar a fonte.

### Gate G — Decisão

Nenhuma ação operacional deve ser promovida somente por tendência estatística ou baseline derivada.

### Gate H — Aprendizado

Confrontar previsto × realizado e encaminhar evidência pelo mecanismo canônico; não promover experiência diretamente a regra.

---

## 19. GAPs atuais conhecidos

No estado de implantação de 2026-10-21:

- a fonte Comercial não informa quantidade física explícita por linha;
- `mt_tenants` ainda não possui tenant canônico estabelecido para esta carga;
- o catálogo canônico de modelos ainda não cobre/reconcilia todos os modelos de CONTÊINER da fonte;
- a semântica de `Período` para EVENTO precisa de validação antes de derivar retorno em meses;
- o histórico completo ainda precisa de backfill no read-model para navegação histórica linha a linha;
- previsão-base estatística não substitui `mt_previsoes_demanda`;
- percentis P75/P90 são política V1 e devem ser recalibrados quando nível de serviço/lead time físico estiverem validados.

---

## 20. Estado implantado

A camada executiva criada em 2026-10-21 possui:

- tabela: `elo_private.pcp_diretoria_comercial_mensal`;
- view: `public.v_elo_diretoria_comercial_estoque`;
- 600 linhas de baseline/read-model no estado validado;
- 24 linhas no nível FAMÍLIA;
- 576 linhas no nível MODELO;
- horizonte inicial: out/2026 a set/2027;
- 48 combinações família/modelo da fonte;
- distinção explícita entre `REGISTRO_EQUIVALENTE` e unidade física.

Esses números descrevem o estado da implantação, não uma regra imutável do processo.

---

## 21. Próximas evoluções governadas

1. backfill histórico mensal comparável;
2. reconciliação de modelos da fonte com o catálogo canônico;
3. estabelecimento do tenant correto;
4. incorporação de quantidade física;
5. reconciliação de retornos com devolução real;
6. incorporação de quarentena/reparo/liberação real;
7. calibração de nível de serviço e lead time para estoque;
8. medição de erro de previsão por família/modelo/natureza;
9. aprendizagem sobre quais sinais externos efetivamente melhoram a previsão.

---

## 22. Referências

- `06-knowledge-engineering/SKILL_PLANEJAMENTO_MULTITEINER.md`
- `06-knowledge-engineering/PCP_INSTRUCOES_GERAIS_GOVERNANCA.md`
- `06-knowledge-engineering/PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL.md`
- `docs/pcp/PCP_VISAO_DIRETORIA_COMERCIAL_ESTOQUE_20261021.md`
- `docs/pcp/PCP_DIRETORIA_COMERCIAL_ESTOQUE_EVIDENCE_20261021.md`
- `public.v_elo_diretoria_comercial_estoque`
- `public.v_elo_pcp_cobertura_demanda_externa`

**Regra final:** usar evidência Comercial para orientar o PCP, sem converter baseline estatística, registro-equivalente ou hipótese externa em fato operacional.