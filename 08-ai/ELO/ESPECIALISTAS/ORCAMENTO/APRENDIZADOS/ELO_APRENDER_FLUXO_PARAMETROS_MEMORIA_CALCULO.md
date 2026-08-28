# ELO APRENDER — Fluxo Padrão de Parâmetros × Memória de Cálculo

## Finalidade

Estabelecer o padrão obrigatório para o gatilho `ELO APRENDER` em todos os orçamentos. O ELO deve extrair, estruturar, relacionar e retornar o conhecimento como uma cadeia cognitiva e quantitativa reproduzível.

## Fluxo canônico

`FONTE → PARÂMETROS → ID MEMÓRIA → MEMÓRIA DE CÁLCULO → QUANTITATIVO → COMPOSIÇÃO → CUSTO → VALIDAÇÃO → APLICAÇÃO NO ORÇAMENTO`

O gatilho não deve retornar somente o resultado financeiro. Deve retornar a lógica que produziu o resultado.

## Regra de identificação

- `ID` identifica o parâmetro ou item do orçamento.
- `ID Memória` identifica a lógica de cálculo que gerou o quantitativo.
- Todo item calculado deve, quando aplicável, possuir vínculo `ID → ID Memória`.
- Uma memória pode gerar múltiplos itens de composição.
- Uma SO que consulta uma memória anterior é referência consultiva; não altera a origem do cálculo aprendido.

## 1. PARÂMETROS DE CÁLCULO

| ID | Parâmetro | Valor/Base | Unidade | Critério / Regra de aplicação | Fonte | ID Memória |
|---|---|---:|---|---|---|---|

Registrar, conforme aplicável: objeto, base física, unidade, produtividade, equipe, periodicidade, período, fator de cobertura, relação de escala, fonte, premissa, arredondamento, escopo, percentual financeiro, logística, responsabilidades e validação.

**Regra:** parâmetro é a regra de dimensionamento; não é o resultado financeiro.

## 2. MEMÓRIA DE CÁLCULO

| ID Memória | Etapa | Entrada | Fórmula / Critério | Resultado | Unidade |
|---|---|---:|---|---:|---|

A memória deve seguir:

`ENTRADA → FÓRMULA/CRITÉRIO → SUBCÁLCULO → RESULTADO → UNIDADE`

Deve permitir que outro analista reconstrua o cálculo sem depender do valor final armazenado.

## 3. COMPOSIÇÃO FINANCEIRA

| ID Item | ID Memória | Descrição | Unidade | Quantidade | Valor Unitário | Valor Total |
|---|---|---|---|---:|---:|---:|

A composição deve manter vínculo explícito com a memória que originou sua quantidade.

## 4. REGRAS DE CÁLCULO

### Cobertura física / manutenção

Quando houver diretriz de cobertura de 30%, o percentual deve ser convertido diretamente em quantidade:

`Quantidade Base × 1,30 = Quantidade Resultante`

Não criar coluna de percentual somente para demonstrar o fator já convertido.

Exemplo: `20 × 1,30 = 26 un.`

### Percentuais financeiros

Percentuais financeiros permanecem como percentuais e devem indicar sua base de incidência. Exemplo: `4%` para ART/RRT somente sobre as composições autorizadas.

### Arredondamento

Frações devem ter o critério demonstrado na memória. Quando a regra determinar arredondamento superior:

`3,67 → 4`

### Manutenção

Manutenção deve separar quantitativo-base do projeto e quantitativo dimensionado para manutenção. Quando aplicável, contemplar separadamente mão de obra, materiais/componentes, apoio e demais custos autorizados.

## 5. RETORNO OBRIGATÓRIO DO GATILHO ELO APRENDER

Ao receber `ELO APRENDER`, o ELO deve:

1. Identificar a SO e suas fontes disponíveis.
2. Extrair os aprendizados relevantes.
3. Identificar parâmetros de cálculo.
4. Criar ou recuperar os `ID Memória` correspondentes.
5. Reconstruir fórmulas e subcálculos.
6. Identificar quantitativos resultantes.
7. Vincular cada quantitativo à composição financeira.
8. Informar custos e base de incidência.
9. Registrar fonte, premissa, evidência, validação e exclusões.
10. Separar conhecimento cognitivo de memória quantitativa.
11. Informar se o conhecimento é novo, precedente, validado, ajustado ou apenas referência consultiva.
12. Retornar a cadeia completa no padrão das tabelas acima.

## 6. SEPARAÇÃO GIT × SUPABASE

**Git:** fonte canônica do conhecimento cognitivo/semântico: prompts, regras, diretrizes, conceitos, instruções e fluxo operacional.

**Supabase:** memória estruturada consultiva: cálculos aprendidos, entradas, fórmulas, subcálculos, resultados, evidências, associações e histórico de decisões.

O ELO deve manter a correspondência entre as duas camadas:

`Conhecimento no Git ↔ Memória quantitativa/evidência no Supabase`

Um registro no Supabase não substitui a regra cognitiva no Git. Uma regra no Git não elimina a necessidade de registrar a memória quantitativa quando ela existir.

## 7. APLICAÇÃO EM TODAS AS SOs

O padrão é transversal aos orçamentos. Não é exclusivo da SO 155.26. A SO 155.26 funciona como caso de aprendizado e evidência para estruturar o padrão, mas futuras SOs devem reutilizar a estrutura sem copiar valores históricos de forma automática.

Quando uma memória anterior for utilizada, informar:

- `SO origem`;
- `SO consultante`;
- `ID Memória` de origem;
- regra recuperada;
- motivo da aplicabilidade;
- diferenças de contexto;
- necessidade de validação.

## 8. CRITÉRIO DE QUALIDADE

Uma memória só está adequadamente extraída quando for possível responder:

**De onde veio? → Qual era a base? → Qual regra foi usada? → Qual fórmula foi aplicada? → Qual resultado foi obtido? → Como virou composição? → Qual custo entrou no orçamento? → Quem/qual fonte validou?**
