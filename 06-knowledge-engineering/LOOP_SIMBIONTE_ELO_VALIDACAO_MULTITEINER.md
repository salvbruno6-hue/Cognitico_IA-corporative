# VALIDAÇÃO V0.1 — LOOP SIMBIÔNTE ELO / MULTITEINER

**Status:** CENÁRIO CONTROLADO — NÃO CONSOLIDADO  
**Base:** branch `feat/skill-planejamento-multiteiner`  
**Objetivo:** verificar a primeira passagem do loop usando a estrutura atualmente disponível no Supabase.

## 1. Evidência operacional observada

Na consulta realizada ao projeto Supabase `fxbpevjrkwhbicpmecow`:

- `fluxo_produtivo_modular`: 1 registro;
- `fluxo_produtivo_modular_etapas`: 17 registros;
- `elo_aprendizado_conceitos`: 2 registros;
- `elo_aprendizado_pcp_planejamento`: 1 registro;
- `elo_aprendizado_padroes_raciocinio`: 6 registros;
- `elo_aprendizado_experiencias`: 3 registros;
- `elo_evolution_events`: 0 registros.

O fluxo encontrado foi identificado como:

`Fluxo Produtivo Modular — Referência`

com 17 etapas e sem `modelo_id` ou `taxonomia_id` associados no registro consultado.

## 2. Passagem controlada

### PERCEPÇÃO

Entrada:

`FLUXO PRODUTIVO MODULAR`

### RETRIEVAL

Fontes relevantes:

- `fluxo_produtivo_modular`;
- `fluxo_produtivo_modular_etapas`;
- `elo_aprendizado_pcp_planejamento`;
- `elo_aprendizado_conceitos`;
- `MULTITEINER_ELO_PROCESS_DATA_DECISION_MAP.md`;
- `SKILL_PLANEJAMENTO_MULTITEINER.md`.

### CONFRONTAÇÃO

O ELO deve confrontar:

`DADO ATUAL × MAPA DE PROCESSO × SKILL VIGENTE × APRENDIZADO`

Não é permitido preencher ausência de `modelo_id`, `taxonomia_id`, capacidade, demanda, estoque, prazo ou resultado de execução por inferência.

### ANÁLISE

A evidência disponível permite confirmar a existência do fluxo e sua quantidade de etapas.

Não permite, isoladamente, concluir:

- capacidade produtiva;
- carga;
- utilização;
- gargalo;
- necessidade líquida;
- data de entrega;
- desempenho;
- resultado planejado × realizado.

Esses pontos devem permanecer como `NÃO LOCALIZADO` quando forem necessários ao raciocínio.

### DECISÃO

Para V0.1, a decisão de teste é:

`NÃO PROMOVER APRENDIZADO OPERACIONAL A PARTIR DESTA EVIDÊNCIA ISOLADA`

O objetivo do cenário é validar o caminho do loop, não produzir uma regra operacional nova.

### RESULTADO

Resultado observado:

`FLUXO EXISTENTE + 17 ETAPAS + CAMPOS DE MODELO/TAXONOMIA NÃO ASSOCIADOS`

Não há execução real suficiente no conjunto consultado para realizar `PLANEJADO × REALIZADO`.

### APRENDIZADO

Estado:

`CANDIDATO / NÃO CONSOLIDADO`

Aprendizado metodológico do teste:

> O loop deve ser capaz de parar a inferência quando a fonte operacional não contém as variáveis necessárias.

## 3. Critério de aprovação do cenário

O cenário será considerado estruturalmente aprovado somente se o teste conseguir demonstrar:

1. recuperação da fonte;
2. preservação da proveniência;
3. identificação das lacunas;
4. bloqueio de inferência indevida;
5. decisão explicitamente rastreável;
6. ausência de promoção automática;
7. retorno do resultado ao ciclo de aprendizado.

## 4. Limitação

Este cenário valida o **caminho cognitivo e a disciplina de evidência**.

Não valida ainda:

- execução automática ponta a ponta;
- atualização automática de Supabase;
- alteração automática de GitHub;
- comparação real planejado × realizado;
- promoção automática de conhecimento.

Portanto, o status permanece:

`V0.1 — EM VALIDAÇÃO`


## 5. Confrontação quantitativa controlada

Foi criado o teste `tests/validation/test_pcp_diagnose_confrontation.py` para confrontar, sobre os mesmos dados simulados do `elo-virtual-core`:

