# OPERAÇÃO 06 — REPARO DE MÓDULOS

## Papel no fluxo

Recupera módulos que chegam ao pátio e precisam ser avaliados, direcionados à oficina e liberados após execução.

## Sequência do fluxograma

`Entrada no pátio → lavagem/higienização → separação/avaliação → direcionamento por oficina → execução → conclusão/liberação`

## Tabelas primárias

- `mt_ordens_reparo`
- `mt_eventos_reparo`
- `mt_nao_conformidades`
- `mt_inspecoes`
- `mt_unidades_modulares`
- `mt_movimentacoes_estoque`
- `rh_mao_obra_custos`

## Oficinas representadas no fluxo

- hidráulica;
- elétrica;
- estrutura;
- pintura;
- marcenaria.

Essas categorias são referência visual do processo. O cadastro efetivamente utilizado deve ser confirmado com o especialista.

## O que o especialista deve ensinar

- como o reparo é aberto;
- como o diagnóstico é registrado;
- como a disciplina é definida;
- como horas de mão de obra são registradas;
- como material consumido é registrado;
- quais eventos significam início, pausa, conclusão e liberação;
- qual evidência autoriza retorno ao estoque/disponibilidade.

## Regra

`diagnóstico` não é causa validada automaticamente. O ELO deve diferenciar descrição do especialista, evento registrado e causa confirmada.

## Saída

Reparo concluído e liberado, ou pendência claramente classificada.
