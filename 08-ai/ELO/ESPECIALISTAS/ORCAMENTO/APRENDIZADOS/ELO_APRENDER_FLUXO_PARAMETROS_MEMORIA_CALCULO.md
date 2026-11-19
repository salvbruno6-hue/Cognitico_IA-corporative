# ELO APRENDER — Fluxo Canônico de Conhecimento + Memória de Cálculo

## Finalidade

Estabelecer o comportamento obrigatório do gatilho `ELO APRENDER` para Solicitações de Orçamento.

Quando `ELO APRENDER` for acionado, ele deve produzir **dois resultados simultâneos**:

1. **Conhecimento cognitivo/instrucional** → Git;
2. **Memória quantitativa e de cálculo** → Supabase.

O aprendizado de uma SO de orçamento não é considerado completo quando somente o conhecimento textual foi consolidado. Se houver cálculo, quantitativo, dimensionamento, composição, percentual, produtividade ou raciocínio matemático utilizado para formar, validar, alterar ou justificar o orçamento, esse cálculo deve ser investigado e persistido no Supabase.

A função investigadora deve procurar o **raciocínio matemático que produziu o número**, e não apenas números isolados. A base do investigador já determina que as fontes incluem SO, TR, projetos, PTS Técnica, orçamento, planilhas, composições, quantitativos, PTS Pós-Orçamento e documentos de apoio. fileciteturn133file0L17-L45

## Fluxo canônico

`SO → FONTES → ELO ANALISA → CONHECIMENTO + VARRER CÁLCULOS → NORMALIZAÇÃO → MEMÓRIA/ID → VALIDAÇÃO → GIT + SUPABASE → RETORNO CONSOLIDADO`

Para orçamento, `VARRER CÁLCULOS` é **etapa obrigatória** do `ELO APRENDER`, não uma operação opcional.

---

## 1. O QUE O ELO APRENDER DEVE FAZER

Ao receber `ELO APRENDER` para uma SO de orçamento, o ELO deve executar no mesmo ciclo:

### Camada A — Conhecimento

Extrair, interpretar, normalizar, agrupar, deduplicar e governar:

- conceitos;
- regras;
- instruções;
- diretrizes;
- precedentes;
- decisões;
- critérios;
- governança;
- interpretação da experiência.

Persistência: **Git**.

### Camada B — Memória de cálculo

Investigar e estruturar:

- dado encontrado;
- fonte;
- parâmetro;
- base;
- unidade;
- premissa;
- fórmula;
- subcálculos;
- quantitativo resultante;
- composição;
- valor unitário;
- custo;
- validação;
- origem;
- evidências.

Persistência: **Supabase**.

**As duas camadas devem ser processadas pelo mesmo acionamento de `ELO APRENDER`.**

---

## 2. CADEIA OBRIGATÓRIA DA MEMÓRIA

Toda memória de cálculo deve buscar construir:

`FONTE → DADO ENCONTRADO → PARÂMETRO → ID → ID MEMÓRIA → FÓRMULA → SUBCÁLCULOS → QUANTITATIVO RESULTANTE → COMPOSIÇÃO → CUSTO → VALIDAÇÃO → ORIGEM`

A base do investigador determina expressamente que não se deve procurar somente números, mas descobrir de onde vieram, qual unidade, quantidade, premissa, composição, fórmula, resultado e utilização do valor. fileciteturn133file0L48-L72

Se uma etapa não estiver disponível na fonte, registrar a ausência/limitação. Não inventar.

---

## 3. ESTRUTURA PADRÃO DE PARÂMETROS

| ID | Parâmetro | Valor/Base | Unidade | Critério / Regra de aplicação | Fonte | ID Memória |
|---|---|---:|---|---|---|---|

Registrar, conforme aplicável: objeto, base física, unidade, produtividade, equipe, periodicidade, período, fator de cobertura, escala, fonte, premissa, arredondamento, escopo, percentual financeiro, logística, responsabilidades e validação.

