# MULTITEINER — FLUXO OPERACIONAL E GOVERNANÇA DE DADOS

## Base

Este conjunto de documentos traduz o fluxograma **FLUXO MULTITEINER — PROCESSO INTEGRADO OPERACIONAL** para a arquitetura de dados do ELO.

A referência visual foi confrontada com o schema atual do Supabase e com a arquitetura PCP existente.

## Macroprocesso

`01 Locação/Comercial → 02 Planejamento → 03 Almoxarifado → 04 Compras → 05 Produção → 06 Reparo de Módulos → 07 Expedição/Externa/Campo`

O fluxo não deve ser tratado como uma sequência rígida de telas. Ele é uma rede operacional com retornos:

`Planejamento → Compras → Almoxarifado → Produção`

`Produção → Falha → Reparo → Produção/Liberação`

`Produção → Expedição → Montagem externa → Campo`

## Quatro contextos de execução que o ELO deve distinguir

1. **Linha de fabricação linear** — sequência principal da produção.
2. **Linha de fabricação personalizada** — roteiro derivado do pedido/projeto personalizado.
3. **Linha de reparo modular** — recuperação de unidade com diagnóstico, oficinas, mão de obra e material.
4. **Operação externa** — montagem/instalação fora da fábrica, com horas, pessoas, atividades, eventos e localização.

Esses contextos usam dados diferentes, mas pertencem ao mesmo ciclo operacional.

## Documentos por operação

| Etapa | Documento |
|---|---|
| 01 | [Locação / Comercial](operacoes/01_LOCACAO_COMERCIAL.md) |
| 02 | [Planejamento](operacoes/02_PLANEJAMENTO.md) |
| 03 | [Almoxarifado](operacoes/03_ALMOXARIFADO.md) |
| 04 | [Compras](operacoes/04_COMPRAS.md) |
| 05 | [Produção](operacoes/05_PRODUCAO.md) |
| 06 | [Reparo de Módulos](operacoes/06_REPARO_MODULOS.md) |
| 07 | [Expedição e Execução Externa](operacoes/07_EXPEDICAO_E_CAMPO.md) |

## Trabalho orientado por tabela

[Guia de orientação para alimentação das tabelas](TABELAS_GUIA_ORIENTACAO_ALIMENTACAO.md)

O guia possui uma seção própria para cada uma das 41 tabelas operacionais selecionadas.

## Regra de implantação

O trabalho com especialistas deve ocorrer por tabela e por operação:

`entender o processo → identificar o dado → localizar a fonte → validar o significado → registrar → confrontar → inserir`

O ELO deve ser **orientador da coleta e da inserção**, não gerador de dados.

## Regra de evidência

- **DADO**: registro estruturado existente;
- **FONTE VISUAL**: informação presente no fluxograma;
- **APRENDIZADO VALIDADO**: regra já governada;
- **INFERÊNCIA CONTROLADA**: relação derivada e explicitamente identificada;
- **NÃO LOCALIZADO**: dado necessário ainda não encontrado.

## Regra de relacionamento

O fluxo visual pode mostrar uma relação conceitual que ainda não existe como FK no banco.

Portanto:

**fluxo conceitual ≠ relacionamento físico confirmado**

O ELO só deve afirmar uma relação física quando o schema a sustentar. Caso contrário, deve registrar o vínculo como **conceitual/pedente de validação**.

## Regra de planejado × realizado

Planejamento:

- plano;
- linha de plano;
- roteiro;
- OP;
- capacidade;
- datas planejadas.

Realizado:

- eventos;
- quantidade concluída/produzida;
- início/fim reais;
- movimentações;
- horas de mão de obra;
- inspeções;
- expedição;
- eventos externos/campo.

## Estado de implantação

A estrutura documental está criada. A alimentação das tabelas deve ser feita com os especialistas, operação por operação, sem criar dados fictícios.

