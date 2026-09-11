# PTS Técnica Pós-Orçamento — Estrutura Padrão do ELO

**Versão:** 2.0  
**Status:** Proposta para incorporação como padrão oficial  
**Responsável:** ELO

## 1. Finalidade

A PTS Técnica Pós-Orçamento comprova a aderência entre o Termo de Referência, demais documentos da solicitação e a composição orçamentária efetivamente elaborada.

Seu objetivo é permitir reconstruir o raciocínio técnico e econômico utilizado no orçamento, preservando rastreabilidade entre requisito, interpretação, solução, quantitativo, composição, orçamento, premissa, justificativa, risco, pendência e validação.

A PTS Pós não deve apenas repetir a PTS Técnica. Ela deve demonstrar o que efetivamente foi precificado, confrontar a previsão técnica com a composição final e identificar divergências, ausências, contradições, equivalências, excedentes e oportunidades de revisão quando houver evidência suficiente.

## 2. Estrutura obrigatória

A PTS Pós-Orçamento deve seguir, quando aplicável, esta sequência:

1. Identificação da Solicitação;
2. Objetivo;
3. Escopo Técnico;
4. Matriz de Rastreabilidade Técnica e Orçamentária;
5. Memórias de Cálculo;
6. Análise Geral da Composição Orçamentária;
7. Comparação entre Orçamentos e Composições;
8. Análise de Contradições, Ausências e Divergências;
9. Análise de Competitividade;
10. Resumo Executivo;
11. Parecer Técnico;
12. Parecer de Competitividade;
13. Legenda e Critérios de Classificação;
14. Registro de Aprendizado.

## 3. Matriz de Rastreabilidade Técnica e Orçamentária

A matriz deve conter, no mínimo:

| Campo | Finalidade |
|---|---|
| Nº | Identificação sequencial do item analisado |
| Tópico / Item | Sistema, serviço, material ou requisito analisado |
| REFERÊNCIA TR / DOCUMENTO | Origem exata da exigência: TR, página, anexo, figura, esclarecimento, SO, layout ou resposta |
| Requisito / Descrição da SO | O que efetivamente deve ser atendido |
| Solução Técnica Proposta | Solução utilizada na composição |
| Quantitativo | Quantidade adotada |
| Unid. | Unidade de medição |
| Composição / Escopo | Materiais, serviços e mão de obra envolvidos |
| Premissa / Critério | Hipótese, método ou critério utilizado para chegar ao quantitativo/custo |
| Referência do Orçamento | Item, código ou seção da planilha onde o requisito foi precificado |
| Valor | Valor correspondente, quando aplicável |
| Inclusão no Orçamento | Sim / Não / Parcial |
| Atendimento | AI / AE / AP / NA |
| Observação / Pendência | Divergência, risco, validação ou condição |

A referência da exigência e a referência do orçamento devem permanecer separadas. Isso permite detectar quando um requisito existe na documentação, mas não possui correspondente na planilha.

## 4. Raciocínio obrigatório de cada item

Cada item relevante deve permitir reconstruir:

**REQUISITO → INTERPRETAÇÃO → SOLUÇÃO → QUANTITATIVO → COMPOSIÇÃO → ORÇAMENTO → PREMISSA → JUSTIFICATIVA → RISCO/PENDÊNCIA → VALIDAÇÃO**

Quando alguma etapa não estiver comprovada, registrar explicitamente a ausência de evidência.

Não preencher lacunas por inferência silenciosa.

## 5. Memórias de Cálculo

Toda memória de cálculo relevante utilizada na formação do orçamento deve ser registrada individualmente.

### 5.1 Tabela padrão de memória de cálculo

| ID MC | Tópico / Item | Referência TR / Documento | Premissa | Fórmula / Desenvolvimento | Quantidade Calculada | Unidade | Material / Serviço | Quantidade Orçada | Valor Unitário | Valor Parcial | Fonte | Composição | Justificativa | Divergência | Status |
|---|---|---|---|---|---:|---|---|---:|---:|---:|---|---|---|---|---|

### 5.2 Desenvolvimento da memória

A memória deve apresentar, quando aplicável:

- dimensões de referência;
- geometria;
- perímetro;
- área;
- volume;
- quantidade de peças;
- comprimento por peça;
- fator de perda;
- consumo unitário;
- produtividade;
- número de profissionais;
- dias ou horas de execução;
- materiais auxiliares;
- consumíveis;
- equipamentos;
- transporte/logística;
- fórmula utilizada;
- resultado matemático;
- quantidade efetivamente levada ao orçamento.

### 5.3 Controle da memória

A memória deve distinguir:

- **quantidade calculada**;
- **quantidade adotada**;
- **quantidade orçada**.

Se forem diferentes, a diferença deve ser explicada.

## 6. Classificação de atendimento

