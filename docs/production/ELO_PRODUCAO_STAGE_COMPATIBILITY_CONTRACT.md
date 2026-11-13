# ELO — Contrato de Compatibilidade das Etapas de Produção

**ID:** ELO-PROD-COMPAT-001  
**Status:** PROPOSTA CONTROLADA — reconciliação documental/física  
**Versão:** 1.0  
**Data:** 2026-09-16  
**Autoridade canônica:** ELO Cognitivo / GitHub  
**Dependências:** `ELO_PRODUCAO_FOUNDATION_CONTRACT.md`, `ELO_PRODUCAO_STAGE_CATALOG.md`  
**Modelo físico de referência:** `ordem_producao_etapa` e estruturas produtivas já existentes

## 1. Finalidade

Formalizar a reconciliação entre:

1. a sequência operacional documentada da Produção Modular;
2. o catálogo governado de 17 etapas;
3. as estruturas físicas de produção já identificadas;
4. os registros existentes de operação, fluxo PCP e etapas de ordem de produção.

Este contrato **não cria uma nova tabela de etapas**, não transforma a sequência documental em sequência física definitiva e não valida automaticamente tempos, capacidade, produtividade ou recursos.

## 2. Fontes reconciliadas

### 2.1 Fonte documental

O fluxo operacional de referência registra:

`Triagem → Chassi → Escovação → Pintura de tratamento → Acabamento branco → Estoque de estruturas → Movimentação → Piso → Teto → Colunas → Trilho → Pintura modular → Paredes → Instalações → Acabamento → Testes → Liberação`

A fonte também determina que divergências entre fluxo projetado e operação observada sejam registradas, e que informação não validada permaneça como `DOCUMENTADO / A VALIDAR` ou `OBSERVADO / A VALIDAR`.

### 2.2 Estruturas físicas já identificadas

Foram identificadas no modelo existente, sem criação de nova autoridade:

| Estrutura | Evidência atual | Uso no contrato |
|---|---|---|
| `ordem_producao_etapa` | modelo de etapas da ordem de produção | candidato principal para representar execução por etapa |
| `elo_prod_operation` | 21 registros de operações | catálogo/definição operacional existente a reconciliar |
| `elo_prod_work_center` | 14 centros de trabalho | referência de recurso |
| `elo_pcp_fluxo_modular` | fluxo modular com produto, etapa, sequência e centro | referência operacional/PCP |
| `elo_prod_flow_event` | eventos de fluxo | evidência/eventos de execução |
| `elo_prod_daily_plan` | planejamento diário | planejamento e apontamento a reconciliar |

**Importante:** a existência física dessas estruturas não significa que todos os seus valores estejam validados como padrão operacional.

## 3. Resultado da reconciliação inicial

A reconciliação é dividida em quatro estados:

- **REUTILIZAR:** estrutura existente atende ao conceito sem criar autoridade paralela;
- **FORTALECER:** estrutura existente é candidata, mas faltam vínculo, evidência ou semântica para cumprir o contrato;
- **DIVERGÊNCIA:** estruturas representam conceitos ou sequências potencialmente diferentes e exigem decisão;
- **NÃO VALIDADO:** existe dado ou campo, mas sua origem/validade operacional ainda não foi comprovada.

### 3.1 Matriz de compatibilidade por etapa

| Seq. | Etapa documental | Correspondência física inicial | Estado | Ação requerida |
|---:|---|---|---|---|
| 01 | Triagem | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | comprovar código, sequência e evidência |
| 02 | Chassi | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | reconciliar operação e centro |
| 03 | Escovação | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | comprovar correspondência |
| 04 | Pintura de tratamento | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | comprovar operação e evidência |
| 05 | Acabamento branco | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | comprovar correspondência |
| 06 | Estoque de estruturas | `elo_pcp_fluxo_modular` / eventos de fluxo | FORTALECER | distinguir estoque/espera de operação produtiva |
| 07 | Movimentação | `elo_pcp_fluxo_modular` / `elo_prod_flow_event` | FORTALECER | validar se é etapa, evento ou recurso de transferência |
| 08 | Piso | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | reconciliar código e sequência |
| 09 | Teto | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | reconciliar código e sequência |
| 10 | Colunas | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | reconciliar código e sequência |
| 11 | Trilho | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | reconciliar código e sequência |
| 12 | Pintura modular | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | comprovar operação e centro |
| 13 | Paredes | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | reconciliar operação e dependências |
| 14 | Instalações | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | separar instalações por natureza somente se evidenciado |
| 15 | Acabamento | `elo_prod_operation` / `elo_pcp_fluxo_modular` | FORTALECER | comprovar correspondência |
| 16 | Testes | `elo_prod_operation` / qualidade/eventos | FORTALECER | vincular teste à etapa e evidência de resultado |
| 17 | Liberação | `ordem_producao_etapa` / qualidade/eventos | FORTALECER | definir gate de liberação sem criar novo estado paralelo |

**Leitura correta:** a matriz não afirma que cada etapa já possui correspondência 1:1 validada. Ela registra candidatos de reutilização e as validações necessárias.

## 4. Divergências estruturais que precisam de decisão

### D-01 — 17 etapas documentadas × 21 operações existentes

O catálogo documental possui 17 etapas, enquanto `elo_prod_operation` possui 21 registros. Isso **não é, por si só, erro ou duplicidade**.

Possibilidades a verificar com evidência:

- operações auxiliares;
- operações específicas por produto;
- subdivisões de uma etapa documental;
- operações de customização;
- operações de reparo;
- registros históricos ou ativos/inativos.

