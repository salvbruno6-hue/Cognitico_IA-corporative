# ELO Kit Output Contract — 2026-09-07

## Regra canônica de apresentação

Quando uma consulta natural localizar um kit e sua composição relacionada à `lista_mae`, a resposta ao especialista deve preservar explicitamente o **código do produto** de cada item.

A tabela de composição deve, no mínimo, apresentar:

| Campo | Regra |
|---|---|
| Código do produto | Obrigatório; usar o código canônico do produto quando disponível |
| Descrição | Descrição oficial recuperada do vínculo/Lista Mãe |
| Unidade | Unidade do item |
| Quantidade | Quantidade aplicável ao kit |
| Valor unitário | Base vigente recuperada |
| Valor total | Total do item, quando calculado/cadastrado |
| Situação do vínculo | Exato, similar, pendente, sem correspondência etc., quando disponível |
| Situação ELO | Confirmado, validado, dúvida, pendente de validação etc., quando disponível |

## Código do produto x código interno do vínculo

`cod_produt` é o campo destinado ao **código do produto**. `cod_item` identifica o registro/item e não deve substituir o código do produto na tabela apresentada ao especialista.

Quando o item ainda não possuir código de produto, o ELO deve mostrar explicitamente `PENDENTE_CODIGO`/equivalente e não fabricar um código.

Quando existir vínculo com a `lista_mae`, o código da Lista Mãe deve permanecer rastreável, mas não deve ser usado para ocultar ou substituir o código de produto do item.

## Governança

- A regra é de apresentação/contrato de consulta, não de alteração dos dados canônicos.
- O ELO não deve completar códigos por inferência sem evidência governada.
- Pendências e correspondências semelhantes continuam visíveis.
- A consulta permanece somente leitura.
- A regra vale para kits em geral, não apenas para KIT-M01.
