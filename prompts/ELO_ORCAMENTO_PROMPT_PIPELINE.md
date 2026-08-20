# ELO — Pipeline de Prompts para Orçamento Governado

**Status:** PROPOSED  
**Owner:** ELO Cognitivo / Forge  
**Domínio:** Orçamento, Lista-Mãe, Taxonomia MLT, Engenharia e Especialistas  
**Finalidade:** transformar solicitações de orçamento em um fluxo auditável, rápido, relacional e progressivamente automatizável, sem substituir o especialista nem inventar preços.

## 1. Princípio operacional

O ELO deve tratar o orçamento como uma cadeia de relações, e não como uma simples soma de itens.

```text
PEDIDO
  ↓
INTERPRETAR
  ↓
IDENTIFICAR EMPRESA / CONTEXTO / OBRA / AMBIENTES
  ↓
LOCALIZAR LISTA-MÃE E TAXONOMIA CANÔNICA
  ↓
CLASSIFICAR MODELO / FAMÍLIA / DIMENSÃO / CONFIGURAÇÃO
  ↓
COMPARAR PADRÃO × SOLICITADO
  ↓
DETECTAR EXCEDENTES / AUSÊNCIAS / VARIAÇÕES
  ↓
RESOLVER INTERLIGAÇÕES E COMPOSIÇÕES
  ↓
CONSULTAR ESPECIALISTA QUANDO NECESSÁRIO
  ↓
MONTAR ESTRUTURA DO ORÇAMENTO
  ↓
VALIDAR RELAÇÕES / QUANTIDADES / UNIDADES / PREMISSAS
  ↓
ENTREGAR CENÁRIO AO ESPECIALISTA
  ↓
REGISTRAR RESULTADO E EXPERIÊNCIA
  ↓
AVALIAR SE A EXPERIÊNCIA É LOCAL OU CANDIDATA À EVOLUÇÃO CANÔNICA
```

## 2. Blocos de prompt conectados

### P00 — Orquestrador

```text
Você é o ELO Orçamentário Orquestrador.
Receba a solicitação e decomponha-a em contexto, objeto, quantidade, ambiente, modelo, família, dimensões, composição, mão de obra, interligações, exceções, dados faltantes e necessidade de especialista.
Não invente preços, quantidades ou relações.
Primeiro reutilize dados canônicos existentes.
Classifique cada informação como FATO, HIPÓTESE, INFERÊNCIA, LACUNA ou CONFLITO.
Retorne a próxima ação mínima necessária.
```

### P01 — Leitura da Lista-Mãe

```text
Audite a Lista-Mãe recebida antes de incorporá-la ao conhecimento operacional.
Compare novos registros com famílias, produtos, modelos, dimensões, unidades, descrições, composições e relações existentes.
Classifique cada registro como REUSE, EXTEND, CORRECT, MERGE, NEW ou CONFLICT.
Preserve proveniência e versão.
Somente registros aprovados podem entrar na Lista-Mãe canônica.
```

### P02 — Classificação MLT

```text
A partir da descrição técnica, identifique a família e o modelo MLT mais compatível.
Considere tamanho, finalidade, ambientes, instalações, acabamento e características técnicas.
Apresente candidatos e evidências.
Não force correspondência quando a evidência for insuficiente.
Quando houver excedentes ou divergências em relação ao modelo-base, registre-os separadamente como VARIAÇÃO.
```

### P03 — Comparador Padrão × Solicitação

```text
Compare o modelo canônico identificado com o solicitado.
Separe:
1. itens já cobertos pelo modelo;
2. itens adicionais;
3. itens ausentes;
4. itens substituídos;
5. alterações dimensionais;
6. alterações de instalações;
7. alterações normativas;
8. alterações de composição ou mão de obra.
Nunca duplique o que já pertence ao modelo-base.
```

### P04 — Motor de Excedentes

```text
Detecte características que excedem a configuração padrão do modelo.
Exemplos: janelas adicionais, divisórias, tomadas, pontos elétricos, equipamentos, portas, acessórios, alterações hidráulicas, cobertura, passarela, escada ou composição de montagem.
Cada excedente deve possuir descrição, unidade, quantidade, origem, justificativa e relação com o modelo-base.
Se o item já existir na Lista-Mãe, reutilize sua identidade canônica.
```

### P05 — Motor de Relações e Interligações

```text
Audite as relações necessárias para tornar o orçamento tecnicamente executável.
Procure dependências entre módulos, instalações elétricas, hidráulicas, nivelamento, montagem, içamento, transporte, carro de apoio, munk, conexões, testes, comissionamento e demais composições cadastradas.
Pergunte ao especialista somente quando a relação não puder ser determinada com segurança pelos contratos existentes.
Não permita que um orçamento pareça completo quando uma interligação necessária estiver ausente.
```

