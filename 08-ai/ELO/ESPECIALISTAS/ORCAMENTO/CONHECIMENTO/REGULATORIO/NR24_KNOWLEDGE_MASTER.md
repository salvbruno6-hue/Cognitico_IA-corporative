# ELO — NR-24 Knowledge Master

## Status
NORMATIVE knowledge model / source-grounded extraction

## Purpose

Consolidar no ELO o conhecimento normativo referente à NR-24 — Condições Sanitárias e de Conforto nos Locais de Trabalho — para que o **Core** compreenda significado, escopo, hierarquia, condições, exceções, relações e regras de cálculo, enquanto o **Forge** possa aplicar esse conhecimento em validações, dimensionamentos, checklists e produtos modulares sem redefinir a norma.

## Authority

- Primary external authority: Ministério do Trabalho e Emprego — NR-24 vigente disponibilizada pelo MTE.
- Current source inspected: NR-24 atualizada 2022, com atualização da Portaria MTP nº 2.772/2022.
- Official source: https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/arquivos/normas-regulamentadoras/nr-24-atualizada-2022.pdf
- This document is a knowledge representation of the source, not a replacement for the DOU.
- External norm must never be silently converted into an internal company directive.

## Provenance model

Every extracted rule must preserve:

- source_type: EXTERNAL_NORM
- authority: MTE
- norm: NR-24
- item: exact normative item/subitem when available
- source_version: 2022 text inspected
- status: NORMATIVE
- interpretation_status: SOURCE_DERIVED unless explicitly marked INFERENCE
- internal_overlay: NONE unless a separate Diretriz is linked

## Core semantic model

The NR-24 knowledge graph should represent at least:

`Norma -> Capítulo -> Item -> Requisito -> Condição -> População de aplicação -> Unidade -> Quantidade/limite -> Exceção -> Evidência -> Regra de cálculo`

### Principal entities

- Norma
- Capítulo
- Item normativo
- Estabelecimento
- Trabalhador
- Trabalhador usuário
- Turno
- Instalação sanitária
- Bacia sanitária
- Mictório
- Lavatório
- Chuveiro
- Vestiário
- Armário
- Local para refeições
- Cozinha
- Alojamento
- Dormitório/quarto
- Cama simples
- Beliche
- Vestimenta de trabalho
- Água potável
- Bebedouro
- Código de obras local
- Legislação local
- Anexo setorial

## 24.1 — Objetivo e campo de aplicação

### 24.1.1
A norma estabelece condições mínimas de higiene e conforto a serem observadas pelas organizações.

**Regra de dimensionamento:** todas as instalações regulamentadas pela NR devem considerar o número de trabalhadores usuários do turno com maior contingente.

### 24.1.1.1 — Trabalhadores usuários
É o conjunto de todos os trabalhadores no estabelecimento que efetivamente utilizem de forma habitual as instalações regulamentadas pela NR.

**Core interpretation:** não assumir automaticamente o total nominal de empregados como população de dimensionamento. Primeiro identificar os trabalhadores usuários e o turno com maior contingente.

## 24.2 — Instalações sanitárias

### 24.2.1
Todo estabelecimento deve possuir instalação sanitária constituída por:

- bacia sanitária sifonada com assento e tampo;
- lavatório.

### 24.2.1.1 — Mictórios masculinos
As instalações sanitárias masculinas devem possuir mictório, exceto quando essencialmente de uso individual.

Para estabelecimentos construídos até 23/09/2019: mictórios dimensionados conforme a redação anterior da NR-24/Portaria MTb nº 3.214/1978.

Para estabelecimentos construídos a partir de 24/09/2019:

- 1 unidade para cada 20 trabalhadores ou fração, até 100 trabalhadores;
- 1 unidade para cada 50 trabalhadores ou fração no que exceder 100 trabalhadores.

### 24.2.2 — Instalação sanitária
Proporção mínima:

- 1 instalação sanitária para cada grupo de 20 trabalhadores ou fração;
- separadas por sexo.

**Important semantic distinction:** o texto fala em `instalação sanitária`, não em uma regra independente de “1 vaso por 20” isoladamente. O Core deve preservar essa distinção.

### 24.2.2.1 — Lavatórios em atividades específicas
Exige-se 1 lavatório para cada 10 trabalhadores nas atividades com exposição e manuseio de:

- material infectante;
- substâncias tóxicas;
- substâncias irritantes;
- aerodispersóides;
- substâncias que provoquem deposição de poeiras que impregnem a pele e roupas.

**Do not generalize:** a proporção 1/10 não deve ser aplicada a toda atividade sem verificar a condição de exposição prevista no item.

