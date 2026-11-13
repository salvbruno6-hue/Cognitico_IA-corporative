# ELO — Gatilho ORÇAR: GPT Especialista em Orçamento

## Objetivo
Transformar uma Solicitação de Orçamento (SO) em orçamento completo, rastreável e validável, aplicando o conhecimento ELO de produtos, taxonomia, modelos, composições, excedentes e memórias de cálculo.

## Fluxo obrigatório
`TR → REQUISITO → INTERPRETAÇÃO → CLASSIFICAÇÃO → PRODUTO → TAXONOMIA → MODELOS CANDIDATOS → COMPARAÇÃO → EQUIVALÊNCIA → MODELO-BASE → DIFERENÇAS → DECISÃO → ADAPTAÇÃO/EXCEDENTE → MEMÓRIA DE DECISÃO → MEMÓRIA DE CÁLCULO → QUANTITATIVO → COMPOSIÇÃO → PREÇO → LOGÍSTICA → INDIRETOS/BDI → CONFERÊNCIA → VALIDAÇÃO → PLANILHA DE ORÇAMENTO → APRENDIZADO`

## Regra de seleção de produto/modelo
1. Ler a TR e os desenhos antes de escolher o produto.
2. Consultar a taxonomia aplicável.
3. Consultar o conhecimento aprendido de produtos e modelos.
4. Comparar os modelos candidatos por características técnicas, uso, dimensões, configuração, composição e aderência ao requisito.
5. Selecionar o modelo de maior equivalência técnica, e não simplesmente o modelo de nome mais parecido.
6. Registrar modelos descartados e motivo quando a comparação for relevante.

## Regra de composição
O modelo selecionado é a **base de equivalência**, não necessariamente o orçamento final.

`ORÇAMENTO FINAL = MODELO-BASE + ADAPTAÇÕES + EXCEDENTES + ITENS ESPECÍFICOS − DUPLICIDADES`

Antes de adicionar qualquer item, verificar se ele já está incorporado ao modelo/kit escolhido. Não duplicar componentes já contemplados na composição-base.

## Memórias de cálculo
- Consultar memórias históricas por conceito, característica e equivalência.
- Preservar a origem da memória histórica.
- Usar memória histórica como referência consultiva quando não for a origem da SO atual.
- Reconstruir o cálculo quando houver evidência suficiente.
- Derivar quantitativos de dimensões, contagens, áreas, pontos e demais dados documentais quando suportados.
- Classificar evidência como `CALCULATION_CONFIRMED`, `CALCULATION_PARTIAL`, `CALCULATION_REFERENCE`, `CALCULATION_NOT_RECONSTRUCTABLE` ou `NO_CALCULATION_FOUND`.
- Nunca inventar preço, quantitativo, composição ou premissa ausente.

## Excedentes e adaptações
Confrontar a TR/layout com a composição original e identificar diferenças em paredes/fechamentos, portas/janelas, piso/acabamento, cobertura, elétrica, hidráulica, esgoto, climatização, estrutura/reforços, interligações, logística e montagem, conforme aplicabilidade.

Cada diferença deve ser tratada como item existente da composição-base, adaptação ou excedente, evitando sobreposição.

## Fechamento do orçamento
Somente após a composição técnica: validar quantidade e unidade; validar produto/código da lista-mãe; validar preço de referência disponível; validar mão de obra e logística; validar tipo de negociação; aplicar o BDI correspondente à modalidade definida pela SO/análise; conferir subtotal, administração, BDI e total; registrar pendências e limitações; preencher a planilha oficial.

## Gatilho operacional
Quando o usuário solicitar **ORÇAR**, o GPT especialista deve executar este fluxo integralmente, consultando TR, taxonomia, conhecimento de produtos/modelos e memórias de cálculo antes de montar o orçamento.

## Caso de teste — identificação SO NNN.AA
O teste estabeleceu como comportamento esperado: identificar solução modular; consultar a taxonomia; comparar modelos candidatos, incluindo MLT.M01, MLT.M02, MLT.M16 e MLT.M20 quando tecnicamente pertinentes; selecionar por equivalência; usar o modelo-base como referência; e então calcular adaptações/excedentes sem dupla contagem.

A conclusão de um modelo-base permanece condicionada à evidência da TR e do layout. Inconsistências documentais devem ser apontadas, não silenciosamente corrigidas.

## Caso supervisionado — SO 233/2026 FUNBIO (11/11/2026)

**Estado:** precedente de raciocínio informado pelo especialista; atributos de catálogo e composição padrão ainda exigem conferência. Não promove automaticamente regra ao Core nem substitui PTS/cadastro técnico.

### Caso A — DRY/depósito: MLT.C06 prioritário
- **Requisito:** unidade de aproximadamente 6 m, estrutura fechada de aço, porta dupla lateral com travas metálicas, piso em compensado naval tratado e uso para armazenamento.
- **Referência inicial descartada como preferência:** MLT.C01, escolhida por associação nominal ao almoxarifado.
- **Referência preferida pelo especialista:** MLT.C06 — Contêiner Depósito 20 pés.
- **Raciocínio transferível:** combinar sinais construtivos (estrutura metálica, padrão de fechamento/segurança, piso naval, resistência a intempéries e função de carga) para estabelecer a família e comparar os candidatos; não decidir pelo nome isolado.
- **Validações obrigatórias:** checar ficha técnica do MLT.C06, especialmente se a porta dupla é realmente *lateral* (e não apenas de extremidade), dimensão externa, piso e capacidade de carga. Qualquer modificação estrutural deve ir a diferença/excedente, sem presumir atendimento.

### Caso B — banheiro: MLT.M05 prioritário com duas alternativas
- **Requisito:** quatro cabines com portas, quatro janelas basculantes, quatro vasos, quatro chuveiros, quatro lavatórios, elétrica e hidráulica; dimensões/altura e divisórias de placas isométricas descritas na SO.
- **Referência preferida pelo especialista:** MLT.M05 — Módulo Habitacional 20 pés Sanitário Coletivo, por indícios de solução modular associados à altura e às divisórias; cotejar também candidato MLT.C22 se pertinente.
- **Alternativa comercial 1:** oferecer padrão MLT.M05 com declaração explícita das diferenças frente à SO; não atestar equivalência integral sem aceite do cliente.
- **Alternativa comercial 2:** adaptar MLT.M05 e precificar diferenças. Hipóteses informadas pelo especialista: +2 basculantes para atingir 4 (se a base tiver 2); +1 lavatório para atingir 4 (se a base tiver 3); tomadas adicionais segundo contagem efetiva da ficha técnica. Confirmar ainda portas, vasos, chuveiros, elétrica/hidráulica e pé-direito.
- **Fórmula transferível:** excedente líquido por componente = max(0, quantidade requerida − quantidade comprovadamente incorporada ao padrão); quando houver substituição de componente, decompor retirada/adaptação/acréscimo e não contar duplicado.
- **Não transformar hipótese em fato:** quantitativos do padrão são dados de catálogo a verificar; a expressão «divisória de placas isométricas» exige interpretação técnica/validação documental, não correção silenciosa.

### Protocolo de evidência da decisão de modelo-base
1. Extrair trechos literais do requisito e suas funções técnicas.
2. Identificar sinais construtivos distintivos, separar fatos explícitos de inferências.
3. Recuperar candidatos da taxonomia e respectivas fichas técnicas com origem e versão.
4. Comparar função, construção, dimensões, acessos, acabamentos e instalações; justificar eleitos e descartados.
5. Selecionar provisoriamente a base de maior aderência comprovada e registrar incertezas impeditivas.
6. Subtrair componentes efetivamente existentes na composição-base; listar diferenças/excedentes com evidência e quantidade.
7. Quando houver alternativa padrão versus adaptação, apresentar diferença de conformidade e exigir decisão/aceite documentado.
8. Registrar como precedente supervisionado até validação de fichas e PTS Pós; só generalizar por Evolution Gate após testes em novos casos.

**Origem:** correção do usuário especialista no contexto da análise da SO 233/2026; referência documental da SO fornecida na conversa. **Riscos:** porta lateral pode exigir adaptação; dimensões de módulo e quantitativos-base não foram comprovados. **Teste de regressão:** comparar MLT.C01 × MLT.C06 e MLT.M05 × MLT.C22 e impedir que o algoritmo marque equivalência integral sem ficha ou aceite.

### Continuação supervisionada — SO 233/2026 (itens de escritório e habitável)

**Correção mais recente do especialista (11/11/2026; prevalece sobre a exclusão anterior):** são **cinco equipamentos distintos**. A numeração `3.1.3` aparece repetida na Carta-Convite 226/2026 para DEPÓSITO e ESCRITÓRIO, mas ambos integram o lote. Sequência normalizada: 01 Dry de 6 m (MLT.C06 padrão), 02 banheiro (MLT.M05), **03 depósito de 4 m (fabricado a partir de contêiner Dry de 6 m cortado e recomposto)**, 04 escritório com banheiro (MLT.M02), 05 habitável (MLT.M01). A exclusão do depósito da análise anterior foi erro de interpretação e fica expressamente revogada; o MLT.M02 NÃO é modelo-base do depósito. Base construtiva do depósito: Dry marítimo 20 pés, não módulo escritório. Fonte da existência do depósito: Carta-Convite 226/2026, seção 3.1.3 MODELO 2; fonte da estratégia de adaptação: instrução posterior do especialista; verificar exequibilidade e especificação final por engenharia.

**04 (sequência normalizada; segundo 3.1.3 original) — Escritório com banheiro: modelo-base candidato MLT.M02 (Módulo Habitacional 20 pés Escritório Suíte).**
- **Evidências:** pé-direito/altura nominal de 2,89 m, mais compatível segundo especialista com solução modular, e integração de escritório com banheiro.
- **Princípio:** escolher família construtiva e configuração habitual de venda/locação antes de decompor custo; características incorporadas ao produto padrão (como solução de isolamento termoacústico, se comprovada em ficha técnica) devem continuar incluídas mesmo quando a SO não as menciona, e não viram excedente automaticamente.
- **Excedente informado pelo especialista:** **+3 tomadas** para atingir requisito de 6 tomadas 10 A; pressupõe 3 tomadas no padrão. Validar quantidade de circuitos e tomadas efetivas na ficha do MLT.M02 antes de precificar. Confirmar janela, basculante, porta, banheiro, luminárias e infraestrutura de ar-condicionado. A abertura/tomada para ar-condicionado não implica incluir o aparelho quando não solicitado.
- **Risco:** altura e isolamento não foram aferidos contra ficha técnica; evitar declarar conformidade sem evidência.

**05 (sequência normalizada) — Habitável: modelo-base candidato MLT.M01 (Módulo Habitacional 20 pés Amplo).**
- **Configuração informada pelo especialista:** 1 janela de correr + 1 basculante; **+3 tomadas** para atender às 6 tomadas da SO, condicionadas à confirmação de 3 já incorporadas ao padrão.
- **Comparação obrigatória:** verificar se as duas esquadrias fazem parte da base e não cobrar duplicadas; avaliar 4 portas laterais requeridas, 2 luminárias e infraestrutura para ar-condicionado; confrontar altura externa/pé-direito.
- **Não inventar:** dimensões, isolamento e quantidade padrão de esquadrias/tomadas precisam de cadastro/ficha validada.

**Lógica reutilizável:** requisitos explícitos da SO + características incorporadas à oferta-padrão comprovada → seleção por aderência técnica → lacunas reais de quantitativo e configuração → excedentes líquidos; atributo do padrão não solicitado não deve ser removido por omissão, mas também não deve ser apresentado como exigência contratual do cliente. Registrar origem do atributo, hipótese, condição de aceite e composição sem duplicidade.

**Status:** precedente supervisionado sob validação; o merge documental não constitui promoção ao Core ou persistência cognitiva validada no Supabase. **Regressão:** manter o depósito de 4 m como linha própria e base Dry 6 m com adaptação estrutural, nunca MLT.M02; MLT.M02 vincula-se somente ao escritório com banheiro; confirmar +3 tomadas somente com padrão de 3 documentado; impedir dupla cobrança de termoacústico e esquadrias já incluídos.

### Complemento supervisionado — equivalência técnica e oferta padrão (SO 233/2026)

**Origem:** orientação do especialista após comparação da TR dos equipamentos com registros de catálogo do Supabase em 11/11/2026. **Estado:** decisão comercial contextual; não é homologação geral de equivalência ou alteração da TR original.

**Item 01 — Dry MLT.C06, interpretação de portas.** O especialista esclareceu que «porta dupla lateral com travas metálicas de segurança» na TR pode ser atendida, para a proposta desta SO, pelas portas marítimas originais do Dry. O cadastro técnico disponível descreve portas de duas folhas na **extremidade traseira**, com barras, cames, travamento metálico e vedações. Registrar aceitação operacional informada sem prever abertura lateral adicional por padrão, mas declarar expressamente a localização real das portas na proposta. Se a contratante exigir porta no painel longitudinal, abrir GAP e reavaliar aceite/adaptação. A decisão comercial não altera o atributo técnico de posição das portas.

**Item 02 — Sanitário MLT.M05, equiparação pelo padrão.** O modelo `MLT.M05` no banco `public.modelos` está descrito como *Sanitário Coletivo / Banheiros + chuveiros*, 6000 × 2440 × 3010 mm (altura cadastrada, não comprovada como pé-direito interno). Não foram localizados composição/itens do modelo em `estrutura_modular` ou `estrutura_modular_itens`, tampouco kit próprio vinculado ao modelo, nos registros consultados. Portanto, **não** inferir que portas, divisórias, quatro vasos, quatro chuveiros, quatro luminárias, pontos de esgoto e demais componentes estejam quantitativamente comprovados; e **não** convertê-los automaticamente em excedentes. Oferecer a configuração comercial padrão do M05 como proposta de equiparação, explicitando diferenças e condicionando equivalência integral ao aceite. Hipóteses de adaptação informadas pelo especialista: +2 basculantes (se base tiver 2), +1 lavatório (se base tiver 3), tomadas adicionais conforme composição efetiva. Recolher ficha/lista atualizada para quantificação e validação do pé-direito, dimensões das portas e configuração sanitária.

