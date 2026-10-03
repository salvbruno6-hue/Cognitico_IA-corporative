# Auditoria de tabelas — referência histórica comparável

## Objetivo

Verificar se as estruturas existentes suportam a primeira etapa do novo fluxo de crescimento: reconstruir setembro/2025–fevereiro/2026 com a mesma estrutura que será utilizada na previsão setembro/2026–fevereiro/2027.

## Estado verificado

| Estrutura | Papel | Situação | Decisão |
|---|---|---|---|
| `mt_pedidos_venda` | origem comercial confirmada | sem registros | reutilizar |
| `mt_pedidos_venda_itens` | produto/modelo + quantidade | sem registros | reutilizar |
| `modelos` | identidade do produto | 21 registros | reutilizar |
| `taxonomia` | classificação do produto | 27 registros | reutilizar |
| `mt_demanda_historico` | base histórica | sem registros | reutilizar e aguardar carga histórica |
| `mt_previsoes_demanda` | base futura prevista | sem registros | reutilizar e aguardar previsão Comercial |
| `mt_balanco_demanda` | balanço PCP | sem registros | não usar como referência histórica neste gate |
| `lista_mae` | composição/material | 474 registros | não usar no cálculo do fator |
| `estrutura_modular` | configuração estrutural | sem registros | não bloquear o gate |
| `estrutura_modular_itens` | composição estrutural | sem registros | não usar para inferir função |

## Evidências relevantes

`modelos` possui vínculo direto com `taxonomia`.

A taxonomia existente distingue, entre outros tipos, `Módulo` e `Contêiner`. Portanto, a separação do produto deve ser feita pelo domínio de produto existente, não por texto criado na camada de cálculo.

`mt_pedidos_venda_itens` já possui `modelo_id`, `lista_mae_id` e `quantidade`. Isso permite ligar demanda comercial a produto sem criar uma nova tabela de demanda comercial.

`mt_demanda_historico` e `mt_previsoes_demanda` já possuem `modelo_id`, período, quantidade e os campos `natureza_demanda` e `chave_comparabilidade` adicionados para esta finalidade.

## Ajuste de semântica

Os campos de natureza e comparabilidade receberam comentários de governança para deixar explícito que:

- natureza classifica a demanda;
- chave identifica a referência equivalente;
- nenhum dos dois representa mão de obra;
- ausência de chave não pode ser preenchida por inferência.

Para `EVENTO` e `SPOT`, a nova visão marca ausência de chave como `SEM_CHAVE_COMPARABILIDADE`.

Para outras naturezas, a ausência de chave pode permitir apenas uma comparação potencial, que ainda exige validação.

## Nova camada analítica

`v_elo_pcp_referencia_demanda_comparavel` foi criada com `security_invoker = true`.

Ela reúne, no mesmo nível analítico:

- tenant;
- modelo;
- código e nome do modelo;
- taxonomia;
- natureza;
- chave de comparabilidade;
- quantidade histórica;
- período histórico;
- quantidade prevista;
- período previsto;
- estado de comparabilidade.

Estados:

- `COMPARAVEL_POTENCIAL`;
- `SEM_HISTORICO`;
- `SEM_PREVISAO`;
- `SEM_CHAVE_COMPARABILIDADE`;
- `SEM_NATUREZA`.

A view **não calcula fator**, produtividade, composição funcional ou demanda humana.

## Regra de não duplicação

Não foi criada uma nova tabela para armazenar demanda comercial, porque as tabelas existentes já possuem as relações necessárias.

Não foi criada tabela de produtividade.

Não foi criada tabela de RH.

Não foi criado campo de chassi.

## Próximo dado necessário

O sistema agora precisa receber os dados reais de:

1. previsão Comercial de setembro/2026–fevereiro/2027;
2. histórico equivalente de setembro/2025–fevereiro/2026;
3. natureza de cada demanda;
4. chave de comparabilidade quando necessária;
5. modelo/taxonomia correspondente.

Somente após essa carga será possível verificar quais linhas são efetivamente comparáveis.

## Gate

> **Sem histórico e previsão reais, a estrutura está pronta, mas nenhum fator deve ser calculado.**

Esse estado é intencional.