### 24.2.2.2 — Pequenos estabelecimentos comerciais/administrativos/similares
Até 10 trabalhadores, pode ser disponibilizada uma instalação sanitária individual de uso comum entre os sexos, desde que garantidas condições de privacidade.

### 24.2.3 — Condições das instalações sanitárias
Devem:

- ser mantidas em conservação, limpeza e higiene;
- ter piso e parede com material impermeável e lavável;
- possuir peças sanitárias íntegras;
- possuir recipientes para descarte de papéis usados;
- ser ventiladas para o exterior ou possuir exaustão forçada;
- dispor de água canalizada e esgoto ligados à rede geral ou sistema que não gere risco à saúde e atenda à regulamentação local;
- comunicar-se com locais de trabalho por passagens com piso e cobertura quando estiverem fora do corpo do estabelecimento.

## 24.3 — Componentes sanitários

### 24.3.1 — Bacias sanitárias
Compartimentos:

- individuais;
- divisórias que mantenham interior indevassável, com vão inferior facilitando limpeza e ventilação;
- portas independentes com fecho que impeça devassamento;
- papel higiênico com suporte e recipiente quando não for permitido descarte na própria bacia; recipiente com tampa quando destinado às mulheres;
- dimensões conforme código de obras local; na ausência deste, área livre mínima de 0,60 m de diâmetro entre borda frontal da bacia e porta fechada.

### 24.3.2 — Mictórios
Pode ser individual ou calha coletiva, com anteparo.

Calha com anteparo:
- cada segmento mínimo de 0,60 m = 1 unidade para dimensionamento.

Calha sem anteparo:
- cada segmento mínimo de 0,80 m = 1 unidade para dimensionamento.

Mictórios devem ser de material impermeável e mantidos limpos e higiênicos.

### 24.3.3 — Lavatórios
Pode ser:

- individual;
- calha;
- tampo coletivo com várias cubas.

Cada segmento de 0,60 m corresponde a uma unidade para dimensionamento do lavatório.

### 24.3.4 — Higiene das mãos
Lavatório deve possuir material/dispositivo para limpeza, enxugo ou secagem das mãos. Toalhas coletivas são proibidas.

### 24.3.5 — Chuveiros
Quando exigidos:

- 1 chuveiro para cada 10 trabalhadores ou fração, em atividades com exposição/manuseio de material infectante, substâncias tóxicas, irritantes ou aerodispersóides que impregnem pele e roupas;
- 1 chuveiro para cada 20 trabalhadores ou fração, em atividades com contato com substâncias que provoquem deposição de poeiras que impregnem pele/roupas, ou que exijam esforço físico, ou submetidas a calor intenso.

### 24.3.5.1
Nas atividades em que há exigência de chuveiros, estes devem fazer parte ou estar anexos aos vestiários.

### 24.3.6 — Compartimentos de chuveiro
Devem:

- ser individuais;
- permanecer conservados, limpos e higiênicos;
- possuir portas que impeçam devassamento;
- possuir água quente e fria;
- possuir piso e paredes impermeáveis e laváveis;
- possuir suporte para sabonete e toalha;
- seguir código de obras local; na ausência, mínimo de 0,80 m x 0,80 m.

## 24.4 — Vestiários

### 24.4.1 — Obrigatoriedade
Vestiários são exigidos quando:

1. a atividade exige vestimentas de trabalho ou uniforme cuja troca deve ocorrer no próprio local; ou
2. a atividade exige que o estabelecimento disponibilize chuveiro.

### 24.4.2 — Dimensionamento até 750 trabalhadores
Área mínima do vestiário por trabalhador:

`A_unit = 1,5 - (N / 1000)`

onde N = número de trabalhadores que necessitam utilizar o vestiário.

### 24.4.2.1 — Mais de 750 trabalhadores
Área mínima:

`A_unit = 0,75 m²/trabalhador`

### 24.4.3 — Condições dos vestiários
Devem:

- ser conservados, limpos e higiênicos;
- possuir piso e parede impermeáveis e laváveis;
- ser ventilados para exterior ou ter exaustão forçada;
- possuir assentos laváveis e impermeáveis em número compatível com trabalhadores;
- possuir armários individuais simples e/ou duplos com sistema de trancamento.

### 24.4.4 — Armários rotativos
É admitido uso rotativo de armários simples, exceto quando utilizados para guardar EPI ou vestimentas expostas a material infectante, substâncias tóxicas, irritantes ou sujidade.

