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

### Retificação supervisionada — depósito de 4 m, item 03 normalizado
- **Seleção corrigida pelo especialista:** MLT.M02 é o modelo-base do **contêiner depósito de 4 m** na SO 233/2026. A referência preliminar MLT.C04 foi rejeitada pelo especialista.
- **Estado epistemológico:** a preferência MLT.M02 é uma decisão explícita para esta SO, mas não há ficha técnica suficiente na conversa para afirmar conformidade dimensional ou construtiva. Registrar a possível divergência de comprimento entre 4 m requeridos e o modelo MLT.M02 de 20 pés, bem como os ajustes de esquadrias, elétrica e uso como depósito. Não transportar automaticamente excedentes de +3 tomadas do escritório para este depósito: o depósito pede 3 tomadas, 1 luminária e 2 janelas basculantes.
- **GAP de evolução:** comparar MLT.M02 contra o MLT.C04 anteriormente sugerido, documentar evidências de equivalência, validar com especialista/PTS e reter o aprendizado como precedente contextual, não regra universal de catálogo.

### Continuação supervisionada — SO 233/2026 (itens de escritório e habitável)

**Desambiguação documental e retificação do especialista:** a SO repete o número 03 para depósito de 4 m e escritório com banheiro. Para análise sequencial de cinco equipamentos: 01 Dry = MLT.C06; 02 banheiro = MLT.M05; **03 depósito de 4 m = MLT.M02, por determinação explícita do especialista**; 04 escritório com banheiro = MLT.M02 como hipótese anteriormente informada; 05 habitável = MLT.M01. As referências simultâneas ao MLT.M02 são intencionais nesta memória, mas sua adequação construtiva às duas aplicações requer comprovação por ficha e confronto técnico. Não confundir o número original repetido com a sequência normalizada.

**04 (numeração normalizada; 03 repetido na SO original) — Escritório com banheiro: modelo-base candidato MLT.M02 (Módulo Habitacional 20 pés Escritório Suíte).**
- **Evidências:** pé-direito/altura nominal de 2,89 m, mais compatível segundo especialista com solução modular, e integração de escritório com banheiro.
- **Princípio:** escolher família construtiva e configuração habitual de venda/locação antes de decompor custo; características incorporadas ao produto padrão (como solução de isolamento termoacústico, se comprovada em ficha técnica) devem continuar incluídas mesmo quando a SO não as menciona, e não viram excedente automaticamente.
- **Excedente informado pelo especialista:** **+3 tomadas** para atingir requisito de 6 tomadas 10 A; pressupõe 3 tomadas no padrão. Validar quantidade de circuitos e tomadas efetivas na ficha do MLT.M02 antes de precificar. Confirmar janela, basculante, porta, banheiro, luminárias e infraestrutura de ar-condicionado. A abertura/tomada para ar-condicionado não implica incluir o aparelho quando não solicitado.
- **Risco:** altura e isolamento não foram aferidos contra ficha técnica; evitar declarar conformidade sem evidência.

**05 (numeração normalizada; 04 na SO original) — Habitável: modelo-base candidato MLT.M01 (Módulo Habitacional 20 pés Amplo).**
- **Configuração informada pelo especialista:** 1 janela de correr + 1 basculante; **+3 tomadas** para atender às 6 tomadas da SO, condicionadas à confirmação de 3 já incorporadas ao padrão.
- **Comparação obrigatória:** verificar se as duas esquadrias fazem parte da base e não cobrar duplicadas; avaliar 4 portas laterais requeridas, 2 luminárias e infraestrutura para ar-condicionado; confrontar altura externa/pé-direito.
- **Não inventar:** dimensões, isolamento e quantidade padrão de esquadrias/tomadas precisam de cadastro/ficha validada.

**Lógica reutilizável:** requisitos explícitos da SO + características incorporadas à oferta-padrão comprovada → seleção por aderência técnica → lacunas reais de quantitativo e configuração → excedentes líquidos; atributo do padrão não solicitado não deve ser removido por omissão, mas também não deve ser apresentado como exigência contratual do cliente. Registrar origem do atributo, hipótese, condição de aceite e composição sem duplicidade.

**Status:** precedente supervisionado sob validação; o merge documental não constitui promoção ao Core ou persistência cognitiva validada no Supabase. **Regressão:** distinguir depósito de escritório apesar da duplicação de numeração e preservar o MLT.M02 como candidato para ambos por fontes distintas; confirmar +3 tomadas somente com padrão de 3 documentado; impedir dupla cobrança de termoacústico e esquadrias já incluídos.
