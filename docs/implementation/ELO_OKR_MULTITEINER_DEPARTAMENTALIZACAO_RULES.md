---
id: ELO-OKR-MT-DEPT-001
name: ELO OKR Multiteiner — Departamentalização e Regras Organizacionais
type: governance-contract
layer: cognitive
owner: strategic-objective-domain + Multiteiner organizational context
status: proposed
authority: reference
version: 0.1
---

# ELO OKR — Departamentalização MULTITEINER

## 1. Finalidade

Integrar a estrutura organizacional real da MULTITEINER ao ELO OKR sem criar autoridade paralela, sem transformar etapas do processo em departamentos automaticamente e sem alterar o fluxo canônico congelado `03-process-library/MULTITEINER_END_TO_END_PROCESS_FLOW.md`.

Princípio: **REUTILIZAR → RELACIONAR → COMPLEMENTAR GAP → PRESERVAR HISTÓRICO → EVITAR DUPLICAÇÃO**.

## 2. Autoridades e estruturas existentes

- GitHub: autoridade operacional/canônica do ELO.
- ELO FORGE/Supabase: autoridade cognitiva/persistente.
- `mt_tenants`: identidade organizacional persistente.
- `mt_setores`: setores/responsabilidades organizacionais.
- `mt_centros_trabalho`: centros/células de trabalho, já relacionados a `mt_setores` por `setor_id`.
- `fluxo_produtivo_modular_etapas`: etapas/processos produtivos; não é cadastro de departamentos.
- `src/elo/contracts/okr.py`: contrato estratégico de Objective/KeyResult/Measurement.
- `mt_definicoes_kpi`: autoridade formal de KPI referenciada pelo contrato OKR.

## 3. Regra de classificação

O ELO deve distinguir obrigatoriamente:

1. **SETOR** — unidade de responsabilidade organizacional.
2. **CENTRO DE TRABALHO / CÉLULA** — unidade operacional/capacidade vinculável a setor.
3. **PROCESSO** — fluxo de transformação transversal.
4. **ETAPA / ATIVIDADE** — execução dentro do processo.
5. **PAPEL** — responsabilidade de pessoa/função.
6. **RECURSO** — capacidade/equipamento/mão de obra/material.
7. **REGRA / GATE** — condição que governa decisão ou passagem.
8. **KPI** — medição formal.
9. **OKR** — direcionamento estratégico.

Nenhum nome presente em uma etapa pode ser promovido automaticamente a SETOR.

## 4. Setores candidatos evidenciados

A classificação abaixo é uma proposta de estruturação a validar, baseada no contexto operacional informado e nas referências existentes do fluxo:

- DIRETORIA
- RH
- COMERCIAL / LICITAÇÃO
- PLANEJAMENTO / PCP
- COMPRAS
- ALMOXARIFADO
- PRODUÇÃO
- PINTURA
- MONTAGEM
- OFICINA DE CUSTOMIZADOS
- QUALIDADE
- EXPEDIÇÃO
- LOGÍSTICA

Possíveis centros/células produtivos, sujeitos à validação de vínculo organizacional:

- CORTE / DOBRA
- SOLDA
- FIBRA
- SERRALHERIA / PREPARAÇÃO
- FABRICAÇÃO DE ESQUADRIAS
- ESCOVAÇÃO / PREPARAÇÃO DE PINTURA
- INSTALAÇÕES ELÉTRICAS
- INSTALAÇÕES HIDRÁULICAS

A existência de uma atividade no fluxo não comprova, por si só, que ela seja um departamento ou centro de trabalho independente.

## 5. Regras organizacionais

Cada relação governada deve poder responder:

**QUEM → FAZ O QUÊ → RECEBE DE QUEM → ENTREGA PARA QUEM → SOB QUAL REGRA → COM QUAL AUTORIDADE → MEDIDO POR QUAL KPI → CONTRIBUI PARA QUAL OKR → COM QUAL EVIDÊNCIA.**

As regras devem preservar, quando aplicável:

- escopo;
- setor responsável;
- setores contribuintes;
- processo/etapa afetada;
- entrada;
- condição/gate;
- decisão;
- saída;
- dependências;
- autoridade de aprovação/bloqueio/priorização;
- tratamento de exceção;
- escalonamento;
- evidência;
- vigência;
- estado de validação.

## 6. Estados de governança de regra

### CANÔNICA
Regra formalmente aprovada/normativa. Pode governar decisão dentro dos limites de sua autoridade.

### OPERACIONAL
Comportamento atual observado e sustentado por evidência. Não altera automaticamente o cânone.

### PROPOSTA
Hipótese/recomendação aguardando validação humana.

Regra obrigatória:

`OPERACIONAL != CANÔNICA`

Uma regra operacional nunca se autopromove a canônica.

## 7. Handoff e responsabilidade

Cada handoff relevante deve identificar origem, destino, objeto transferido, condição de liberação, evidência e exceção.

Exemplo lógico:

`COMERCIAL/LICITAÇÃO → AF/DEMANDA → PCP → PLANO/LIBERAÇÃO → PRODUÇÃO → QUALIDADE → EXPEDIÇÃO/LOGÍSTICA`

O handoff não substitui o fluxo canônico; ele explicita responsabilidade organizacional sobre o fluxo.

## 8. Integração com ELO OKR

Relação cognitiva alvo:

`ESTRATÉGIA → OBJECTIVE → KEY RESULT → KPI → SETOR RESPONSÁVEL → PROCESSO → CENTRO DE TRABALHO → ETAPA/ATIVIDADE → REGRA/GATE → EVIDÊNCIA → RESULTADO → APRENDIZADO`

Relações laterais devem permitir setores contribuintes, dependências e handoffs.

### Regra de causalidade

`OWNER DO OKR != CAUSA AUTOMÁTICA DO DESVIO`

O owner responde pelo acompanhamento/governança do objetivo, mas a causalidade de um desvio exige investigação baseada em evidências da cadeia de dependências.

## 9. Proteção do fluxo canônico

O arquivo `03-process-library/MULTITEINER_END_TO_END_PROCESS_FLOW.md` permanece congelado por decisão de governança do responsável.

Esta integração pode consultar, relacionar, comparar e detectar GAPs/desvios, mas não pode alterar, corrigir ou sobrescrever o fluxo canônico sem autorização explícita.

Quando processo documentado divergir do observado:

`PROCESSO DOCUMENTADO != PROCESSO OBSERVADO → DESVIO DE PROCESSO / GAP PARA VALIDAÇÃO`

## 10. Persistência

Não criar tabela paralela de departamentos.

Reutilizar `mt_setores` para responsabilidade organizacional e `mt_centros_trabalho` para centros/células quando a classificação estiver validada.

Não preencher automaticamente `fluxo_produtivo_modular_etapas.setor` apenas por similaridade textual. O relacionamento exige validação organizacional e rastreabilidade.

## 11. Evolution Gate

Antes de promover esta proposta para baseline/implemented:

1. validar classificação SETOR vs CENTRO vs PROCESSO/ETAPA;
2. validar nomes e códigos organizacionais MULTITEINER;
3. confirmar relacionamentos com o tenant canônico MULTITEINER no ELO FORGE;
4. verificar ausência de estruturas equivalentes/duplicadas;
5. testar integridade de FK e unicidade;
6. validar integração OKR/KPI/evidência;
7. registrar GAPs e contradições;
8. obter decisão humana para promoção de regras propostas/canônicas.