### 24.4.5 — Armários duplos / dois simples
Nas atividades com exposição/manuseio de material infectante, substâncias tóxicas, irritantes ou aerodispersóides, ou contato com substâncias que provoquem deposição de poeiras que impregnem pele e roupas, devem ser fornecidos:

- armários de compartimentos duplos; ou
- dois armários simples.

### 24.4.5.1 — Dispensa
Ficam dispensadas de fornecer dois armários simples ou armário duplo as organizações que:

- promovam higienização diária das vestimentas; ou
- forneçam vestimentas descartáveis;

mantendo 1 armário simples para roupas comuns de uso pessoal.

### 24.4.6 — Armário simples
Dimensões mínimas:

- altura: 0,40 m;
- largura: 0,30 m;
- profundidade: 0,40 m.

### 24.4.6.1 — Armário duplo
Alternativa A:

- 0,80 m altura;
- 0,30 m largura;
- 0,40 m profundidade;
- divisão/prateleira horizontal;
- dois compartimentos de 0,40 m de altura, um para roupa comum e outro para roupa de trabalho.

Alternativa B:

- 0,80 m altura;
- 0,50 m largura;
- 0,40 m profundidade;
- divisão vertical;
- dois compartimentos de 0,25 m de largura, isolando roupa comum e roupa de trabalho.

### 24.4.7 — Guarda-volume
Empresa que oferece serviço de guarda-volume para roupas e acessórios pessoais fica dispensada de fornecer armários.

### 24.4.8 — Empresas desobrigadas de vestiário
Devem garantir escaninho, gaveta com tranca ou similar para guarda individual de pertences, ou serviço de guarda-volume.

## 24.5 — Locais para refeições

### 24.5.1
Empregadores devem oferecer locais em condições de conforto e higiene para refeições nos intervalos.

### 24.5.1.1
É permitida divisão dos trabalhadores do turno em grupos para organizar fluxo e conforto, garantindo intervalo de alimentação e repouso.

### 24.5.2 — Até 30 trabalhadores atendidos
O local deve:

- ser destinado/adaptado para refeições;
- ser arejado e apresentar boas condições de conservação, limpeza e higiene;
- possuir assentos e mesas, balcões ou similares suficientes para os usuários atendidos.

Nas proximidades deve haver:

- meios para conservação e aquecimento;
- local/material para lavagem de utensílios;
- água potável.

### 24.5.3 — Mais de 30 trabalhadores atendidos
Deve:

- ser destinado a refeições e ficar fora da área de trabalho;
- ter piso lavável e impermeável;
- ter paredes laváveis e impermeáveis;
- possuir espaços para circulação;
- ser ventilado para exterior ou possuir exaustão, salvo ambientes climatizados;
- possuir lavatórios nas proximidades ou no próprio local;
- possuir assentos e mesas com superfícies/coberturas laváveis ou descartáveis em número correspondente aos usuários atendidos;
- ter água potável;
- manter conservação, limpeza e higiene;
- possuir meios de aquecimento;
- possuir recipientes com tampa para restos alimentares e descartáveis.

### 24.5.4 — Dispensas
Dispensados das exigências do item 24.5:

- estabelecimentos comerciais, bancários e afins que interrompam atividades por 2 horas no período de refeições;
- estabelecimentos industriais em cidades do interior quando houver vila operária ou trabalhadores residindo nas proximidades, permitindo refeições nas residências;
- estabelecimentos que ofereçam vale-refeição, desde que disponibilizem condições de conservação/aquecimento e local para trabalhadores que tragam refeição de casa.

## Historical distinction — antigo texto de refeitórios

O material CNI de 2019 fornecido no chat registra como texto anterior a exigência de 1,00 m² por usuário, atendimento de 1/3 do turno de maior contingente e circulação principal de 75 cm / circulação entre bancos e banco/parede de 55 cm. O mesmo quadro registra esses requisitos como `Item excluído` na redação atual de 2019.

**Core rule:** esses valores devem ser armazenados como HISTORICAL/LEGACY, nunca como requisito atual da NR-24 sem fonte posterior que os restabeleça.

## 24.6 — Cozinhas
Quando houver cozinha:

- deve ficar anexa aos locais de refeições e ligada a eles;
- pisos e paredes impermeáveis e laváveis;
- aberturas de ventilação protegidas por telas ou ventilação exaustora;
- lavatório para trabalhadores da alimentação, com material/dispositivo para limpeza e secagem das mãos, sem toalhas coletivas;
- condições para acondicionamento e disposição de lixo conforme normas locais;
- sanitário próprio para trabalhadores que manipulam alimentos, separado por sexo.

Câmaras frigoríficas: dispositivo de abertura pelo lado interno, permitindo abertura mesmo trancada externamente.