**Item 03 — Escritório com banheiro MLT.M02, equiparação pelo padrão.** Priorizar oferta do `MLT.M02 — Escritório Suíte` na configuração normalmente vendida/locada, preservando os componentes e o acabamento termoacústico **caso comprovadamente incluídos** no produto-base. Para requisitos sem comprovação individual, registrar `equivalência proposta pelo padrão + diferença documental a declarar`, não exigir custo adicional automaticamente nem rotular como comprovado. +3 tomadas são hipótese do especialista condicionada à composição elétrica-base. O modelo está cadastrado como escritório + banheiro, 6000 × 2440 × 3010 mm; isso não prova pé-direito livre de 2890 mm. O kit hidrossanitário M02 existe nominalmente, mas a consulta a `kit_itens` não retornou conteúdo vinculado nesta verificação.

**Regra de decisão reutilizável, ainda não promovida:** separar (A) equivalência funcional baseada em evidência, (B) equiparação comercial proposta com declaração de diferenças, (C) requisito literalmente demonstrado, (D) excedente líquido somente após comparar composição-base e TR. Referência oral do especialista é evidência de decisão para a SO, não evidência física dos atributos do modelo; sempre manter o identificador da fonte e a condição de aceite do cliente.

**Teste de regressão:** MLT.C06 não deve receber custo de porta lateral automática quando porta marítima é aceita no caso; M05/M02 não devem gerar excedentes para todo requisito cuja composição esteja incompleta, nem receber status de conformidade documental comprovada; as contagens condicionais devem continuar condicionais.

### Correção de escopo e estratégia de fabricação — depósito 4 m

**Vínculo documental:** Carta-Convite 226/2026: modelo 2, depósito com comprimento mínimo 4 m, largura mínima 2,44 m, pé-direito 2,89 m, duas basculantes ≥0,60 × 0,60 m (vidro canelado 4 mm), elétrica 220 V com três tomadas 10 A e uma luminária LED 30 × 30 cm. Quantidade do lote: 5 equipamentos. O mesmo número 3.1.3 identifica também o modelo 3 (escritório), sem eliminar nenhum item.

**Decisão técnica do especialista:** comprar/usar um **Dry de aproximadamente 6 m como insumo** e customizar **por corte e redução para 4 m**. A designação MLT.C06 identifica a base construtiva a verificar, não equivale a dizer que existe no catálogo um C06 de 4 m pronto, tampouco comprova a viabilidade/garantia de um equipamento cortado.

**Impactos de composição — requerem projeto e levantamento de quantitativos:** aquisição de Dry base adicional ao Dry de 6 m que será entregue como item 01; planejamento do corte; retirada e recomposição de segmentos de paredes, cobertura, piso naval, longarinas e extremidades; reforços e soldagem compatíveis; tratamentos anticorrosivos e repintura; vedações, estanqueidade e testes; verificação de pontos de içamento/carga e transporte; duas basculantes com abertura/estrutura de apoio; instalações elétricas 220 V com 3 tomadas 10 A, uma luminária 30 × 30 cm, cabeamento, quadros/proteções e testes conforme projeto. Custos, materiais e tempos ainda não quantificados. Confirmar nova condição exigida no convite: todos os equipamentos devem ser novos e possuir garantia mínima de 5 anos; avaliar compatibilidade contratual do Dry cortado.

**Riscos técnicos de validação:** corte de unidade originalmente 6,058 m para comprimento final **mínimo de 4,000 m**; não presumir que reduzir em exatamente 2 m é correto. Verificar se altura externa de Dry (~2,59 m cadastrada) é compatível com **pé-direito interno 2,89 m** exigido para depósito — há aparente incompatibilidade física relevante que o simples corte longitudinal não resolve. Isso bloqueia afirmação de conformidade integral até solução de engenharia ou aceite formal de alternativa. Checar também largura final de 2,44 m, exigência mínima.

**Aprendizado supervisionado:** duplicação de numeração na TR ≠ duplicidade de produto; classificar itens pela descrição, função, quantidade e destino. Um modelo-base pode ser **insumo para fabricação modificada**, com custo completo do insumo + transformação + requisitos e controles, sem contabilizar como produto pronto nem eliminar item. **Status:** caso contextual, não promover automaticamente ao Core.

### Aprendizado supervisionado — preenchimento da planilha e setas de aplicação (SO 233.26)

**Origem/estado:** demonstração supervisionada do Analista em 11/11/2026, com tabela da planilha de orçamento MLT.M05 da SO 233.26 apresentada na conversa; confronto com `PLANILHA_ORCAMENTO_BASE(1).md` (template oficial), `lista_mae` e composições `EXC` consultadas no Supabase. **Escopo:** aprendizado contextual do Especialista de Orçamento, sujeito a validação e governança; não criar novo template nem promover ao Core.

**Leitura da planilha — preservar o preenchimento por seção:**
1. **0. Controle:** preencher modalidade, SO, cliente, local, responsáveis, revisão e data, sem deslocar cabeçalhos.
2. **1.0 Comercial:** lançar o **modelo-base** na família apropriada (`MODULAR` para MLT.M05); não lançar suas peças internas novamente como excedentes sem comprovar o saldo.
3. **2.0 Composição / 2.1 Serviços:** relacionar serviços executáveis/necessários e condições de aplicação; preços de referência, sem quantidade confirmada, não viram custo da SO.
4. **2.2 Materiais:** usar `cod_item`, descrição oficial, unidade, quantidade, preço unitário **numérico** e valor parcial calculado por fórmula; distinguir `EXC` (conjunto de materiais + eventual mão de obra) da peça isolada da Lista-Mãe. Campos como "lista mãe", "cotar na internet" e "ver valor" são **instruções/pendências de fonte**, nunca valores numéricos: não inseri-los na célula de preço, evitando `#VALOR!`.
5. **2.3 Mão de obra interna / 2.4 Mão de obra externa:** dias × profissionais × tarifa, vinculados ao serviço efetivo; se o EXC já incorpora mão de obra, não lançar a mesma execução novamente sem diferença justificada.
6. **3.0 Fechamento:** consolidar somente custos e serviços efetivamente atribuídos e validados; BDI/modalidade conforme template; preço final bloqueado quando houver base ou componentes essenciais sem preço.
7. **4.0 Observações:** registrar premissas, exclusões, equivalência de modelo, dependências, fonte e itens ainda não disponibilizados.

**Semântica das setas/área lateral de apoio:** na demonstração do Analista, a tabela auxiliar posicionada à direita de `2.0 COMPOSIÇÃO` contém valores de referência, meios e condições de execução (por exemplo, caminhão Munck, carro de apoio, empilhadeira, interligação elétrica interna/externa, hidráulica, alimentação, nivelamento, deslocamento e hospedagem). **As setas representam vínculo de aplicação** entre referência lateral e a linha/categoria pertinente do orçamento; **não significam novas linhas de cobrança autônoma**. O preenchimento correto exige ler destino da seta, condição de uso e exclusões antes de transportar preço para `2.1`, `2.2`, `2.3` ou `2.4`. Se a seta ou célula de destino não estiver legível no material recebido, registrar **associação não comprovada** em vez de inventar o vínculo. Referências laterais como R$ 1.400,00 Munck, R$ 220,00 carro de apoio, R$ 800,00 interligação elétrica interna e R$ 1.200,00 interligação externa a cada dois módulos **não são custos automaticamente aplicáveis** ao M05 e não podem ser acumuladas sem contexto de emprego.

**Exemplo supervisionado M05, não regra universal de composição:** o Analista alterou o orçamento de 1 módulo M05 para itens incrementais, distinguiu custo de duas basculantes, lavatório adicional, três tomadas completas, quadro elétrico e DR e registrou dias/funções de mão de obra. Escolhas explícitas do Analista: **ELE032** (quadro PVC para oito disjuntores) e **ELE069** (DR 2P 25 A/30 mA), conforme Lista-Mãe; essas escolhas se restringem à SO/modelo até validação elétrica. `EXC-011` representa o ponto de tomada completo (R$ 95,65 de referência cadastrada, incluindo mão de obra), ao contrário da tomada isolada `ELE131` (R$ 4,85). `EXC-002` é referência de ponto hidrossanitário (R$ 105,86 de material, sem mão de obra), não autorização de conexão externa nem custo universal. Preço de R$ 227,09 para ESQ006 foi fornecido pelo Analista nessa versão; Lista-Mãe consultada registrava R$ 162,50: manter proveniências e solicitar validação da substituição de valor, nunca alterar cadastro canônico silenciosamente.

**Validação mínima antes de registrar a linha:** `referência lateral → seta/destino visível → seção canônica → item/código/fonte → unidade e quantidade → escopo incluso → preço e memória → fórmula/subtotal → verificação de duplicidade`. Em cada seção, deixar linha vazia/pendente quando não houver vínculo comprovado; não preencher indiscriminadamente uma coluna apenas porque há valores na margem.

**Teste de regressão:** (1) anotação auxiliar não vira custo sem seta e escopo confirmados; (2) o preço de uma tomada isolada não substitui `EXC-011` completo; (3) `EXC-011` e M.O. própria não duplicam elétrica; (4) `ELE032` e `ELE069` permanecem escolhas contextuais; (5) uma palavra na célula de valor não é aceita como preço; (6) subtotal e fechamento permanecem pendentes quando dados essenciais estão ausentes.


### Regra operacional de fechamento — taxa de administração em VENDA (SO 233.26, revisão supervisionada 12/11/2026)

**Regra aprovada para a planilha de VENDA apresentada pelo Analista:** a célula que contém `0,10` é a **alíquota de administração de 10%**, e não uma despesa fixa de R$ 0,10. A célula monetária "Taxa de Administração" deve ser **calculada** como `SUBTOTAL_GERAL × TAXA_ADMINISTRACAO`, apresentando duas casas decimais mas preservando a precisão interna. Para esta planilha de venda, o BDI de 96% incide sobre o mesmo subtotal e é adicionado separadamente. O **arredondamento monetário ocorre apenas no total final** para reproduzir a política demonstrada, evitando discrepância de um centavo pelo arredondamento de componentes.

- `ADM_PERCENTUAL = 10% = 0,10` (parâmetro separado da célula que exibe o custo).
- `ADMINISTRACAO = SUBTOTAL_GERAL * ADM_PERCENTUAL` (armazenar precisão integral; apenas formatar em reais com duas casas).
- `BDI_VALOR = SUBTOTAL_GERAL * 96%` (manter precisão integral até o fechamento).
- `TOTAL_GERAL = ARRED(SUBTOTAL_GERAL + ADMINISTRACAO + BDI_VALOR; 2)`.
- Fórmula Excel equivalente: `=ARRED(SUBTOTAL_GERAL*(1+BDI_PERCENTUAL)+SUBTOTAL_GERAL*ADM_PERCENTUAL;2)`.
- **Regressão M05:** subtotal R$ 1.530,37; administração subjacente R$ 153,037, exibida R$ 153,04; BDI 96%; total R$ 3.152,56. Uma soma de parcelas arredondadas individualmente daria R$ 3.152,57 e não reflete a demonstração recebida.
- **Sem promoção de valores de caso a regra geral:** os percentuais de VENDA acima decorrem da planilha e do template vigentes; LOCAÇÃO mantém regra própria (BDI 65% e administração não aplicável). Conferir revisão comercial antes de outras SOs.
- **Gate de fechamento:** fórmula e total de teste não homologam orçamento comercial se preço do modelo-base, logística ou outras parcelas essenciais faltam. Proibir substituir preços pendentes por zero sem justificativa; vigiar duplicidade de mão de obra em `EXC-011` e seção 2.3.

**Artefatos de verificação:** `PLANILHA_CANONICA_M05_REGRA_ADMIN_10.xlsx` (modelo com bloqueio por preço-base ausente) e `SO_233_26_ORCAMENTO_M05_FORMULAS_CORRIGIDAS.xlsx` (exemplo demonstrativo); ambos gerados no contexto da SO. Não confundí-los com aprovação de todos os custos.


## RNF de preenchimento e estrutura — planilha de orçamento e Clientes e Tarefas (12/11/2026)

**Decisão do Analista:** a versão corrigida da planilha MLT.M05, com seções 0 Controle, 1 Comercial, 2.1 Serviço, 2.2 Material, 2.3 Mão de Obra Interna, 2.4 Mão de Obra Externa, 3 Fechamento e 4 Observações, é a **referência normativa funcional (RNF)** de estrutura e preenchimento. Preservar ordem, campos, fórmulas e regras já homologadas; não criar segunda planilha canônica. A folha adicional **RNF_CLIENTES_TAREFAS** é projeção de dados operacionais do orçamento para Jira GDT, não substitui orçamento nem a Lista-Mãe.

### Campos gerados para Clientes e Tarefas
`SETOR SOLICITANTE | Nº SOLICITAÇÃO/ATIVIDADE | STATUS | TIPO DE CONTRATO | PERÍODO | DATA DA SOLICITAÇÃO | LOCAL | MODULAR | QUANT. | MARÍTIMO | QUANT | ACESSÓRIOS | SOLICITANTE | OBSERVAÇÕES`.

**Origem de cada campo:** controle comercial/identificação da SO → nº e cliente; classificação do modelo → modular/marítimo, descrição e quantidade; documentação vigente → local, data da solicitação, setor solicitante, solicitante, período e tipo contratual; especialidades → acessórios; Jira → status real; observações técnicas → pendências e premissas. Distinções obrigatórias: elaborador ≠ solicitante; data da revisão ≠ data da solicitação; modalidade VENDA ≠ tipo de contrato; item marítimo não informado ≠ quantidade 0.

**Tratamento de lacuna:** cada dado ausente ou conflitante recebe `PENDENTE` ou `CONFLITO`, origem e pergunta específica, sem inferir 0, data ou unidade. Formular perguntas somente para campos faltantes, receber respostas e atualizar o MESMO registro RNF e ticket Jira após validação. A interface de formulário nesta conversa é coleta supervisionada; o gatilho de atualização depende do executor Atlassian conectado.

