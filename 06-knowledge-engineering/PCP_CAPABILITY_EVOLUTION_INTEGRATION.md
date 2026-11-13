# PCP ↔ EVOLUÇÃO_DE_CAPACIDADES

A integração entre PCP e o gatilho transversal da Simbionte é feita por
evidência e por delegação, não por duplicação de autoridade.

```
PCP
  ↓
confrontação
  ↓
diagnóstico
  ↓
PCP Operational Evidence Package
  ↓
PCP Capability Evolution Bridge
  ↓
EVOLUÇÃO_DE_CAPACIDADES
  ↓
diagnóstico de curvatura
  ↓
proposta/experimento
  ↓
Evolution Gate
  ↓
governança
```

## Regra de propriedade

- PCP é proprietário das métricas e fatos do domínio PCP.
- O bridge somente transporta medições explicitamente fornecidas.
- EVOLUÇÃO_DE_CAPACIDADES é proprietário da leitura de evolução.
- Evolution Gate permanece proprietário da decisão de evolução.
- Learning Governance permanece proprietário da promoção/candidato.

## Regra de não-inferência

O bridge não transforma `diagnosis.status`, quantidade produzida, capacidade,
estoque, prazo ou qualquer outro contador PCP em `baseline/current` de
capacidade automaticamente.

Para entrar no gatilho de evolução, a medição deve chegar explicitamente com:

- item;
- baseline;
- current;
- direction;
- measurement_period;
- evidence_refs.

Dados ausentes permanecem ausentes.

## Independência

A implementação PCP não importa `symbiont_capability_evolution`. O contrato
usa factories/callables injetados. Assim, PCP pode ser testado sem Symbiont e
Symbiont pode consumir evidência de outros domínios.

A conexão canônica entre as branches ocorre quando a capacidade
`EVOLUÇÃO_DE_CAPACIDADES` estiver disponível no runtime alvo; o bridge não
cria uma segunda implementação.
