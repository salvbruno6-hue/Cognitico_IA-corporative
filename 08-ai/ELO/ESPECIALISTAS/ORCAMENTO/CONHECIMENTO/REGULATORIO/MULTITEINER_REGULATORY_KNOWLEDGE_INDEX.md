# ELO — MULTITEINER REGULATORY KNOWLEDGE INDEX

## Purpose
Índice canônico para o conhecimento regulatório aplicável à natureza das obras e soluções Multiteiner. O índice orienta o ELO Core sobre quais famílias normativas devem ser consideradas e o ELO Forge sobre quais domínios devem ser aplicados, calculados e testados.

## Architecture
**Core entende e governa. Forge aplica, dimensiona, testa e evidencia.**

Nenhuma diretriz interna, cálculo derivado ou prática de projeto deve ser apresentado como texto de NR. Toda conclusão de conformidade deve preservar fonte, item, versão, condição de aplicação e evidência.

## Regulatory domains

| ID | Domínio | Fontes prioritárias | Aplicações Multiteiner |
|---|---|---|---|
| REG-01 | SST/GRO | NR-01, NR-07 | PGR, riscos, saúde ocupacional |
| REG-02 | EPI | NR-06 | fabricação, montagem, manutenção |
| REG-03 | Edificações | NR-08 + legislação/códigos | ambientes de trabalho |
| REG-04 | Elétrica | NR-10, NBR 5410 | alimentação, quadros, circuitos, proteção |
| REG-05 | Aterramento/equipotencialização | NR-10, NBR 5410 | módulos metálicos e instalações |
| REG-06 | SPDA | NBR 5419 + legislação aplicável | módulos/edificações sujeitas ao sistema |
| REG-07 | Construção | NR-18 | montagem, implantação, canteiro |
| REG-08 | Movimentação | NR-11 | carga, descarga, içamento, armazenamento |
| REG-09 | Máquinas | NR-12 | máquinas e equipamentos |
| REG-10 | Ergonomia | NR-17 | postos e áreas operacionais |
| REG-11 | Incêndio | NR-23 + Corpo de Bombeiros + NBRs aplicáveis | extintores, alarmes, iluminação, saídas |
| REG-12 | Sanitários | NR-24 | vasos, lavatórios, chuveiros |
| REG-13 | Vestiários | NR-24 | troca de roupa, armários, área |
| REG-14 | Refeitórios/cozinhas | NR-24 + sanitária + incêndio + elétrica + acessibilidade | preparação, distribuição, circulação |
| REG-15 | Acessibilidade | Lei 13.146/2015, NBR 9050, NBR 16537 + local | cadeirantes, mobilidade, rotas, sanitários |
| REG-16 | Hidráulica | NBR 5626 | água fria/quente |
| REG-17 | Esgoto | NBR 8160 | instalações sanitárias/cozinhas |
| REG-18 | Pluvial | NBR 10844 | coberturas e drenagem |
| REG-19 | Gás | normas técnicas + Corpo de Bombeiros + local | cozinhas/aquecimento quando aplicável |
| REG-20 | Resíduos | NR-25 + sanitária/ambiental/local | fabricação e operação |
| REG-21 | Sinalização | NR-26 + incêndio + acessibilidade | segurança, emergência, identificação |
| REG-22 | Altura | NR-35 | cobertura, montagem, manutenção |
| REG-23 | Estruturas | NBR 6120, 6123, 8681, 8800, 6118, 6122 conforme sistema | módulos, suportes, fundações |
| REG-24 | Projeto/representação | NBR 6492 e normas específicas | documentação técnica |

## Accessibility baseline
O Core deve avaliar acessibilidade como conjunto de requisitos, não apenas “cadeirante”: rota acessível, entradas, circulação, rampas, escadas, portas, manobra, transferência, sanitário acessível, sinalização e interfaces com emergência. A aplicabilidade depende do uso, ocupação, legislação e aprovação local.

## Electrical baseline
O Core deve relacionar NR-10 + NBR 5410 + requisitos locais + projeto elétrico. O Forge deve verificar circuitos, proteção, seccionamento, choque, cargas, quadros, tomadas, iluminação, equipotencialização, aterramento e documentação/testes conforme escopo.

## SPDA baseline
SPDA não é sinônimo de aterramento. O Core determina aplicabilidade e metodologia conforme NBR 5419 vigente, características da edificação, análise de risco e legislação local. O Forge verifica captação, descidas, aterramento, equipotencialização, DPS e evidências quando aplicáveis.

## Kitchen/circulation baseline
Para cozinha, nunca aplicar uma única “largura padrão” sem classificar a circulação. Core deve distinguir circulação operacional, circulação de serviço/material, rota acessível e rota de fuga. O conjunto pode envolver NR-24, NBR 9050, NR-10/NBR 5410, hidráulica/esgoto, gás, incêndio e requisitos sanitários/local.

## NR-24 knowledge anchors
- instalações sanitárias: regra de proporcionalidade conforme item vigente da NR-24;
- lavatórios e chuveiros: proporções condicionadas ao tipo de atividade/exposição;
- vestiário: obrigação vinculada às hipóteses normativas e dimensionamento conforme texto vigente;
- refeitórios/cozinhas: considerar também requisitos sanitários e demais sistemas aplicáveis;
- alojamentos: tratar separadamente de vestiário/refeitório.

## Internal Multiteiner directive boundary
**Módulo “sem bolsa” = 13,56 m² de área interna útil.**

Classificação: `INTERNAL_DIRECTIVE / PRODUCT_PARAMETER`.

Não é requisito da NR. Pode ser utilizado pelo Forge para dimensionamento.

Exemplo do projeto: para 200 trabalhadores e 260 m² de área exigida pelo critério de vestiário considerado, `CEILING(260 / 13,56) = 20 módulos`. O resultado é uma aplicação derivada e não uma obrigação normativa.

## Query routing
- palavra `NR` → base normativa NR;
- palavra `Diretriz` → base interna;
- `NR + Diretriz` → NR primeiro; diretriz separada e identificada;
- “atende a norma?” → Core identifica o conjunto regulatório aplicável antes de Forge calcular.

## Required metadata for every knowledge record
`source_type`, `source_identifier`, `title`, `edition/version`, `effective_date`, `section/item`, `requirement`, `condition`, `exception`, `formula`, `applicability`, `evidence`, `verification_method`, `provenance`, `status`.

## Status taxonomy
`SOURCE_REQUIREMENT | FACT | DERIVED_CALCULATION | INTERNAL_DIRECTIVE | HISTORICAL | INFERENCE | HYPOTHESIS | PROPOSAL`.

## Governance
A lista é uma matriz de aplicabilidade, não autorização para aplicar todas as fontes a toda obra. O Core deve analisar atividade, ocupação, local, risco, projeto, contrato e licenciamento. O Forge somente aplica regras cuja autoridade e condição de aplicação tenham sido resolvidas.