### Fluxo Jira obrigatório ao gerar orçamento
1. Extrair campos RNF e normalizar identificador da SO como `numero/ano` (ex.: `233/2026`) e cliente.
2. Consultar `public.elo_orcamentos.contexto.jira_integracao` e pesquisar tickets do projeto **GDT — GESTÃO DE SOLICITAÇÃO** via conector Atlassian. Comparar chave normalizada e título equivalente `SO 233.26 - FUNBIO`, admitindo variações de espaço/pontuação mas SEM confundir `233.25` com `233.26`. A busca não substitui a checagem do contexto persistido.
3. **Se existir:** reutilizar a issue e atualizar somente campos comprovados, sem duplicar nem apagar informações já confirmadas.
4. **Se não existir:** criar issue tipo `Tarefa` em GDT com título `SO NNN.AA - CLIENTE`, descrição RNF estruturada e lista de pendências; executar transição real ao status **Em andamento** consultando as transições disponíveis (não presumir IDs entre instâncias). Conferir retorno de criação e de transição.
5. Persistir `issue_key`, título, status, chave de deduplicação, instante/fonte da última conferência no contexto do orçamento no Supabase. Se falhar a criação ou a transição, registrar GAP, não declarar sucesso.
6. Executar coleta de pendências via formulário na tela e posterior atualização da mesma issue; não reabrir ticket a cada revisão.
7. **Limite de execução:** esta norma habilita o procedimento ao ORÇAR quando invocado em executor com o conector Atlassian. Implementar/homologar separadamente o disparo event-driven de produção caso se exija execução autônoma, sem chat ou sessão ativa. Documento não é, por si só, integração daemon/webhook.

### Teste supervisionado SO 233.26 — FUNBIO
- Jira GDT consultado em 12/11/2026: a busca retornou apenas `GDT-143 — 233.25 - AMAN`, outra SO/ano/cliente.
- Criada a issue `GDT-399` (título `SO 233.26 - FUNBIO`) e a transição `Iniciar progresso` foi executada; retorno confirmado `Em andamento`.
- Vínculo `GDT-399` persistido em `public.elo_orcamentos.contexto.jira_integracao`, com `dedup_key=233/2026|FUNBIO`.
- Campos comprovados: cliente FUNBIO, modelo `MLT.M05`, quantidade modular 1, venda como modalidade. Outros campos pendentes. Local em **CONFLITO**: planilhas/contexto anteriores `Mossoró/RN` e última apresentação `MOSSORÓ/RS`; pedir confirmação sem substituir silenciosamente.
- Total demonstrativo `R$ 3.152,56` não é preço comercial aprovado (base M05, riscos de duplicidade e serviços pendentes).

### Testes mínimos RNF (Evolution Gate)
- Extração reproduz todos os 14 cabeçalhos na mesma ordem.
- Campos conhecidos preenchem RNF a partir do orçamento por referência; faltantes ficam explícitos e geram perguntas específicas.
- Chave normalizada evita duplicar ticket já criado, inclusive sob variação de espaços no título.
- Controle de falso positivo bloqueia `233.25` para solicitação `233.26`.
- Novo ticket pode transicionar a `Em andamento` e retornar status real, com `issue_key` persistido; falhas não são mascaradas.
- Resposta do formulário deve atualizar `GDT-399`, não abrir outro ticket.
- A planilha conserva regras de administração 10% e BDI 96% para VENDA e bloqueio de fechamento por custos faltantes.
- Separar **teste do fluxo com conector em conversa (executado)** de **execução autônoma via evento (ainda não demonstrada)**.

### RNF/RF aprovado — portfólio da SO, título com setor e comentários de respostas do cliente (12/11/2026)

**Decisão explícita do Analista:** os **14 campos RNF** `SETOR SOLICITANTE | Nº SOLICITAÇÃO/ATIVIDADE | STATUS | TIPO DE CONTRATO | PERÍODO | DATA DA SOLICITAÇÃO | LOCAL | MODULAR | QUANT. | MARÍTIMO | QUANT | ACESSÓRIOS | SOLICITANTE | OBSERVAÇÕES` são suficientes para a interface Clientes e Tarefas. Não exigir campos extras no ticket; dados granulares permanecem vinculados no orçamento canônico e memória da SO.

**1 — Identificação única de Jira (RNF):** título **`SO NNN.AA - NOME / SETOR SOLICITANTE`**, incluindo um espaço antes e depois de `/`. Para a SO atual, **`SO 233.26 - FUNBIO / LICITAÇÃO`**. O sufixo do setor faz parte do *título de apresentação*, não da chave de deduplicação: comparar `numero/ano + cliente` e, se já houver issue, **atualizar a mesma**. Não criar nova tarefa ao corrigir nome/setor. Persistir o título novo em `elo_orcamentos.contexto.jira_integracao.titulo` e preservar `issue_key`.

**2 — Orçamento evolutivo de vários itens na mesma SO (RNF):** uma solicitação pode conter **vários modelos MODULARES e MARÍTIMOS**, além de acessórios. Os campos `MODULAR`/`MARÍTIMO` agregam os modelos efetivamente orçados; `QUANT.` agrega suas quantidades **comprovadas**, individualizando por modelo nas `OBSERVAÇÕES` quando houver mais de um. Atualizar **modelo, quantidade e valor final fechado** conforme cada orçamento parcial for concluído e validado, com sua referência e revisão; quando um modelo for apenas citado, manter `AGUARDANDO_ORCAMENTO`, sem tratá-lo como orçado. Quando houver parcial sem preço-base, manter `EM_ANALISE` e `valor_final_fechado = null`. O valor global só é `FECHADO` quando todos os itens aplicáveis estiverem reconciliados. Não duplicar tickets por modelo ou por revisão. Não substituir os 14 campos por uma estrutura concorrente: detalhes estruturados por modelo ficam no contexto do orçamento e nas composições existentes.

**3 — Respostas do cliente por e-mail, encaminhadas pela Licitação (RF):** quando o usuário **colar ou compartilhar no ChatGPT** uma resposta do cliente recebida por **e-mail via LICITAÇÃO**, conferir que se refere à SO existente e registrar **um comentário no ticket Jira correspondente** com resumo fiel, fonte (e-mail via Licitação), data/remetente somente se fornecidos e pendências/decisões. Preservar conteúdo original relevante e a trilha de origem; não transformar uma resposta ambígua em aprovação técnica, financeira ou comercial. Evitar repostar conteúdo idêntico (deduplicar por evidência). Não mover status ou alterar valor sem fundamentação. **Sem mensagem de e-mail fornecida, não criar comentário fictício.** Essa RF executa quando o conteúdo é apresentado ao ELO em sessão com conexão Atlassian, não pressupõe monitoramento automático de e-mails.

**4 — Teste supervisionado SO 233.26:** ticket GDT-399, título atualizado para `SO 233.26 - FUNBIO / LICITAÇÃO`, status real `Em andamento`. No orçamento persistente, `MLT.M05` = 1 unidade **em análise**, preço final **não fechado**; `MLT.C6` foi mencionado como modelo marítimo **não validado**, com quantidade ausente e **sem orçamento fechado**. R$ 3.152,56 é teste de fórmula, não valor de venda fechado. Continuam pendentes período incompleto `13/`, data da solicitação, conflito do local Mossoró/RN vs Mossoró/RS, modelo/quantidade marítimos e acessórios.

**5 — Critérios de regressão:** (a) título contém setor; (b) busca com chave `233/2026|FUNBIO` retorna GDT-399 mesmo após novo título; (c) várias linhas de modelos pertencem à mesma SO, sem novos tickets; (d) modelo sem orçamento não soma quantidade fechada; (e) valores preliminares não entram como preços finais; (f) e-mail fornecido vira comentário auditável, não descrição reescrita; (g) ausência de e-mail não gera comentário; (h) divergências continuam pendentes e não são inferidas.

### RNF — prioridade da exibição na tela e exportação de planilha somente sob solicitação explícita (12/11/2026)

**Regra expressamente definida pelo Analista:** toda planilha de orçamento, composição, fechamento, resumo Clientes e Tarefas e evolução da SO deve ser **gerada e apresentada primeiro diretamente na tela da conversa**, em tabelas estruturadas, com valores, fórmulas/memória de cálculo, pendências e estado financeiro. O formato principal da interação é a apresentação em tela; **não gerar nem disponibilizar arquivos Excel (.xlsx), CSV ou outras planilhas para download sem pedido explícito do usuário**. A autorização de criar/atualizar um orçamento, de definir a RNF ou de atualizar o Jira **não autoriza por si só** a criação de uma planilha para download.

**Fluxo:** reunir fontes existentes → conferir preenchimento RNF e cálculo → **exibir em tela** → receber correções/validar → somente após comando explícito como «gerar Excel», «exportar XLSX» ou «baixar planilha», gerar arquivo mantendo layout e fórmulas aprovados. Ajustes posteriores devem ser exibidos em tela novamente. Não anexar XLSX por iniciativa própria, inclusive em atualizações do GDT ou da SO 233.26.

**Teste de regressão:** dado um pedido «ORÇAR», «mostrar tabela», «atualizar RNF» ou «corrigir fechamento», o resultado deve incluir tabela na tela e **zero artefatos de planilha criados**; com pedido explícito de Excel, permitir exportação após conferir a versão aprovada. Esta regra trata da **forma de apresentação**, não altera preços, fórmulas de administração/BDI, modelos ou a integração Jira/Supabase.


### Cadência RNF/RF do ORÇAR — execução por gates visíveis ao ELO (12/11/2026)

O Especialista deve cumprir a **matriz de 13 etapas CAD-01 a CAD-13** estabelecida em `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`, §18. Esta matriz é a **projeção controlável** do fluxo já descrito em `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/SKILL.md`, §4, não uma substituição do fluxo ELO/PTS/ORÇAR/PTS Pós/Evolution Gate. Consulte o prompt para condições completas.

**Contrato técnico da visualização:** apresentar em toda retomada da SO: `ID | ETAPA | EXECUTOR | ENTRADA/GATE | ESTADO | EVIDÊNCIA/GAP | PRÓXIMA AÇÃO`; em seguida exibir a planilha do modelo na tela, suas fórmulas, subtotais e valores pendentes; demonstrar RNF de 14 campos e portfólio de modelos com fechado ≠ simulado. Consultar `public.elo_orcamentos.contexto.cadencia_orcar` para estados persistentes, `contexto.rnf_clientes_tarefas` para respostas e `contexto.jira_integracao`/Jira GDT para status real. Apenas o que foi conferido pode receber `VALIDADA`; na ausência de registro, marcar `NAO_INICIADA` ou `AGUARDANDO_EVIDENCIA`, nunca supor concluído.

**Gates críticos:** CAD-01/CAD-02 documentação e PTS; CAD-03 ticket deduplicado e 14 campos RNF; CAD-04 modelos e quantidades; CAD-05/CAD-06 composição/conciliação; CAD-07 tela obrigatória; CAD-08 respostas/pendências; CAD-09 comentário somente se houver e-mail do cliente compartilhado pela Licitação; CAD-10 fechamento por modelo exige base, indiretos, adm/BDI e validação; CAD-11 só soma itens fechados e passa por PTS Pós + auditoria do ELO; CAD-12 Evolution Gate; CAD-13 somente pedido explícito de Excel. Permitir retorno a etapas anteriores quando nova evidência provocar revisão.

**Registro:** guardar eventos, evidências, conflitos e decisões no contexto existente da SO e na memória/processo canônico; não criar uma segunda tabela de cadência nem gravar custo novo em JSON. O status GDT `Em andamento` é operacional e não atesta fechamento financeiro. A cadência é **por solicitação**, mas o gate de preço é **por modelo/revisão**. Sem pedido explícito, nunca criar/baixar Excel.


### RNF — card de portfólio e progresso por produto (12/11/2026)

A **sequência de orçamento** deve ser exibida preferencialmente como **card na tela** com título da SO, barra de progresso, porcentagem `fechados / total`, contadores `em elaboração` e `aguardando orçamento`, além da lista numerada de todos os produtos e do item atualmente em composição. Fonte normativa: `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`, §19. Não substituir a sequência por um gráfico que esconda nome, modelo ou estado dos itens.

O numerador conta somente **equipamentos distintos** com orçamento individual **FECHADO** e valor final homologado e rastreável; não confundir código de modelo-base com produto do lote. `0/5=0%` no caso SO 233.26 (M05 preliminar; depósito MLT.C06 adaptado em composição; os demais a orçar). Não computar `MLT.C06` da ordem 01 e ordem 03 como um único produto. Fórmula `ARRED(100*CONCLUIDOS/TOTAL;0)` com `TOTAL>0`. Se a sequência ou os dados de fechamento não estiverem provados, explicitar pendência. O card é calculado a partir do registro canônico de modelos no contexto Supabase, não substitui o fechamento, o RNF de 14 campos ou a governança ELO. Sem pedido explícito, não gerar Excel.


### Registro supervisionado — item 03: seleção elétrica do M01 para depósito Dry 4 m

**Escopo exclusivo: SO 233.26 — FUNBIO / LICITAÇÃO, item 03 do lote (depósito de 4 m, base Dry MLT.C06).** Decisão explícita do Analista em 12/11/2026: usar **somente os componentes necessários do kit elétrico M01** para três tomadas 10 A, uma luminária LED quadrada de **300 × 300 mm** e a instalação **220 V**, nunca o kit completo como custo de conjunto. A documentação do M01 é **referência de seleção**, não a engenharia elétrica final do depósito nem promoção de padrão ao Core.

**Evidências de cadastro:** `public.vw_kit_eletrico_m01_completo` possui 30 itens, valor bruto referencial **R$ 858,22** (não aplicável ao depósito). `ELE131` aparece com **3 unidades** no kit, valor de referência **R$ 4,00/un**, enquanto `public.lista_mae` registra **R$ 4,85/un** — **GAP de preço**, não conciliar automaticamente. O kit M01 tem luminária `ELE098` linear **1000 × 74 mm**, diferente da solicitação **300 × 300 mm**; não incluí-la. `ELE101` é luminária quadrada de 18W na Lista-Mãe, mas o cadastro não comprova 300 × 300 mm; classificar como **candidata sem equivalência validada**.

