# ELO Forge Knowledge Promotion Protocol

**Status:** PROPOSED FOR VALIDATION  
**Issue:** #101 / ELO-014  
**Purpose:** definir como o ELO observa conhecimento já existente no Forge e incorpora somente o que é necessário, preservando independência, proveniência, versionamento e capacidade de remoção.

## 1. Princípio

O Forge é fonte de conhecimento e histórico. Não é o Cognitive Core.

O ELO deve:

`OBSERVE → CLASSIFY → COMPARE → EVIDENCE → DECIDE → PROMOTE/REUSE/EXTEND/REJECT/ROADMAP → TRACE`

Ler uma fonte não significa aprender. Aprender não significa promover a informação a conhecimento canônico.

## 2. Fonte de referência analisada

`04-knowledge-handbook/MULTITEINER_ORGANIZATIONAL_CONTEXT.md`

Método de análise:

`04-knowledge-handbook/MULTITEINER_ELO_CONTEXT_GAPS_AND_STRUCTURE_PLAN.md`

A fonte de contexto descreve fluxo end-to-end, setores, entidades, relações, riscos, KPIs, casos históricos e governança. O plano de análise exige que lacunas sejam explicitamente registradas e que nenhuma informação ausente seja inventada.

## 3. Classificação obrigatória

| Classe | Tratamento |
|---|---|
| REUSE | capacidade já existente no ELO; apenas registrar a referência/proveniência |
| EXTEND | conhecimento complementar que pode ampliar uma capacidade existente |
| NEW | capacidade/conhecimento ainda inexistente e relevante |
| ROADMAP | relevante, mas não necessário no ciclo atual |
| DUPLICATE | semanticamente já coberto; não incorporar novamente |
| CONFLICT | diverge de conhecimento canônico ou de outra fonte; não promover automaticamente |

## 4. O que foi selecionado da fonte atual

### REUSE — fluxo corporativo

A cadeia end-to-end já coincide com a capacidade sistêmica corporativa do ELO:

`COMERCIAL → ENGENHARIA → ORÇAMENTO → PCP → COMPRAS → ALMOXARIFADO → PRODUÇÃO → EXPEDIÇÃO → CLIENTE/LOCAÇÃO → RETORNO → RECEBIMENTO → INSPEÇÃO → REPARO/REPROCESSO → ESTOQUE → NOVA EXPEDIÇÃO`

Não duplicar esta cadeia em outro modelo canônico.

### REUSE — entidades corporativas

Reaproveitar como referências de domínio, sem promover automaticamente todos os nomes como entidades canônicas: `AF`, `SO`, `projeto`, `contrato`, `BOM/LM`, `material`, `estoque`, `pedido`, `equipamento`, `expedição`, `locação`, `retorno`, `avaria`, `reparo`, `risco`, `restrição`, `decisão`, `KPI`, `evidência`, `experiência` e `aprendizado`.

### EXTEND — faculdade lógica corporativa

A fonte fornece mecânicas úteis para enriquecer a faculdade lógica do ELO:

- Comercial: demanda, escopo, modalidade, prazo e alterações;
- Engenharia: versão, BOM/LM, aprovação e liberação técnica;
- PCP: capacidade, sequenciamento, prioridade, planejamento e desvio;
- Compras: demanda, cotação, pedido, lead time e material crítico;
- Produção: etapas, capacidade, WIP, gargalos, retrabalho e liberação;
- Logística/Expedição: movimentação, conformidade, carregamento e liberação;
- Pós-locação: retorno, inspeção, avaria, reparo e liberação ao estoque.

Esses elementos devem ser tratados como candidatos à faculdade lógica porque descrevem relações e decisões recorrentes, não apenas documentos isolados.

### EXTEND — knowledge-gap framework

Promover como padrão metodológico do ELO o registro estruturado de `INFORMATION GAP`, pergunta de esclarecimento, prioridade, proprietário provável, fonte provável, impacto e proveniência.

### EXTEND — decisão baseada em evidência

Reforçar a separação:

`FATO → EVIDÊNCIA → HIPÓTESE → ANÁLISE → RECOMENDAÇÃO → DECISÃO`

Nenhuma regra operacional deve ser promovida apenas porque aparece em um documento contextual.

### ROADMAP — indicadores e casos históricos

KPIs, gargalo de pintura, componentes críticos, reprogramações, BOM e crescimento comercial são conhecimento útil para análise e testes, mas não devem virar regra universal sem validação adicional.

### ROADMAP — sistemas e ferramentas

`Najason`, `CAD`, planilhas e outros sistemas são fontes/integrações potenciais. Não devem ser incorporados como dependências do Core.

## 5. Overlay removível

Conhecimento específico de uma implementação deve ser representado como overlay com:

- `source_id`
- `source_version`
- `domain`
- `scope`
- `valid_from`
- `valid_until`
- `confidence`
- `evidence_refs`
- `status`

A remoção do membro ou da fonte deve remover o overlay somente quando governado, sem remover conhecimento promovido e validado do ELO.

## 6. Promoção para faculdade

Uma informação só pode ser promovida quando:

1. possui proveniência;
2. possui contexto e escopo;
3. não é duplicação conhecida;
4. não possui conflito aberto não resolvido;
5. possui evidência suficiente para o nível de confiança declarado;
6. representa padrão/mecânica relevante, e não apenas detalhe local;
7. passou pelo gate de evolução aplicável.

## 7. Detach test

Após promoção válida, a fonte original deve poder ser desconectada em teste sem corromper o Core.

Resultado esperado:

`fonte removida → conhecimento promovido permanece → overlay específico pode desaparecer → proveniência permanece → Core íntegro`.

## 8. Não permitido

- copiar o Forge inteiro para a memória do ELO;
- duplicar entidades canônicas sem comparação;
- transformar documento em regra automaticamente;
- preencher gaps por inferência apresentada como fato;
- fazer o Core depender do sistema de origem;
- apagar histórico válido apenas porque surgiu uma nova versão;
- promover conflito como verdade única sem decisão governada.

## 9. Critério de aceite

ELO-014 só pode ser promovido quando houver evidência de:

- classificação determinística dos candidatos;
- ausência de duplicação nos itens REUSE;
- proveniência dos itens promovidos;
- distinção entre faculdade e overlay;
- conflito bloqueando promoção automática;
- detach sem corrupção do conhecimento promovido;
- CI verde no commit final;
- Evolution Gate aprovado.