**Parâmetro é a regra/base de dimensionamento; não é o resultado financeiro.**

---

## 4. ESTRUTURA PADRÃO DA MEMÓRIA

| ID Memória | Etapa | Entrada/Base | Unidade | Parâmetro | Fórmula / Critério | Subcálculo | Resultado | Unidade Resultado | Validação | Origem |
|---|---|---:|---|---|---|---|---:|---|---|---|

A memória deve permitir reconstrução independente do valor final:

`ENTRADA → PARÂMETRO → FÓRMULA → SUBCÁLCULO → RESULTADO`

Uma `ID Memória` pode relacionar vários parâmetros, subcálculos e itens de composição pertencentes à mesma cadeia lógica.

---

## 5. REGRA DOS IDs — BANCO É O CONTROLADOR

### ID

O `ID` do registro **não é criado, escolhido, incrementado ou reutilizado pelo modelo**.

O Supabase é a autoridade do identificador persistente. O ID deve ser:

- único;
- permanente;
- não reutilizável;
- não reiniciado;
- não duplicado;
- vinculado permanentemente ao registro.

O ELO deve inserir ou recuperar o registro e **usar o ID retornado pelo Supabase**.

### ID Memória

`ID Memória` identifica a cadeia lógica do cálculo.

Quando a memória já existir, recuperar o identificador existente. Quando não existir, criar a memória no Supabase e usar o identificador devolvido pelo banco.

O modelo nunca deve fabricar um ID para simular persistência.

---

## 6. PERSISTÊNCIA DIRETA

Quando houver cálculo aplicável, o `ELO APRENDER` deve encaminhar a memória para persistência no Supabase durante o próprio fluxo:

1. criar/recuperar a varredura da SO;
2. consultar memória existente;
3. verificar conceito e duplicidade;
4. criar/recuperar `ID Memória`;
5. persistir o cálculo estruturado;
6. capturar o `ID` gerado pelo banco;
7. vincular o cálculo à memória;
8. persistir as evidências;
9. registrar classificação/status;
10. retornar o estado da persistência.

Se a persistência falhar, registrar **PENDENTE DE PERSISTÊNCIA** e não afirmar que a memória foi consolidada.

As tabelas de varredura, cálculo aprendido, evidência e memória constituem a camada quantitativa do fluxo.

---

## 7. MODELO DE DADOS MÍNIMO

### `elo_orcamento_calculo_varreduras`

Controla a execução da varredura por SO/learning.

### `elo_orcamento_memoria`

Representa a memória lógica da cadeia de cálculo.

### `elo_orcamento_calculos_aprendidos`

Representa o cálculo estruturado, vinculado ao `memoria_id`, com entrada, fonte, premissa, fórmula, subcálculo, resultado, validação, origem e aplicabilidade.

### `elo_orcamento_calculo_evidencias`

Representa as evidências documentais que sustentam o cálculo.

O `ID` dessas entidades é responsabilidade do banco.

---

## 8. ESTRUTURA DO CÁLCULO APRENDIDO

Cada cálculo deve ser estruturado, conforme aplicável, com:

- `id` — gerado pelo Supabase;
- `memoria_id` — ID da cadeia lógica;
- `varredura_id`;
- `learning_id`;
- `origem_so`;
- `origem_documento`;
- `item_origem`;
- `conceito_key`;
- `categoria`;
- `descricao`;
- `entrada/base`;
- `fonte`;
- `premissa`;
- `formula`;
- `subcalculo`;
- `resultado`;
- `unidade_resultado`;
- `validacao`;
- `status`;
- `origem_tipo`;
- `referencia_so`;
- `aplicabilidade`;
- `evidencia`;
- `hash_calculo`, quando aplicável.

---

## 9. EVIDÊNCIAS E DEDUPLICAÇÃO

Se o mesmo cálculo aparecer em PTS, Orçamento e PTS Pós-Orçamento, não criar três memórias independentes.

