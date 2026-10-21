# Evidence — Visão Diretiva Comercial e Estoque

**Data da validação:** 2026-10-21  
**Regra:** `DIRETORIA_COMERCIAL_ESTOQUE_V1`  
**Fonte:** `Cópia de Relatório Comercial (1).csv`  
**SHA-256:** `181cba3132f844e855fa8f846ef25b7f1b41d6d147bc33acda5bda59e4daf59a`

## Estado efetivo no Supabase

Objetos implantados:

- `elo_private.pcp_diretoria_comercial_mensal`;
- `public.v_elo_diretoria_comercial_estoque`.

Carga analítica atual para o horizonte de planejamento outubro/2026–setembro/2027:

- 600 linhas `PREVISAO_BASE`;
- 24 linhas no nível `FAMILIA` — 2 famílias × 12 meses;
- 576 linhas no nível `MODELO` — 48 combinações família/modelo × 12 meses;
- 31 modelos/famílias de origem classificados como `CONTEINER` na fonte;
- 17 modelos/famílias de origem classificados como `MODULO` na fonte.

Os valores permanecem em `REGISTRO_EQUIVALENTE`. A view não calcula saldo contra estoque físico enquanto não houver reconciliação com quantidade física, tenant e modelo canônico.

## Política mensal de estoque por família

### CONTÊINER

| Mês | mínimo SPOT (P75) | segurança | alvo SPOT (P90) | reserva EVENTO (P75) | proteção comercial |
|---|---:|---:|---:|---:|---:|
| Jan | 42 | 23 | 65 | 9 | 74 |
| Fev | 42 | 28 | 70 | 11 | 81 |
| Mar | 63 | 6 | 69 | 0 | 69 |
| Abr | 59 | 2 | 61 | 5 | 66 |
| Mai | 61 | 5 | 66 | 16 | 82 |
| Jun | 75 | 5 | 80 | 8 | 88 |
| Jul | 70 | 6 | 76 | 14 | 90 |
| Ago | 82 | 9 | 91 | 3 | 94 |
| Set | 69 | 14 | 83 | 2 | 85 |
| Out | 70 | 28 | 98 | 3 | 101 |
| Nov | 46 | 8 | 54 | 7 | 61 |
| Dez | 42 | 8 | 50 | 9 | 59 |

### MÓDULO

| Mês | mínimo SPOT (P75) | segurança | alvo SPOT (P90) | reserva EVENTO (P75) | proteção comercial |
|---|---:|---:|---:|---:|---:|
| Jan | 21 | 16 | 37 | 44 | 81 |
| Fev | 20 | 6 | 26 | 49 | 75 |
| Mar | 35 | 3 | 38 | 18 | 56 |
| Abr | 26 | 8 | 34 | 52 | 86 |
| Mai | 26 | 7 | 33 | 115 | 148 |
| Jun | 40 | 3 | 43 | 20 | 63 |
| Jul | 22 | 18 | 40 | 60 | 100 |
| Ago | 52 | 9 | 61 | 34 | 95 |
| Set | 25 | 1 | 26 | 52 | 78 |
| Out | 33 | 5 | 38 | 17 | 55 |
| Nov | 23 | 7 | 30 | 25 | 55 |
| Dez | 29 | 2 | 31 | 100 | 131 |

Esses números são referências estatísticas da frequência de registros comerciais, não quantidades físicas de módulos/contêineres.

## Campos executivos disponíveis na view

Filtros/dimensões:

- `nivel_analise` (`FAMILIA`/`MODELO`);
- `familia_produto` (`MODULO`/`CONTEINER`);
- `modelo_chave_normalizada` / `modelo_nome_apresentacao`;
- `ano`, `mes_num`, `mes_nome`;
- `tipo_registro`.

Indicadores:

- demanda total, SPOT, EVENTO e venda;
- participação percentual SPOT/EVENTO/VENDA;
- participação mensal no ano e índice de sazonalidade quando disponível;
- crescimento MoM/YoY e YoY por SPOT/EVENTO;
- retorno previsto e cobertura de derivação do retorno;
- estoque mínimo SPOT, segurança, alvo SPOT e reserva EVENTO;
- proteção comercial;
- estoque/reparo/produção operacionais quando reconciliados;
- estado de estoque, sinal de demanda e nível de alerta ELO;
- orientação cognitiva e ferramenta recomendada (`SWOT + 5W2H` para variação relevante).

## Gates ainda abertos

1. **Quantidade física:** a fonte comercial não possui quantidade explícita por linha.
2. **Tenant:** `mt_tenants` ainda não fornece tenant canônico para vincular essa baseline.
3. **Catálogo:** o catálogo canônico atual possui modelos de MÓDULO, mas não a taxonomia completa de CONTÊINER necessária para mapear os 31 modelos de origem.
4. **Retorno:** a data prevista de saída/período possui cobertura parcial; EVENTO continua fora da regra de retorno mensal até validar a unidade do campo `Período`.
5. **Previsão:** `PREVISAO_BASE` é referência estatística e não substitui `mt_previsoes_demanda`.

## Critério de promoção

Somente depois de reconciliar quantidade física + tenant + modelo canônico a unidade pode mudar para `UNIDADE_FISICA`. Nesse momento a própria view passa a habilitar os saldos físicos contra estoque mínimo e proteção comercial sem alterar a autoridade das tabelas operacionais.