# Cognitive Platform

Camada cognitiva operacional do ecossistema ELO. É o owner canônico dos fundamentos, motores cognitivos, memória, raciocínio, decisão, conhecimento, RAG e integrações cognitivas governadas.

## Fluxo lógico

1. **Fundamentos e filosofia** — define princípios e limites cognitivos.
2. **Recursos e demanda** — traduz capacidade, contexto e demanda em objetos de decisão.
3. **Conhecimento** — estrutura conhecimento para reutilização, recuperação e evolução.
4. **RAG e grounding** — organiza recuperação e montagem de contexto rastreável.
5. **Motores cognitivos** — executa raciocínio, memória, decisão e demais capacidades especializadas.
6. **Aplicações e Forge** — conecta capacidades cognitivas a contratos de domínio e execução governada.
7. **Aprendizado e retroalimentação** — registra evidências e evolução sem transformar histórico em verdade não validada.

## Artefatos fundamentais

- `COGNITIVE_FUNDAMENTALS.md` — fundamentos da plataforma.
- `CORE-004_Filosofia_do_ELO.md` — princípios filosóficos e arquiteturais.
- `CORE-007_Recursos_Estrategicos.md` — recursos estratégicos e operacionais relevantes à decisão.
- `INTELIGENCIA_DE_DEMANDA.md` — entrada analítica e ciclo de previsão, cenários e recomendações.
- `KNOWLEDGE_MODEL.md` — organização conceitual do conhecimento.
- `RAG.md` — recuperação aumentada e montagem de contexto.
- `ELO_COGNITIVE_ENGINE.md` — motor cognitivo.
- `ELO_DECISION_ENGINE.md` — motor de decisão.
- `ELO_MEMORY_ENGINE.md` — memória governada.
- `ELO_REASONING_ENGINE.md` — raciocínio.
- `ELO-018-GOVERNED-CYCLE-MEMORY.md` — memória do ciclo governado.
- `MULTITEINER_CORE_FORGE_REGULATORY_APPLICATION.md` — aplicação regulatória Core Forge.
- `NR24_CORE_FORGE_CONTRACT.md` — contrato regulatório NR-24.

## Ownership

`05-cognitive-platform/` é o único owner canônico da família 05. A antiga raiz `05-cognitivo-plataforma/` é apenas proveniência histórica durante a migração e não deve voltar a receber conteúdo novo.

## Regra de manutenção lógica

Antes de criar ou mover um artefato, o ELO deve verificar identidade, finalidade, duplicidade, complementaridade, consumidores e referências. Conteúdo útil deve ser incorporado ao owner canônico; conteúdo concorrente deve ser reconciliado; conteúdo obsoleto deve ser removido somente após validação. O caminho físico nunca é a identidade do conhecimento.

## Critério de consolidação

A família só pode ser considerada fisicamente consolidada após:

- classificação arquivo a arquivo concluída;
- conteúdo útil incorporado ao owner canônico;
- referências e aliases reconciliados;
- consumidores auditados;
- testes de resolução aprovados;
- CI e gates do ELO verdes;
- remoção física da raiz legada validada.