- **AI — Atendido Integralmente:** requisito plenamente contemplado.
- **AE — Atendido por Solução Equivalente:** solução diferente da referência original, mas tecnicamente equivalente, com justificativa.
- **AP — Atendido Parcialmente:** somente parte do requisito foi contemplada ou existe complementação pendente.
- **NA — Não Atendido:** requisito sem correspondente suficiente no orçamento.

A classificação não pode mascarar ausência de item.

## 7. Análise Geral da Composição Orçamentária

Após a matriz, consolidar a solução efetivamente orçada:

- produto/módulo base;
- adaptações;
- estrutura;
- arquitetura e acabamentos;
- elétrica;
- SPDA/aterramento;
- climatização;
- hidrossanitário;
- drenagem;
- dados;
- mobiliário;
- mão de obra;
- logística;
- projetos;
- documentação;
- comissionamento;
- demais componentes relevantes.

## 8. Comparação entre Orçamentos e Composições

Quando existirem dois ou mais orçamentos, versões, fornecedores ou composições para o mesmo escopo, executar comparação estruturada.

### 8.1 Matriz de comparação

| Item / Sistema | Orçamento A | Orçamento B | Diferença de Quantidade | Diferença de Preço | Diferença de Composição | Contradição | Item Ausente | Explicação | Conclusão |
|---|---|---|---:|---:|---|---|---|---|---|

A comparação deve verificar:

1. mesmos requisitos;
2. mesmos quantitativos;
3. mesmas unidades;
4. mesmos materiais;
5. mesma solução técnica;
6. componentes auxiliares;
7. mão de obra;
8. logística;
9. impostos/encargos quando comparáveis;
10. exclusões;
11. itens incorporados em verbas globais;
12. itens presentes em um orçamento e ausentes em outro.

Diferença de preço, isoladamente, não deve ser tratada como erro.

## 9. Análise de Contradições, Ausências e Divergências

Executar varredura específica procurando:

- requisito da TR sem item no orçamento;
- item do orçamento sem requisito identificável;
- quantitativo calculado diferente do orçado;
- unidade incompatível;
- composição incompleta;
- item duplicado;
- item necessário implicitamente para executar outro item, mas não identificado;
- preço sem fonte;
- composição com preço zerado;
- premissa incompatível com a geometria;
- conflito entre versões de orçamento;
- divergência entre PTS Técnica e orçamento;
- divergência entre orçamento e memória de cálculo;
- divergência entre fornecedores;
- solução equivalente sem justificativa;
- verba global sem conteúdo demonstrável.

### 9.1 Tabela de divergências

| ID | Origem | Item | Tipo de Divergência | Evidência | Impacto Técnico | Impacto Econômico | Risco | Tratamento | Status |
|---|---|---|---|---|---|---|---|---|---|

## 10. Rastreabilidade de excedentes

Para cada excedente identificado, preservar:

**EXCEDENTE → CATEGORIA → NOME MATERIAL → QUANTIDADE → VALOR UNITÁRIO → VALOR TOTAL → COMPOSIÇÃO → FONTE → MEMÓRIA DE CÁLCULO**

O Nome Material deve ser tratado como camada semântica para análise e rastreabilidade, sem criar uma segunda identidade material.

## 11. Análise de Competitividade

Quando houver dados suficientes, aplicar análise econômica à composição final.

### 11.1 Curva ABC

`peso = valor_item / valor_total_orcamento`

Ordenar os itens por valor decrescente, calcular acumulado e classificar A/B/C conforme os limites parametrizados.

A Curva ABC define prioridade de investigação econômica; não autoriza redução automática.

### 11.2 Ordem de investigação

1. concentração financeira;
2. excedentes;
3. Nome Material;
4. memória de cálculo;
5. evidência e conhecimento disponível;
6. flexibilidade técnica/comercial;
7. risco;
8. oportunidade.

### 11.3 Estados

**Conhecimento:** `FORTE | MEDIO | FRACO | AUSENTE | CONFLITANTE`

**Flexibilidade:** `ALTA | MEDIA | BAIXA | INDETERMINADA`

**Risco:** `BAIXO | MEDIO | ALTO | CRITICO`

**Recomendação:** `MANTER | REVISAR | NEGOCIAR | SUBSTITUIR | REESTRUTURAR | CONFIRMAR | NAO_REDUZIR | AGUARDAR_DECISAO`

### 11.4 Oportunidade

Só registrar oportunidade quando houver fundamento verificável:

- item e classe ABC;
- peso financeiro;
- origem do valor;
- memória de cálculo;
- conhecimento relacionado;
- evidências;
- flexibilidade;
- impacto econômico;
- risco;
- recomendação;
- responsável pela decisão.

Ausência de evidência não autoriza redução.

## 12. Cenários econômicos

Quando houver dados suficientes:

- **BASE:** composição original;
- **COMPETITIVO:** oportunidades apoiadas por evidência e viabilidade;
- **MÁXIMO:** limite analítico das oportunidades tecnicamente possíveis, com riscos e premissas explícitos.

Cada cenário deve apresentar:

- valor total;
- variação absoluta;
- variação percentual;
- itens alterados;
- premissas alteradas;
- risco.

## 13. Autoridade e governança

Fluxo obrigatório:

**ANÁLISE → RECOMENDAÇÃO → ARBITRAGEM → DECISÃO**

O ELO não deve alterar automaticamente orçamento, Lista-Mãe, conhecimento canônico, Core ou Soul.

O Especialista de Orçamento permanece responsável pela composição técnica. A decisão final permanece com o responsável competente.

## 14. Resumo Executivo

Apresentar quantitativamente:

- itens técnicos analisados;
- AI;
- AE;
- AP;
- NA;
- índice de atendimento, somente quando a metodologia estiver definida;
- memórias de cálculo identificadas;
- memórias com divergência;
- itens Classe A;
- itens ausentes;
- contradições identificadas;
- oportunidades de competitividade;
- riscos relevantes;
- decisões pendentes.

## 15. Parecer Técnico

Concluir sobre a aderência da composição ao TR, distinguindo:

- atendimento integral;
- equivalência;
- atendimento parcial;
- não atendimento;
- pendências impeditivas;
- divergências de quantitativo/composição;
- limitações de evidência.

Não declarar 100% de atendimento quando existirem AP, NA ou equivalências ainda dependentes de aceite.

## 16. Parecer de Competitividade

Responder objetivamente:

**QUAIS ITENS CONCENTRAM VALOR → QUAIS TÊM FUNDAMENTO PARA REVISÃO → QUAL IMPACTO → QUAL RISCO → QUAL DECISÃO É NECESSÁRIA**

Não transformar automaticamente a análise em redução de preço.

## 17. Evidência e origem

Toda conclusão deve preservar a origem:

- TR/SO;
- projeto/layout;
- orçamento;
- composição;
- memória de cálculo;
- premissa interna;
- solução de engenharia;
- fornecedor;
- vistoria;
- confirmação do cliente;
- conhecimento aplicável.

Quando a evidência não existir, registrar a limitação.

## 18. Relação com a PTS Técnica

A PTS Pós deve comparar:

**O QUE FOI IDENTIFICADO → O QUE FOI CALCULADO → O QUE FOI ORÇADO → COMO FOI ATENDIDO → O QUE DIVERGIU → POR QUE DIVERGIU → QUAL É O EFEITO.**

Registrar especialmente:

- itens excluídos;
- itens acrescentados;
- alterações de quantitativo;
- substituições;
- equivalências;
- premissas alteradas;
- pendências mantidas;
- oportunidades de revisão.

## 19. Registro de Aprendizado

A PTS Pós deve transformar análises concluídas em conhecimento estruturado somente após avaliação governada.

O aprendizado deve preservar:

**CONTEXTO → PROBLEMA → PREMISSA → CÁLCULO → SOLUÇÃO → DECISÃO → RESULTADO → EVIDÊNCIA → CONDIÇÃO DE APLICAÇÃO → LIMITAÇÃO**

Não memorizar somente preço ou quantidade. O parâmetro reutilizável deve registrar como o resultado foi obtido e em quais condições pode ser aplicado novamente.

## 20. Regra de reutilização das memórias de cálculo

Uma memória de cálculo pode tornar-se parâmetro consultável somente quando houver:

- origem identificada;
- desenvolvimento verificável;
- unidade definida;
- premissas conhecidas;
- resultado conferido;
- limitações registradas;
- ausência de contradição não resolvida.

Memórias com inconsistência devem permanecer disponíveis como **parâmetros com alerta**, nunca como padrão automático.

## 21. Governança do aprendizado

Fluxo:

**ORÇAMENTO → PTS PÓS → VARREDURA → ANÁLISE → DECISÃO → RESULTADO → AVALIAÇÃO → LEARNING CANDIDATE → GOVERNED LEARNING**

O ELO deve distinguir conhecimento forte de conhecimento derivado de uma única solicitação.

Aprendizado específico de uma SO não deve ser promovido automaticamente a regra global.

## 22. Regra final

A PTS Pós-Orçamento é simultaneamente:

1. documento de comprovação técnica;
2. instrumento de rastreabilidade orçamentária;
3. registro das memórias de cálculo;
4. mecanismo de comparação entre composições;
5. detector de contradições e ausências;
6. base para análise de competitividade;
7. fonte estruturada para aprendizado governado.

O padrão deve privilegiar **evidência, rastreabilidade, reconstrução do raciocínio e identificação explícita das incertezas**, sem completar lacunas por suposição.