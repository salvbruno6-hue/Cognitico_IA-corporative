# ELO — Entrevista de Experiência do Orçamento

## Objetivo

Durante a construção de uma Solicitação de Orçamento (SO), o ELO realiza três checkpoints curtos — início, meio e fim — para registrar **como o orçamento foi construído e o que determinou o resultado final**.

O objetivo não é interromper o trabalho nem transformar toda conversa em aprendizado. O objetivo é produzir uma experiência observada, estruturada e rastreável para posterior validação.

## Três checkpoints

### 1. INÍCIO — entendimento

Perguntas mínimas:

- Qual é o objetivo deste orçamento e qual resultado precisa ser entregue?
- Quais requisitos podem mudar a solução, quantidade ou custo?
- O que ainda não está claro ou precisa ser confirmado?
- Existe precedente, modelo, composição ou regra que será considerada? Por quê?
- Há restrição técnica, contratual, prazo, logística ou comercial que limite as alternativas?

Saída: contexto, objetivo, requisitos críticos, incertezas, restrições e conhecimento inicialmente utilizado.

### 2. MEIO — raciocínio

Perguntas mínimas:

- O que mudou ou ficou mais claro desde o início e qual decisão isso provocou?
- Qual alternativa foi considerada e por que a solução adotada foi escolhida?
- Qual decisão tem maior impacto no valor ou viabilidade?
- Que informação, precedente, regra, produto ou experiência foi determinante?
- Qual cálculo, premissa ou evidência sustenta a escolha?
- Houve erro, incongruência ou informação ausente? Como foi tratado?

Saída: decisões, alternativas, premissas, evidências, problemas e correções.

### 3. FIM — reconstrução

Perguntas mínimas:

- O que efetivamente determinou o orçamento final?
- Quais decisões foram mais importantes e por quê?
- O que ficou diferente do modelo, precedente ou expectativa inicial?
- Quais evidências/validações sustentam o resultado?
- O que vale recuperar em próximo orçamento e em qual contexto?
- O que deu errado, quase deu errado ou precisou ser corrigido?
- Qual é a confiança no resultado e o que ainda depende de confirmação?

Saída: fatores determinantes, decisões finais, divergências, evidências, correções, reutilização contextual e pendências.

## Regra cognitiva

O ELO não deve aprender apenas:

`RESULTADO = X`

Deve preservar:

`REQUISITO → INTERPRETAÇÃO → ALTERNATIVAS → DECISÃO → PREMISSA → CÁLCULO → EVIDÊNCIA → RESULTADO → VALIDAÇÃO`

## Persistência

A captura deve ser compatível com a estrutura existente de `elo_aprendizado_experiencias`, especialmente `contexto`, `sequencia`, `conhecimentos_utilizados`, `decisoes`, `verificacoes`, `resultado`, `erros`, `correcoes`, `origem` e `origem_referencia`.

A captura inicial permanece:

- `status_validacao = OBSERVADA`
- `learning_candidate = false`
- `canonical_mutation = false`

Portanto, **responder às perguntas não promove conhecimento automaticamente**.

A posterior promoção continua obedecendo evidência, consistência, validação, governança e Evolution Gate.

## Operação adaptativa

As perguntas são checkpoints, não formulário obrigatório de 18 perguntas em toda SO. O ELO deve perguntar somente o necessário em cada fase e aprofundar quando uma resposta revelar:

- decisão de alto impacto;
- mudança de premissa;
- divergência de modelo;
- cálculo relevante;
- erro/correção;
- nova evidência;
- adaptação/excedente;
- precedente determinante.

O mecanismo deve preservar a experiência mesmo quando uma etapa não possuir informação suficiente; ausência de resposta é uma lacuna, não um dado inventado.