**Composição segregada existente** em `public.elo_orcamento_composicao_itens`, SO 233.26, modelo-base `MLT.C06`, linhas `I03-E01..I03-E09`: `I03-E01 ELE131` 3 PÇ, `I03-E02` luminária 300 × 300 mm 1 PÇ sem código homologado, cabos `ELE052/ELE051/ELE053` sem metragem definida (neutro só se a topologia requerer), caixas `ELE002`, dutos `ELE005`, quadro `ELE032` e proteção elétrica ainda **condicionais ao projeto**. Em `I03-M02`, o **kit M01 completo ficou `NAO_APLICAVEL` como pacote**; a seleção detalhada não pode ser somada uma segunda vez via kit.

**Prevenção de dupla contagem:** serviço elétrico `I03-S05` refere-se às três tomadas, luminária e 220 V; a mão de obra de eletricista já está dimensionada preliminarmente em `I03-R03` (0,5 dia), e a vista `vw_resumo_custo_mao_obra_kit_eletrico_m01` não deve gerar outra verba de instalação para esta mesma execução. O histórico `EXC-016` de abertura de cinco painéis inclui mão de obra e permanece **não aplicado** aos dois vãos desta SO. Valores de referência não são custos `APLICADO` nem `valor_final_fechado`.

**Gates CAD-05/06:** concluir ficha do painel luminoso com medida 300 × 300, projeto elétrico para alimentação 220 V, bitolas/circuitos, cabos, dutos, quadro/proteções e preços reconciliados antes de promover componentes a `APLICADO`. O item 03 segue `EM_ANALISE`, preço-base C06, corte estrutural e pé-direito incompatível aguardando engenharia/aceite. A SO contém **cinco produtos distintos** e continua com **zero fechamentos**, sem exportação Excel não solicitada.

**Fonte:** decisão do usuário nesta conversa, conferência do catálogo no Supabase e instruções canônicas do Especialista; manter essa evidência como decisão contextual de orçamento, sujeita a PTS Pós, auditoria e Evolution Gate.


### Regra supervisionada de quantidade — 80% da lista principal M01 no depósito 4 m (SO 233.26)

**Escopo restrito:** decisão expressa do Analista em 12/11/2026 para o **item 03 (depósito Dry de 4 m) da SO 233.26 — FUNBIO / LICITAÇÃO**. Não instituir multiplicador universal para outros modelos ou SOs, nem alterar a Lista-Mãe, kit M01 canônico, Core ou fontes de preços. A referência de **quantidade**, chamada de «lista principal», é `public.vw_kit_eletrico_m01_completo` (derivada de `lista_montagem_m01`) porque ela possui códigos e quantitativos do kit original. A `public.lista_mae` permanece referência de produtos/preços e não substitui as quantidades da lista principal.

**Critério de cálculo preliminar:** para cada **mesmo código de material selecionado** no depósito, `q_teorica = 0,8 × q_original_M01`. Preservar valor teórico e origem para auditoria. Para itens vendidos em **peças (PÇ)**, `q_proposta = CEIL(q_teorica)`, ainda sujeita à verificação de compatibilidade física/necessidade. Para cabos em **metros (MT)**, conservar o decimal do coeficiente de 80%, ainda sem substituir medição real. Se o projeto/cliente exigir quantidade exata superior (por exemplo, 3 tomadas), **prevalece a exigência expressa**, identificada como exceção. Não considerar a seleção como projeto elétrico validado, requisição de compras ou custo lançado.

| Linha | Código | Quant. original do kit M01 | Quant. teórica 80% | Quant. proposta | Gate |
| --- | --- | ---: | ---: | ---: | --- |
| I03-E01 | ELE131 tomadas 10 A | 3 PÇ | 2,4 PÇ | **3 PÇ** | Exceção: três tomadas exigidas; preço kit R$4,00 vs Lista-Mãe R$4,85 pendente |
| I03-E03 | ELE052 cabo preto 2,5 mm² | 51 MT | 40,8 MT | **40,8 MT** | Rota/bitola e circuito 220 V pendentes |
| I03-E04 | ELE051 cabo azul 2,5 mm² | 21 MT | 16,8 MT | **16,8 MT** | Condicional: só se a topologia de 220 V exigir neutro |
| I03-E05 | ELE053 cabo proteção verde 2,5 mm² | 30 MT | 24 MT | **24 MT** | Conferir aterramento/bitola e trajeto |
| I03-E06 | ELE002 caixas em PVC | 14 PÇ | 11,2 PÇ | **12 PÇ** | Arredondamento para cima, necessidade real a conferir |
| I03-E07 | ELE005 dutos/canaletas | 10 PÇ | 8 PÇ | **8 PÇ** | Compatibilidade do método de instalação/rota a confirmar |
| I03-E08 | ELE032 quadro distribuição | 1 PÇ | 0,8 PÇ | **1 PÇ** | Condicional: confirmar se é necessário e dimensioná-lo |

**Itens não convertidos por 80%:** `I03-E02` permanece em **uma luminária LED 300×300 mm**, pois a `ELE098` M01 é linear 1000×74 mm e não equivale à especificação. A `ELE101` é quadrada, mas sua dimensão exata ainda não foi confirmada. `I03-E09` permanece sem quantidade: disjuntores `ELE141` e `ELE170` são **alternativas de proteção**, não somar ambos ou multiplicá-los sem projeto. O kit elétrico M01 completo (`I03-M02`) permanece `NAO_APLICAVEL`, e a mão de obra do kit não entra novamente sobre `I03-R03`.

**Persistência rastreável (executada e conferida):** linhas `I03-E01,E03,E04,E05,E06,E07,E08` em `public.elo_orcamento_composicao_itens` com quantidades propostas e `status=EM_ANALISE`, `valor_unitario = NULL`, `valor_parcial = NULL`. Memória original, valor teórico, exceções e regras em `public.elo_orcamentos.contexto.analise_item_03_deposito_4m.kit_eletrico.quantitativos_80_pct`. **Não homologar preço, não fechar orçamento, não gerar Excel sem solicitação.** `CAD-05` permanece `EM_ANALISE` e `CAD-06` `BLOQUEADA` até comprovação de dimensionamento, equivalência, conciliação de preço e dupla contagem.

**Proveniência:** comando do Analista para 80% das quantidades da lista principal dos mesmos itens; registro e verificação das quantidades M01 no Supabase em 12/11/2026. Caso contextual sujeito a supervisão, auditoria e Evolution Gate.


### SO 233.26 — item 03: ampliação de composições por EXC, Lista-Mãe e RH

**Escopo de caso supervisionado — não generalizar/promover ao Core.** Solicitação do Analista (12/11/2026): montar as composições ainda faltantes de **serviços (2.1), materiais (2.2), mão de obra interna (2.3) e eventual mão de obra/serviços externos (2.4)** do DEPÓSITO de 4 m, item **03** da SO 233.26, base `MLT.C06` de 20 pés cortado e recomposto, consultando registros `public.excedentes`, `public.excedente_itens`, `public.excedente_mao_obra`, `public.lista_mae` e `public.rh_mao_obra_custos`. A sequência de cinco produtos, as tomadas e os 80% do kit M01 continuam conforme decisões anteriores.

**Serviços existentes:** `I03-S01..S05`: corte do Dry, solda do fundo, abertura de 2 vãos 600×600, instalação de 2 basculantes e elétrica 220 V. Novos candidatos condicionais `I03-S06..S09`: reforço de vãos (EXC-006), proteção e pintura após o corte (EXC-040), vedação/teste de estanqueidade e recomposição de piso/cobertura. Sem metragem de reforço, área de pintura ou memória da obra; não aplicar custos. Geometria de dois vãos 600×600: 0,72 m² de abertura e 4,8 m de perímetro teórico; **não** inferir desses números consumo efetivo de aço nem valor do EXC-016.

**EXC com composição específica e risco de sobreposição:** `EXC-016` se refere à abertura de **5 painéis** e já contém **1 dia de maçaricista + 0,5 dia esmerilhador + 0,5 dia ajudante + 0,15 dia encarregado**; contém gases/insumos e registra valores conflitantes (`custo_total = R$ 2.183,69` vs anotação `R$ 947,49` e referência unitária R$ 71,03/m²). Não lançá-lo sobre dois vãos nem duplicar a equipe `I03-R01..R04`. `EXC-006` (reforço de vãos em metalon) tem 24 m em memória **de outro caso**, sem preço cadastral e sem aplicação aqui. `EXC-035` (grade de janela 1,20×1,40) serve **apenas para localizar materiais** de solda/corte/estrutura, não para copiar seus quantitativos ou dias. `EXC-036` perfil R$ 29,11/m serve a **vãos forrados** somente. `EXC-040` pintura de contêiner: R$ 7,99/m² de referência histórica, inclui MO e requer reexecutar memória para a área de trabalho; não copiar R$ 469,82 de base 58,80 m². `EXC-034` é pintura da estrutura **modular**, não sistema automaticamente válido para Dry.

**Materiais complementares pesquisados e registrados:** `I03-M04..M18`: `ABR006` eletrodo R$ 38,70/kg, `ABR008` disco corte R$ 1,90/pç, `ABR009` desbaste R$ 5,00/pç, `ABR010` flap R$ 4,58/pç, `ABR002` antirrespingo R$ 18,00/pç, `EST039` metalon 30×20 R$ 41,33/barra 6 m, `EST042` metalon 50×30 R$ 14,35/m **alternativa** (não somar), `EST004` chapa aço 3 mm R$ 5,40/kg, `VED017` PU40 cinza R$ 32,00/pç, `PIN023` primer R$ 150,05/un, `PIN050` tinta PU R$ 178,36/la, `FIX033` parafuso R$ 0,08/pç, `PEND-ACAB-VAO-001` perfil apenas se forrado R$ 29,11/m, oxigênio e GLP **somente referenciais históricos EXC-016 sem `cod_item` e sem preço aplicado**. **Todos 15 candidatos** foram persistidos com `quantidade = NULL, valor_unitario = NULL, status = EM_ANALISE`; os preços da Lista-Mãe permanecem na fonte e podem ser exibidos como referência, não contabilizados. No sistema elétrico as quantidades propostas 80% permanecem inalteradas.

**Mão de obra interna — apenas simulação com 1 colaborador/função:** `I03-R01` maçaricista 0,7 dia × R$ 275,82 = R$ 193,07; `I03-R02` soldador 1,5 × R$ 275,82 = R$ 413,73; `I03-R03` eletricista 0,5 × R$ 275,82 = R$ 137,91; `I03-R04` ajudante 3 × R$ 235,92 = R$ 707,76. **R$ 1.452,47 de referência**, com equiparação das profissões ao cargo genérico RH `Profissional` ainda pendente de validação. Serviços externos `I03-X01..X02` (engenharia/ensaios) **somente condicionais**, não contratados nem precificados. Não somar MO dentro de EXC ou kit elétrico M01 de novo.

**Controle financeiro fail-closed:** materiais com quantidade e preço de consulta (2 janelas `ESQ006` + 7 componentes elétricos com quantidade) resultam em **R$ 824,49** por soma de produtos com precisão integral e arredondamento final; combinados com a MO simulada seriam **R$ 2.276,96**, **parcial de referência não aplicado e não homologado**, já que inclui cabos/quadro condicionais e discrepâncias de preço/especificação. Não há preço do Dry-base, consumos de solda e corte, reforços, vedação, acabamento, serviços externos ou aprovação da engenharia. Não aplicar BDI/administração sobre subtotal incompleto e não fechar orçamento.

**Estado técnico e rastreio:** 42 linhas `I03-*` no Supabase: 9 serviços, 27 materiais (inclui kit completo `I03-M02 = NAO_APLICAVEL`), 4 MO interna e 2 externas condicionais; **0 linhas `APLICADO`**, zero valores unitários lançados. Estado `elo_orcamentos.contexto.analise_item_03_deposito_4m.composicoes_complementares` preserva evidência, bloqueios, referências e subtotal apenas de análise. Engenharia ainda precisa resolver pé-direito requerido 2.890 mm versus base interna 2.380 mm. `CAD-05=EM_ANALISE`, `CAD-06=BLOQUEADA`, `CAD-10/11` seguem sem fechamento. Exibir todas as seções na tela. **Não criar Excel sem solicitação explícita.**


### Revisão supervisionada SO 233.26 item 03 — EXC abertura, metalon, esmalte e anticorrosivo

**Fonte e prioridade:** correção explícita do Analista em 12/11/2026 sobre a composição do depósito de 4 m com Dry-base MLT.C06. Esta revisão **substitui** as indicações anteriores de `EST039` (30×20) e `PIN050` (tinta PU WEG) como materiais de aplicação; não reinterpreta o catálogo nem generaliza a decisão para outro modelo/caso. A fonte operacional real permanece `public.elo_orcamento_composicao_itens` com histórico de revisão em `public.elo_orcamentos.contexto.analise_item_03_deposito_4m.revisao_correcoes_excedentes_e_pintura`.

