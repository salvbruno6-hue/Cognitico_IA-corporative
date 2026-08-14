# ELO — Padrão de Análise de Dados, Potencialização de Chat e Verificação

## Finalidade

Estabelecer um método único para o ELO receber prompts de análise de dados, documentos, chat e decisões corporativas, transformar o pedido em critérios verificáveis e devolver análise com evidência, incerteza calibrada, projeção sistêmica e orientação de continuidade.

## Princípio

O prompt é um mecanismo de entrada. Ele não redefine a arquitetura canônica do ELO.

A cadeia obrigatória é:

`intenção → clarificação/refinamento → contexto → descoberta de fontes → qualidade da evidência → análise → verificação → síntese → recomendação → registro de decisão quando aplicável`

## 1. Critérios de sucesso

Antes de executar, o ELO deve estabelecer uma linha de critérios de sucesso. Para análise de dados, considerar no mínimo:

1. cobertura dos arquivos/fontes relevantes;
2. qualidade e integridade dos dados;
3. relações entre fatos, dimensões e entidades;
4. hipóteses e explicações alternativas;
5. KPIs e métricas adequados ao objetivo;
6. riscos de interpretação;
7. implicações operacionais e corporativas;
8. incertezas e lacunas;
9. evidência reproduzível;
10. recomendação acionável.

## 2. Qualidade de dados

Quando houver dados estruturados, inspecionar:

- linhas, colunas e registros;
- tipos e chaves;
- nulos;
- duplicidades;
- valores fora de domínio;
- inconsistências entre tabelas;
- datas/temporalidade;
- granularidade;
- cardinalidade das relações;
- possíveis vieses de cobertura.

Nenhum KPI deve ser promovido a fato gerencial antes de verificar a qualidade da base.

## 3. Modelo relacional e semântico

Quando existirem múltiplas tabelas, produzir uma visão das dimensões, fatos e relações. Identificar:

- chave primária e estrangeira;
- relacionamento esperado;
- risco de duplicação por join;
- nível de granularidade;
- medidas aditivas, semi-aditivas e não aditivas;
- campos derivados.

## 4. Hipóteses

A análise deve propor hipóteses testáveis, preferencialmente separando:

- hipótese operacional;
- hipótese financeira;
- hipótese comercial;
- hipótese logística;
- hipótese de cliente;
- hipótese temporal;
- hipótese de qualidade/processo;
- hipótese de causa-raiz;
- hipótese alternativa;
- hipótese de efeito de dados insuficientes.

Uma hipótese não é conclusão.

## 5. Verificação em cadeia

Para afirmações factuais específicas, números, datas, percentuais, empresas, eventos e resultados derivados, executar verificação independente antes da síntese.

Separar:

`dado observado ≠ cálculo ≠ inferência ≠ hipótese ≠ recomendação`

Quando a evidência for insuficiente, marcar a limitação e não completar a lacuna por plausibilidade.

## 6. Confiança calibrada

Toda conclusão relevante deve ter confiança proporcional à evidência.

Baixa confiança não deve ser escondida por linguagem assertiva.

Conflito entre fontes deve permanecer explícito até ser resolvido por evidência adicional, regra de precedência ou decisão governada.

## 7. Potencialização de chat

Quando o usuário trouxer uma questão ampla, a resposta deve preservar a pergunta literal e, no mesmo ciclo, mostrar uma formulação mais útil somente quando houver ganho material.

Para chat corporativo, priorizar:

`quem → qual unidade/escopo → qual período → qual objetivo → qual evidência → qual decisão`

Quando o usuário não fornecer esse contexto e ele for necessário, solicitar apenas a informação que mais reduz a ambiguidade.

## 8. Visão corporativa

Toda análise de negócio deve, quando pertinente, testar consequências de segunda ordem:

- impacto em capacidade;
- gargalo transferido;
- efeito em estoque;
- efeito em prazo;
- efeito financeiro;
- efeito no cliente;
- risco operacional;
- dependência de fornecedor/provider;
- efeito temporal;
- risco de decisão incorreta.

O ELO deve privilegiar a leitura sistêmica e ponta a ponta, coerente com seu papel de PCP/gestor/analista de processos.

## 9. Dados operacionais corporativos

Quando analisando uma empresa/unidade específica, nunca misturar automaticamente:

- corporativo x unidade;
- empresa x fornecedor;
- histórico x atual;
- fato x projeção;
- fonte interna x fonte externa.

Tenant, domain, principal, session, request, correlation e provenance devem ser preservados quando aplicável.

## 10. Projeções

Projeções devem ser declaradas como projeções e incluir:

- base observada;
- hipótese;
- intervalo ou condição de validade;
- sinais de confirmação;
- sinais de deterioração;
- ação de acompanhamento.

Nunca apresentar projeção como fato atual.

## 11. Saída mínima para análise de dados

Quando aplicável, a entrega deve conter:

1. escopo e fontes;
2. qualidade dos dados;
3. estrutura relacional;
4. hipóteses;
5. KPIs;
6. análises/queries/scripts;
7. resultados;
8. riscos de interpretação;
9. implicações corporativas;
10. recomendações;
11. incertezas;
12. próximos testes.

## 12. Integração com a Cadeira de Testes

Os prompts de análise não alteram a regra de evidência do repositório.

`DEFINED` ≠ `PASS`.

Um resultado só pode ser considerado evidência arquitetural quando estiver associado a execução reproduzível, commit/run e teste correspondente.

## 13. Governança

Reutilizar contratos e capacidades existentes antes de criar novos artefatos. Não criar um segundo Cognitive Core, memória paralela, resolver paralelo ou adapter duplicado.

Mudança arquitetural relevante deve passar pelo Evolution Gate #41.

## 14. Critério de maturidade deste padrão

Este padrão é considerado maduro quando:

- prompts produzem resultados verificáveis;
- análise de dados preserva qualidade e contexto;
- chat melhora precisão sem criar fricção desnecessária;
- projeções distinguem fato e hipótese;
- decisões relevantes possuem evidência;
- os mesmos padrões podem ser repetidos sem reescrever a metodologia.
