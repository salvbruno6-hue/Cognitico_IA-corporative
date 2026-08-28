# SO 155.26 — Aprendizado de Orçamento

## 1. Análise cognitiva do orçamentista

| Parâmetro | Identificado | Adotado |
|---|---|---|
| Quantidade total de módulos | 24 | 20 módulos da composição original + 4 MLT.M01 adaptados para sanitários |
| Composição original | 20 módulos | 9 × MLT.M06 Sanitário Ele e Ela; 9 × MLT.M01 Módulo Amplo; 1 × MLT.M02 Escritório Suíte; 1 × MLT.M20 Módulo Bipartido |
| Complementação | 4 módulos | 4 × MLT.M01 transformados/adaptados para sanitários |
| Resultado final | 24 módulos | 20 originais + 4 adaptados |
| Manutenção preventiva de climatização | 22 equipamentos; 6 meses | Dimensionamento por produtividade e 2 ciclos |
| Manutenção corretiva de climatização | 6 visitas; 6 meses | 1 equipe/mês |
| Manutenção das estruturas modulares | 6 visitas; 6 meses | 1 visita/mês, com equipe dimensionada |
| Manutenção de sanitários | 4 sanitários | Composição específica, evitando duplicidade de materiais |
| Calha e drenagem | 55 m | Conversão da composição global em custo por metro |
| Ponto de tomada 10 A | 1 ponto | Composição completa por unidade |

## 2. Memória de cálculo estruturada

| ID | Memória | Categoria | Entrada/Base | Unidade | Premissa | Fórmula | Subcálculo | Resultado | Validação | Origem |
|---:|---|---|---:|---|---|---|---|---|---|---|
| 1 | Manutenção preventiva de climatização — 6 meses | CÁLCULO | 22 equipamentos | Dia | 6 equipamentos/dia; arredondamento superior; 2 ciclos | 22 ÷ 6 | 3,67 → 4 × 2 | 8 dias técnico; 16 dias profissional; 2 visitas de carro | Validado por reconstrução da memória | SO 155.26 |
| 2 | Manutenção corretiva de climatização — 6 meses | CÁLCULO | 6 visitas | Visita | Periodicidade mensal | 1 equipe/mês × 6 meses | 6 visitas × 1 dia; 2 profissionais × 6 | 6 visitas; 6 dias técnico; 12 dias profissional | Validado por reconstrução da memória | SO 155.26 |
| 3 | Manutenção das estruturas modulares — 6 meses | CÁLCULO | 6 visitas | Visita | 1 visita/mês | 1 × 6 | 1 encarregado × 6; 1 profissional × 6 × 2; 1 ajudante × 6 × 2 | 6 dias encarregado; 12 dias profissional; 12 dias ajudante; 6 visitas | Validado por reconstrução da memória | SO 155.26 |
| 4 | Manutenção de 4 sanitários — 6 meses | CÁLCULO | 4 sanitários | Verba | Material já contemplado; evitar duplicidade | 2×448,21 + 4×275,82 + 4×235,92 + 998,73 | 896,42 + 1.103,28 + 943,68 + demais composição | R$ 3.942,11 | Validado por reconstrução da memória | SO 155.26 |
| 5 | Calha e drenagem — custo por metro | CÁLCULO | 55 m | R$/m | Dividir subtotal pelo comprimento | 4.270,63 ÷ 55 | 4.270,63 ÷ 55 | R$ 77,65/m | Validado por reconstrução da memória | SO 155.26 |
| 6 | Ponto de tomada 10 A — composição completa | CÁLCULO | 1 ponto | R$/ponto | 0,1 dia/profissional + 0,1 dia/ajudante | 33,17 + 27,58 + 23,59 | Materiais + mão de obra | R$ 84,34/ponto | Validado por reconstrução da memória | SO 155.26 |

## 3. Inteligência reutilizável do ELO

| Conhecimento | Regra | Condição de reutilização | Exemplo |
|---|---|---|---|
| Composição original × adaptação | Separar quantitativo originalmente previsto da complementação | Quando módulos da composição original forem transformados/adaptados | 20 + 4 = 24 módulos |
| Manutenção preventiva | Quantidade ÷ produtividade × ciclos | Mesma natureza, produtividade e periodicidade equivalentes | 30 ÷ 6 × 2 = 10 dias técnico |
| Manutenção corretiva | Periodicidade × visitas/equipe | Quando periodicidade e equipe forem equivalentes | 6 meses = 6 visitas |
| Calha/drenagem | Composição global ÷ extensão | Quando composição, material e condição de execução forem equivalentes | R$ 4.270,63 ÷ 55 = R$ 77,65/m |
| Ponto elétrico | Compor por unidade | Quando especificação e composição forem equivalentes | R$ 84,34/ponto |
| Manutenção modular | Dimensionar equipe pela periodicidade | Quando condições de execução forem equivalentes | 1 visita/mês × 6 meses |

## 4. Histórico e aplicação

A SO 155.26 deve ser tratada como precedente de orçamento. O ELO não deve copiar resultados numéricos isolados. Deve recuperar a lógica, comparar as premissas com a nova solicitação, substituir as variáveis, recalcular e validar.

Fluxo:

NOVO REQUISITO → CONSULTAR GIT → LOCALIZAR PRECEDENTE NO SUPABASE → COMPARAR PREMISSAS → VERIFICAR EQUIVALÊNCIA → SUBSTITUIR VARIÁVEIS → RECALCULAR → VALIDAR → APLICAR AO NOVO ORÇAMENTO.

### Regra de persistência

Este arquivo é o registro cognitivo específico da SO 155.26 no caminho canônico de aprendizados do ELO. Memórias quantitativas devem permanecer também rastreáveis no Supabase pela origem SO 155.26.
