# ELO — Material Evolution Gate

## Status

`NORMATIVE / LABORATORY`

## Regra central

Toda implementação que pretenda ser reconhecida como evolução do ELO deve demonstrar **melhoria material mensurável** sobre uma linha de base. Executar corretamente, adicionar código, aumentar cobertura ou conectar componentes não constitui evolução suficiente por si só.

A implementação pode permanecer em laboratório sem alterar o canon quando a evidência ainda não demonstra melhoria material.

## Critério mínimo do primeiro gate

Uma proposta experimental deve apresentar:

- `delta >= 0.10` entre resultado observado e baseline, em escala normalizada `0..1`;
- confiança da evidência `>= 0.70`;
- pelo menos `2` execuções comparáveis;
- ausência de regressão;
- provenance e evidências reconstruíveis;
- tenant scope preservado;
- hipótese explícita de utilidade e generalização;
- reutilização da autoridade canônica existente.

Esses valores são um **piso do laboratório**, não uma garantia de promoção.

## O que conta como melhoria

A melhoria deve ser vinculada à missão e ao mecanismo alterado. Exemplos de dimensões válidas:

- qualidade do resultado;
- precisão/consistência;
- redução de erro ou retrabalho;
- redução de custo/latência sem perda de qualidade;
- aumento de cobertura de casos válidos;
- melhor rastreabilidade/provenance;
- maior capacidade de generalização sem violar tenant ou governança.

A métrica deve ser comparável com uma baseline explícita. Não é permitido fabricar score ou tratar ausência de medição como melhoria.

## Fluxo obrigatório

`BASELINE → HIPÓTESE → EXPERIMENTO → EVIDÊNCIA → COMPARAÇÃO → IMPACTO MATERIAL → LABORATÓRIO → GOVERNED LEARNING → EVOLUTION GATE → PROMOÇÃO GOVERNADA`

Falha em qualquer gate mantém o resultado como `LAB_ONLY` ou bloqueado conforme a causa.

## Regra de arquitetura

A busca por evolução material não autoriza:

- segundo Core;
- segunda memória canônica;
- segundo router de seleção;
- segundo provider registry;
- segundo Evolution Gate;
- alteração inferida de Soul/Core/canon;
- promoção automática;
- cruzamento de tenants.

O objetivo é **aumentar capacidade sem multiplicar autoridade**.

## Aplicação ao Budget Intelligence

O runtime deve medir uma configuração de execução como:

`mission + capability + specialist/context + model + tool + method`

A configuração observada é evidência experimental. Uma única execução não pode declarar um novo padrão ótimo. O ganho deve ser comparado contra baseline e submetido ao caminho governado já existente.

## Resultado esperado para a Simbionte

A Simbionte não deve apenas acumular experiências. Ela deve identificar quais mecanismos produziram melhoria material, quais condições permitiram o ganho, quais limites foram encontrados e se o padrão é generalizável.

Assim, o aprendizado útil passa a ser:

`experiência → relação → hipótese → experimento → comparação → melhoria material → candidato → validação → evolução governada`.
