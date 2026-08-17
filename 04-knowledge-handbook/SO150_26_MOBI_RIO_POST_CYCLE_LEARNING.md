# ELO — SO 150.26 MOBI-Rio — Post-Cycle Learning

## Status

`CONTEXTUAL_EXPERIENCE_RECORDED`

## Origem

Experiência de análise e pós-orçamento da SO 150.26 — MOBI-Rio, realizada a partir do TR, das marcações do analista Samuel, das decisões de escopo e dos cinco orçamentos finais dos Itens 04 a 08.

Este registro preserva decisões e padrões observados nesta SO. Não promove números ou premissas específicas para Core sem validação independente.

## Escopo efetivamente orçado

- Itens 01, 02 e 03: não orçados por definição recebida durante a análise.
- Itens 04 a 08: orçados.
- Orçamento realizado de forma unitária: a quantidade apresentada pela licitação é multiplicada posteriormente pelo valor unitário informado.
- Transporte dos módulos: não orçado.

## Método de leitura do TR aprendido

1. O TR marcado pelo analista deve ser interpretado preservando as marcações de engenharia.
2. Sublinhado/grifo amarelo nos endereços não deve ser tratado como sinal técnico, excedente ou alteração de escopo.
3. Outras marcações amarelas podem representar excedente, ponto de atenção, divergência ou requisito que chamou atenção e devem ser avaliadas separadamente.
4. Indicações de módulos feitas pelo analista devem ser preservadas como referência da solução da Engenharia Modular.
5. Quantidade comercial da licitação deve ser separada de quantidade física de módulos, especialmente em conjuntos unificados.
6. Não transformar automaticamente uma solução interna da Engenharia Modular em exigência do TR.
7. Quando o TR for omisso, registrar a premissa adotada pela Engenharia em vez de inventar uma exigência contratual.

## Aprendizados técnicos da SO

### 1. Orçamento unitário

A composição deve representar uma unidade da solução. Exemplos observados:

- Item 04: 1 MLT.M01, embora o TR tenha quantidade 4.
- Item 05: 1 MLT.M02, embora o TR tenha quantidade 3.
- Item 06: 1 conjunto formado por 3 MLT.M01.
- Item 07: 1 conjunto formado por 2 MLT.M01.
- Item 08: 1 MLT.M01, embora o TR tenha quantidade 2.

A multiplicação pela quantidade da licitação não deve ser duplicada dentro da composição unitária.

### 2. Manutenção corretiva como verba anual

Para os módulos climatizados, foi adotada nesta SO uma premissa de orçamento de quatro atendimentos presenciais por ano.

Premissas usadas no ciclo:

- 4 carros de apoio por ano, a R$ 220/dia por visita;
- equipe geral de profissional + ajudante a R$ 512/dia;
- técnico de refrigeração a R$ 449/dia;
- ajudante de refrigeração a R$ 236/dia;
- 5% de acréscimo sobre os materiais corretivos.

Para conjuntos com múltiplos módulos, materiais podem ser multiplicados proporcionalmente, enquanto deslocamento e mão de obra por visita não devem ser multiplicados pelo número de módulos quando uma mesma visita atende o conjunto.

### 3. Vida útil e manutenção

A quantidade de quatro visitas/ano foi tratada como reserva orçamentária para manutenção corretiva, e não como obrigação de visitas programadas trimestrais. A análise identificou que o ar-condicionado é um dos principais riscos de manutenção dos módulos climatizados.

### 4. Elétrica: diferença entre requisito do TR e padrão interno

- Item 04: o TR não especificava alimentação trifásica; foi adotado o padrão interno bifásico 220 V + neutro + terra.
- Itens 06 e 07: o TR exigia QDL trifásico 220 V, neutro, terra e disjuntor geral de 63 A; foi adotada adequação para QDL trifásico.
- Item 08: foi aproveitado o quadro padrão existente do MLT.M01, com adequação para atender à exigência de 63 A trifásico, em vez de criar um novo quadro.

A solução interna deve ser descrita como premissa/solução da Engenharia quando não estiver explicitamente exigida pelo TR.

### 5. Solução elétrica do Item 08

O quadro padrão considerado possui 9 posições e, conforme informado no ciclo, utiliza:

- geral 25 A bipolar;
- 16 A bipolar para ar-condicionado;
- 16 A monopolar para tomadas;
- 10 A bipolar para iluminação.

A solução adotada foi retirar o geral bipolar de 25 A, substituir por geral de 63 A trifásico, adequar o barramento e considerar mão de obra de profissional por 2 horas. O valor orçado para essa adequação foi R$ 149,34.

Esta solução permanece contextual à configuração do quadro utilizado nesta SO e não deve ser promovida como regra universal sem validação.

### 6. Módulos comerciais utilizados