Criar/recuperar uma memória e associar múltiplas evidências:

`MEMÓRIA ÚNICA → PTS + ORÇAMENTO + PTS PÓS`

A evidência deve identificar, quando possível:

- SO;
- documento;
- item;
- trecho/identificação;
- tipo de evidência;
- observação.

Se o conceito/cálculo já existir, agregar a nova evidência e ocorrência, preservando a origem original.

---

## 10. CATEGORIAS MÍNIMAS DE VARREDURA

Investigar obrigatoriamente, quando houver evidência:

- quantitativos derivados;
- excedentes;
- estrutura/metalurgia;
- cobertura/telhado;
- hidráulica/esgoto subterrâneo;
- elétrica aérea/subterrânea;
- climatização;
- manutenção;
- mão de obra;
- produtividade;
- mobilização/desmobilização;
- transporte/logística;
- acoplamento de módulos;
- ART/RRT/projetos;
- áreas/pavimentos/ambientes;
- equipamentos;
- composição de preços;
- equivalências técnicas;
- cálculos ocultos ou implícitos.

A investigação deve procurar quantitativos derivados, excedentes e relações matemáticas, conforme a especificação do investigador. fileciteturn133file0L75-L104

---

## 11. CÁLCULOS OCULTOS

Investigar afirmações como:

- “foram considerados 2 ajudantes”;
- “serão necessários 3 dias”;
- “adotado 30%”;
- “considerado 4 módulos/dia”;
- “valor unitário obtido de outra composição”.

Essas afirmações podem representar memória de cálculo implícita. Reconstruir somente quando houver evidência suficiente. A base também exige atenção a percentuais: não guardar apenas o percentual, mas sua base, fórmula, resultado, justificativa e fonte. fileciteturn133file0L280-L315

---

## 12. CLASSIFICAÇÃO OBRIGATÓRIA

Cada achado deve retornar uma das situações:

- `CALCULATION_CONFIRMED`;
- `CALCULATION_PARTIAL`;
- `CALCULATION_REFERENCE`;
- `CALCULATION_NOT_RECONSTRUCTABLE`;
- `NO_CALCULATION_FOUND`.

Não inventar dados para completar cálculo parcial.

---

## 13. REFERÊNCIA NÃO É ORIGEM

Se uma SO atual consultar uma memória encontrada em outra SO:

`SO de origem = origem da memória`

`SO atual = consultante`

A referência deve informar:

- SO origem;
- documento de origem;
- item de origem;
- valor/quantitativo;
- unidade;
- características;
- data, quando disponível;
- fonte;
- motivo da comparação;
- grau de equivalência;
- motivo pelo qual pode ser aplicável;
- diferenças de contexto;
- validação necessária.

Exemplo:

“Referência consultiva da SO 155.26. Pode ser considerada porque o item possui características técnicas equivalentes, unidade compatível e referência temporal adequada. Validar diferenças de especificação, espessura, dimensão, material e contexto antes de aplicar.”

A base original estabelece que referência de outra SO não deve ser tratada como origem da SO consultante. fileciteturn133file0L516-L534

---

## 14. NÃO CONFUNDIR REGRA COM CÁLCULO

Exemplo:

“Utilizar 30% para componentes sujeitos a falha.”

→ conhecimento/instrução → **Git**.

“100 unidades × 30% = 30 unidades adicionais.”

→ memória quantitativa → **Supabase**.

O ELO deve registrar ambos quando ambos existirem, mantendo os destinos separados.

---

## 15. COMPOSIÇÃO FINANCEIRA

| ID Item | ID Memória | Descrição | Unidade | Quantidade | Valor Unitário | Valor Total |
|---|---|---|---|---:|---:|---:|

A composição deve manter vínculo explícito com a memória que originou sua quantidade.

Percentuais financeiros devem informar sua base de incidência. Nunca assumir que um percentual incide sobre todo o orçamento sem evidência.

---

