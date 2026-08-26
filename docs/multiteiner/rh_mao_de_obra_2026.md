# Multiteiner — Estrutura de Mão de Obra

## Referência

- Fonte: RH/RJ
- Data de referência: 23/01/2026
- Ano-base: 2026
- Natureza: estrutura de custo de mão de obra para integração ao ELO

## Custos informados

| Cargo | Salário | 13º salário | Férias + 1/3 | FGTS/Multa | INSS patronal (30,30%) | Vale transporte | Vale refeição | Ajuda de custo (insalubridade) | PLR | Cesta básica | Uniformes/EPI | Plano de saúde | Plano odontológico | Seguro de vida | Total | Custo/dia (22 dias) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ajudantes | R$ 1.900,80 | R$ 158,40 | R$ 211,19 | R$ 202,84 | R$ 575,94 | R$ 413,60 | R$ 684,20 | R$ 150,00 | R$ 133,34 | R$ 250,00 | R$ 120,00 | R$ 361,89 | R$ 13,00 | R$ 15,00 | R$ 5.190,21 | R$ 235,92 |
| Profissional | R$ 2.457,30 | R$ 204,78 | R$ 273,03 | R$ 247,36 | R$ 744,56 | R$ 413,60 | R$ 684,20 | R$ 150,00 | R$ 133,34 | R$ 250,00 | R$ 120,00 | R$ 361,89 | R$ 13,00 | R$ 15,00 | R$ 6.068,06 | R$ 275,82 |
| Encarregado/Supervisor | R$ 4.861,49 | R$ 405,12 | R$ 540,15 | R$ 439,70 | R$ 1.473,03 | R$ 413,60 | R$ 684,20 | R$ 150,00 | R$ 133,34 | R$ 250,00 | R$ 120,00 | R$ 361,89 | R$ 13,00 | R$ 15,00 | R$ 9.860,53 | R$ 448,21 |

## Integração ao ELO

A estrutura deve alimentar o modelo de mão de obra e ser cruzada com RH, PCP, Produção, Reparos e Orçamento.

Entidades lógicas relacionadas:

- `rh_colaborador`
- `rh_funcao`
- `rh_equipe`
- `rh_especialidade`
- `rh_custo_hora`
- `rh_disponibilidade`
- `apontamento_mao_obra`

O custo de mão de obra deve ser preservado separadamente do custo de material e posteriormente agregado ao custo total da operação ou reparo.

> Os valores são registrados conforme informação fornecida para RH/RJ em 23/01/2026. Não foram recalculados ou alterados.