GLP: recipientes de armazenamento em área externa ventilada, conforme normas técnicas brasileiras pertinentes.

## 24.7 — Alojamento

### 24.7.1
Alojamento = conjunto de espaços/edificações composto por dormitório, instalações sanitárias, refeitório, áreas de vivência e local para lavagem/secagem de roupas, sob responsabilidade do empregador, para hospedagem temporária.

### 24.7.2
Dormitórios devem:

- ser conservados, higiênicos e limpos;
- ser dotados de quartos;
- possuir 1 instalação sanitária com chuveiro para cada 10 trabalhadores hospedados ou fração;
- ser separados por sexo.

Se sanitários não forem integrantes dos dormitórios, distância máxima de 50 m, com passagens de piso lavável e cobertura.

### 24.7.3 — Quartos
Devem:

- possuir camas correspondentes ao número de trabalhadores, vedadas 3 ou mais camas na mesma vertical;
- permitir movimentação segura por espaçamentos vertical/horizontal;
- possuir colchões certificados pelo INMETRO;
- possuir enxoval limpo/higienizado e adequado ao clima;
- possuir ventilação natural em conjunto com ventilação artificial considerando condições locais;
- capacidade máxima de 8 trabalhadores;
- armários;
- no mínimo 3,00 m² por cama simples ou 4,50 m² por beliche, incluindo circulação e armário;
- conforto acústico conforme NR-17.

### 24.7.3.1 / 24.7.3.1.1
Camas/beliches devem ser resistentes, sem rebarbas/arestas cortantes/tubos abertos e compatíveis com o colchão. Camas superiores de beliche devem possuir proteção lateral e escada fixa.

### 24.7.3.2
Armários dos quartos devem possuir trancamento e dimensões compatíveis para roupas, pertences pessoais e enxoval.

### 24.7.4
Preferencialmente trabalhadores do mesmo quarto devem pertencer ao mesmo turno.

### 24.7.5
Locais de refeições do alojamento devem atender ao item 24.5 e podem ser internos ou externos. Se externos, deve ser garantido transporte.

É proibido preparar alimentos nos quartos.

### 24.7.6–24.7.10
Alojamentos devem dispor de infraestrutura para lavar/secar roupas ou lavanderia; pisos impermeáveis/laváveis; coleta diária de lixo; lavagem de roupa de cama; manutenção; renovação de vestuário de camas/colchões; sanitários higienizados diariamente; proibição de fogões/fogareiros nos quartos; controle de vetores conforme legislação local; avaliação médica de suspeita de doença infectocontagiosa.

## 24.8 — Vestimenta de trabalho

Vestimenta de trabalho é peça/conjunto destinado a atividades/condições que impliquem contato com sujidade, agentes químicos, físicos ou biológicos, ou melhor visualização do trabalhador; não é uniforme nem EPI.

O empregador deve fornecê-la gratuitamente, em tamanho/material adequados, substituir conforme vida útil/danos, fornecer quantidade adequada e higienizar quando a lavagem oferecer risco de contaminação. Quando inviável fornecer vestimenta exclusiva, deve assegurar higienização prévia ao uso.

## 24.9 — Disposições gerais

### Água potável
- água potável em todos os locais de trabalho;
- proibidos copos coletivos;
- bebedouro mínimo de 1 para cada 50 trabalhadores ou fração, ou sistema equivalente;
- recipientes portáteis hermeticamente fechados quando não houver água potável corrente;
- limpeza/higienização/manutenção periódica dos reservatórios;
- análise periódica de potabilidade;
- água não potável separada e sinalizada;
- proteção contra contaminação.

### Higiene
Locais de trabalho devem ser mantidos em estado de higiene compatível com o gênero da atividade. Limpeza, quando possível, fora do horário de trabalho e por processo que minimize levantamento de poeiras.

### Construção dos ambientes
Todos os ambientes previstos devem seguir código de obras local e possuir:

- cobertura adequada/resistente contra intempéries;
- paredes resistentes;
- pisos compatíveis com uso e circulação;
- iluminação segura contra acidentes.

Na ausência de código local:
- pé-direito mínimo 2,50 m;
- quartos de dormitórios com beliche: mínimo 3,00 m.

Instalações elétricas devem ser protegidas contra choque.

Trabalhadores devem poder interromper atividades para utilizar instalações sanitárias.

Instalações podem ser atendidas coletivamente em edificações com diversos estabelecimentos, mantendo o empregador responsável pela disponibilização.

Dimensionamento coletivo: maior número de trabalhadores por turno.

## Anexos

