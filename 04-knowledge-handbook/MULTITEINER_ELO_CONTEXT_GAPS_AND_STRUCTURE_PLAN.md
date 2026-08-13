# MULTITEINER — ELO CONTEXT GAP ANALYSIS & STRUCTURE PLAN

**Status:** PROPOSED / REFERENCE  
**Purpose:** orientar o ELO a analisar o contexto organizacional da Multiteiner de ponta a ponta, identificar lacunas de conhecimento e produzir um plano de estruturação governado.  
**Parent context:** `MULTITEINER_ORGANIZATIONAL_CONTEXT.md`

---

## 1. Objetivo

Este documento não descreve novamente a empresa. Ele define **como o ELO deve analisar o contexto Multiteiner** depois de carregar o contexto organizacional.

O ELO deve passar de:

`CONHECER A EMPRESA`

para:

`ENTENDER RELAÇÕES → IDENTIFICAR LACUNAS → INVESTIGAR → PRIORIZAR → RECOMENDAR → ESTRUTURAR → APRENDER`.

Nenhuma lacuna deve ser preenchida por invenção. Quando a informação não estiver disponível, o ELO deve registrar `INFORMATION GAP` e formular perguntas objetivas.

---

## 2. Fonte de contexto

A fonte primária é:

`04-knowledge-handbook/MULTITEINER_ORGANIZATIONAL_CONTEXT.md`

O contexto deve ser relacionado, quando pertinente, aos artefatos canônicos do ELO sobre:

- arquitetura;
- domínios;
- entidades;
- relacionamentos;
- regras de negócio;
- processos;
- conhecimento;
- memória;
- evidência;
- reasoning;
- decision support;
- provenance;
- agents;
- integration;
- governance.

Antes de propor novos artefatos, classificar a necessidade como:

`REUSE | EXTEND | NEW | ROADMAP | DUPLICATE | CONFLICT`.

---

## 3. Pergunta central do ELO

> **O que o ELO ainda precisa conhecer, medir, relacionar ou validar para conseguir compreender a operação Multiteiner de ponta a ponta e apoiar decisões com segurança?**

---

## 4. Modelo de análise ponta a ponta

O ELO deve reconstruir e testar a cadeia:

```text
COMERCIAL
  ↓
ENGENHARIA / PROJETOS
  ↓
ORÇAMENTO
  ↓
PCP
  ↓
COMPRAS
  ↓
ALMOXARIFADO
  ↓
PRODUÇÃO
  ↓
OFICINAS / APOIO INDUSTRIAL
  ↓
LOGÍSTICA INTERNA
  ↓
EXPEDIÇÃO
  ↓
CLIENTE / LOCAÇÃO
  ↓
RETORNO
  ↓
RECEBIMENTO / INSPEÇÃO
  ↓
AVARIAS / REPARO / REPROCESSO
  ↓
ESTOQUE
  ↓
NOVA EXPEDIÇÃO
```

Para cada transição, verificar:

- entrada;
- saída;
- responsável;
- informação necessária;
- sistema de registro;
- decisão;
- dependência;
- recurso;
- indicador;
- risco;
- exceção;
- evidência disponível.

---

## 5. Mapa mínimo de entidades

O ELO deve identificar e relacionar, no mínimo:

### Pessoas

- diretoria;
- gestores;
- líderes;
- analistas;
- operadores;
- responsáveis técnicos;
- fornecedores;
- clientes;
- transportadores.

### Operacionais

- módulo;
- container;
- projeto;
- SO;
- AF;
- contrato;
- pedido;
- material;
- BOM/LM;
- excedente;
- equipamento;
- ferramenta;
- estoque;
- lote;
- avaria;
- reparo;
- expedição;
- locação;
- retorno.

### Gestão

- meta;
- KPI;
- risco;
- decisão;
- prioridade;
- exceção;
- plano;
- capacidade;
- restrição;
- incidente;
- ação corretiva;
- lição aprendida.

---

## 6. Mapa de relações

O ELO deve procurar relações como:

```text
CLIENTE → CONTRATO → AF → PROJETO → SO
SO → BOM/LM → ALMOXARIFADO → COMPRAS
SO → PCP → CAPACIDADE → SEQUENCIAMENTO → PRODUÇÃO
PRODUÇÃO → QUALIDADE → EXPEDIÇÃO
EXPEDIÇÃO → LOCAÇÃO → CAMPO → RETORNO
RETORNO → INSPEÇÃO → AVARIA → REPARO → ESTOQUE
```

