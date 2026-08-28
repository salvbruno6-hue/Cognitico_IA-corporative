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
> Primeiro crie/recupere uma execução em `elo_orcamento_calculo_varreduras` com `learning_id`, `origem_so` e status `EM_ANALISE`. Essa execução é o cursor da varredura.
>
> Para cada cálculo encontrado, produza um registro compatível com `elo_orcamento_calculos_aprendidos`: `learning_id`, `varredura_id`, `origem_so`, `origem_documento`, `item_origem`, `conceito_key`, `descricao`, `categoria`, `entrada` (JSON), `fonte`, `premissa`, `formula`, `subcalculo` (JSON), `resultado` (JSON), `unidade_resultado`, `validacao`, `status`, `origem_tipo`, `referencia_so`, `aplicabilidade`, `evidencia` e `hash_calculo`.
>
> Categorias mínimas: `QUANTITATIVO`, `EXCEDENTE`, `ESTRUTURA`, `COBERTURA`, `HIDRAULICA_ESGOTO`, `ELETRICA`, `CLIMATIZACAO`, `MANUTENCAO`, `MAO_DE_OBRA`, `MONTAGEM`, `LOGISTICA`, `ACOPLAMENTO`, `ART_RRT`, `AREA_AMBIENTE`, `EQUIPAMENTO`, `COMPOSICAO_PRECO`, `EQUIVALENCIA_TECNICA` e `OUTRO`.
>
> Considere, entre outros: excedentes; telhado/cobertura; esgoto subterrâneo; elétrica aérea; reforço estrutural; quantitativos derivados; áreas; comprimentos; volumes; pesos; dimensionamentos; conversões; rateios; produtividade; composição de preços; equivalências técnicas com impacto econômico.
>
> Se houver cálculo apenas implícito, reconstruí-lo somente quando a evidência documental permitir. Não invente fórmula, premissa, fonte ou resultado. Se houver apenas um preço isolado sem memória de cálculo identificável, não o classifique como cálculo.
>
> Se o mesmo cálculo aparecer em mais de um documento da SO, consolide em um único cálculo usando `hash_calculo` e registre cada ocorrência na tabela `elo_orcamento_calculo_evidencias`, vinculada pelo `calculo_id`.
>
> Se o cálculo vier de outra SO, mantenha a SO anterior em `origem_so`, preencha `referencia_so` com a SO atual e descreva em `aplicabilidade` por que a referência pode se aplicar. Nunca alterar a origem do cálculo.
>
> O campo `status` do cálculo deve refletir a situação real: `CALCULATION_CONFIRMED`, `CALCULATION_PARTIAL`, `CALCULATION_REFERENCE` ou `CALCULATION_NOT_RECONSTRUCTABLE`.
>
> Ao finalizar a varredura, atualizar `elo_orcamento_calculo_varreduras` com os totais por status e `concluido_em`. Se houver falha de persistência, manter a execução como pendente e retornar `CALCULATION_NOT_REGISTERED`; não declarar a experiência plenamente consolidada.
>
> Retorne o resultado em formato estruturado para persistência no Supabase, um cálculo por registro. Cada registro persistido deve receber `calculation_id` real (`elo_orcamento_calculos_aprendidos.id`).
>
> Se nenhum cálculo for encontrado, retornar `NO_CALCULATIONS_FOUND` e registrar a varredura concluída com `total_sem_calculo`.

## Saída mínima esperada

```text
CALCULATION_SUMMARY
SO: {{SO_ID}}
VARREDURA_ID: {{UUID}}
STATUS: FOUND | NO_CALCULATIONS_FOUND | CALCULATION_NOT_REGISTERED
TOTAL: {{N}}

CALC-001
calculation_id: ...
Categoria: ...
Documento: ...
Item: ...
Conceito: ...
Entrada: ...
Unidade: ...
Fonte: ...
Premissa: ...
Fórmula: ...
Subcálculo: ...
Resultado: ...
Unidade do resultado: ...
Validação: ...
Origem SO: ...
Referência SO: ...
Aplicabilidade: ...

CALC-002
...
```

## Persistência — contrato

A tabela `elo_orcamento_calculo_varreduras` registra a execução do subfluxo e seus totais.

A tabela `elo_orcamento_calculos_aprendidos` é a memória canônica do cálculo. Ela recebe a reconstrução estruturada e o `calculation_id`.

A tabela `elo_orcamento_calculo_evidencias` registra múltiplas ocorrências/documentos que sustentam o mesmo cálculo.

`elo_orcamento_memoria` não deve receber a memória matemática detalhada quando o objetivo for apenas registrar cálculo; ele continua reservado ao fluxo de memória/conhecimento de orçamento já existente.

## Relação com o fluxo principal

```text
ELO APRENDER
   ├── reconstrução da experiência
   ├── fluxo cognitivo → conhecimento/instruções → Git
   └── VARRER_CÁLCULOS
          ├── execução → elo_orcamento_calculo_varreduras
          ├── cálculos → elo_orcamento_calculos_aprendidos
          └── evidências → elo_orcamento_calculo_evidencias
```

O subfluxo de cálculos não substitui, duplica ou reescreve o aprendizado instrucional.
