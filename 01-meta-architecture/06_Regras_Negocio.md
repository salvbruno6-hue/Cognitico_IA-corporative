# Regras de Negócio do ELO

## Objetivo

Estabelecer regras de negócio transversais que preservem coerência entre estratégia, domínios, dados, conhecimento, decisões e capacidades cognitivas.

## BR-001 — Orientação à decisão

Todo dado, integração, modelo analítico ou capacidade cognitiva incorporado ao ELO deve estar associado a uma necessidade operacional, pergunta de negócio ou decisão relevante.

## BR-002 — Recursos estratégicos

O ELO deve ser organizado prioritariamente pelos recursos estratégicos do negócio e não pela estrutura administrativa de departamentos.

## BR-003 — Fonte de verdade

Cada informação crítica deve possuir uma fonte de verdade identificada. O ELO não deve criar cópias concorrentes sem necessidade arquitetural explícita.

## BR-004 — Rastreabilidade

Previsões, recomendações, alertas e decisões assistidas devem manter vínculo com fontes, contexto, regras, modelos e evidências que contribuíram para sua geração.

## BR-005 — Separação de responsabilidades

Domínio, aplicação, dados, infraestrutura e IA devem manter responsabilidades explícitas. Regras centrais de negócio não devem ser deslocadas para interfaces ou infraestrutura.

## BR-006 — Sistemas especialistas

Funções administrativas e transacionais permanecem nos sistemas especialistas quando não fizer sentido incorporá-las ao ELO. A integração ocorre quando seus dados forem necessários ao planejamento, operação, conhecimento ou governança.

## BR-007 — Demanda e capacidade

Nenhum plano de demanda deve ser considerado executável sem confronto com capacidade produtiva, materiais, recursos operacionais e restrições de tempo relevantes.

## BR-008 — Forecast

Toda previsão deve registrar horizonte, data de geração, entradas, premissas, versão e medida de confiança ou erro quando disponível.

## BR-009 — Retroalimentação

Resultados reais de produção, suprimentos, logística, operação e manutenção devem retroalimentar os modelos e análises que suportam decisões futuras.

## BR-010 — Engenharia

Revisões de modelos, produtos, componentes e BOM devem preservar histórico e impacto para permitir análise de retrabalho, custo, confiabilidade e recorrência.

## BR-011 — Suprimentos

Necessidades de compra devem considerar demanda prevista, estoque disponível, cobertura, criticidade, lead time e capacidade de fornecimento.

## BR-012 — Produção

Sequenciamento e planejamento de produção devem considerar capacidade, gargalos, instalações, recursos, horas previstas e impacto de setup.

## BR-013 — Manutenção

Falhas e reincidências devem ser relacionadas, quando possível, a modelos, componentes, fornecedores e condições operacionais para retroalimentar decisões de engenharia e suprimentos.

## BR-014 — Conhecimento

Conhecimento usado para decisão deve possuir origem, contexto e estado de validade identificáveis.

## BR-015 — IA governada

A IA pode analisar, recomendar e automatizar dentro de limites definidos, mas não deve ocultar a origem do contexto nem eliminar controles humanos exigidos pela governança.

## BR-016 — RAG

Conteúdo recuperado por RAG deve respeitar permissões, validade, proveniência e escopo do usuário ou agente solicitante.

## BR-017 — Auditoria

Ações relevantes executadas ou recomendadas por componentes cognitivos devem ser registradas de forma suficiente para auditoria posterior.

## BR-018 — Evolução arquitetural

Alterações que modifiquem fronteiras de domínio, responsabilidades centrais, fontes de verdade ou princípios estruturais devem ser documentadas por decisão arquitetural apropriada.

## BR-019 — Qualidade

Dados e conhecimento críticos devem possuir critérios mínimos de completude, consistência, atualidade e confiabilidade adequados à decisão suportada.

## BR-020 — Segurança

Acesso a dados, conhecimento, APIs e capacidades cognitivas deve seguir princípio de menor privilégio e controles definidos pela governança.

## Aplicação

Estas regras funcionam como baseline transversal. Regras específicas de cada domínio devem complementar este documento sem contradizê-lo.

## Rastreabilidade

Este documento deve permanecer coerente com o Mapa de Domínios, Modelo Conceitual, Entidades, Relacionamentos, Filosofia do ELO, Recursos Estratégicos, Knowledge Model, RAG e documentos de governança.