Também deve identificar relações transversais:

```text
DECISÃO → RESPONSÁVEL
DECISÃO → EVIDÊNCIA
DECISÃO → RISCO
DECISÃO → RESULTADO
RESULTADO → APRENDIZAGEM
APRENDIZAGEM → REGRA / PADRÃO
```

---

## 7. Análise por setor

Para cada setor, o ELO deve responder:

1. Qual é a finalidade do setor?
2. Quais são suas entradas?
3. Quais são suas saídas?
4. Quem fornece a entrada?
5. Quem recebe a saída?
6. Quais decisões são tomadas?
7. Quais informações sustentam essas decisões?
8. Onde a informação é registrada?
9. Quais recursos são críticos?
10. Quais são os gargalos conhecidos?
11. Quais indicadores existem?
12. Quais indicadores deveriam existir?
13. Quais exceções ocorrem?
14. Quais riscos dependem de outros setores?
15. Quais dados estão ausentes?
16. Quais atividades ainda dependem de conhecimento informal?
17. Quais oportunidades de automação existem?
18. Qual decisão permanece necessariamente humana?

---

# 8. Dimensões específicas de análise

## 8.1 Comercial

Investigar:

- origem da demanda;
- AF;
- venda x locação;
- padrão x personalizado;
- escopo;
- prazo prometido;
- condições comerciais;
- interface com engenharia e PCP;
- alterações após aprovação;
- exceções comerciais.

**Gaps prioritários a procurar:** origem formal da demanda, versão do escopo, histórico de alterações e autoridade para alterar prazo/escopo.

## 8.2 Engenharia / Projetos

Investigar:

- CAD;
- levantamento dimensional / As-Built;
- versão do projeto;
- aprovação;
- padrão x excedente;
- LM/BOM;
- componentes críticos;
- critérios de liberação.

**Gaps prioritários:** vínculo projeto → BOM → SO, versionamento, excedentes e rastreabilidade da aprovação.

## 8.3 PCP

Investigar:

- gate de SO;
- capacidade;
- carteira;
- sequenciamento;
- prioridades;
- planejamento semanal;
- gargalos;
- exceções;
- aderência;
- interface com diretoria.

**Gaps prioritários:** capacidade real por recurso, tempos padrão, regras de prioridade e histórico planejado x realizado.

## 8.4 Compras

Investigar:

- demanda recebida;
- cotação;
- pedido;
- lead time;
- fornecedor;
- material crítico;
- follow-up;
- atrasos;
- compras emergenciais.

**Gaps prioritários:** lead time confiável, fornecedores críticos, causas de compras emergenciais e vínculo com SO/LM.

## 8.5 Almoxarifado

Investigar:

- recebimento;
- conferência;
- endereço;
- estoque;
- picking;
- requisição;
- devolução;
- inventário;
- rastreabilidade.

**Gaps prioritários:** acuracidade de estoque, estoque disponível real, localização, reservas e consumo por obra.

## 8.6 Produção

Investigar o fluxo físico e os recursos de:

- triagem;
- chassi;
- escovação;
- pintura de tratamento;
- acabamento branco;
- estoque de estruturas;
- piso;
- teto;
- colunas;
- trilho;
- pintura modular;
- paredes;
- instalações;
- acabamento;
- testes;
- liberação.

**Gaps prioritários:** tempos por etapa, capacidade por recurso, WIP, gargalos, retrabalho e motivos de parada.

## 8.7 Oficinas e apoio industrial

Investigar:

- corte e dobra;
- solda;
- serralheria;
- reparo;
- manutenção;
- pintura;
- escovação;
- oficinas especializadas;
- recursos compartilhados.

**Gaps prioritários:** capacidade compartilhada, fila de serviços, manutenção preventiva, disponibilidade de equipamentos e tempos de setup.

## 8.8 Logística interna

Investigar:

- empilhadeiras;
- pórticos;
- trilhos;
- rotas;
- movimentação;
- pátio;
- segurança.

**Gaps prioritários:** tempos de movimentação, utilização, conflitos de rota, disponibilidade, custo e dependência de equipamentos.

## 8.9 Expedição

Investigar:

- identificação;
- checklist;
- NF;
- conformidade;
- sistema Najason;
- carregamento;
- motorista;
- liberação.

**Gaps prioritários:** critérios de liberação, vínculo equipamento/NF/cliente, tempo de carregamento e ocorrências.