## 16. RETORNO OBRIGATÓRIO DO COMANDO “ELO APRENDER”

O comando deve retornar **conhecimento + memória de cálculo**, no mesmo resultado.

### A. Conhecimento cognitivo — Git

Mostrar:

- o que foi aprendido;
- conceitos;
- regras;
- instruções;
- precedentes;
- decisões;
- governança;
- aplicabilidade.

### B. Memória de cálculo — Supabase

Para cada cálculo, mostrar:

`FONTE → DADO → PARÂMETRO → ID → ID MEMÓRIA → FÓRMULA → SUBCÁLCULOS → QUANTITATIVO → COMPOSIÇÃO → CUSTO → VALIDAÇÃO → ORIGEM`

O ELO deve identificar explicitamente que a memória foi **recuperada, criada, agregada ou ficou pendente**.

### C. Estado de persistência

Cada memória deve retornar:

- `PERSISTIDA`;
- `RECUPERADA`;
- `AGREGADA`;
- `PENDENTE_VALIDACAO`;
- `PENDENTE_PERSISTENCIA`;
- `NAO_RECONSTRUIVEL`.

---

## 17. CONSULTA POSTERIOR DE UMA SO

Quando o usuário perguntar “o que sabemos sobre a SO X?” ou solicitar dados de um orçamento, o ELO deve consultar **as duas camadas**:

`GIT → conhecimento cognitivo`

`SUPABASE → memória de cálculo`

Depois deve apresentar uma resposta única, identificando a origem de cada informação.

Se houver cálculo, mostrar a cadeia reproduzível e não somente o resultado.

---

## 18. CRITÉRIO DE CONCLUSÃO

Uma SO de orçamento somente pode ser considerada completamente processada quando:

1. o conhecimento cognitivo aplicável tiver sido tratado no Git;
2. os cálculos tiverem sido investigados;
3. os cálculos reconstruíveis tiverem sido persistidos no Supabase;
4. os IDs tiverem sido gerados/controlados pelo banco;
5. as evidências estiverem vinculadas;
6. duplicidades tiverem sido tratadas;
7. referências consultivas estiverem separadas das origens;
8. pendências estiverem registradas.

**Não considerar “aprendido” apenas porque existe um arquivo `.md` no Git.**

---

## 19. REGRA FINAL

`ELO APRENDER` para orçamento significa:

**APRENDER O QUE FOI DECIDIDO + APRENDER COMO O NÚMERO FOI PRODUZIDO.**

Git preserva o conhecimento cognitivo.

Supabase preserva a memória quantitativa.

O ELO deve consultar as duas camadas quando solicitado a explicar uma experiência de orçamento.

O objetivo é permitir que outro analista responda simultaneamente:

**O que aprendemos? De onde veio? Qual cálculo foi feito? Como foi feito? Qual resultado produziu? Em qual composição entrou? Qual custo produziu? Como foi validado? Essa memória é da SO atual ou é referência consultiva?**

**NUNCA INVENTAR.**

---

## 20. APRENDIZADO CANDIDATO — TELHA SUBSTITUTA × TRELIÇA PADRÃO (SO 238.26)

**Status:** `LEARNING_CANDIDATE`, sujeito a validação e Evolution Gate. **Origem:** decisão do Analista na SO 238.26, Item 01, em 19/11/2026. Esta seção exemplifica a regra geral já existente de reconciliar composição comercial, padrão e excedente; não substitui as composições/memórias canônicas de treliças existentes no Supabase.

### Ordem de decisão obrigatória ao identificar telha diferente da padrão no edital/TR

**Gate 1 — Solicitar a substituição:** Antes de compor custo de telha especial, confrontar a exigência com a telha galvanizada padrão Multi Teiner e **solicitar formalmente ao cliente autorização para utilizar a telha padrão**, apresentando equivalência técnica quando demonstrável. O pedido não equivale a aceite. Verificar desempenho, norma, projeto e resposta formal.

