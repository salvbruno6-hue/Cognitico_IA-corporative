# ELO Forge — Matriz de Validação

| Gate | Pergunta | Evidência mínima | Falha |
|---|---|---|---|
| G1 | O objetivo está definido? | objetivo observável | parar |
| G2 | O limite canônico foi lido? | contrato/regra identificada | parar |
| G3 | A construção está completa? | artefatos identificados | corrigir |
| G4 | Foi testada? | resultado de teste | corrigir/justificar |
| G5 | Há evidência rastreável? | fonte ou resultado | parar |
| G6 | Foi comparada ao cânone? | compatibilidade/divergência | corrigir |
| G7 | Existe decisão explícita? | estado de decisão | parar |
| G8 | Existe reversão? | rollback ou justificativa | parar |

## Critério de promoção

A promoção é consequência da passagem pelos gates; não é consequência da existência do artefato.

```
CONSTRUÍDO ≠ VALIDADO ≠ PROMOVIDO
```

## Estados

- **EM CONSTRUÇÃO** — trabalho ainda aberto.
- **TESTADO** — teste executado, sem promoção.
- **VALIDADO** — compatibilidade demonstrada nos critérios aplicáveis.
- **CANDIDATO** — pronto para o fluxo de promoção.
- **REJEITADO** — incompatível ou sem justificativa suficiente.
- **ISOLADO** — preservado para análise sem integração.
