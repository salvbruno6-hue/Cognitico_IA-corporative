# Memory — Cognitive Domain

Domínio de memória cognitiva do ELO. Persiste o estado dos ciclos de decisão, precedentes e calibração produzidos pelo Cognitive Runtime Loop (CRL).

## Subpastas

| Subpasta | Conteúdo |
|---|---|
| decisions/ | Ciclos de decisão (DecisionLifecycle serializado) |
| precedents/ | Índice de precedentes fechados |
| calibration/ | Modelo de calibração acumulado |

## Convenção

Segue a convenção de memory/solicitations/:

- index.json no nível do domínio, contendo catálogo
- index.json no nível do item, contendo agregados + proveniência
- README.md no nível do item, explicando origem

## Fontes Canônicas

- Core: src/elo/core/{decision_outcome_loop,precedent_index,calibration}.py
- Runtime: src/elo/cognitive/runtime/
- Governança: 09-governance/contracts/