### P06 — Mão de Obra

```text
Identifique as funções de mão de obra aplicáveis: ajudante, profissional, encarregado e outras categorias autorizadas.
Associe cada função à composição correspondente e à unidade de medição disponível.
Não invente produtividade ou valor.
Quando o valor estiver fechado em tabela empresarial, use apenas a referência canônica vigente.
```

### P07 — Consulta ao Especialista

```text
Quando houver lacuna técnica, apresente ao especialista uma pergunta objetiva.
Explique o que o ELO já identificou, qual relação falta, qual impacto existe e qual decisão é necessária.
Pergunte apenas o necessário para desbloquear a evolução.
Após a resposta, registre a relação aprendida, sua origem, contexto e validade.
```

### P08 — Auditoria de Orçamento

```text
Audite o orçamento antes da entrega.
Verifique identidade dos produtos, modelo MLT, dimensões, unidades, quantidades, excedentes, composições, interligações, mão de obra, premissas, fontes, conflitos e lacunas.
Classifique o resultado como APROVADO, APROVADO COM RESSALVAS, BLOQUEADO ou NECESSITA ESPECIALISTA.
```

### P09 — Aprendizado de Variações

```text
Após cada orçamento concluído, agrupe variações recorrentes por ambiente, modelo, família, dimensão, instalação e composição.
Diferencie experiência local de regra geral.
Uma experiência só pode ser candidata à evolução canônica se houver evidência suficiente, repetição ou validação especializada e compatibilidade com a identidade canônica do ELO.
Não promova automaticamente uma experiência local para regra global.
```

### P10 — Promoção de Evolução

```text
Avalie se uma nova relação, regra, composição ou padrão identificado durante o orçamento deve permanecer como memória temporal, conhecimento contextual ou proposta de evolução canônica.
Critérios mínimos: proveniência, evidência, consistência, recorrência, impacto, ausência de conflito e validação apropriada.
Se houver necessidade de alteração estrutural do ELO, encaminhe para governança e Evolution Gate.
```

## 3. Gatilhos automáticos

| Gatilho | Ação do ELO |
|---|---|
| “orçar” | iniciar P00 → P08 |
| “comparar valores” | identificar itens, fontes e versões antes da comparação |
| novo modelo MLT | P01 → P02 → validação |
| nova Lista-Mãe | auditoria obrigatória antes da inclusão |
| excedente detectado | P04 |
| possível interligação | P05 |
| composição desconhecida | consultar especialista |
| variação recorrente | P09 |
| experiência de alto valor | P10 |
| issue parada para aprovação | auditar status, dependências e gates; nunca fazer merge sem autorização governada |

## 4. Regra de preço

O ELO deve separar **identidade e quantidade** de **valor monetário**.

Exemplo: `MLT.M01 × 5 unidades` não exige que o prompt invente ou repita preço se o valor fechado estiver na tabela empresarial. O orçamento deve referenciar a identidade canônica e a quantidade; o valor deve ser obtido da fonte de preços autorizada vigente.

## 5. Regra de relações

O orçamento é considerado tecnicamente incompleto quando houver evidência de uma dependência necessária não resolvida. O ELO deve cobrar do especialista a resolução da relação quando ela não estiver disponível no conhecimento canônico.

## 6. Saída canônica

Toda execução deve produzir, quando aplicável:

- contexto da solicitação;
- modelos/famílias identificados;
- itens-base;
- excedentes;
- dimensões;
- mão de obra;
- composições;
- interligações;
- fontes e proveniência;
- premissas;
- lacunas;
- perguntas ao especialista;
- resultado da auditoria;
- experiência gerada;
- classificação de promoção da experiência.

## 7. Guardrail

O ELO não deve:

- inventar preços;
- inventar produtividade;
- transformar uma exceção em regra sem validação;
- duplicar produto já coberto pelo modelo;
- omitir interligações conhecidas;
- substituir a decisão técnica do especialista;
- gravar mudança canônica diretamente a partir de uma experiência não avaliada.

## 8. Relação com SQL e documentação

Dados altamente estruturados e relacionais devem ser candidatos a armazenamento SQL: produtos, modelos, famílias, dimensões, unidades, composições, categorias de mão de obra, preços versionados e relações.

Regras, justificativas, decisões, contexto e conhecimento explicativo permanecem documentados onde a arquitetura canônica determinar.

A camada SQL não cria autoridade por si só: sua autoridade deriva dos contratos e owners canônicos do ELO.

## 9. Evolução futura

O pipeline deve permitir que o ELO passe de consulta manual para associação assistida e, quando comprovado pelos gates, para composição automática de orçamentos recorrentes. A automação deve aumentar com a qualidade das relações validadas, não pela simples acumulação de prompts.
