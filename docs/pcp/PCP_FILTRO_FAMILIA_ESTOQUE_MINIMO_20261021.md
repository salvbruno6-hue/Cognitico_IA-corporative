# PCP — Filtro Módulo × Contêiner e baseline de estoque mínimo

**Data:** 2026-10-21  
**Fonte comercial desta etapa:** `Cópia de Relatório Comercial (1).csv`  
**Status:** baseline analítica com GAPs explícitos; não equivale ainda a estoque físico governado.

## 1. Objetivo

Separar MÓDULO de CONTÊINER nas leituras de cobertura do PCP e estabelecer uma primeira referência de estoque mínimo a partir do histórico comercial, sem transformar registros da planilha em unidades físicas sem evidência.

## 2. Filtro de família na view

A view `public.v_elo_pcp_cobertura_demanda_externa` passa a expor `familia_produto` com valores:

- `MODULO`
- `CONTEINER`
- `OUTRO`

A classificação deriva de `modelos.familia` e, na ausência, `taxonomia.tipo`. O filtro não cria uma nova autoridade; apenas normaliza o catálogo canônico para leitura analítica.

### GAP atual do catálogo

No estado operacional verificado em 2026-10-21, o catálogo `public.modelos` possui modelos classificados como Módulo e um item sem taxonomia, mas não possui modelos canônicos classificados como Contêiner. Portanto, a coluna já suporta o filtro, porém linhas `CONTEINER` somente aparecerão depois que os modelos de contêiner da base comercial forem reconciliados com `modelos`/`taxonomia`.

## 3. Regra para estoque mínimo

Para não misturar demanda recorrente com picos de evento, o estoque mínimo base deve usar **SPOT**. Nesta etapa, a planilha representa SPOT por `Locação/Evento/Venda = LOCAÇÃO`; `EVENTO` permanece reserva sazonal separada.

A primeira política candidata é:

`estoque_minimo_base_modelo = ceil(P75 da demanda mensal SPOT histórica do modelo)`

O P75 foi escolhido como baseline inicial de cobertura porque protege contra um mês acima da mediana sem elevar o estoque ao nível dos picos extremos. Ele deve permanecer parametrizável e ser validado pelo PCP depois que existirem unidades físicas, retornos e lead times confiáveis.

### Regra de cobertura futura

`necessidade_cobertura = max(estoque_minimo_base + reserva_evento_confirmada - estoque_livre - retornos_liberaveis - reparos_liberaveis - producao_programada, 0)`

`retornos_liberaveis` não é igual a retorno físico. Um retorno somente pode entrar como oferta depois de quarentena, inspeção, reparo quando necessário e verificação de compromisso anterior.

## 4. Baseline calculada da planilha

Critérios usados:

- famílias analisadas: `MÓDULO` e `CONTÊINER`;
- natureza base: `LOCAÇÃO` (SPOT não-evento);
- eixo temporal: `Data da Proposta`, porque `Data Prevista da Saída` está incompleta em grande parte do histórico;
- meses completos: até setembro/2026;
- meses sem demanda entre a primeira ocorrência e setembro/2026 entram como zero;
- unidade da métrica nesta etapa: **registros-equivalentes**, não unidades físicas.

### Família

| Família | média mensal SPOT | P75 | P90 | baseline P75 arredondada |
|---|---:|---:|---:|---:|
| CONTÊINER | ~49,5 | 62,0 | 77,0 | 62 registros-equivalentes |
| MÓDULO | ~24,2 | 31,75 | 39,7 | 32 registros-equivalentes |

O EVENTO não deve ser incorporado automaticamente ao estoque mínimo fixo. Como referência histórica separada, o P75 mensal de EVENTO foi aproximadamente 7 registros-equivalentes para CONTÊINER e 52 para MÓDULO. Essa parcela deve ser tratada por previsão/evento confirmado, não como estoque permanente.

### Principais modelos — CONTÊINER / SPOT

| Modelo | média mensal | P75 | P90 |
|---|---:|---:|---:|
| DEPÓSITO 20 PÉS | 13,4 | 17 | 21 |
| ESCRITÓRIO SIMPLES 20 PÉS | 7,4 | 10 | 14,9 |
| ALMOXARIFADO 20 PÉS | 5,9 | 8 | 10 |
| SANITÁRIO COL. CABINADO 20 PÉS | 5,2 | 8 | 10 |
| DEPÓSITO 40 PÉS | 4,5 | 5,8 | 13,1 |
| SUÍTE SIMPLES 20 PÉS | 4,5 | 6 | 9 |
| ESCRITÓRIO FORRADO 20 PÉS | 3,4 | 5 | 7 |
| SUÍTE FORRADA 20 PÉS | 2,4 | 4 | 6 |

### Principais modelos — MÓDULO / SPOT

| Modelo | média mensal | P75 | P90 |
|---|---:|---:|---:|
| ESCRITÓRIO 20 PÉS | 11,2 | 15 | 23,4 |
| ESCRITÓRIO ACOPLADO 20 PÉS | 5,2 | 8,5 | 13,4 |
| SUÍTE 20 PÉS | 3,4 | 5 | 8 |
| SANITÁRIO COL. CABINADO 20 PÉS | 1,6 | 2 | 3 |
| SANITÁRIO | 1,2 | 1 | 3 |

## 5. GAPs que impedem tratar a baseline como estoque físico definitivo

### Quantidade por linha

A planilha não possui coluna de quantidade. Logo, uma linha não pode ser promovida automaticamente para uma unidade física. Os números acima são registros-equivalentes.

### Data de saída incompleta

Para `LOCAÇÃO`, a cobertura de `Data Prevista da Saída` válida é aproximadamente:

- CONTÊINER: 27,9%;
- MÓDULO: 36,0%.

A ausência é concentrada em anos inteiros do histórico, então não é seguro substituir `Data da Proposta` por `Data Prevista da Saída` como eixo operacional até ocorrer saneamento.

### Retorno previsto

A regra `Data Prevista da Saída + Período` continua válida como reconstrução de retorno contratual previsto, mas só pode reduzir necessidade de estoque quando houver:

1. data de saída válida;
2. período válido;
3. modelo reconciliado;
4. unidade/quantidade conhecida;
5. previsão de quarentena;
6. reparo/liberação provável;
7. ausência de compromisso anterior conflitante.

## 6. Critério para promover a estoque mínimo físico governado

A baseline pode evoluir de `REGISTROS_EQUIVALENTES` para `UNIDADES_FISICAS` quando forem satisfeitos:

1. mapa canônico dos modelos de CONTÊINER e MÓDULO;
2. regra validada de quantidade por linha/proposta;
3. histórico de saída suficientemente completo ou fonte alternativa reconciliada;
4. retornos previstos por modelo/mês;
5. tempos reais de quarentena e reparo;
6. taxa de liberação por modelo;
7. estoque livre versus comprometido;
8. validação PCP do percentil/nível de serviço escolhido.

## 7. Leitura cognitiva esperada

O ELO deve responder por família e modelo:

- estoque mínimo base;
- estoque livre atual;
- retornos previstos;
- retornos liberáveis;
- unidades em quarentena;
- reparos recuperáveis no horizonte;
- reserva de evento;
- demanda prevista;
- déficit/excesso projetado;
- confiança e GAPs da conclusão.

O alerta cognitivo deve impedir que `retorno previsto` seja tratado como `estoque disponível` e deve escalar ao PCP quando cobertura projetada ficar abaixo do estoque mínimo ou quando a conclusão depender de GAP relevante.
