# SO 131.26 — Município de Porto Belo/SC

## Aprendizado Pós-Ciclo — Orçamento e Análise Técnica

### 1. Separação entre produto comercial e composição
- O código comercial **MLT.C11** deve representar somente os componentes efetivamente contemplados pelo produto base.
- Quando o C11 já contempla forração, paredes e forro em painel isotérmico PIR, esses componentes não devem ser novamente lançados como materiais na composição, evitando duplicidade de custos.
- Itens que não pertencem ao C11 devem permanecer individualizados na composição, especialmente instalações hidrossanitárias, instalações elétricas, esquadrias, portas, piso, pintura, pia e demais adaptações específicas.
- Regra operacional: **produto comercial base ≠ composição de adequações**.

### 2. Coerência documental do orçamento
A análise deve verificar a cadeia:
**TR → Produto → Composição → Descrição → Observações → PTS**.

Sempre identificar se uma exigência do TR está:
- incorporada ao produto comercial;
- lançada em composição específica;
- excluída formalmente do escopo;
- pendente de esclarecimento ao cliente.

### 3. Substituições técnicas
- Não substituir automaticamente uma especificação do TR.
- Quando houver solução tecnicamente equivalente com potencial de redução de custo ou melhoria de desempenho, formular **pedido formal de esclarecimento** ao contratante antes de alterar o orçamento.
- Caso não exista autorização formal, manter a especificação original do TR na proposta.

### 4. Equivalências aplicadas à SO 131.26
**Piso:** avaliar substituição de piso cerâmico por piso vinílico LVT comercial, condicionada à aceitação formal do cliente.

**Forro:** solução em painel PIR 32 mm considerada dentro do C11, sem necessidade de lançar novamente o painel na composição quando o produto comercial já o contempla. A justificativa técnica deve enfatizar isolamento térmico e desempenho quanto à reação ao fogo quando esses requisitos forem relevantes no TR.

### 5. Bancada da cozinha
Quando o TR exigir pia, mas excluir expressamente bancadas, deve-se questionar o escopo antes de precificar bancada.

Pergunta padrão:
> Considerando que o Termo de Referência exclui expressamente o fornecimento de bancadas, esclarecer se a contratada deverá fornecer apenas a pia com sua estrutura metálica de sustentação (cavalete), sem o fornecimento de bancada fixa.

### 6. PTS Pós-Orçamento
A matriz padrão deve utilizar as colunas:
**Item TR | Trecho do TR | Exigência Técnica | Item(s) do Orçamento | Atendimento | Evidência Técnica | Responsabilidade**.

### 7. Controle crítico aprendido
Durante a revisão final, não avaliar somente os valores. Conferir também se:
- componentes do produto comercial foram duplicados na composição;
- componentes exigidos pelo TR ficaram sem origem orçamentária;
- observações descrevem itens que não existem na composição;
- o C11 recebeu indevidamente instalações ou esquadrias que são itens separados;
- substituições dependentes de aprovação do cliente foram implementadas antes da resposta oficial.

### 8. Loop operacional
**TR → Identificação da exigência → Análise de equivalência → Pedido de esclarecimento → Resposta do cliente → Adequação do orçamento → PTS Técnica → PTS Pós-Orçamento → Aprendizado.**

Este ciclo deve ser reutilizado nas próximas solicitações de orçamento de contêineres e estruturas modulares.

### 9. Memória quantitativa consolidada da SO 131.26
Os cálculos quantitativos permanecem como camada de memória de cálculo no Supabase; este arquivo registra apenas os principais aprendizados e as referências para reconstrução.

- **Abertura de vãos:** 3 portas de 2,10 × 0,80 m = 5,04 m²; 2 janelas de 1,20 × 1,00 m = 2,40 m²; total = **7,44 m²**.
- **Reforços:** 4 barras de metalon 50 × 30 × 1,20 mm, barras de 6 m = **24,00 m**.
- **Divisórias PIR 40 mm:** 5 × 1,13 × 2,65 = **14,9725 m²** teóricos.
- **Piso:** **27,255 m²**, quantitativo de planilha; origem geométrica integral não disponível, portanto tratar como memória parcial.
- **Pintura externa:** **114,65 m²**, quantitativo de planilha; tratar como memória parcial quando não houver origem geométrica.
- **Subtotal geral:** **R$ 21.473,42**.
- **BDI:** **65%**.
- **Total matemático com BDI:** R$ 21.473,42 × 1,65 = aproximadamente **R$ 35.431,14**.
- **Total apresentado na planilha:** **R$ 35.431,15**; diferença de **R$ 0,01**, preservada para auditoria.

### 10. Regra de memória e rastreabilidade
- Conhecimento, regras, decisões, critérios e precedentes: **Git**.
- Fórmulas, entradas, quantitativos, resultados e validações: **Supabase**.
- Não inventar cálculo para preencher lacunas.
- Não alterar silenciosamente valores divergentes da planilha.
- Toda memória deve permitir rastrear **fonte → item → parâmetro → fórmula → resultado → validação**.