**Serviços EXC agora vinculados explicitamente no banco:**
- `I03-S03 — EXC-016`: abertura de **2 vãos para esquadrias 600×600 mm**. Composição EXC histórica para **5 painéis**, inclui maçaricista/esmerilhador/ajudante/encarregado, oxigênio/GLP e apresenta conflito `custo_total R$ 2.183,69` versus observação `R$ 947,49` e consulta `R$ 71,03/m²`. Código vinculado **para rastreio e adaptação**, sem importar preço/MO. Duas aberturas 0,6×0,6 m dão **0,72 m² de área geométrica**; diferença de escopo e equipe `I03-R01..R04` impedem aplicar EXC-016 integralmente.
- `I03-S06 — EXC-006`: **reforço de vão com metalon 50×30 mm ou seção superior**. `EST042` 50×30×1,20 mm `R$ 14,35/m` é perfil-base candidato; `EST040` 60×60×1,50 mm `R$ 8,50/kg` é alternativa de seção maior, **sem somar os dois automaticamente**. O `EST039` 30×20 foi marcado `NAO_APLICAVEL` para esse reforço. EXC-006 tem memória histórica de 24 m em outra obra, não transferir. Perímetro geométrico das duas janelas 4,8 m é somente dimensão inicial, **não** metragem validada para compra.
- `I03-S07 — EXC-040`: pintar superfície afetada usando **esmalte/sintético por m²**, conforme pintura externa de contêiner marítimo; referência histórica `R$ 7,99/m²` **já inclui MO** e insumos. Memória histórica EXC-040 apresenta primer `R$ 3,58/m²` de superfície imprimada (20% da área-base), esmalte `R$ 4,50/m²` de superfície pintada (100%), além de solvente e MO de pintura/lixador. Medir área real e reexecutar memória antes de aplicar. Não lançar de novo MO contida no EXC-040.

**Materiais atualizados:**
- `I03-M14 PIN050`: tinta PU WEG 2,7 L **NÃO SERVE**, exclusão do Analista; `status=NAO_APLICAVEL`. Não reaproveitar preço R$ 178,36 como esmalte.
- `I03-M19`: **tinta/tratamento anticorrosivo R$ 260,00**, preço expressamente **informado pelo Analista** e lançado como referência numérica `valor_unitario=260,00` com `quantidade=NULL`, unidade/código produto **a confirmar**, status `EM_ANALISE`, `valor_parcial=NULL`. Busca na Lista-Mãe não identificou por descrição uma tinta equivalente com esse preço; não inventar SKU/embalagem nem somar ao subtotal. Verificar se o tratamento é complementar ou já incluso em primer/esmalte `EXC-040`.
- `I03-M12 VED017`: **selante PU40 cinza R$ 32,00/pç** da Lista-Mãe, consumo a medir; vedação das janelas e juntas, evitar duplicação com outro selante e serviço de vedação.
- `I03-M13 PIN023`: **primer WEG 3,6 L R$ 150,05/un** da Lista-Mãe fica somente **condicional**, pois o EXC-040 já contempla primer e a compatibilidade com o anticorrosivo informado não está confirmada. Não excluir PIN023 por inferência: o Analista excluiu explicitamente **PIN050**.
- `I03-M10 EST042` é referência-base metalon 50×30 e `I03-M20 EST040` referência de perfil maior; ambos `quantidade=NULL`, sem total, sujeitos ao cálculo de engenharia.

**Gates e testes:** (a) conferência de EXC-016, EXC-006 e EXC-040 preenchidos em `codigo_excedente`; (b) EST039/PIN050 `NAO_APLICAVEL`; (c) preço informado R$ 260 preservado sem unidade/quantidade e sem `valor_parcial`; (d) preços EXC históricos não são lançados junto com RH e nem duplicados com primer/anticorrosivo; (e) CAD-05 continua `EM_ANALISE`, CAD-06 `BLOQUEADA`, item 03 ainda **sem preço final** e SO em **0/5 produtos fechados**. Apresentar composição em tela; **não gerar Excel** sem pedido expresso. Este registro é evidência contextual no procedimento canônico, não nova norma do ELO Core.


### RNF de correção — preencher valor unitário da Lista-Mãe com quantidade ainda pendente (12/11/2026)

**Falha diagnosticada pelo Analista:** na composição `SO 233.26`, depósito 4 m (item 03, base `MLT.C06`), os materiais cadastrados com códigos válidos na Lista-Mãe tinham `valor_unitario=NULL` apesar de preço ativo e unidade compatível. **Correção executada no Supabase:** 20 materiais `EM_ANALISE` receberam preços de `public.lista_mae`, sem alterar quantidades, status, exclusões, fonte de preços ou custo final. Foram mantidos `EST039`, `PIN050` e kit M01 integral como `NAO_APLICAVEL`. Tratamento anticorrosivo de R$260 informado pelo Analista continua sem código/quantidade, identificado como preço informado, não preço Lista-Mãe.

**Regra operacional (detalhada em `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`, §20):** buscar preço unitário sempre que houver código exato ativo, ocorrência única, preço `>0` e unidade compatível; apresentar a linha em tela com `CÓDIGO | DESCRIÇÃO | QTD | UN. | VALOR UNI | VALOR TOTAL | ESTADO`, **mesmo sem quantidade**. Com quantidade vazia, `valor_total = PENDENTE`; com quantidade existente, o PostgreSQL gera automaticamente `valor_parcial=round(quantidade*valor_unitario,2)`, ainda **referencial** enquanto `status=EM_ANALISE`. Não incluir no fechamento os parciais não aprovados; controlar `APLICADO` exclusivamente após CAD-06/10. Não atribuir um preço de outro item com embalagem/unidade divergente.

**Reconciliação de arredondamento observada:** os 8 materiais com quantidade e preço de referência apresentam **R$824,48 pela soma dos parciais gerados por linha** (valor a exibir como subtotal referencial da própria composição), enquanto `round(sum(qtd * preco),2)` resulta em **R$824,49**. Memória persistida em `elo_orcamentos.contexto.analise_item_03_deposito_4m.composicoes_complementares.parciais_referencia`, incluindo simulação RH R$1.452,47 e parcial conjunto R$2.276,95. A diferença de R$0,01 não autoriza alterar preços nem criar arredondamento fictício. A regra evita reincidência nas próximas SOs sem mudar o Core ou a estrutura do banco. **Não gerar Excel** sem pedido explícito.


### Correção supervisionada SO 233.26 item 03 — reforços medidos, fundo reaproveitado, luminárias M01 e disjuntores

**Decisão expressa do Analista 12/11/2026 para o depósito 4m adaptado do Dry MLT.C06.** Esta memória corrige somente o caso e prevalece sobre as decisões **anteriores do item 03**, sem atualizar especificações gerais de outros modelos, sem promoção ao ELO Core, sem alterar schema nem tabela canônica de preços. Identidade de produtos permanece 03/05, nenhuma venda fechada.

**1. Reforço para esquadrias com `EST042` — 50×30×1,20 mm.** Duas esquadrias nominais 600×600 mm → perímetro total geométrico `2×(2×0,60+2×0,60)=4,80m`, sem folgas/perdas. Linha `I03-M10` no Supabase atualizada para `quantidade=4,80`, `unidade=M`, `valor_unitario=R$14,35` da Lista-Mãe, `valor_parcial=R$68,88` gerado pelo banco com `status=EM_ANALISE`. Linha `I03-S06` EXC-006 tem também 4,80m **somente como serviço de referência**, sem valor de material duplicado. A metragem para compra precisa de folgas, cortes e decisão de engenharia.

**2. Reforço para abertura estrutural com `EST040` — 60×60×1,5 mm.** Analista especificou duas alturas e uma travessa superior/teto do **vão aberto no contêiner Dry de 20 pés**, distinto dos reforços 50×30 das janelas. A base `elo_produtos_conhecimento` registra altura externa **2.590 mm** e largura externa **2.440 mm**; se a abertura for **transversal** (HIPÓTESE EXPRESSA A VALIDAR), a geometria `2×2,590 + 2,440 = 7,620 m` foi registrada em `I03-S10` como medição `m` **não precificada**. Verificar desenho/orientação real do vão antes de consolidar. `EST040` tem **unidade KG e preço R$8,50/kg** na Lista-Mãe; sem fonte de massa por metro válida, manter `I03-M20.quantidade=NULL`, mas unitário visível, **não inventar total em reais**. Não substituir por EST042: são aplicações estruturais distintas; não são alternativas no novo escopo.

**3. Reutilizar fundo original:** serviço `I03-S02` passou a `reinstalação e soldagem do fundo original do Dry`; material adicional `EST004` chapa aço 3mm na `I03-M11` foi marcado `NAO_APLICAVEL`, sem custo. Permanecem necessários verificação estrutural, cortes, selagem e vedação.

**4. Iluminação `ELE098` padrão M01:** por decisão do Especialista, **2 luminárias** de LED 36W bivolt 1000×74 mm, não a única luminária quadrada 300×300 anteriormente proposta. `I03-E02` = código ELE098, 2 PÇ × Lista-Mãe R$19,73 = **R$39,46 referencial**. **GAP de conformidade**: 1000×74 NÃO equivale ao requisitado 300×300 mm. Não registrar aceite do cliente inexistente; necessidade de autorização técnica/documentada.

**5. Disjuntores propostos e preços Lista-Mãe:**
- `I03-E10` PEND-M01-008 = disjuntor **geral bipolar 2P 25A**, 1 un × R$23,68 = R$23,68. Não usar `ELE078` com preço zero no cadastro como se precificado.
- `I03-E11` ELE170 = disjuntor **10A para iluminação**, candidato **1P**, 1 PÇ × R$13,80 = R$13,80; alternativa **2P 10A ELE141**, preço de referência R$13,80, se topologia 220 V entre duas fases exigir proteção seccionando ambos os polos.
- `I03-E12` PEND-M01-009 = disjuntor **16A para tomadas**, candidato **1P**, 1 un × R$8,44 = R$8,44; alternativa 2P16A PEND-M01-007 a R$34,52, se requerida. Kit M01 descreve ELE085 como 1P16 R$8,44 mas Lista-Mãe ELE085 descreve 3P16 sem preço; **não usar código ambíguo**.
- `I03-E09` proteção genérica ficou `NAO_APLICAVEL` para não duplicar as três linhas acima. O cliente/especialista definiu correntes **25A, 10A, 16A**, mas **não** os polos dos derivados. Exigir projeto/diagrama de alimentação 220 V (fase-neutro vs fase-fase), proteção adequada, capacidade de interrupção, dimensionamento e conformidade antes de aplicar/instalar.

**6. Conciliação e estágio:** itens originais 80% do M01 permanecem nas demais linhas. Excluir indicação histórica `ELE098_LUMINARIA_LINEAR_1000X74` do campo `kit_eletrico.nao_aplicar` do contexto **só para esta SO**; componente atualizado para 2 unidades e registrado com GAP de conformidade. Preços de catálogo são consultivos. Com `EST042` R$68,88, `ELE098` R$39,46 e três disjuntores R$45,92 acrescidos às referências anteriores, materiais **R$978,74** por soma dos parciais gerados (arredondar agregados produziria R$978,75), simulação RH **R$1.452,47** e **parcial conjunto não fechado R$2.431,21**. O 60×60 sem kg e outros custos não compõem esse parcial. `CAD-05=EM_ANALISE`, `CAD-06=BLOQUEADA`; nunca promover itens `EM_ANALISE` a `APLICADO` sem engenharia, quantidades e aceite. Preço do Dry e pé-direito de 2.890 mm vs altura interna de 2.380 mm permanecem GAP. Não gerar Excel sem pedido explícito.


### Layout BASE MESTRE canônico ratificado pelo Analista — 12/11/2026

O Analista forneceu como **layout canônico** a planilha `PLANILHA DE ORÇAMENTO — BASE MESTRE | MLT.M05` em Markdown e solicitou atualizar o Excel SO 233.26. O contrato de apresentação operacional está em `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`, §21: grade **A:H**, seções `0 Controle`, `1.0 Comercial`, `2.0 Composição` (`2.1 Serviços`, `2.2 Materiais`, `2.3 M.O. interna`, `2.4 M.O. externa`), `3.0 Fechamento`, `4.0 Observações`; não usar o painel antigo de onze colunas como estrutura principal. Controles de modelos, RNF, cadência, fontes e GAPs são abas auxiliares. O estado e os insumos continuam no Supabase.

**Regressão do M05 conforme a fonte do Analista:** 2 ESQ006 a R$227,09/un **na revisão M05**, materiais R$1.111,72, M.O. interna R$418,65, subtotal R$1.530,37; administração 10% e BDI venda 96% ambos sobre subtotal, total **somente preliminar** R$3.152,56. Não confundir o preço histórico de ESQ006 com R$162,50/un da Lista-Mãe usada no depósito item03. Conflito Mossoró/RN no Markdown versus MOSSORÓ/RS no RNF continua GAP. A ausência de preço do M05-base impede aprovação.

**Regressão do item03:** 48 linhas preservadas na grade canônica, 10 serviços, 32 materiais, 4 M.O. interna, 2 potenciais externos; preços unitários disponíveis permanecem visíveis mesmo sem quantidade. Referências do Supabase: materiais R$978,74, RH R$1.452,47, parcial R$2.431,21, 0 custos APLICADO. Preço do Dry-base, kg/m de EST040, projeto/altura, luminárias e EXC com M.O. em disputa bloqueiam CAD-05/06/10/11. Fórmulas de fechamento ilustrativas não homologam venda.

**Arquivo produzido nesta conversa:** `ELO_ORCAR_SO23326_PADRAO_CANONICO_ATUALIZADO_20261112.xlsx` contendo M05 Base Mestre, I03 Depósito 4m, Controle Modelos, Cadência ELO, RNF 14 Campos, Fontes e GAPs. Revisão da planilha é exportação pontual, não altera automaticamente o banco nem substitui as instruções no GitHub. Conservar as fontes, não criar autoridade paralela, não promover caso ao Core sem Evolution Gate.


### SO 233.26 — M05 padrão aceito e abertura de orçamento M02 (12/11/2026)

**Decisão do Analista:** após ratificar o layout de planilha Base Mestre A:H, estabeleceu que o **primeiro modelo trabalhado (MLT.M05 Sanitário Coletivo) será a configuração padrão e pode ser considerado OK nessa dimensão**, e solicitou seguir ao **MLT.M02 escritório com banheiro**. Este aceite é **exclusivamente de configuração padrão**, não constitui aceitação comercial do demonstrativo M05, não comprova itens físicos na ficha e não fecha valor final. Preservar valor demonstrativo M05 R$3.152,56 com GAP de base, divergência ESQ006 e PTS Pós. Não remover o Dry C06 padrão da ordem 01 nem o depósito Dry adaptado da ordem 03. O usuário continua na sequência do lote: 01 C06 Dry 6m, 02 M05 padrão funcionalmente aceito, 03 Dry depósito 4m em análise, 04 M02 escritório suíte agora ativo, 05 M01 habitável pendente. Progresso financeiro **0/5**.