`diagnose() × kernel analítico da SKILL_PLANEJAMENTO_MULTITEINER`

### 5.1 Capacidade

Para `REC-001`:

- capacidade: 160 h;
- comprometido: 145 h;
- `DEM-001`: +20 h;
- `DEM-003`: +30 h.

A projeção do diagnóstico existente é:

- `DEM-001`: 165/160 = **1,03125**;
- `DEM-003`: 175/160 = **1,09375**.

O kernel PCP calcula, no agregado do recurso:

- carga: 195 h;
- capacidade: 160 h;
- `GARG = 195/160 = 1,21875`;
- recurso identificado: `REC-001`.

**Confrontação:** os dois mecanismos apontam para o mesmo recurso como restrição, mas operam em escopos diferentes: `diagnose()` sinaliza por demanda; `GARG` consolida a carga do recurso. Não devem ser tratados como fórmulas duplicadas.

### 5.2 Material

Para `MAT-003`:

- necessidade: 8;
- estoque disponível: 2;
- déficit bruto observado pelo diagnóstico: **6**.

Entretanto, o cálculo `NLM = NM - (EM - ESM)` exige `ESM) (estoque de segurança), inexistente no conjunto controlado.

Resultado do kernel:

`NLM = NÃO LOCALIZADO`

Isso demonstra o bloqueio de inferência previsto na Skill.

### 5.3 Atraso material

O diagnóstico existente calcula o atraso pelas datas:

- disponibilidade: 2026-09-08;
- necessidade: 2026-09-03;
- atraso calculado: **5 dias**.

A visão `v_elo_pcp_inteligente` apresenta `atraso_dias = 6` para `MAT-003`.

A divergência é registrada como evidência de confronto:

`CAMPO DERIVADO DO SUPABASE: 6 × CÁLCULO REPRODUZÍVEL PELAS DATAS: 5`

Não há base, neste ciclo, para declarar qual valor operacional deve prevalecer fora do escopo do cenário. O ponto deve permanecer aberto para validação da origem do campo `atraso_dias`.

### 5.4 Resultado do confronto

O cenário demonstrou:

1. reutilização do diagnóstico existente;
2. execução das fórmulas exclusivas do kernel PCP quando as variáveis existem;
3. bloqueio de `NLM` quando falta `ESM`;
4. identificação explícita de divergência entre fontes/camadas;
5. ausência de promoção automática.

O teste é **estruturalmente útil**, mas ainda não constitui validação operacional real.

## 6. Estado após a segunda passagem

`RETRIEVE → EVIDENCIAR → CONFRONTAR → EXECUTAR (CENÁRIO CONTROLADO) → OBSERVAR`

Próximo gate:

`VALIDAR → EVOLUTION GATE → REGISTRAR → EVOLUIR`

A passagem pelo `DecisionLifecycle → SymbiontSkillRuntime → SymbiontLabAdapter` ainda depende de uma observação de ciclo com estado `ATTRIBUTED` e evidência de execução compatível. O teste atual não deve fabricar esse estado.

## 7. Limitação atual

O cenário permanece simulado. As tabelas operacionais consultadas continuam sem registros:

- `mt_planos_pcp`: 0;
- `mt_ordens_producao`: 0;
- `mt_necessidades_materiais`: 0;
- `mt_capacidade_diaria`: 0.

Portanto, não se deve promover os resultados quantitativos acima para regra operacional consolidada.


## 8. Validação do Evolution Gate

Foi acrescentado um teste controlado que envia a evidência ao mecanismo existente `SymbiontLabAdapter → EvolutionGate`, sem criar uma nova via de aprendizado.

Como o proprietário canônico informado é:

`SKILL_PLANEJAMENTO_MULTITEINER`

o `EvolutionGate` classifica a proposta como:

`DUPLICATE/SUPERSEDED`

e o adaptador retorna:

`REUSE`

Sem:

- novo `ExperienceRecord`;
- novo `LearningCandidate`;
- mutação canônica;
- promoção.

Isso confirma, no cenário controlado, a regra de reutilização da capacidade já existente.

O teste foi registrado em:

`tests/validation/test_pcp_diagnose_confrontation.py`

O commit do teste é:

`8f14fad248b597c9a0b5ea44f9d122694af38ffc`

O workflow associado ainda não apresentou execução retornada pela integração no momento desta verificação; portanto, o teste não é declarado como executado em CI.
