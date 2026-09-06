# ELO — PTS Pós-Orçamento: Análise de Competitividade

**Status:** Proposta implementável / camada operacional
**Domínio:** Análise de Solicitações → Orçamento → PTS Pós
**Autoridade:** ELO governa e audita; Especialista de Orçamento executa; decisão permanece com responsável competente.

## 1. Finalidade

Transformar a PTS Pós-Orçamento em uma camada de análise de competitividade capaz de identificar, priorizar e simular itens cujo valor possa ser discutido para aumentar a competitividade de uma proposta, sem reduzir automaticamente requisitos técnicos, viabilidade, margem ou controles de risco.

A Curva ABC é instrumento de priorização econômica, não autorização de redução.

## 2. Fluxo

`ORÇAMENTO → COMPOSIÇÃO → ABC → CONHECIMENTO/EVIDÊNCIA → VALOR → FLEXIBILIDADE → RISCO → OPORTUNIDADE → CENÁRIOS → DECISÃO → PTS PÓS → RESULTADO → APRENDIZADO`

## 3. Entradas canônicas

- orçamento e composição;
- PTS Técnica;
- Lista-Mãe e taxonomia;
- modelos e composições;
- excedentes e Nome Material;
- memória de cálculo;
- cálculos aprendidos e evidências;
- conhecimento aplicável;
- decisões arbitradas;
- resultado da licitação, quando disponível.

Não criar uma segunda memória ou uma segunda metodologia de orçamento.

## 4. Curva ABC

Para cada item relevante:

`peso = valor_item / valor_total_orcamento`

Ordenar por valor decrescente e calcular percentual acumulado. A classificação A/B/C deve usar limites parametrizáveis e não deve ser confundida com criticidade técnica.

- ABC A: maior concentração econômica;
- ABC B: concentração intermediária;
- ABC C: menor concentração econômica.

A classificação serve para definir prioridade de análise.

## 5. Análise semântica do item

Cada item deve ser rastreável, quando aplicável, por:

`DOCUMENTO → REQUISITO → SOLUÇÃO → MODELO → QUANTIDADE → EXCEDENTE → COMPOSIÇÃO → VALOR → PREMISSA → EVIDÊNCIA`

Para excedentes, preservar a camada:

`EXCEDENTE → CATEGORIA → NOME MATERIAL → QUANTIDADE → VALOR UNITÁRIO → VALOR TOTAL → COMPOSIÇÃO → FONTE → MEMÓRIA DE CÁLCULO`

## 6. Estados de análise

### Conhecimento

`FORTE | MEDIO | FRACO | AUSENTE | CONFLITANTE`

### Flexibilidade

`ALTA | MEDIA | BAIXA | INDETERMINADA`

### Risco

`BAIXO | MEDIO | ALTO | CRITICO`

### Decisão

`MANTER | REVISAR | NEGOCIAR | SUBSTITUIR | REESTRUTURAR | CONFIRMAR | NAO_REDUZIR | AGUARDAR_DECISAO`

## 7. Oportunidade

Uma oportunidade só deve ser apresentada quando houver fundamento verificável. O ELO deve registrar:

- item e classe ABC;
- peso financeiro;
- origem do valor;
- memória de cálculo;
- conhecimento relacionado;
- evidências;
- possibilidade de alteração;
- impacto econômico;
- risco;
- recomendação;
- responsável pela decisão.

Ausência de evidência não autoriza redução. Conflito de conhecimento exige preservação de proveniência e arbitragem.

## 8. Cenários

### BASE

Preserva a composição original.

### COMPETITIVO

Aplica somente oportunidades sustentadas por evidência e viabilidade.

### MÁXIMO

Demonstra o limite das oportunidades tecnicamente possíveis, explicitando riscos e premissas. Não representa autorização de execução.

Todo cenário deve informar valor total, variação absoluta, variação percentual, itens alterados, premissas alteradas e risco.

## 9. Regra de autoridade

O componente analítico não altera automaticamente orçamento, Lista-Mãe, conhecimento canônico ou regras do ELO.

`ANÁLISE → RECOMENDAÇÃO → ARBITRAGEM → DECISÃO`

Aprendizado somente após avaliação governada.

## 10. Integração com PTS Pós

A PTS Pós deve apresentar, além da comprovação de atendimento:

1. Curva ABC;
2. itens Classe A prioritários;
3. concentração de excedentes;
4. análise de evidências;
5. oportunidades de competitividade;
6. riscos e proteções;
7. cenários;
8. decisões pendentes;
9. resultado e aprendizado quando disponíveis.

## 11. Regra de não manipulação

A camada serve à análise interna de competitividade e revisão fundamentada de composição. Não deve fabricar, distorcer ou selecionar artificialmente referências de mercado para produzir um preço desejado. Toda referência deve manter fonte, premissa, condição de comparação e memória de cálculo.

## 12. Critério de conclusão

A análise está completa quando cada oportunidade relevante puder responder:

`O QUE → QUANTO → POR QUÊ → COM QUAL EVIDÊNCIA → QUAL IMPACTO → QUAL RISCO → QUEM DECIDE → QUAL RESULTADO`