**Evidências GitHub e Supabase verificadas antes da composição:**
- `public.modelos`: código `MLT.M02`, nome `Escritório Suíte`, família `Módulo`, descrição `Escritório + banheiro`, versão 1.0, ativo, **`valor_total=NULL`**.
- `public.dimensoes`: referência 20 pés, **6000×2440×3010 mm** (altura externa, **não** pé-direito livre de 2890 mm).
- `public.kits`: `KIT-M02-HIDROSANITARIO` ativo e nominalmente originário de SO 157.26; `public.kit_itens` apresenta **zero linhas vinculadas**. Não inventar louças/itens/composição nem custo adicional.
- `public.excedentes`: `EXC-011` adição de tomada 10A em circuito existente, **R$95,65/un**, contém mão de obra. A hipótese anterior de até **três tomadas extras** pressupõe três tomadas no padrão e requisito total de seis; enquanto composição elétrica-base não for comprovada, `quantidade=NULL` e `valor_parcial=NULL`, mantendo apenas memória **3×95,65=R$286,95 hipotéticos**. Não lançar `ELE131` e M.O. elétrica como custos adicionais sobre EXC-011.
- `public.lista_mae`: `ESQ006` basculante 600×600 por R$162,50/pç é **referência apenas condicional**. Precedente funcional relata duas janelas e basculante no padrão M02, sem provar a lista de produção desta SO. Não usar como excedente automático.
- Exigir conferência de banheiro, esquadrias/porta, isolamento termoacústico já incluído no produto-base se comprovado, infraestrutura elétrica/abertura para ar-condicionado **sem adicionar aparelho não solicitado**.

**Persistência executada:** a SO `SO 233.26` foi atualizada em `public.elo_orcamentos.contexto.sequencia_modelos_orcamento` com `indice_atual=4`, `modelo_atual=MLT.M02_ESCRITORIO_SUITE_COM_BANHEIRO`; item 02 recebeu `configuracao_padrao_aceita=true` mas preservou `status_orcamento=COMPOSICAO_PRELIMINAR` e `valor_final_fechado=NULL`. Item 04 passou a `EM_ANALISE_TECNICA`, sem preço final. `contexto.analise_item_04_m02` guarda origem, hipóteses, preços consultivos, catálogo e GAPs.

**Composição canônica M02 em tela:** `1.0 Comercial` registrado em **contexto** como um M02 padrão, pois o check constraint da tabela SQL permite apenas `secao='2.1'|'2.2'|'2.3'|'2.4'`; não alterar o esquema para forçar 1.0. As **12 linhas `I04-*`** em `public.elo_orcamento_composicao_itens` são 5 serviços de inspeção de excedentes/composição, 5 candidatos de materiais incluindo EXC-011/ESQ006, 1 linha de eventual M.O. interna, 1 de serviços externos, todas `EM_ANALISE`, com **quantidades não confirmadas e `valor_parcial=NULL`**. Manter a grade de planilha Base Mestre A:H (0,1,2.1–2.4,3,4) em apresentação, com `1.0` via contexto. Não emitir Excel sem novo pedido explícito.

**Gates:** `CAD-04=EM_ANALISE`, `CAD-05=EM_ANALISE`, `CAD-06=BLOQUEADA`, `CAD-07=EXECUTADA_COM_PENDENCIAS`; `CAD-10/11` impedem fechamento. A estrutura aceita pelo usuário não é evidência de preço nem composição homologada. O GitHub é autoridade operacional da planilha, o Supabase dos estados e itens. Evento é caso supervisionado para a SO, não regra do Core/Evolution Gate.


### Correção supervisionada — SO 233.26 item 04 M02: três tomadas extras e basculante padrão (12/11/2026)

**Decisão expressa do Analista:** a configuração **MLT.M02 Escritório Suíte com banheiro** contém **3 tomadas 10A no padrão**, e **mais 3 tomadas 10A** já haviam sido definidas inicialmente para atingir **6 tomadas**. O basculante existente no sanitário está **incluído no M02 padrão**. É indevida a tentativa de orçamento de basculante adicional na linha 2.2.2 (`ESQ006`).

**Composição corrigida e gravada no Supabase:** no orçamento `SO 233.26`, modelo `MLT.M02` (item físico 04), `I04-M01 / 2.2.1` corresponde a **3 unidades do `EXC-011`**, R$95,65 por unidade, custo de referência **R$286,95** gerado automaticamente por `valor_parcial`. O EXC-011 ativo na fonte `public.excedentes` é *adição de tomada simples 10 A em circuito existente* e **inclui mão de obra**. Permanecem `status=EM_ANALISE` e fechamento bloqueado; esse é somente **subtotal parcial conhecido**, não preço de venda final. **Não** cobrar material de tomada `ELE131`, serviço separado ou diária elétrica novamente para o mesmo escopo. A linha `I04-S02` ficou `NAO_APLICAVEL` como instalação em separado. `I04-R01` fica para outros trabalhos eventuais, sem preço.

Na linha `I04-M02 / 2.2.2`, o basculante `ESQ006` foi marcado `NAO_APLICAVEL` como excedente, `quantidade=NULL` e `valor_unitario=NULL`, preservando código, histórico e decisão. **O componente padrão continua existindo no M02**; não removê-lo da solução física, não cobrar outro basculante e não inventar preço-base em função dessa correção. `I04-S04` segue como conferência das **demais** portas/janelas do padrão, sem reabrir o basculante já confirmado.

**Governança/estado:** `contexto.analise_item_04_m02.tomadas` indica 3 padrão + 3 adicionais = 6, com origem da confirmação do Analista, e `contexto.analise_item_04_m02.esquadrias` marca `basculante_sanitario_incluso_no_padrao=true`. `contexto.sequencia_modelos_orcamento.itens` mantém cinco equipamentos, M05 padrão aceito **configuracionalmente** sem preço homologado e M02 ativo em `EM_ANALISE_TECNICA`. `CAD-05=EM_ANALISE` e `CAD-06=BLOQUEADA`. Persistem GAP de custo-base M02 nulo, kit hidrossanitário nominal sem `kit_itens`, pé-direito interno, demais esquadrias, circuitos e projeto. Não gerar novo Excel por esta correção isolada; preservar Planilha BASE MESTRE A:H na apresentação. Esta é evidência contextual, não mudança no Core ou aprovação da venda.


### SO 233.26 item 05 — M01: uma janela substituída por basculante e três tomadas adicionais (13/11/2026)

**Decisão expressa do Analista (13/11/2026) e escopo:** último modelo físico da SO, `05 — MLT.M01 Habitável`, terá **1 basculante**. O M01 padrão possui **2 janelas**, das quais uma permanece e a outra é **substituída pelo basculante**, abatendo o custo da janela original; também terá **+3 tomadas 10A**, além das três no padrão, para totalizar seis. Não converter a substituição em terceira esquadria nem somar ambas as janelas originais com uma basculante.

**Fontes reais consultadas:**
- `public.vw_kit_montagem_m01_completo`: 2 × `PEND-M01-019` *JANELA SALOMÃO 900×1200*; `public.lista_mae` código PEND-M01-019 ativo, descrição *PAINEL JANELA 900X1200MM*, **R$1.325,72/un**. A `PEND-M01-020` *janela ar-condicionado 410×690* é OUTRA linha do kit, não foi confundida com as duas janelas objeto da troca.
- `public.lista_mae`: `ESQ006` janela basculante alumínio **600×600 mm**, **R$162,50/pç**, **candidata à basculante especificada**, ainda sujeita à conferência de vidro/dimensões/encaixe. Uma peça.
- `public.excedentes`: `EXC-011` adição de tomada simples 10 A em circuito existente **R$95,65/un**, `inclui_mao_obra=true`. Três unidades = R$286,95, **sem mão de obra elétrica duplicada**.
- `public.modelos` contém código `M01`, Habitacional Amplo 20 pés, `valor_total=R$28.500`, mas não se comprovou a natureza custo/preço de venda nem a correspondência direta ao registro `MLT.M01` da sequência; **não aplicar esse valor como custo-base ou como venda homologada** sem conciliar cadastro e escopo.

**Memória de substituição, só referencial:**
```text
Crédito da 1 janela original PEND-M01-019:   -R$ 1.325,72
1 basculante ESQ006:                          +R$   162,50
3 tomadas adicionais EXC-011:                 +R$   286,95
Δ referencial sobre M01 padrão:               -R$   876,27
```
É **ajuste incremental**, não custo total nem preço de venda. O preço do PEND-M01-019 se refere a um **painel janela completo**, e o do ESQ006 a **peça basculante avulsa**; a diferença só é financeiramente aplicável após validar se o painel original está no preço-base e se a troca exige obra, vedação, estrutura/instalação. Não fabricar homologação ou tratar equivalência como comprovada.

**Persistência e restrições do Supabase:** `public.elo_orcamento_composicao_itens` aceita quantidades e unitários **não negativos**, e `valor_parcial` é calculado. Para não registrar crédito como compra positiva nem inventar valor negativo na coluna gerada, linha `I05-M01` mantém **PEND-M01-019**, unitário R$1.325,72 **visível**, status `NAO_APLICAVEL` e quantidade/parcial nulos; o **crédito −R$1.325,72** com quantidade 1 está em `public.elo_orcamentos.contexto.analise_item_05_m01.delta_credito_janela`. Linha `I05-M02` registra 1 ESQ006 R$162,50, e `I05-M03` 3 EXC-011 R$95,65 cada, gerando R$286,95. `I05-S01` documenta serviço de troca estrutural sem preço e `I05-S02` está `NAO_APLICAVEL` como instalação separada já incluída no EXC. Soma dos parciais positivos gerados = R$449,45, **não confundir** com o ajuste líquido −R$876,27 do contexto. Nenhuma linha `APLICADO`.

**Fluxo:** `sequencia_modelos_orcamento.indice_atual=5` e item físico M01 agora `EM_ANALISE_TECNICA`; M05 permanece padrão aceito somente quanto à configuração, M02 contém 3 tomadas adicionais e basculante sanitário incluso, depósito Dry segue distinto do Dry de 6m. `CAD-05 EM_ANALISE`, `CAD-06 BLOQUEADA` e `CAD-10/11` não liberam preço final. Exigir validação de demais portas, luminárias, ar-condicionado, altura interna e preço-base, sem promover experiência ao Core. Preservar planilha canônica BASE MESTRE A:H, **não gerar Excel sem solicitação explícita**.


### Revisão prevalecente do M01 — crédito ESQ004 R$891,80 em vez de painel PEND-M01-019 (13/11/2026)

**Decisão mais recente e vinculante do Analista:** corrigir a memória anterior do item 05 da SO 233.26: **não** abater o valor de R$1.325,72 do `PEND-M01-019` (painel janela original do kit M01). O abatimento unitário expressamente definido é o valor **somente da janela de alumínio**, código **`ESQ004`**, R$**891,80/PÇ** na Lista-Mãe, para **uma janela substituída**. Acrescentar **uma báscula `ESQ006` R$162,50**, mantendo uma das duas janelas do M01 original; e **três tomadas `EXC-011` R$95,65/un, total R$286,95**, já com mão de obra. A janela do ar-condicionado `PEND-M01-020` é distinta e não entra nesta substituição.

**Proveniência:** consulta `public.lista_mae` confirmou `ESQ004` *JANELA ALUMÍNIO 1200×900 MM* ativa a R$891,80/PÇ e `ESQ006` *JANELA BASCULANTE ALUMÍNIO 600×600 MM* ativa a R$162,50/PÇ. `public.vw_kit_montagem_m01_completo` continua contendo `2 × PEND-M01-019` *JANELA SALOMÃO 900×1200* R$1.325,72/un; **esse custo do painel completo não foi alterado na Lista-Mãe nem no kit**. A decisão do Analista estabelece o **critério de abatimento do orçamento da SO**, e não afirma que o preço da peça ESQ004 já era discriminado no kit. Preservar separação entre composição completa do painel e preço avulso da janela. Não aplicar outros créditos presumidos.

**Memória correta do ajuste líquido referencial em relação ao M01 padrão:**
```text
1 janela alumínio ESQ004 retirada:      - R$ 891,80
1 janela basculante ESQ006 inserida:    + R$ 162,50
Diferença da esquadria:                  - R$ 729,30
3 tomadas EXC-011 (M.O. incluída):      + R$ 286,95
DELTA LÍQUIDO M01:                      - R$ 442,35
```
**Supera e revoga expressamente a memória anterior `-R$876,27` e o crédito anterior `-R$1.325,72`** para este caso. Não reutilizar esses valores na planilha, no resumo da SO ou na próxima exportação; histórico permanece para auditoria, **não** é ativo.

**Supabase confirmado:** `public.elo_orcamento_composicao_itens` na SO 233.26, MLT.M01: `I05-M01` agora tem `cod_item=ESQ004`, `valor_unitario=891.80`, `unidade=PÇ`, `status=NAO_APLICAVEL` e `quantidade/valor_parcial=NULL` porque crédito negativo é armazenado em `elo_orcamentos.contexto.analise_item_05_m01.delta_credito_janela` com `valor_credito_sinalizado=-891.80`; preservar `PEND-M01-019` como `codigo_kit_original` e não reescrever seu cadastro. `I05-M02=ESQ006` 1 × R$162,50 e `I05-M03=EXC-011` 3 × R$95,65 (=R$286,95) continuam `EM_ANALISE`, subtotais positivos gerados = R$449,45. `contexto.analise_item_05_m01.ajuste_liquido.total_delta_referencia=-442.35`; o item da sequência física 05 foi atualizado e `CAD-05` segue `EM_ANALISE`, `CAD-06` `BLOQUEADA`. No layout canônico BASE MESTRE A:H, exibir o **crédito negativo** como linha de ajuste e não apenas a soma positiva dos materiais, sem falsear o valor gerado no banco.