### Anexo I
Condições sanitárias e de conforto para trabalhadores em Shopping Center.

### Anexo II
Condições sanitárias e de conforto para trabalhadores em trabalho externo de prestação de serviços.

### Anexo III
Condições sanitárias e de conforto para trabalhadores em transporte público rodoviário coletivo urbano de passageiros em atividade externa.

**Core rule:** anexos são extensões normativas específicas e devem ser consultados quando o contexto da organização/atividade os enquadrar.

## Mathematical rule set

### General ceiling rule
Para proporções `1 para cada N trabalhadores ou fração`:

`quantidade_minima = ceil(trabalhadores_aplicáveis / N)`

### Mictórios pós-24/09/2019
Até 100 trabalhadores:
`ceil(N / 20)`

Acima de 100:
`ceil(100 / 20) + ceil((N - 100) / 50)`

O Core deve preservar a condição de data de construção antes de aplicar esta regra.

### Vestiário até 750
`area_unitaria = 1.5 - (N / 1000)`
`area_total_minima = N * area_unitaria`

### Vestiário > 750
`area_total_minima = N * 0.75`

### Módulos
O cálculo de módulos é **aplicação interna**, não regra da NR:

`modulos = ceil(area_total_exigida / area_util_modulo)`

Somente aplicar quando a diretriz/produto interno informar a área útil do módulo.

## Internal data captured from this conversation — NOT NR

### Módulo “sem bolsa”
- área interna útil informada pelo usuário: **13,56 m² por unidade**;
- classificação: DIRETRIZ/DADO INTERNO;
- não atribuir essa medida à NR-24;
- uso: variável de entrada para dimensionamento modular no Forge.

### Example captured from conversation
Para 200 trabalhadores, usando a fórmula do item 24.4.2:

`1.5 - (200 / 1000) = 1.30 m²/trabalhador`

`200 x 1.30 = 260 m²`

Com módulo interno de 13,56 m²:

`ceil(260 / 13.56) = 20 módulos`

**Classification:** cálculo derivado de requisito normativo + dado interno de produto. O resultado não é uma exigência da NR de “20 módulos”; é uma aplicação interna do Forge.

## Forbidden semantic shortcuts

1. Não transformar “1 instalação sanitária/20” em “1 vaso/20” sem explicitar a interpretação.
2. Não aplicar lavatório 1/10 a qualquer atividade sem verificar a condição do item 24.2.2.1.
3. Não aplicar chuveiro 1/10 ou 1/20 sem classificar a atividade segundo 24.3.5.
4. Não usar 75 cm/55 cm do antigo refeitório como requisito atual sem fonte vigente.
5. Não usar 1 m² por trabalhador em refeitório como requisito atual sem fonte vigente.
6. Não usar área de vestiário de 0,50/0,60 m² por trabalhador como se fosse texto da NR.
7. Não usar 3 m² por trabalhador como regra de alojamento: a NR atual especifica 3,00 m² por cama simples ou 4,50 m² por beliche, incluindo circulação e armário.
8. Não tratar diretriz interna como norma legal.
9. Não tratar produto modular existente como automaticamente conforme: conformidade depende do contexto, população, layout, instalações, acessibilidade e demais normas aplicáveis.
10. Não emitir “conforme NR” apenas porque a área total foi atingida; validar todos os requisitos aplicáveis.

## Retrieval keys

Consultas contendo `NR`, `NR-24`, `norma`, `norma regulamentadora`, `requisito normativo` ou item explícito devem priorizar esta base normativa e suas fontes oficiais.

Consultas contendo `Diretriz` devem priorizar a base interna de diretrizes, sem converter seu conteúdo em norma.

Consultas contendo ambos devem apresentar primeiro a exigência normativa e depois a diretriz interna, explicitamente separadas.

## Core/Forge boundary

**Core:** entende o significado normativo, autoridade, contexto, condições, exceções, relações, provenance e regras de cálculo.

**Forge:** recebe o conhecimento aprovado pelo Core e executa aplicações como:

- dimensionamento de módulos;
- cálculo de quantidade de equipamentos;
- validação de layouts;
- checklists;
- simuladores;
- geração de requisitos de projeto;
- testes de conformidade;
- comparação de alternativas;
- produção de evidências para revisão.

Forge não pode alterar o significado da NR. Divergência entre aplicação e norma retorna ao Core para classificação e decisão.

## Promotion rule

`Fonte externa -> extração -> normalização -> provenance -> interpretação Core -> contrato -> Forge -> teste -> evidência -> revisão -> promoção`

Nunca:

`Forge -> resultado operacional -> verdade normativa`
