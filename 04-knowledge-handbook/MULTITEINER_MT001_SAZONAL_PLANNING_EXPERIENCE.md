# Multiteiner MT-001 — Experiência de Planejamento Sazonal

> **Status:** EXPERIENCE / UNVALIDATED
> **Fonte:** informações operacionais fornecidas durante a sessão de análise do ELO.
> **Uso:** experiência contextual para testes e simulações; não constitui regra canônica nem decisão operacional.

## 1. Contexto

No período de agosto, o Comercial informa em reunião uma expectativa de eventos sazonais potencialmente fechados até o início de dezembro, totalizando aproximadamente **300 módulos**, com predominância dos modelos **M01, M05 e M14**.

A demanda é sazonal. Os 300 módulos representam o total esperado para o período, e não uma demanda mensal.

Existe também uma demanda recorrente de clientes menores, anteriormente na ordem de **70 módulos/mês**. Diante do cenário atual, a empresa decidiu **suspender o atendimento desses clientes menores** para concentrar capacidade na demanda sazonal.

## 2. Estado dos módulos

O estoque de módulos informado é **zero**.

Módulos que retornam de clientes passam primeiro por **quarentena no pátio** e depois seguem para reparos. A capacidade informada para reparos é aproximadamente **3 módulos/dia**.

Os módulos que estão atualmente em quarentena já possuem destinação/compromisso com clientes de locações fechadas em meses anteriores. Portanto, **não devem ser tratados como estoque livre para a demanda sazonal**.

Está previsto o retorno de aproximadamente **100 módulos no início de setembro**. A existência física desses retornos não implica disponibilidade automática para a demanda sazonal: é necessário verificar condição, reparo, modelo, data de liberação e compromisso/destinação anterior.

## 3. Montagem

A capacidade anteriormente informada de aproximadamente **3 módulos/dia** deve ser qualificada antes de qualquer cálculo: o cenário possui uma capacidade de reparo de aproximadamente 3 módulos/dia e também foi informada uma referência de montagem de 3 módulos/dia. Essas duas capacidades não devem ser confundidas.

Tempos de montagem atualmente informados:

- **M01:** aproximadamente 4 horas/unidade.
- **M05:** aproximadamente 6 horas/unidade.
- **M14:** tempo ainda não informado.

M05 e M14 são módulos sanitários e demandam mais tempo de montagem que M01, segundo a experiência operacional fornecida.

## 4. Restrição contratual de mão de obra

Parte dos eventos possui contratos que exigem funcionários **CLT destinados ao contrato**. A disponibilidade atual de funcionários CLT foi informada como insuficiente para atender todos esses contratos potenciais.

Portanto, capacidade física de montagem não deve ser confundida com capacidade contratualmente habilitada.

## 5. Estrutura da experiência

```text
DEMANDA SAZONAL (~300)
        |
        +--> M01 / M05 / M14
        |
        +--> datas dos eventos
        |
        v
PLANEJAMENTO / PCP
        |
        +--> capacidade de montagem
        +--> capacidade de reparo
        +--> módulos comprometidos
        +--> módulos potencialmente liberáveis
        |
        v
RETORNOS DE LOCAÇÃO (~100 no início de setembro)
        |
        v
QUARENTENA -> REPARO (~3/dia) -> LIBERAÇÃO
        |
        v
ALOCABILIDADE REAL
        |
        +--> demanda sazonal
        +--> compromissos anteriores
        |
        v
CONTRATOS / CLT
        |
        v
DECISÃO INTEGRADA
```

## 6. Conhecimentos ainda não determinados

Esta experiência deliberadamente preserva lacunas:

- distribuição dos 300 módulos por evento;
- quantidade de M01, M05 e M14;
- datas exatas de cada evento;
- quais dos 300 já estão contratados;
- tempo de montagem do M14;
- horas/equipe disponíveis para montagem;
- dias produtivos do horizonte;
- produtividade real versus nominal;
- composição dos aproximadamente 100 retornos por modelo;
- datas individuais dos retornos;
- condição dos retornos;
- quantidade efetivamente liberável após reparo;
- compromissos contratuais associados aos retornos;
- quantidade disponível e déficit de CLT;
- impacto logístico e datas de entrega.

## 7. Regra cognitiva extraída para teste

A experiência demonstra uma distinção que deve ser preservada nos testes do ELO:

> **Existência física de um módulo não significa disponibilidade operacional.**

Também:

> **Demanda sazonal, demanda recorrente, pipeline comercial, estoque comprometido e capacidade de produção/reparo são entidades diferentes e não devem ser agregadas sem validação de contexto.**

## 8. Classificação cognitiva

- **Tipo:** experiência operacional contextual.
- **Domínio:** Comercial / PCP / Montagem / Locação / Reparos / RH-CLT.
- **Empresa de referência:** Multiteiner.
- **Validade:** contextual, pendente de validação pelos especialistas.
- **Não promover automaticamente para Faculty.**
- **Não tratar como Overlay permanente sem validação.**
- **Lacunas devem permanecer como GAP até obtenção de evidência.**

## 9. Uso nos próximos testes

O ELO deve usar esta experiência para construir cenários nos quais:

1. Comercial apresenta a demanda sazonal.
2. PCP calcula necessidade e capacidade.
3. Locação informa retornos e compromissos.
4. Reparos informa fila e capacidade.
5. Montagem informa carga por modelo.
6. RH informa restrição de CLT.
7. Logística informa datas críticas.
8. ELO cruza as informações.
9. ELO identifica conflitos e lacunas.
10. ELO apresenta cenários conservador, provável e crítico.
11. ELO registra decisão, evidência, impacto e resultado.
12. Após o ciclo, o aprendizado é avaliado antes de qualquer promoção cognitiva.
