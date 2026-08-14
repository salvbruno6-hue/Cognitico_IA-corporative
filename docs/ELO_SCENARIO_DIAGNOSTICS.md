# ELO — Scenario Diagnostics

## Objetivo

O ELO não deve diagnosticar um cenário por uma única ótica. Antes de recomendar uma decisão, deve comparar perspectivas compatíveis com a pergunta e com as evidências disponíveis.

## Perspectivas canônicas

`BASELINE` representa o estado de referência.

`STRESS` representa deterioração controlada de uma ou mais variáveis relevantes.

`FAILURE` representa uma ruptura ou indisponibilidade explicitamente definida.

`COUNTERFACTUAL` compara uma decisão alternativa com a situação observada.

`SENSITIVITY` verifica como uma mudança em uma variável altera o resultado observado.

## Critérios de leitura

O diagnóstico deve separar:

- fatos sustentados por evidência;
- variações observadas;
- hipóteses e pressupostos;
- riscos;
- lacunas de informação;
- conflitos entre fontes;
- recomendação.

Ausência de evidência impede diagnóstico conclusivo. Pressuposto não pode ser promovido silenciosamente a fato.

## Critérios de teste

Cada cenário deve demonstrar:

1. identificação do estado de referência;
2. alteração explícita das variáveis;
3. cálculo/registro do delta observado;
4. rastreabilidade para evidências;
5. preservação das incertezas;
6. bloqueio quando não houver evidência suficiente;
7. comportamento consistente entre tipos de cenário;
8. capacidade de comparar cenários sem alterar o estado canônico.

## Critério de decisão

`decision_ready` não significa que o ELO deve executar uma decisão. Significa somente que o cenário possui evidência e observações suficientes para entrar no próximo estágio de reasoning/governança.

A decisão continua sujeita a política, impacto, autoridade humana quando exigida e Evolution Gate.

## Aplicação à operação

A camada deve ser reutilizável por produção, compras, estoque, PCP, expedição, financeiro e outros domínios. Ela não deve duplicar o modelo de domínio. Os adaptadores fornecem variáveis e evidências; esta camada fornece a leitura comparativa.