**Bloqueios:** delta não é preço final ou custo-base do M01. Ainda faltam validações de montagem/vedação no vão substituído, preço-base, exigências técnicas e conciliação. Não marcar nada `APLICADO` ou `FECHADO` pela decisão de valor; não alterar Core nem emitir Excel sem novo pedido explícito.


### SO 233.26 item 03 — EXC-016 para dois vãos de esquadrias no depósito Dry de 4 m (13/11/2026)

**Orientação mais recente do Analista:** no depósito de 4 m fabricado de Dry 20 pés (`MLT.C06`, item físico 03), utilizar a **referência de EXC de abertura de vão**, considerando os **dois vãos de abertura de esquadrias** deste modelo. Há **duas janelas basculantes de 600×600 mm**: não tratar a abertura delas como apenas a seção transversal do contêiner. A abertura dessas esquadrias já estava vinculada à linha `I03-S03 — EXC-016`, portanto **atualizar esta linha existente, sem criar EXC ou serviço redundante**.

**Geometria e escopos diferentes no canônico BASE MESTRE A:H:**
1. `I03-S03` (`2.1 Serviços`) → `EXC-016` *abertura de 2 vãos laterais de janelas 600×600 mm*: **2 unidades físicas × (0,60m × 0,60m) = 0,72m²**. O catálogo EXC está em **m²**; retificar a unidade antes registrada como `vão` e a quantidade antes registrada como `2` para **quantidade=0,72, unidade=m²**; manter o número físico dois na descrição, observação e JSONB da SO.
2. `I03-S04` instalação das **2 basculantes** ESQ006 em unidade de peça; material `I03-M01` contém **2 × ESQ006**, sem duplicidade.
3. `I03-S06` (`EXC-006`) = **4,80m lineares de reforço perimetral dos dois vãos** `2×2×(0,60+0,60)=4,80m`. O material correspondente `I03-M10` é `EST042` 50×30×1,20, **4,80m × R$14,35/m = R$68,88** referencial. Não misturar metragem linear de reforço com área de abertura nem duplicar o material em EXC-006.
4. `I03-S01` = **corte estrutural separado** do Dry de 20 pés para obter o depósito de 4m. Abertura lateral de esquadrias `EXC-016` em 0,72m² **não representa** esse corte transversal nem sua recomposição. `I03-S02` mantém reaproveitamento do fundo original. Reforço EST040 60×60 da seção aberta segue distinto com geometria provisória 7,62m e preço unitário em KG, sem conversão assumida.

**Fonte EXC e motivo do bloqueio de preço:** `public.excedentes` `EXC-016` é **histórico da SO 169.26 para 5 painéis laterais** em aço de contêiner, unidade m², descrição com referência **R$71,03/m²**, custo_total cadastrado **R$2.183,69**, nota adicional **R$947,49**: números inconciliados. `inclui_mao_obra=true`, com maçaricista, esmerilhador, ajudante, encarregado, oxigênio, GLP, contingência/insumos e movimentação. `public.excedente_itens` registra material e MO; `public.excedente_mao_obra` detalha a mesma MO histórica. Não importar as linhas históricas na íntegra para duas aberturas 600×600. A taxa histórica geraria **0,72m²×R$71,03/m² ≈ R$51,14**, **somente simulação isolada, NÃO lançada como preço**. Não somar EXC à equipe do depósito `I03-R01` maçaricista ou `I03-R04` ajudante nem duplicar gases, corte, esmerilhamento já cobertos por diárias/insumos; antes de preço final, reexecutar memória técnica e deduplicar.

**Persistência e validações:** em `public.elo_orcamento_composicao_itens` a linha **I03-S03** foi atualizada `codigo_excedente=EXC-016, quantidade=0,7200, unidade=m², valor_unitario=NULL, valor_parcial=NULL, status=EM_ANALISE`. Linhas `S01,S04,S06` tiveram descrição/observação precisadas, sem nova linha. Em `public.elo_orcamentos.contexto.analise_item_03_deposito_4m` foram consolidados o número de aberturas, as duas medidas, a referência do EXC e os escopos distintos. `CAD-05=EM_ANALISE`, `CAD-06=BLOQUEADA`, nenhum custo `APLICADO`; materiais R$978,74 e RH simulado R$1.452,47 permanecem **parciais** e não homologados. A exportação `ELO_ORCAR_SO23326_05_MODELOS_BASE_MESTRE_CANONICA_20261113.xlsx` é fotografia anterior ao ajuste e está marcada para nova revisão em `ultima_exportacao_excel`; não gerar automaticamente outro Excel sem solicitação específica.

**Governança:** correção contextual da SO 233.26 na Forge/Especialista ORÇAR, não muda Core, schema nem cadastra novo EXC. Preservar a rastreabilidade da fonte e precedentes. Não homologar custo ou sinalizar entrega/merge antes dos testes.


### SO 233.26 item 03 — Metalon EST040 60×60×1,5 por metro, geometria interna 7,23m (13/11/2026)

**Decisão expressa posterior do Analista — PREVALECE sobre os 7,62m anteriores.** Na abertura estrutural do **depósito Dry cortado de 4m**, usar `EST040` aço carbono quadrado **60×60×1,5mm** com dois montantes de **altura INTERNA 2,45m cada** e uma travessa superior de **comprimento interno 2,33m**. **Comprimento líquido = 2×2,45 + 2,33 = 7,23m.** Substituir a geometria PROVISÓRIA de dimensões externas `2×2,590+2,440=7,62m` do registro anterior, preservando-a apenas no histórico com indicação `revogada`. Não associar o EST040 aos dois perímetros de esquadrias 600×600: `EST042` 50×30×1,20mm permanece separado com 4,80m no `I03-M10` e EXC-006 `I03-S06`.

**Conversão da unidade comercial sem alterar a Lista-Mãe:** `public.lista_mae.EST040` permanece `KG`, **R$8,50/KG**, item *TUBO DE AÇO CARBONO QUADRADO (METALON) 60 X 60 X 1,5MM X 6000MM - PESO APROX.*. Para precificar **por metro somente nesta composição da SO**, foi consultada tabela técnica Tubonasa `https://www.tubonasa.com.br/tubos-quadrados`: **60×60, espessura 1,50mm, peso linear de referência 2,765KG/M (barra de 6m =16,59KG)**. Preço de equivalência `8,50×2,765=R$23,5025/M`, arredondado a **R$23,50/M** para lançamento; subtotal por fórmula por linha `ARRED(7,23×23,50;2)=R$169,91`. Massa líquida aproximada `7,23×2,765=19,99095KG`; esta aproximação não é medição do lote. Se as peças forem obtidas de barras comerciais inteiras de 6m sem reaproveitamento de estoque, são necessárias pelo menos duas barras, mas a quantidade bruta comprada, aparas, plano de corte e eventual saldo reutilizável NÃO foram orçados.

**Implementação persistida:** `public.elo_orcamento_composicao_itens`, `SO 233.26` / `MLT.C06` / `I03-M20` `(secao=2.2)` agora: `cod_item=EST040`, `quantidade=7.2300`, `unidade=M`, `valor_unitario=23.50`, `valor_parcial=169.91`, `status=EM_ANALISE`. `I03-S10` é **somente linha geométrica** `quantidade=7.2300 M`, `valor_unitario=NULL`, `valor_parcial=NULL` para não duplicar o custo do perfil. Os `I03-M10` e `I03-S06` de perímetros de esquadrias não foram alterados. A memória está em `elo_orcamentos.contexto.analise_item_03_deposito_4m.revisao_geometria_e_eletrica.metalon_vão_aberto` e `revisao_metalon_60_20261113` com fonte, conversão, hipótese anterior superada e GAPs.

**Totais PARCIAIS após a conversão:** materiais anteriormente R$978,74, acréscimo referencial EST040 R$169,91 => **R$1.148,65**. RH simulada **R$1.452,47** não alterada; subtotal conjunto **R$2.601,12**, exclusivamente parcial de referência, com **zero custos APLICADO**. Preço de Dry-base, corte, solda, EXC-016 e pintura, projeto/altura, perdas de materiais, transporte e outros custos seguem pendentes. `CAD-05=EM_ANALISE`, `CAD-06=BLOQUEADA`, portanto não apresentar subtotal como preço homologado.

**Próxima exportação:** a planilha consolidada `ELO_ORCAR_SO23326_05_MODELOS_BASE_MESTRE_CANONICA_20261113.xlsx` foi emitida **antes** das revisões de EXC-016 dois vãos =0,72m² e EST040 7,23m. `contexto.cadencia_orcar.ultima_exportacao_excel.sincronizacao_com_estado_atual` marca exportação defasada; **não** gerar novo XLSX sem pedido. Na revisão explícita, garantir layout Base Mestre A:H, atualizando `I03-S03` e `I03-M20/S10` na aba depósito com as memórias, mantendo as outras quatro abas modelo e os estados de fechamento.


### SO 233.26 item 03 — substituir caixa PVC DUTOPOP por caixa 4×2 do sistema condulete (13/11/2026)

**Decisão expressa do Analista:** no depósito feito de Dry cortado de 4m, **substituir** a caixa PVC DUTOPOP 105×60×40mm por uma **caixa 4×2 do sistema condulete** para as instalações. A linha que já continha 12 peças ×R$7,87 =R$94,44 era `I03-E06 / ELE002` (`2.2 Materiais`). Não transferir o preço da caixa DUTOPOP para outro sistema.

**Pesquisa canônica executada antes da correção:** `public.lista_mae` contém `ELE002` *CAIXA EM PVC PARA DUTOPOP 105×60×40MM CREME* R$7,87/PÇ (a excluir no orçamento), `ELE150` *CAIXA CONDULETE C 3/4* R$30,00/PÇ, `ELE151` *CAIXA CONDULETE E 3/4* R$0,00/PÇ, `ELE152` LB, `ELE153` LL, `ELE154` X com unitários R$0,00, e `PEND-DRY-005` *CAIXA DRYWALL 4X2* R$6,02/PÇ. **Nenhum deles foi demonstrado como caixa 4×2 do sistema condulete com SKU e preço exatos.** O tipo C de 3/4 ou a caixa drywall não devem ser impostos como equivalentes. Não criar linha na Lista-Mãe com SKU ou preço inventados, nem tratar valor R$0,00 como cotação.

**Persistência no orçamento (Supabase):**
- Preservar a linha anterior `I03-E06` (`ELE002`) como **`NAO_APLICAVEL`**, com `quantidade=NULL`, `valor_parcial=NULL`, preço unitário histórico R$7,87 visível e anotação do abatimento histórico de **R$94,44**. Não somar novamente ao subtotal.
- Nova linha `I03-E06C` **"Caixa 4×2 para sistema condulete"**, `secao=2.2`, `cod_item=NULL`, `quantidade=12 PÇ`, `valor_unitario=NULL`, `valor_parcial=NULL`, `status=EM_ANALISE`. O quantitativo 12 provém da **composição preliminar anterior**, que fora escalonada de 14 peças do kit M01 em 80% (11,2 arredondado para 12), não de medição de eletrodutos do depósito. **Não declarar 12 homologadas** nem fixar valor do substituto sem código e especificação.
- `public.elo_orcamentos.contexto.analise_item_03_deposito_4m.kit_eletrico.caixas_eletricas_20261113` e `kit_eletrico.componentes` conciliam o ELE002 retirado e a linha nova; `quantitativos_80_pct.itens` marca a linha antiga como histórico, não seleção vigente.
- Os preços/parciais de `ELE005` (dutos/canaletas, atualmente 8 peças) e `ELE131` (3 tomadas) permanecem inalterados por esta decisão, mas **devem ser confrontados com as entradas, tampas/espelhos, passagem e instalação do sistema condulete**; não trocar outros materiais silenciosamente.

**Impacto financeiro referencial, não homologado:** a retirada dos R$94,44 gera materiais **R$1.054,21** (antes R$1.148,65), equipe RH simulada continua **R$1.452,47**, parcial conhecido **R$2.506,68**, mas agora **FALTA INCLUIR o preço da nova caixa condulete 4×2**. Portanto, R$2.506,68 não é custo completo, mínimo garantido nem preço final; valores anteriores a esta revisão ficam históricos. Nenhuma linha `APLICADO`, `CAD-05=EM_ANALISE`, `CAD-06=BLOQUEADA`.

**Regressões:** verificar status de `I03-E06`, entrada de `I03-E06C` sem preço, soma por linhas (materiais R$1.054,21 + RH R$1.452,47), inexistência de aplicação dupla e preservação da configuração de 2 vãos EXC-016 0,72m² e EST040 7,23m/R$23,50/m, além de ESQ006 2 peças. O Excel consolidado anterior continua snapshot desatualizado; novo XLSX só quando solicitado. Escopo contextual Forge/Especialista ORÇAR, não promover ao Core nem alterar Lista-Mãe ou schema.


### SO 233.26 item 04 — M02 exclusivamente excedentes (decisão do Analista 13/11/2026)

**Regra de escopo vinculante da SO, prevalente:** o **item físico 04 — MLT.M02 Escritório Suíte com banheiro**, na composição canônica Base Mestre A:H, deve demonstrar **SOMENTE EXCEDENTES em relação ao produto M02 padrão**, e não deve detalhar como despesas extras a base do módulo, seus componentes, materiais sanitários de série, esquadrias padrão, acabamentos, nem lançar serviços de inspeção como custo. Esta decisão não homologa conformidade de requisitos não demonstrados: o padrão técnico deve ser validado em GAPs, não convertido automaticamente em cobranças.

**Único excedente confirmado até a revisão:** `I04-M01` seção `2.2 Materiais/Excedentes`, `EXC-011`, **3 tomadas 10 A adicionais** em circuitos existentes, **3 × R$95,65 = R$286,95**, com **mão de obra já incluída** no EXC. M02 padrão possui três tomadas; após incremento, seis. Não cobrar `ELE131`, `I04-S02`, eletricista ou outro RH para instalação dessas mesmas três tomadas. Preço **referencial**, não homologado para venda.

