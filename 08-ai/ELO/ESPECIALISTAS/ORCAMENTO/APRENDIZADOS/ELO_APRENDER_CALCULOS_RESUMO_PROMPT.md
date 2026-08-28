# ELO APRENDER — Prompt operacional de resumo de cálculos

## Objetivo

Durante `ELO APRENDER`, depois que a experiência da SO for reconstruída, executar uma etapa exclusiva para extrair **somente cálculos de orçamento**. As instruções, regras e conhecimento continuam sendo tratados pelo fluxo cognitivo existente no Git.

## Prompt operacional

> **VARRER_CÁLCULOS — SO {{SO_ID}}**
>
> Percorra a SO, PTS Técnica, Orçamento, PTS Pós-Orçamento e documentos/anexos disponíveis. Extraia somente cálculos efetivamente utilizados, avaliados ou aprendidos que tenham utilidade para orçamento.
>
> Não gere instruções, regras ou interpretação de governança nesta etapa.
>
> Para cada cálculo encontrado, produza um registro curto e estruturado com: `origem_so`, `origem_documento`, `item_origem`, `conceito`, `descricao`, `entrada`, `unidade`, `fonte`, `premissa`, `formula`, `subcalculo`, `resultado`, `unidade_resultado`, `validacao` e `status`.
>
> Considere, entre outros: excedentes; telhado/cobertura; esgoto subterrâneo; elétrica aérea; reforço estrutural; quantitativos derivados; áreas; comprimentos; volumes; pesos; dimensionamentos; conversões; rateios; produtividade; composição de preços; equivalências técnicas com impacto econômico.
>
> Se houver cálculo apenas implícito, reconstruí-lo somente quando a evidência documental permitir. Não invente fórmula, premissa, fonte ou resultado. Se houver apenas um preço isolado sem memória de cálculo identificável, não o classifique como cálculo.
>
> Se o mesmo cálculo aparecer em mais de um documento da SO, consolide em um único cálculo e preserve as ocorrências como evidências.
>
> Se o cálculo vier de outra SO, mantenha a SO anterior como origem. Ele é referência consultiva e não passa a ser cálculo da SO atual.
>
> Retorne o resultado em formato estruturado para persistência no Supabase, um cálculo por registro. Cada registro persistido deve receber `calculation_id` real.
>
> Se nenhum cálculo for encontrado, retornar `NO_CALCULATIONS_FOUND`.
>
> Se cálculo for encontrado mas não puder ser persistido, retornar `CALCULATION_NOT_REGISTERED` e manter a etapa pendente.

## Saída mínima esperada

```text
CALCULATION_SUMMARY
SO: {{SO_ID}}
STATUS: FOUND | NO_CALCULATIONS_FOUND | CALCULATION_NOT_REGISTERED
TOTAL: {{N}}

CALC-001
Documento: ...
Item: ...
Conceito: ...
Entrada: ...
Fonte: ...
Premissa: ...
Fórmula: ...
Subcálculo: ...
Resultado: ...
Validação: ...

CALC-002
...
```

## Persistência

O resumo é uma etapa de extração. A persistência operacional deve gravar os registros na tabela de memória de cálculos do Supabase, preservando a SO e o documento de origem. O Git recebe apenas a referência aos `calculation_id` quando essa ligação fizer parte do aprendizado.

## Relação com o fluxo principal

```text
ELO APRENDER
   ├── reconstrução da experiência
   ├── fluxo cognitivo → conhecimento/instruções → Git
   └── VARRER_CÁLCULOS → resumo de cálculos → Supabase
```

O resumo de cálculos não substitui nem reescreve o aprendizado instrucional.