- **Cliente aprova a telha padrão:** usar a composição comercial padrão efetivamente aplicável, **sem excedente de troca de telha**; investigar eventuais outras adequações comprovadas.
- **Cliente não aprova a substituição / exige a telha do TR:** seguir obrigatoriamente ao Gate 2. Na ausência de resposta em prazo hábil, manter a telha exigida como base de atendimento e registrar consulta pendente; nunca orçar telha padrão como se aprovada.

**Gate 2 — Verificar a treliça e toda a estrutura de sustentação:**

- **Treliça padrão confirmada e compatível com a telha do TR:** manter o produto comercial base somente se ele efetivamente contiver treliça padrão e telha galvanizada substituível. Calcular apenas o **diferencial da telha**: `delta_material_m2 = preco_telha_TR_m2 - preco_telha_galvanizada_padrao_m2`; `excedente_telha = delta_material_m2 * area_efetivamente_comparavel_m2`. O Comercial forma o preço a partir da base + excedente validado. Evitar cobrança integral da segunda telha e duplicidade com a primeira.
- **Treliça diferente da padrão ou incompatível com o novo sistema:** **não usar o cálculo isolado de diferença de telha**. Compor **do zero** a solução completa — treliça especial (aço, peças e fabricação), telha especificada, fixações, vedações, acessórios e mão de obra de fabricação, montagem e instalação — conforme projeto e memórias de quantitativos. Conferir o produto comercial original para **retirar/créditar** parcelas que deixem de ser utilizadas, evitando somar a cobertura inteira duas vezes. Não presumir que o preço da treliça padrão ainda se aplica.
- **Compatibilidade da treliça não demonstrada:** registrar `GAP_TRELICA_EQUIVALENCIA`, solicitar projeto/fichas e não fechar o excedente.

**Conferências obrigatórias:** modelo de telha, espessura, material, vãos, treliça, geometria e apoios, dimensões úteis, transpasse, perdas, fixadores e montagem; consultar precedentes existentes de treliça/EXC antes de nova composição. Os preços do material padrão e especial devem ser vigentes, documentados e referidos à mesma unidade/condição comercial. Preço diferencial zero ou negativo exige decisão comercial, sem concessão automática de desconto.

**Alerta quantitativo da SO de origem:** MLT.E03 foi informado com **68 m²**, enquanto o excedente TP100 considerou **72 m²** (10 × 8,00 × 0,90 m). A área da telha galvanizada efetivamente substituída precisa ser conciliada; não presumir crédito de 72 m² se a base abrange apenas 68 m².

### Exemplo reconstruível — válido somente com treliça padrão

| Entrada | Valor | Origem/classificação |
|---|---:|---|
| Telha TP100 0,65 mm | R$ 85,00/m² | Preço informado pelo Analista na SO 238.26 |
| Telha galvanizada padrão | R$ 35,00/m² | Referência informada pelo Analista; verificar composição vigente |
| Telhas especiais | 10 × 8,00 × 0,90 m | Quantidade/dimensão informada pelo Analista |
| Área de referência | 72 m² | Cálculo bruto; validar área comparável |
| Diferença unitária | R$ 50,00/m² | 85 − 35 |
| Excedente ilustrativo | R$ 3.600,00 | 72 × 50; sujeito a reconciliação 68/72 m² |

**Rastreabilidade e governança:** `DOCUMENTO/TR → PEDIR SUBSTITUIÇÃO POR TELHA PADRÃO → RESPOSTA DO CLIENTE → CONFERÊNCIA TRELIÇA PADRÃO? → (SEM EXCEDENTE, DELTA DE TELHA OU COMPOSIÇÃO INTEGRAL) → QUANTITATIVOS → MEMÓRIA SUPABASE → COMERCIAL → PTS PÓS → EVOLUTION GATE`. Não promover preços, áreas ou desenho de treliça da SO 238.26 a padrão universal; nenhuma experiência individual gera regra de Core sem generalização e validação.