**Regra:** não reduzir 21 para 17 por inferência.

### D-02 — `Movimentação` e `Estoque de estruturas`

Esses elementos aparecem na sequência documental, mas podem representar estados/logística interna em vez de operações produtivas equivalentes às demais etapas.

**Decisão necessária:** validar com processo físico se devem permanecer como etapas, eventos ou interfaces entre centros.

### D-03 — Qualidade e testes

`Testes` e `Liberação` possuem relação direta com o gate de qualidade, mas o contrato não permite presumir que a inspeção de qualidade esteja armazenada como uma simples etapa produtiva.

**Decisão necessária:** preservar a relação `ordem → etapa → evidência → inspeção/teste → liberação/retenção` usando as estruturas existentes.

### D-04 — Sequência documental × `sequence_no` / `etapa_seq`

Os campos de sequência existentes são candidatos à reconciliação, mas nenhum valor deve ser promovido a sequência padrão sem comprovar origem e vigência.

### D-05 — Tempos e capacidade

`standard_minutes` e `standard_qty_per_day` existem no modelo de `elo_prod_operation`, porém a documentação de processo determina que tempos e capacidade sejam obtidos de dados/documentos validados.

**Estado:** NÃO VALIDADO como padrão operacional até evidência específica.

## 5. Mapa de responsabilidades por estrutura

| Necessidade | Estrutura candidata | Tratamento |
|---|---|---|
| Definição da operação | `elo_prod_operation` | REUTILIZAR + validar semântica |
| Centro/recurso | `elo_prod_work_center` | REUTILIZAR + validar vínculo |
| Sequência PCP modular | `elo_pcp_fluxo_modular` | REUTILIZAR + reconciliar com operação |
| Etapa da ordem | `ordem_producao_etapa` | REUTILIZAR como estrutura transacional, após validação |
| Plano diário | `elo_prod_daily_plan` | REUTILIZAR |
| Evidência/evento | `elo_prod_flow_event` | REUTILIZAR |
| Qualidade/teste | estruturas existentes de inspeção/teste | REUTILIZAR; não duplicar gate |

## 6. Regras de compatibilidade

1. Um conceito canônico deve possuir um único proprietário semântico.
2. O catálogo documental não pode criar uma segunda tabela apenas para espelhar `ordem_producao_etapa`.
3. `elo_prod_operation`, `elo_pcp_fluxo_modular` e `ordem_producao_etapa` devem ser reconciliados por identificadores, sequência, produto, centro, estado e evidência antes de qualquer refatoração.
4. Divergência de nome não deve ser tratada como divergência semântica automática.
5. Divergência semântica deve possuir evidência ou decisão arbitrada.
6. Operações adicionais podem existir sem alterar as 17 etapas de referência, desde que seu papel seja comprovado.
7. Tempos, capacidade, produtividade, equipes e metas permanecem fora do padrão canônico enquanto não houver validação.
8. Produção customizada pode reutilizar etapas, mas não deve alterar silenciosamente o fluxo modular padrão.
9. Qualidade e reparo continuam sendo domínios relacionados, sem duplicação de autoridade.
10. Nenhuma alteração física de banco deve ocorrer nesta etapa apenas para fazer o modelo documental “caber”.

## 7. Evidência mínima para fechar o P03

Para transformar esta matriz de proposta em reconciliação validada, devem ser obtidos:

- lista completa das 21 operações com código, nome, sequência, produto e estado;
- lista completa dos 14 centros de trabalho e vínculos;
- registros de `elo_pcp_fluxo_modular` com produto, etapa, sequência e centro;
- estrutura e registros de `ordem_producao_etapa`;
- vínculo entre etapa e evidência/evento;
- vínculo entre etapa e qualidade/teste;
- origem e validade dos valores de `standard_minutes` e `standard_qty_per_day`;
- evidência operacional para `Estoque de estruturas` e `Movimentação` como etapa/evento/interface.

## 8. Gate P03

P03 só pode ser considerado **RECONCILIADO** quando:

```text
17 ETAPAS DOCUMENTADAS
        ↓
ESTRUTURAS FÍSICAS IDENTIFICADAS
        ↓
MAPEAMENTO 1:N / N:1 EXPLICADO
        ↓
DIVERGÊNCIAS REGISTRADAS
        ↓
ORIGEM/EVIDÊNCIA CONFIRMADA
        ↓
DECISÕES ARBITRADAS QUANDO NECESSÁRIO
        ↓
CONTRATO VALIDADO
```

Enquanto qualquer item obrigatório permanecer sem evidência, o estado é `A VALIDAR`.

## 9. Próxima sequência após P03

1. **P03.1 — Extrair snapshot físico completo** das estruturas existentes.
2. **P03.2 — Construir matriz real de correspondência** por código/nome/produto/sequência.
3. **P03.3 — Classificar 21 operações** em etapa principal, operação auxiliar, customização, reparo ou outro estado comprovado.
4. **P03.4 — Reconciliar `ordem_producao_etapa`** com o mapa.
5. **P03.5 — Validar tempos/capacidade separadamente.**
6. **P03.6 — Produzir evidência para Evolution Gate.**
7. Somente depois avaliar mudanças de Core, banco ou ELO Web.

## 10. Proibição explícita

Este contrato não autoriza:

- criar uma nova tabela de etapas;
- sobrescrever `ordem_producao_etapa`;
- alterar `elo_prod_operation`;
- promover tempos/capacidade a padrão;
- alterar a sequência física por inferência;
- criar uma segunda autoridade no ELO Web ou Supabase.