- `MLT.M01_Módulo Habitacional 20pés Amplo`: utilizado nos Itens 04, 06, 07 e 08.
- `MLT.M02_Módulo Habitacional 20pés Escritório Suíte`: utilizado no Item 05.

Foi validado durante o ciclo que o MLT.M01 contempla integralmente a especificação do TR do Item 04.

O MLT.M02 padrão contempla duas janelas e possui basculante de 60 x 60 cm no banheiro.

### 7. Unificação de módulos

- Item 06: 3 MLT.M01 formando uma Copa Unificada.
- Item 07: 2 MLT.M01 formando um Almoxarifado Unificado.

A unificação pode ter valor tabelado no comercial, mas em alguns casos pode exigir mão de obra de acoplagem calculada pela Engenharia. O tratamento deve ser definido conforme a composição comercial e a solução efetivamente adotada.

### 8. Copa Unificada — solução observada

Para o Item 06 foram considerados:

- 3 MLT.M01;
- 1 ar-condicionado de 18.000 BTU por módulo;
- pia dupla como excedente;
- porta dupla como excedente;
- adequação para QDL trifásico 220 V, neutro, terra e disjuntor geral de 63 A.

Foi avaliada a possibilidade de utilizar QGBT trifásico para interligar os QDLs dos módulos. Essa arquitetura foi tratada como solução técnica da Engenharia, e não como requisito textual explícito do TR.

### 9. Almoxarifado Unificado — solução observada

Para o Item 07 foram considerados:

- 2 MLT.M01;
- porta dupla e abertura/visita para passagem de materiais;
- adequação para QDL trifásico 220 V, neutro, terra e disjuntor geral de 63 A;
- manutenção corretiva anual.

### 10. Exclusões recorrentes identificadas

Nesta SO, foram mantidos fora das composições:

- transporte dos módulos;
- telhado/sobreteto, quando não exigido pelo TR;
- interligações externas;
- SPDA.

Essas exclusões são específicas desta experiência e não devem ser aplicadas automaticamente a futuras SOs sem verificar o TR correspondente.

## Resultado financeiro registrado

Valores unitários finais com BDI de 65%:

| Item | Subtotal | Total com BDI |
|---|---:|---:|
| 04 | R$ 6.361,66 | R$ 10.496,74 |
| 05 | R$ 7.059,88 | R$ 11.648,80 |
| 06 | R$ 15.043,52 | R$ 24.821,81 |
| 07 | R$ 11.842,80 | R$ 19.540,62 |
| 08 | R$ 8.702,04 | R$ 14.358,37 |

Valor calculado para as quantidades do TR dos Itens 04 a 08: R$ 150.012,53 com BDI.

## Aprendizado operacional para o ELO

- Separar sempre `TR`, `interpretação do analista`, `solução da Engenharia`, `excedente`, `premissa` e `exclusão`.
- Não somar quantidade física de módulos dentro do preço unitário quando a licitação fará a multiplicação do item.
- Em conjuntos unificados, o preço unitário deve representar o conjunto completo, incluindo seus módulos físicos e excedentes necessários.
- Manutenção deve ser tratada como risco contratual quando houver obrigação de manutenção corretiva e SLA, mas a frequência de visitas é uma premissa de orçamento salvo exigência expressa.
- Para componentes repetidos dentro de um conjunto, multiplicar materiais sem multiplicar automaticamente visitas e equipes quando a mesma mobilização atende todos os módulos.
- Em elétrica, distinguir exigência explícita do TR de solução de engenharia adotada para atender ao requisito.
- Antes de fechar a PTS, revisar nomes das verbas para garantir que cada manutenção esteja associada ao item correto.

## Limites de promoção

Nenhum dos seguintes parâmetros deve ser promovido isoladamente para Core sem validação adicional:

- quatro visitas/ano;
- 5% sobre materiais;
- valores de mão de obra;
- valores de materiais;
- BDI de 65%;
- arquitetura específica de QGBT/QDL;
- composição específica dos quadros;
- exclusões desta SO.

Eles permanecem como experiência contextual da SO 150.26.

## Próximo uso pelo ELO

Quando uma nova SO apresentar estrutura semelhante, o ELO pode consultar esta experiência como referência contextual, mas deve primeiro verificar no novo TR:

1. quais itens realmente serão orçados;
2. se o orçamento é unitário ou global;
3. quais marcações do analista existem;
4. quais módulos comerciais atendem ao escopo;
5. quais excedentes são explícitos;
6. quais exigências elétricas são expressas;
7. se transporte e interligações estão incluídos;
8. qual manutenção/SLA foi exigido;
9. se a solução comercial já contempla os requisitos.

## Estado do aprendizado

`RETAIN_AS_CONTEXTUAL_EXPERIENCE`

A experiência está registrada para reutilização contextual. Não é regra corporativa universal até passar por validação em outras solicitações.