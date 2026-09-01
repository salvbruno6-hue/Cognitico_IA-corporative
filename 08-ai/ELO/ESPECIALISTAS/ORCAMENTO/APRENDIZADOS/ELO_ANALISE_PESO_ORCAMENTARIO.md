# ELO — REGRA DE ANÁLISE DE PESO ORÇAMENTÁRIO E IMPACTO

## Objetivo
Durante a elaboração de cada nova SO, identificar itens de maior relevância financeira e/ou estratégica e, após o fechamento, levar à PTS/PST uma análise objetiva sobre peso, redução, remoção, substituição e consequências.

## Separação dos processos
ELO APRENDER → VARRER DADOS E MEMÓRIA DE CÁLCULO → BASE DE CONHECIMENTO → NOVO ORÇAMENTO → ANÁLISE DE PESO ORÇAMENTÁRIO → RANKING → PTS/PST.

A varredura histórica reconstrói e valida memórias. Não deve transformar automaticamente memória histórica em análise de peso da nova SO.

## Momento de execução
1. Durante o orçamento: sinalizar itens que já apresentem impacto relevante.
2. No fechamento: recalcular o ranking considerando o orçamento completo.
3. Na PTS/PST: apresentar somente a síntese dos itens relevantes.

## Cálculo
Quando houver BDI: Valor BDI = custo base × percentual. Valor final = custo base + BDI. Peso (%) = valor final do item ÷ valor final do orçamento × 100. Declarar sempre se a base é custo, subtotal ou preço final.

## Critérios
Considerar conjuntamente: peso financeiro; obrigatoriedade no TR; risco contratual; dependência técnica; necessidade operacional; incerteza do quantitativo/preço; possibilidade de redução; remoção; substituição; impacto da alteração.

Classificação: NORMAL, MÉDIA, ALTA ou CRÍTICA. Não depender exclusivamente de percentual fixo universal.

## Redução
Para cada item relevante: pode reduzir? SIM/NÃO/AVALIAR. Quando aplicável, informar quantidade reduzível, economia e impactos técnico, operacional e contratual.

## Remoção
Analisar separadamente da redução. Verificar obrigação no TR, especificação, necessidade de funcionamento, dependências, impacto contratual e alternativas. Classificar: permitido; não recomendado; risco contratual; depende de esclarecimento.

## Substituição
Comparar custo, especificação, desempenho, durabilidade, atendimento ao TR, economia e risco. Menor custo não implica aceite automático.

## PTS/PST
Apresentar objetivamente: item; peso no preço final; relevância; possibilidade de redução; remoção; substituição; economia potencial; impacto técnico; impacto operacional; impacto contratual; recomendação.

## Proteção contra decisões indevidas
Identificar peso não significa recomendar corte. Fluxo obrigatório: ITEM RELEVANTE → PESO → MOTIVO → OBRIGATORIEDADE → REDUÇÃO → REMOÇÃO → SUBSTITUIÇÃO → ECONOMIA → CONSEQUÊNCIAS → RECOMENDAÇÃO.

Itens obrigatórios pelo TR devem ser identificados como tais e não podem ser sugeridos para remoção apenas por possuírem alto peso.

## Estrutura mínima
so; item; categoria; custo_base; percentual_bdi; valor_bdi; valor_final; peso_percentual; ranking; relevancia; pode_reduzir; pode_remover; pode_substituir; economia_potencial; impacto_tecnico; impacto_operacional; impacto_contratual; recomendacao; fonte; status.

## Regra definitiva
ELO APRENDER aprende e consolida. VARRER CÁLCULOS reconstrói e valida. O ORÇAMENTO calcula o peso da SO atual. A PTS/PST apresenta os itens relevantes e as consequências das possíveis decisões. A memória histórica orienta, mas o peso é recalculado para cada nova SO.
