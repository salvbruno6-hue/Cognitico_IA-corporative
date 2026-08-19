# ADR — Consolidação das Árvores Português/English do ELO

- **Status:** APPROVED FOR CONTROLLED CONSOLIDATION
- **Data:** 2026-08-19
- **Escopo:** organização documental e arquitetural do repositório
- **Não escopo:** mudança do Cognitive Core, contratos executáveis ou comportamento runtime

## 1. Decisão

O repositório terá **uma única árvore estrutural canônica por camada**. A árvore operacional atualmente definida em inglês será a autoridade de localização para novos artefatos. Conteúdo português existente que represente o mesmo conceito será **migrado para o proprietário canônico**, preservando conteúdo, histórico rastreável e referências necessárias.

Nenhum conteúdo será apagado apenas por diferença de idioma. Antes de remover uma árvore histórica, seus arquivos devem ser classificados como:

- DUPLICADO_EQUIVALENTE — mesmo conceito e mesma finalidade;
- COMPLEMENTAR — mesmo domínio, mas informação adicional;
- CONFLITANTE — mesmo conceito com regras/conteúdo incompatível;
- EXCLUSIVO — não possui equivalente seguro;
- HISTÓRICO — deve ser preservado como registro de evolução.

## 2. Evidência da auditoria inicial

A auditoria do `main` confirmou que algumas árvores portuguesas contêm material substantivo enquanto as equivalentes inglesas permanecem apenas como scaffolding ou possuem conteúdo muito menor. Exemplos confirmados:

- `01-meta-arquitetura/` contém documentos de inteligência de demanda, mapa de domínios, glossário, modelo conceitual, entidades, relacionamentos, regras de negócio e arquitetura mestre; `01-meta-architecture/` possui apenas README, `.gitkeep` e a subárvore `cognitive-architecture`.
- `05-cognitivo-plataforma/` contém fundamentos cognitivos, filosofia, recursos estratégicos, inteligência de demanda, modelo de conhecimento e RAG; `05-cognitive-platform/` contém a estrutura operacional mais recente, incluindo engine cognitivo, decision engine, memory/reasoning, especialistas e contratos Multiteiner.
- `07-engenharia-de dados/` contém modelo lógico, dicionário, SQLite, APIs, eventos e master de engenharia de dados; `07-data-engineering/` possui atualmente apenas scaffolding/README/AGENTS.
- `11-modelos/` contém `MODELS_LIBRARY_MASTER.md`, enquanto `11-models-library/` possui apenas `.gitkeep`.
- `12-sistemas/` contém `SYSTEMS_ENGINEERING_MASTER.md`, enquanto `12-system-engineering/` possui apenas `.gitkeep`.

Esses fatos indicam que a duplicidade é principalmente **histórica/organizacional**, e não prova de duas arquiteturas independentes.

## 3. Estratégia de migração segura

1. Não alterar `src/elo/` nesta consolidação.
2. Não alterar contratos canônicos ou schemas executáveis por motivo de nomenclatura.
3. Fazer inventário antes de cada movimentação.
4. Copiar/migrar primeiro para a árvore canônica.
5. Verificar links, referências, imports e índices.
6. Só depois marcar a árvore portuguesa como DEPRECATED/SUPERSEDED ou removê-la quando não houver conteúdo exclusivo.
7. Manter referências históricas em ADR/índice quando necessário.
8. Executar CI/gates após cada lote significativo.

## 4. Regra de conflito

Se os conteúdos não forem equivalentes, não fazer merge textual automático. O artefato com maior autoridade permanece vigente e o conteúdo complementar ou conflitante será encaminhado para revisão específica.

## 5. Critério de segurança

A consolidação só pode ser considerada concluída quando:

- nenhuma nova arquitetura é criada;
- cada conceito possui um único proprietário canônico;
- referências antigas são resolvidas ou registradas;
- conteúdo exclusivo não foi perdido;
- provenance/histórico permanece rastreável;
- CI permanece verde;
- `ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md` e `ELO_REPOSITORY_NAVIGATION_RULES.md` refletem o estado real.

## 6. Resultado esperado

A organização final será:

`um conceito → um proprietário canônico → múltiplas referências permitidas → nenhum segundo authority path`.

Português e inglês passam a ser idiomas de documentação, não arquiteturas paralelas.