**O que não é excedente:** basculante do sanitário já **incluído no padrão** e não gera `ESQ006` faturável; `I04-M02` permanece `NAO_APLICAVEL` com parcela nula. Inspeções de padrão, kit hidrossanitário nominal, isolamento termoacústico, infraestrutura de ar-condicionado (sem aparelho), eventuais serviços e mão de obra apenas candidatos, ainda sem prova de serem adicionais, não devem aparecer como linhas financeiras do item 04. A instrução NÃO prova que todos eles estejam incluídos na ficha física: preservar pendências de isolamento/AC, altura interna, esquadrias/circuitos e kit sem `kit_itens` em `contexto.analise_item_04_m02.pendencias`, sem custos inventados. Reabrir candidato como exceção apenas se demonstrado não padrão, quantificado, precificado e validado pelo Analista.

**Persistência e contrato de renderização:** `public.elo_orcamento_composicao_itens`, `SO 233.26, modelo_codigo='MLT.M02', linha_codigo like 'I04-%'`: 12 linhas históricas preservadas; **uma linha `EM_ANALISE` (I04-M01, valor_parcial=286,95) e 11 `NAO_APLICAVEL` com `quantidade/valor_unitario/valor_parcial=NULL`** (exceto código e histórico de fonte conservados). A classificação `NAO_APLICAVEL` nos itens em inspeção significa não aplicável à **cobrança de excedentes neste estágio**, não confirmação da conformidade física do padrão. Não excluir registros de auditoria nem alterar Lista-Mãe/EXC. `public.elo_orcamentos.contexto.analise_item_04_m02.regra_de_orcamento='SOMENTE_EXCEDENTES_EM_RELACAO_AO_M02_PADRAO'`, `linhas_excedentes_confirmadas=['I04-M01']`, valor referencial R$286,95. `sequencia_modelos_orcamento.itens[3].tipo_orcamento='SOMENTE_EXCEDENTES'` e base explicitamente excluída da composição de excedentes. Exportação/grade de item 04 **exibe apenas I04-M01**, documentando histórico e GAPs na seção 4.0, sem listar inspeções nem basculante padrão como custo, mesmo a R$0. Não gerar preço-base fictício na seção 1.0 nem confundir R$286,95 com preço total do módulo.

**Gates e testes:** `CAD-05 EM_ANALISE`, `CAD-06 BLOQUEADA`, 0 de 5 equipamentos fechados. Somatório de valores parciais com status `EM_ANALISE` no item 04 permanece R$286,95 e `APLICADO=0`; demais modelos intactos, depósito Dry distinto e revisões de EXC016/EST040/caixa condulete preservadas. A planilha anterior é snapshot histórico marcado desatualizado; nova exportação só com solicitação expressa. É regra da experiência desta SO, não promoção ao Core.


### SO 233.26 — seção 3.0 fechamento: fórmulas visíveis, M02 somente excedentes (13/11/2026)

**Solicitação do Analista:** deixar definidos os cálculos na seção **3.0 FECHAMENTO** da Base Mestre canônica A:H, com referência específica ao **item 04 — MLT.M02 escritório suíte** em Markdown colado em 13/11/2026. A decisão imediatamente anterior, já integrada no canônico, exige orçamento do M02 **SOMENTE EXCEDENTES**, com apenas `I04-M01` ativo (3 `EXC-011` a R$95,65/un = **R$286,95**, valor com mão de obra incluída). O Markdown de entrada reproduz 1 dia de eletricista (R$275,82), subtotal M.O. R$275,82 e subtotal conhecido R$562,77, mas **essa parcela duplica o escopo do EXC-011** e contradiz a decisão mais recente. Consequentemente, não lançar os R$275,82 e não utilizar R$562,77 como subtotal. A linha de eletricista não é custo adicional válido sem escopo distinto e comprovação.

**Contrato econômico canonizado (já descrito no PROMPT §21):** VENDA aplica **ADM 10% e BDI 96%, ambos sobre o mesmo subtotal** (não compor BDI sobre subtotal+administração). Manter valores internos com precisão e **arredondar o total ao centavo**, sem antecipar todos os arredondamentos à soma. Em todo modelo, `subtotal_comercial/serviços/materiais/MO` devem referenciar os subtotais de cada seção do próprio modelo; `subtotal_geral=ARRED(SOMA(das seções);2)`; `ADM=subtotal×0,10`, `BDI=subtotal×0,96`, `total_demonstrativo=ARRED(SOMA(subtotal;ADM;BDI);2)`. Quanto faltar preço-base, escopo, validação ou aceite, **total homologado continua BLOQUEADO**, mesmo com simulação matemática calculável. Não substituir preço ausente por zero homologado. O modelo M01 possui **ajuste negativo incremental** e não recebe venda/markup automaticamente sem conciliar preço-base.

**M02 item04 — verificação do exemplo numérico de somente excedentes:**
```text
I04-M01 EXC-011:     3 × 95,65                        = R$ 286,95
Subtotal conhecido:                                  = R$ 286,95
ADM (10%):            286,95 × 0,10                  = R$  28,695   [visível: 28,70]
BDI (96%):            286,95 × 0,96                  = R$ 275,472   [visível: 275,47]
Total demonstrativo: ARRED(286,95+28,695+275,472;2) = R$ 591,12
TOTAL HOMOLOGADO:                                     = BLOQUEADO
```
A simulação de R$591,12 é **somente dos excedentes**, sem custo/preço do M02 padrão, sem comprovar venda e sem adição da equipe elétrica. O Excel registra `C56` subtotal vinculado, `C57=C56×H57` e `H57=10%`, `C58=C56×H58` e `H58=96%`, `F59` total demonstrativo e `C59` dependente de homologação; `H59=EM_ANALISE` impede a liberação. A planilha exibe status e memória explícita na seção 3.0; 11 linhas M02 não aplicáveis para cobrança mantidas como evidência histórica.

**Arquivo atualizado por solicitação:** `ELO_ORCAR_SO23326_BASE_MESTRE_FECHAMENTOS_FORMULAS_20261113.xlsx`, **9 abas** com as cinco abas financeiras e quatro auxiliares. Revisão das fórmulas em todas as cinco abas; manutenção de M05 demonstrativo histórico **R$3.152,56** (sem preço-base homologado), M01 apenas ajuste referencial **−R$442,35**, Dry 6m ainda sem valor, depósito com `EXC-016 I03-S03 = 0,72m²`, `EST040 I03-M20 = 7,23m × R$23,50/m = R$169,91` e **caixa 4×2 de sistema condulete 12 peças preliminares SEM preço** substituindo o `ELE002` DUTOPOP. O subtotal parcial do depósito passa a **R$2.506,68** (materiais 1.054,21 + RH simulada 1.452,47), e o cálculo ilustrativo `2.506,68×(1+0,10+0,96)=R$5.163,76` permanece não homologado.

**Testes/executado:** livro XLSX com nove abas, ZIP íntegro, export/reimport, fórmulas legíveis nos campos de fechamento e zero erros de fórmula `#REF/#DIV0/#VALUE/#NAME/#N/A` na varredura. Evidência persistida em `public.elo_orcamentos.contexto.analise_item_04_m02.revisao_fechamento_formula_20261113` e `cadencia_orcar.ultima_exportacao_excel`; CAD-07/CAD-13 executados com pendências e **CAD-05 em análise, CAD-06 e CAD-10/11 bloqueados**. Nenhum custo-base criado ou homologação realizada, sem modificação no Core ou na Lista-Mãe.


### SO 233.26 — PTS Técnica: decisões prévias do Analista sobre padrões, portas, +2 básculas M05, LED e janela M01 (13/11/2026)

**Escopo e autoridade.** Correção expressa feita pelo Analista após ver a PTS Técnica inicial da **SO 233.26 — FUNBIO**. Owner do contrato da PTS Técnica continua `08-ai/ELO/DIRETRIZES/PTS/` (`contrato_maturidade=1.0`), sem nova pasta, renderer, schema, Core ou PTS Pós. Dados específicos revisados permanecem **apenas** em `public.elo_orcamentos.contexto.pts_tecnica`; este registro no procedimento ORÇAR preserva as decisões e seus efeitos sobre a composição, não constitui nova autoridade de PTS. Comparar com Carta-convite 226/2026 sem substituir unilateralmente os termos do cliente.

**Decisões operacionais já respondidas, NÃO reapresentar ao Analista como perguntas abertas:**

1. **Dimensões:** trabalhar com medidas aproximadas da **configuração padrão Multiteiner**, sem reprojetar módulos ou acrescentar EXCs dimensionais automaticamente por divergências entre o padrão e a Carta-convite. Isso é **aceite interno da premissa de solução**, **NÃO** confirmação documental de atendimento ao pé-direito literal `2,89m` nem aceitação formal pela FUNBIO. Em especial, depósito Dry C06 cortado conserva altura-base externa ~2,59m / reforço interno 2,45m: divergência geométrica permanece visível como ressalva de risco, agora `T08=🟡` por escolha do Analista (antes `🔴` por bloqueio operativo automático). T03/T12/T18 permanecem em atenção pela comprovação não realizada.
2. **T02 Dry 6m:** `porta dupla` é a **porta marítima original** do contêiner, conforme interpretação expressa do Analista; **NÃO adicionar porta lateral nem orçar adaptação de nova porta**. Documento TR diz `porta dupla lateral`: preservar a redação e classificar equivalência textual com a solução original como ressalva documental, não como consulta interna sem decisão.
3. **T04 M05:** as quatro portas descritas correspondem, para a solução do Analista, às **portas internas dos sanitários**, não quatro portas externas adicionais. Verificar padrão e ferragens funcionais, sem lançá-las como EXC automaticamente. Manter literal do TR `portas na lateral` e possibilidade de aceite externo distinto.
4. **T05 M05:** **duas básculas adicionais para instalação já estão na aba M05 BASE MESTRE seção 2.2**, `2 × ESQ006` a preço **histórico da revisão enviada `R$227,09/PÇ`**, subtotal de material **R$454,18**. Lista-Mãe atual `ESQ006 = R$162,50/PÇ`: a divergência de preço permanece registrada, **não** reprecificar retroativamente sem conciliação do Analista. A aba M05 tem `M.O. interna agregada R$418,65` (encarregado R$44,82; eletricista R$55,16; bombeiro R$82,75; ajudante R$235,92; profissional R$0), **SEM linha específica que comprove montagem/vedação/instalação das duas básculas adicionais**. Logo verificar se instalação está coberta pelas funções/dias existentes antes de adicionar outra mão de obra. Não lançar mais duas básculas: material já existe.
5. **LED:** utilizar **o preço da luminária própria/padrão Multiteiner**, não outro SKU inventado para LED 30×30cm. No depósito `I03-E02`, já existe `ELE098`, LED 36W bivolt 1000×74mm, **2 PÇ × R$19,73 = R$39,46**, `status=EM_ANALISE`. O Analista mantém essa seleção sem substituição de preço/quantidade nesta revisão; TR continua pedindo 1 unidade 30×30cm, diferença formal anotada como ressalva, sem tratar como custo extra automático. Para M05/M02/M01 confirmar se os pontos LED pertencem à configuração padrão; só precificar excedente realmente comprovado com SKU Multiteiner correspondente. Não inferir que `ELE101` de sobrepor quadrada seja 30×30cm apenas pelo formato.
6. **T20 M01:** preservar a **janela padrão Salomão 900×1200mm** que permanece no M01. **NÃO criar outra janela ou EXC para convertê-la a 1000×1500mm**; o TR pede 1,00×1,50m, e a diferença é um **risco residual de equivalência documental**, não nova pergunta ao Analista. A outra das duas janelas originais M01 é substituída por **uma basculante ESQ006**; crédito da janela avulsa **ESQ004 -R$891,80**, não crédito do painel completo `PEND-M01-019 R$1.325,72`; preservar delta M01 **-R$442,35** previamente decidido. `T20=🟡` (antes `🔴`).

**PTS atual e validação:** `public.elo_orcamentos.contexto.pts_tecnica` foi revisada mantendo 27 requisitos e 16 IDs de consultas historicamente rastreáveis, com **0 verdes, 26 em atenção, 1 crítico (T26: prazo textual incompatível da Carta-convite)**. Q01/02/03/08/12 foram resolvidas como decisões operativas internas; Q04 confirmou **material** de duas básculas mas manteve a **instalação** como GAP; Q05/Q13 mantêm verificações elétricas que não se resolvem apenas pela escolha do LED. As 16 entradas permanecem no histórico da matriz com `situacao` e `resposta_analista` quando aplicável, **sem alegar envio/resposta formal do cliente**. Reabrir decisão interna somente se houver nova evidência material ou pedido expresso; tratar inconsistências remanescentes como **ressalvas contratuais separadas**.

**Orçamento e gates:** nenhum novo excedente/valor foi aplicado pela PTS. M05 materiais, M.O. e demonstrativo R$3.152,56 **não alterados**; item03 LED ELE098 R$39,46 **não alterado**; M02 permanece **somente excedentes** (3 × EXC-011 = R$286,95 com MO); M01 delta -R$442,35 **não alterado**. `CAD-02 EXECUTADA_COM_PENDENCIAS`, `CAD-05 EM_ANALISE`, `CAD-06 BLOQUEADA`, `0/5` homologados. PTS Pós não deve ser gerada por essa correção; nova planilha/DOC somente se solicitado. A PTS de maturidade 1.0 está no Supabase, não replicar uma instância paralela no GitHub.

**Regressões/Evolution Gate:** confrontar IDs 27/27, 16 consultas sem órfãos, unicidade de requisitos, T08/T10/T20 em atenção, T26 crítico, exclusões de porta lateral Dry e de quatro portas externas M05, +2 ESQ006 já lançadas, ausência de linha própria para instalação, LED depósito sem dupla contagem, e crédito M01 ESQ004 preservado. Mudança contextual, sem promoção de premissa interna a verdade universal do Core.