## 8.10 Locação / Campo

Investigar:

- transporte;
- montagem;
- uso;
- manutenção;
- ocorrências;
- desmobilização;
- retorno.

**Gaps prioritários:** condição do ativo no campo, histórico de manutenção, eventos e vínculo com contrato.

## 8.11 Pós-locação / Avarias

Investigar:

- aviso;
- NF;
- descarregamento;
- vistoria;
- avaria;
- quarentena;
- oficina;
- liberação ao estoque.

Para cada avaria, procurar separar:

`MATERIAL + MÃO DE OBRA + MOVIMENTAÇÃO`.

**Gaps prioritários:** padrão de classificação, evidência, custo, tempo, movimentação, causa e histórico.

---

# 9. Information Gap Framework

Quando uma informação necessária não existir, criar registro:

```yaml
information_gap:
  gap_id:
  domain:
  process:
  missing_information:
  why_needed:
  impact_if_missing:
  likely_owner:
  likely_source:
  priority:
  status:
  confidence:
  provenance:
```

### Classificação de prioridade

**P0 — crítico:** impede decisão ou pode gerar risco grave.  
**P1 — alto:** compromete planejamento ou execução.  
**P2 — médio:** reduz eficiência ou qualidade da análise.  
**P3 — baixo:** melhoria futura.

---

# 10. Clarification Questions

O ELO deve transformar gaps relevantes em perguntas direcionadas.

Formato:

```yaml
clarification_question:
  question_id:
  gap_id:
  question:
  intended_decision:
  owner:
  priority:
  expected_evidence:
```

Perguntas devem ser curtas, verificáveis e vinculadas a uma necessidade concreta.

---

# 11. Diagnóstico de maturidade

Avaliar cada domínio em cinco dimensões:

| Dimensão | Pergunta |
|---|---|
| Processo | Existe fluxo definido? |
| Informação | A informação é registrada? |
| Medição | Existe indicador confiável? |
| Governança | Existe responsável/autoridade? |
| Integração | O dado conversa com outros processos? |

Classificar:

`0 — inexistente`  
`1 — informal`  
`2 — parcialmente estruturado`  
`3 — estruturado`  
`4 — integrado`  
`5 — adaptativo/aprendente`.

Não atribuir nota sem evidência suficiente. Quando não houver dados, usar `NÃO AVALIADO`.

---

# 12. Priorização da estruturação

O ELO deve considerar:

```text
IMPACTO
+ URGÊNCIA
+ RISCO
+ DEPENDÊNCIAS
+ FREQUÊNCIA
+ ESFORÇO DE IMPLEMENTAÇÃO
+ VALOR PARA DECISÃO
```

O resultado deve separar:

### Quick Wins
Baixo esforço / alto impacto.

### Estruturantes
Necessários para organizar o sistema.

### Integrações
Dependem de sistemas ou dados.

### Governança
Dependem de regras, autoridade ou aprovação.

### Roadmap
Importantes, porém não prioritários no ciclo atual.

---

# 13. Plano de estruturação esperado

O ELO deve produzir um plano com:

| Prioridade | Problema | Evidência | Gap | Ação | Owner | Dependência | Indicador | Horizonte |
|---|---|---|---|---|---|---|---|---|

O plano não deve presumir que toda solução seja software.

Possíveis ações:

- padronização;
- treinamento;
- documento;
- indicador;
- coleta de dados;
- integração;
- automação;
- mudança de processo;
- mudança de governança;
- experimento controlado;
- decisão gerencial.

---

# 14. Casos de análise obrigatórios

O ELO deve testar seu entendimento usando pelo menos:

### Caso A — Falta de material

`SO → LM → estoque → compra → lead time → produção → impacto no prazo`.

Deve identificar onde a informação pode se perder.

### Caso B — Conflito de prioridade

`Comercial solicita urgência → PCP avalia capacidade → Produção/Almoxarifado/Compras são impactados → decisão humana`.

O ELO deve mostrar consequências antes de recomendar alteração.

### Caso C — Avaria pós-locação

`Retorno → vistoria → avaria → material + HH + movimentação → orçamento → reparo → estoque`.

Deve separar fato, custo, hipótese de causa e decisão.

### Caso D — Gargalo produtivo

`Demanda → capacidade → etapa restritiva → fila/WIP → impacto no lead time → alternativas`.

Não assumir que aumentar uma etapa isolada aumenta o throughput total.

---

