# ELO APRENDER — Extração obrigatória de cálculos

## Regra canônica

Ao executar `ELO APRENDER` sobre uma Solicitação de Orçamento, o ELO deve extrair, além das instruções/conhecimentos, **todos os cálculos efetivamente usados, avaliados ou aprendidos na solicitação** que sejam relevantes para orçamento.

Exemplos não exaustivos:

- composição de excedentes;
- estrutura/cobertura de telhado;
- instalação de esgoto subterrâneo;
- elétrica aérea;
- reforço estrutural;
- quantitativos derivados;
- equivalências técnicas com impacto de custo;
- conversões de unidade;
- dimensionamentos e memórias de cálculo;
- composições de preço calculadas;
- rateios, áreas, comprimentos, pesos ou volumes usados para formar valores.

## Momento da extração

A extração ocorre **durante o gatilho `ELO APRENDER`**, depois da reconstrução da experiência e antes da consolidação final do aprendizado.

Fluxo:

`SO → PTS Técnica → Orçamento → PTS Pós → identificar cálculos → reconstruir cálculo → validar → registrar no Supabase → consolidar instrução no Git → commit/PR/merge`

## O que deve ser extraído

Para cada cálculo identificado, preservar, quando disponível:

1. SO de origem;
2. documento de origem;
3. item/subitem de origem;
4. conceito associado;
5. entradas e unidades;
6. fonte;
7. premissas;
8. fórmula;
9. subcálculos;
10. resultado;
11. unidade do resultado;
12. validação/evidência;
13. relação com custo ou orçamento;
14. status de avaliação;
15. identificador persistente do cálculo no Supabase.

## Separação Git × Supabase

**Git:** instruções, interpretação, conhecimento, governança e critérios aprendidos.

**Supabase:** somente a memória estruturada dos cálculos aprendidos/avaliados.

O arquivo de aprendizado no Git deve referenciar os `calculation_id` reais quando existirem. Não duplicar a memória de cálculo detalhada no Git.

## Proveniência

Um cálculo encontrado em outra SO é uma **referência consultiva**, não a origem da solicitação atual. Ao reutilizá-lo, o ELO deve informar fonte, características comparadas, equivalência, motivo de aplicabilidade e necessidade de validação.

## Falha de registro

Se um cálculo for identificado mas não puder ser registrado no Supabase, a experiência não deve ser marcada como plenamente consolidada. Registrar `CALCULATION_NOT_REGISTERED` e manter a pendência para retomada.

Nunca inventar fórmula, premissa, resultado, fonte ou `calculation_id`.

## Critério de completude

Uma experiência de orçamento somente pode ser considerada consolidada quando:

- os aprendizados instrucionais aplicáveis estiverem consolidados no Git;
- os cálculos identificados tiverem sido registrados/confirmados no Supabase, ou explicitamente classificados como não aplicáveis;
- a proveniência estiver preservada;
- os commits aplicáveis estiverem confirmados;
- a governança de aprovação estiver respeitada.
