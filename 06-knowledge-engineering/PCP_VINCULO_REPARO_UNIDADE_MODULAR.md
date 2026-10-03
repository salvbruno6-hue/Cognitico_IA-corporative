# Instrução PCP: vínculo entre reparo e unidade modular

## Objetivo
Estabelecer o procedimento canônico para vincular uma ordem de reparo à unidade modular física que está sendo reparada. O vínculo é requisito para que um reparo possa ser considerado cobertura futura da demanda.

## Fonte operacional
A planilha da Qualidade será recebida como fonte de reconciliação. Deve conter, quando disponível: ID do módulo, identificação do produto, tipo, taxonomia, status do reparo e datas.

A planilha ainda não deve ser importada antes da conferência de estrutura e qualidade.

## Regra de identidade
O ID do módulo é a identidade da unidade física. A reconciliação esperada é:

ID da planilha → unidade modular → modelo → taxonomia.

Se o identificador não corresponder a uma unidade existente, registrar GAP. Não criar unidade fictícia.

## Regra de vínculo
A ordem de reparo deve apontar para a unidade física por meio de mt_ordens_reparo.unidade_modular_id.

Tipo, número de contêiner ou descrição textual podem apoiar a reconciliação, mas não substituem o vínculo da unidade quando a identidade física estiver disponível.

## Critérios para reparo recuperável
Um reparo somente pode reduzir a necessidade de fabricação quando:
1. a unidade estiver identificada;
2. possuir modelo válido;
3. a ordem estiver em status compatível com recuperação;
4. houver data confiável quando o horizonte depender dela;
5. não houver cancelamento ou descarte;
6. a unidade não estiver sendo contada simultaneamente como estoque disponível.

## Estados de GAP
- GAP_UNIDADE_NAO_ENCONTRADA
- GAP_ID_AUSENTE
- GAP_TAXONOMIA_DIVERGENTE
- GAP_DATA_REPARO
- GAP_DUPLICIDADE

## Fluxo
Receber planilha → validar colunas → validar IDs → reconciliar unidades → validar modelo/taxonomia → reconciliar ordens de reparo → verificar duplicidades → validar datas/status → registrar GAPs → somente então importar/atualizar.

## Não fazer
- Não criar ID por inferência.
- Não considerar reparo sem unidade como estoque.
- Não considerar reparo sem data confiável como cobertura futura.
- Não criar taxonomia paralela.
- Não transformar quantidade de reparos em quantidade fabricável automaticamente.
- Não aplicar fator de crescimento diretamente ao reparo.

## Rastreabilidade
Origem Qualidade → ID do módulo → unidade modular → modelo/taxonomia → ordem de reparo → status/data → cobertura da demanda.

## Gate
A carga somente será liberada após validar a estrutura da planilha, o significado do ID, a correspondência com as unidades, a taxonomia, datas/status, duplicidades e uma amostra de teste.

Planilha recebida não significa dado validado.
