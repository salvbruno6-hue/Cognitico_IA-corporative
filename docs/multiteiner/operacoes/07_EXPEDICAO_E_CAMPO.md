# OPERAÇÃO 07 — EXPEDIÇÃO E EXECUÇÃO EXTERNA

## Papel no fluxo

Fecha o ciclo físico: módulos montados são conferidos, embalados quando necessário, expedidos e, quando previsto, seguem para instalação/montagem externa e registro de campo.

## Sequência do fluxograma

`Módulos montados → segregação no pátio → instalação excedente? → packing → conferência final → gate de expedição → saída controlada → entrega final`

## Tabelas primárias

- `mt_expedicoes`
- `mt_expedicao_itens`
- `mt_ordens_montagem_externa`
- `mt_montagem_externa_modulos`
- `mt_eventos_montagem_externa`
- `mt_mao_obra_montagem_externa`
- `mt_eventos_campo`
- `mt_unidades_modulares`

## Execução externa

A montagem externa possui planejamento e realizado próprios:

- início/fim planejado;
- início/fim real;
- horas planejadas;
- horas realizadas;
- eventos;
- pessoa;
- função;
- atividade;
- localização.

O ELO deve usar esses dados para confrontar o planejado com a execução, sem transformar estimativa em realizado.

## O que o especialista deve ensinar

- quando um módulo está pronto para expedição;
- quais itens acompanham a unidade;
- como ocorre a conferência;
- quando uma instalação externa é aberta;
- quais eventos comprovam execução;
- como mão de obra é apontada;
- quais eventos de campo encerram ou reabrem o ciclo.

## Saída

Entrega/execução externa registrada com evidência suficiente para fechar o ciclo ou localizar a pendência.