# 15. Resultado esperado do ELO

Depois de processar o contexto, o ELO deve ser capaz de produzir quatro níveis de saída:

## Nível 1 — Mapa

"Como a Multiteiner funciona."

## Nível 2 — Diagnóstico

"Onde existem lacunas, riscos, dependências e gargalos."

## Nível 3 — Recomendação

"O que deveria ser estruturado primeiro e por quê."

## Nível 4 — Plano adaptativo

"Como acompanhar a implementação, medir resultado e replanejar quando a realidade mudar."

---

# 16. Limites de inferência

O ELO NÃO deve:

- inventar capacidade produtiva;
- inventar tempos;
- inventar estoque;
- inventar custos;
- atribuir culpa a pessoas sem evidência;
- interpretar opinião como regra;
- tratar hipótese como fato;
- assumir que um processo informal é inexistente;
- criar um novo Engine apenas porque surgiu uma nova necessidade;
- alterar arquitetura canônica sem governança;
- recomendar ação irreversível sem autoridade humana apropriada.

Quando faltar evidência:

`INFORMATION GAP → QUESTION → EVIDENCE → UPDATE`.

---

# 17. Provenance

Toda conclusão relevante deve permitir rastrear:

`CONCLUSÃO → EVIDÊNCIA → FONTE → DATA → CONTEXTO → RESPONSÁVEL`.

Separar:

- fato;
- dado;
- inferência;
- hipótese;
- simulação;
- recomendação;
- decisão humana.

---

# 18. Saída final recomendada

A primeira análise completa do ELO deve gerar um relatório estruturado com:

1. **Mapa executivo da Multiteiner**
2. **Mapa end-to-end**
3. **Mapa por setor**
4. **Mapa de entidades**
5. **Mapa de relações**
6. **Mapa de decisões**
7. **Mapa de riscos**
8. **Mapa de indicadores**
9. **Information Gaps**
10. **Clarification Questions**
11. **Diagnóstico de maturidade**
12. **Quick Wins**
13. **Prioridades estruturantes**
14. **Dependências**
15. **Roadmap sugerido**
16. **Pontos que exigem decisão humana**
17. **Hipóteses ainda não validadas**
18. **Próximo ciclo de coleta de evidências**

---

# 19. Regra de evolução

Este documento deve ser tratado como **estrutura de análise**, não como verdade definitiva sobre a operação.

À medida que o ELO receber evidências da Multiteiner:

```text
CONTEXTO
→ EVIDÊNCIA
→ ATUALIZAÇÃO DO MODELO
→ NOVAS RELAÇÕES
→ NOVOS GAPS
→ NOVAS PRIORIDADES
→ NOVO PLANO
→ RESULTADO
→ APRENDIZAGEM
```

O objetivo final é que o ELO consiga acompanhar a evolução da empresa sem congelar o modelo organizacional em uma fotografia estática.

---

# 20. Definition of Done

A análise será considerada inicializada quando:

- [ ] Contexto organizacional foi carregado.
- [ ] Cadeia end-to-end foi reconstruída.
- [ ] Setores foram mapeados.
- [ ] Entidades foram identificadas.
- [ ] Relações principais foram identificadas.
- [ ] Decisões críticas foram identificadas.
- [ ] Dependências foram identificadas.
- [ ] Gaps foram registrados.
- [ ] Perguntas foram geradas para gaps relevantes.
- [ ] Evidências disponíveis foram classificadas.
- [ ] Hipóteses foram separadas de fatos.
- [ ] Riscos foram classificados.
- [ ] Indicadores existentes foram identificados.
- [ ] Indicadores ausentes relevantes foram apontados.
- [ ] Maturidade foi avaliada somente onde há evidência.
- [ ] Quick Wins foram separados de iniciativas estruturantes.
- [ ] Dependências de implementação foram registradas.
- [ ] Human-in-the-loop foi preservado.
- [ ] Provenance foi preservada.
- [ ] Nenhuma nova capacidade arquitetural foi criada sem classificação REUSE/EXTEND/NEW/ROADMAP/DUPLICATE/CONFLICT.
- [ ] O primeiro plano de estruturação foi produzido.

---

## Regra final

> **O ELO não deve simplesmente receber o contexto da Multiteiner. Deve construir, a partir dele, uma representação verificável de como a empresa funciona, descobrir o que ainda não sabe, buscar as evidências necessárias e transformar esse conhecimento em prioridades de estruturação governadas.**
