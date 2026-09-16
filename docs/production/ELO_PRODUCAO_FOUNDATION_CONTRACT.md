# ELO — Fundação do Domínio PRODUÇÃO

**Status:** PROPOSTA CONTROLADA — Fundação estrutural
**Versão:** 1.0
**Data:** 2026-09-16
**Autoridade canônica:** ELO Cognitivo / GitHub
**Persistência operacional prevista:** Supabase, mediante validação física

## 1. Objetivo

Estabelecer a fundação do domínio `PRODUCAO` no ELO sem criar uma autoridade paralela e sem antecipar regras operacionais que ainda não tenham evidência ou arbitragem.

A fundação deve conectar PCP, Produção, Qualidade, Suprimentos, Logística e Resultado/Pós-execução por objetos rastreáveis.

## 2. Estruturas já existentes que devem ser reutilizadas

O modelo lógico Multiteiner já define estruturas para:

- `ordem_pcp`
- `lista_material`
- `lista_material_item`
- `estoque`
- `ordem_compra`
- `ordem_producao`
- `ordem_producao_etapa`
- `inspecao_qualidade`
- `expedicao`
- `retorno_modulo`
- `ordem_reparo`
- `reparo_etapa`
- `reparo_material`
- `apontamento_reparo`
- `teste_reparo`
- `elo_evento_processo`
- `elo_sinal`
- `elo_plano_tatico`

Estas estruturas são a base existente e devem ser consolidadas antes da criação de novas tabelas equivalentes.

## 3. Cadeia estrutural

```text
DEMANDA / AF
    ↓
ORÇAMENTO / CUSTOMIZAÇÃO
    ↓
PCP — ORDEM_PCP
    ↓
LISTA-MATERIAL + ESTOQUE + COMPRAS
    ↓
PRODUÇÃO — ORDEM_PRODUÇÃO
    ↓
ETAPAS DE PRODUÇÃO
    ↓
QUALIDADE / INSPEÇÃO
    ↓
EXPEDIÇÃO
    ↓
RESULTADO / PÓS-EXECUÇÃO
```

Fluxos de recuperação devem permanecer conectados por:

```text
RETORNO → QUARENTENA → AVARIA → ORDEM_REPARO → REPARO_ETAPA → TESTE → RESULTADO
```

## 4. Objetos mínimos da Produção

A primeira implementação operacional deve reconhecer, no mínimo:

| Objeto | Função | Fonte estrutural existente |
|---|---|---|
| Ordem PCP | Demanda programada para produção | `multiteiner.ordem_pcp` |
| Lista-Mãe | Necessidade de materiais | `multiteiner.lista_material` |
| Item Lista-Mãe | Quantidade por material | `multiteiner.lista_material_item` |
| Ordem de Produção | Unidade executável | `multiteiner.ordem_producao` |
| Etapa | Registro sequencial da execução | `multiteiner.ordem_producao_etapa` |
| Inspeção | Evidência de qualidade | `multiteiner.inspecao_qualidade` |
| Evento | Rastreabilidade do processo | `multiteiner.elo_evento_processo` |
| Sinal | Anomalia/indicador para análise | `multiteiner.elo_sinal` |
| Plano Tático | Ação decorrente de sinal | `multiteiner.elo_plano_tatico` |

## 5. Regras de fundação

1. Uma Ordem de Produção deve estar vinculada a uma Ordem PCP.
2. Uma Ordem PCP deve estar vinculada a uma AF.
3. A produção não deve receber como fato uma demanda que não possua origem rastreável.
4. Quantidades de materiais devem derivar de uma Lista-Material identificada e versionada.
5. Disponibilidade de material deve ser separada de necessidade planejada.
6. Etapas devem possuir ordem sequencial e estado explícito.
7. Qualidade deve poder apontar para a etapa em que a evidência foi produzida.
8. Retrabalho deve ser distinguível de execução normal.
9. Eventos de processo devem apontar para o objeto de origem.
10. Sinais não são decisões; devem alimentar análise e eventual plano tático.
11. O ELO pode diagnosticar, analisar e recomendar; não deve alterar uma ordem de produção sem autorização operacional definida.
12. Nenhum indicador, lead time, capacidade ou sequência padrão deve ser promovido a regra canônica sem evidência validada e governança.

## 6. Estruturas que ainda precisam ser edificadas

A implementação posterior deve tratar, nesta ordem:

1. **Catálogo de etapas de produção** — somente após levantamento real do fluxo fabril.
2. **Centros/recursos de produção** — galpão, célula, equipamento ou recurso, conforme evidência operacional.
3. **Capacidade** — disponibilidade, carga e restrições.
4. **Calendário produtivo** — jornadas, paradas e exceções.
5. **Apontamento de produção** — quantidade, início, fim, equipe e evidência.
6. **Planejamento de sequência** — prioridade e dependências.
7. **Controle de WIP** — ordens em processo e posição no fluxo.
8. **Retrabalho e não conformidade** — ligação formal entre Produção e Qualidade.
9. **KPIs de produção** — somente com definições, fontes e fórmulas governadas.
10. **Dashboard ELO Web** — somente após o contrato de dados e a API cognitiva estarem definidos.

## 7. Limites

Este documento não define:

- tempos padrão de fabricação;
- capacidade diária dos galpões;
- número de operadores;
- produtividade por equipe;
- sequência física definitiva das operações;
- custos padrão;
- metas de produção;
- qualquer decisão de alteração da produção.

Esses elementos dependem de levantamento, evidência, validação e arbitragem.

## 8. Critério de evolução

Qualquer nova estrutura deve passar por:

`REUSE → STRENGTHEN → REFACTOR → DEPRECATE → CREATE`

A criação de uma nova tabela, capability, regra ou componente só deve ocorrer quando a estrutura existente não atender ao contrato e houver evidência dessa necessidade.

## 9. Próxima etapa

A próxima etapa técnica é transformar este contrato em um **registro governado do domínio PRODUÇÃO**, mapear cada campo contra o modelo lógico existente e somente então definir as alterações físicas necessárias no banco e no ELO Web.
