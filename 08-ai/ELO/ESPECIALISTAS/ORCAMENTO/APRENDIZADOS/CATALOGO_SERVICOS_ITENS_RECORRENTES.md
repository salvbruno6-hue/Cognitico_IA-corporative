# ELO — CATÁLOGO DE SERVIÇOS E ITENS RECORRENTES DO ESPECIALISTA DE ORÇAMENTO

## 1. FINALIDADE

Este documento orienta o **Especialista de Orçamento** a reconhecer famílias de serviços e itens que aparecem de forma recorrente nas Solicitações de Orçamento (SO), identificar **quando cada família é aplicável** e direcionar a consulta para a memória quantitativa correta no Supabase.

Este catálogo não é uma lista de itens obrigatórios e não autoriza inclusão automática em orçamento.

Regra central:

`REQUISITO / CONDIÇÃO → GATILHO DE VERIFICAÇÃO → APLICAÇÃO → MEMÓRIA / PRECEDENTE → RECÁLCULO PARA A SO ATUAL`

Nunca aplicar:

`ITEM RECORRENTE = INCLUIR AUTOMATICAMENTE`

Preço histórico, quantidade histórica e equipe histórica não são transportados automaticamente para uma nova SO.

---

## 2. CLASSIFICAÇÃO DE RECORRÊNCIA

Cada família deve ser tratada em um dos estados abaixo:

- **RECORRENTE VALIDADO** — há regra/memória validada ou repetição suficiente para atuar como gatilho confiável de consulta.
- **PRECEDENTE RECORRENTE** — há composição reaproveitável como método, mas exige validação de geometria, quantitativo, material, produtividade ou preço vigente.
- **GATILHO DE VERIFICAÇÃO** — o item aparece com frequência no processo, porém sua existência depende do TR, layout, projeto, condição de campo ou decisão comercial.
- **DEPENDÊNCIA EXTERNA** — o especialista identifica a necessidade, mas o dado final vem de outro setor, fornecedor ou cliente.

---

## 3. CATÁLOGO COGNITIVO

| Família | Serviço / item recorrente | Quando verificar / aplicação | O especialista deve identificar | Dependências / alertas | Referência de memória |
|---|---|---|---|---|---|
| Produto-base | Módulo ou contêiner MLT-M / MLT-C | Sempre que a SO envolver fornecimento, locação ou adaptação de unidade | categoria, modelo, dimensão, quantidade, uso, o que já está incorporado | nunca escolher apenas pelo nome; comparar requisito × base corporativa | Diretriz do Especialista / Lista de produtos |
| Customização estrutural | Abertura de vão | Portas, janelas, ar-condicionado, integração entre módulos/contêineres, passagens e grandes aberturas | geometria do vão, área de corte, posição, necessidade de reforço, acabamento posterior | corte não equivale a reforço; verificar estabilidade e função do perfil | Supabase: CALC-ABERTURA-VAO-5PAINEIS / EXC-016 |
| Customização estrutural | Reforço de vão / requadro | Quando o corte afetar chapa, montante, longarina, coluna ou elemento resistente | dimensão do vão, perfil, metragem, função estrutural | não usar perfil histórico sem validar função e seção | Supabase: regra de conversão EST040 e memórias de reforço |
| Acabamento | Acabamento perimetral de vão | Vãos em paredes forradas ou painéis com espessura aparente | perímetro efetivo, espessura final da parede, perfil compatível | mudança de PIR/Drywall/MDF altera a seção do acabamento | Supabase: perfil_acabamento_vao_forrado_60x102x60x3000 |
| Forração | Painel PIR / Drywall / MDF / outros revestimentos | Quando a SO exigir revestimento, isolamento, acabamento interno ou divisão | área, paginação, espessura, orientação, perdas, estrutura auxiliar, fixadores | material solicitado pelo cliente prevalece; não substituir silenciosamente | Supabase: EXC_DRY_001, MC-ESTRUTURA-MDF-DRYWALL-40HC, memórias PIR |
| Forração | Estrutura de fixação do revestimento | MDF, drywall, painéis ou acabamentos que exijam subestrutura | perímetros, modulação, montantes/travessas, barras comerciais, reserva e fixadores | juntas das chapas devem coincidir com apoio; sobras não viram peça contínua automaticamente | Supabase: MC-ESTRUTURA-MDF-DRYWALL-40HC |
| Fixação | Parafusos, rebites, abraçadeiras e consumíveis de montagem | Sempre que houver estrutura auxiliar, painéis, eletrodutos, grades, esquadrias ou acabamentos | tipo de ligação: metal-metal, painel-metal, perfil-casco, acessório-perfil | não tratar todos os fixadores como equivalentes | Lista-Mãe FIX / memórias específicas |
| Piso | Piso vinílico LVT | Quando houver melhoria/acabamento de piso interno | área líquida, preparação da base, perdas, rodapé/arremates se aplicável | composição pode já conter mão de obra; verificar antes de duplicar | Supabase: CALC-PISO-VINILICO |
| Piso | Piso cerâmico / porcelanato | Sanitários, copas, áreas molhadas ou exigência específica | área, paginação, argamassa, rejunte, preparação e mão de obra | confirmar substrato e necessidade de regularização | Supabase: EXC-013 / EXC-014 |
| Esquadrias | Porta social / porta metálica / porta dupla | Acesso principal, ambientes internos, segurança ou substituição do padrão | dimensão, material, sentido de abertura, ferragens, fabricação e instalação | separar MO-FAB de MO-INST; validar abertura do vão | Supabase: EXC-003, EXC-004, MC-PORTA-EXTERNA-CORTEN-800X2100, MC-INSTALACAO-PORTA-METALICA |
| Esquadrias | Janelas | Ventilação, iluminação, atendimento ao layout/TR | dimensão, quantidade, material, tipo de abertura, grade/tela | referência cadastrada não é equivalência dimensional automática | Lista-Mãe ESQ / precedentes da SO |
| Proteção | Grade metálica para janela | Segurança patrimonial ou exigência expressa | vão, transpasse, espaçamento, fabricação, fixadores e instalação | MO dentro da composição pode ser fabricação; instalação deve ser classificada separadamente | Supabase: EXC-035_GRADE_METALICA_PROTECAO_JANELA_1200X1400 |
| Pintura | Pintura externa de contêiner/módulo | Renovação, padronização de cor, proteção anticorrosiva | área líquida, preparação, primer, acabamento, diluente e produtividade | reexecutar por área; não copiar total-base de outra dimensão | Supabase: pintura_externa_esmalte_container_maritimo_20pes / PINTURA_PU_ESTRUTURA_MODULAR_20_EXC_034 |
| Pintura | Tratamento anticorrosivo / primer | Superfícies metálicas novas, cortadas, soldadas ou deterioradas | área afetada, condição do substrato, rendimento e sistema de pintura | distinguir tratamento do casco de acabamento do revestimento interno | Lista-Mãe PIN / memórias de pintura |
| Elétrica | Ponto de tomada | Tomadas adicionais ou circuitos existentes | quantidade, tensão, corrente, circuito existente/novo, eletroduto, cabeamento e mão de obra | tomada em circuito existente ≠ circuito dedicado novo | Supabase: CALC-EXC-001-TOMADA / ponto_tomada_10a_custo |
| Elétrica | Kit elétrico / instalação interna | Módulos e contêineres com iluminação, tomadas, quadro e proteção | pontos, circuitos, quadro, disjuntores, cabos, aterramento, infraestrutura e mão de obra | separar materiais de MO; validar norma e alimentação disponível | Supabase: MAO_OBRA_KIT_ELETRICO_M01 e precedentes elétricos |
| Elétrica | Infraestrutura aparente | Eletroduto galvanizado, Dutoplast ou sistema especificado | metragem de rota, caixas, conduletes, curvas, luvas, abraçadeiras e fixações | quantidade de conexões depende do traçado; não copiar rota de outra SO | Lista-Mãe ELE/FIX e memória da SO correspondente |
| Dados | Rede lógica / infraestrutura seca | Quando TR exigir dados, lógica, telecom ou previsão futura | pontos, categoria, infraestrutura, cabos, racks/ativos, interligações e limites de escopo | distinguir infraestrutura passiva de equipamentos ativos e rede externa | Supabase: so156_rede_logica |
| Proteção elétrica | Aterramento / SPDA | Quando exigido por TR, projeto, norma aplicável ou solução validada | extensão, captores/condutores, hastes, equipotencialização, medição e MO | não assumir SPDA automaticamente; validar exigência | Supabase: EXC-023 / so156_spda |
| Climatização | Fornecimento e instalação de A/C | Ambientes climatizados ou preparação para equipamento futuro | BTU, quantidade, tensão, dreno, circuito dedicado, distância de instalação e suporte | preparação não significa fornecimento do equipamento | Supabase: so156_ac e memórias de instalação/manutenção |
| Climatização | Manutenção preventiva/corretiva | Contratos com período de manutenção ou obrigação pós-entrega | equipamentos, frequência, produtividade, ciclos, equipe, deslocamento e materiais | quantidade de visitas deriva da periodicidade | Supabase: manutencao_climatizacao_6m / manutencao_corretiva_climatizacao_6m |
| Cobertura | Estrutura de telhado / treliças | Cobertura adicional sobre módulos, conjuntos ou passarelas | vão, tipo de treliça, quantidade por módulo, metalon e geometria | tipo G/M/P depende da configuração; não transportar quantidade sem layout | Supabase: EXC-TRELICA-* / TRELICA_METALICA_CUSTO_EXC_* |
| Cobertura | Telhas, rufos, arremates | Sistemas de cobertura | área inclinada, sobreposição, beiral, perímetro e encontros | área em planta pode diferir da área real de telha | memórias de cobertura da SO correspondente |
| Drenagem | Calhas e condutores | Cobertura com coleta de águas pluviais | comprimento de calha, boquilhas, tubos, curvas, descidas e fixação | separar materiais e mão de obra; recalcular por geometria | Supabase: EXC-CALHA-METRO-LINEAR / calha_drenagem_custo_m |
| Estrutura metálica | Corte, dobra, solda, preparação e montagem | Fabricação de módulos, reforços, treliças, portas e componentes | peso/comprimento, operação, equipe, produtividade, perdas e acabamento | classificar MO-FAB; não confundir com instalação em campo | Supabase: MAO_OBRA_ESTRUTURA_20_CORTE_DOBRA, MAO_OBRA_ESTRUTURA_20_SOLDA_PREPARACAO, MAO_OBRA_MONTAGEM_ESTRUTURA_20 |
| Estrutura metálica | Perda de matéria-prima | Fabricação com perfis/chapa e plano de corte | peso comprado, peso utilizado, sobras recuperáveis e perda positiva | percentual histórico é precedente, não fator universal | Supabase: PERDA_ESTRUTURA_METALICA_MODULAR_20_PES |
| Hidráulica / sanitária | Interligações hidráulicas e esgoto | Sanitários, copas, chuveiros, lavatórios e conexão à rede existente | pontos, diâmetro, distância, aérea/subterrânea, caixas e condição de campo | limite de metragem do contrato deve ser explícito | Supabase: so156_interligacoes_10m e memórias hidrossanitárias |
| Fundação / implantação | Nivelamento, apoios e bases | Implantação de módulo/contêiner em campo | desnível, quantidade de apoios, solução de base, acesso e responsabilidade | serviço simples de nivelamento não substitui fundação quando esta for exigida | precedentes de serviço / PTS da SO |
| Logística | Carro de apoio | Equipe externa, montagem, manutenção, vistoria ou atendimento em campo | dias de mobilização, quantidade de veículos e disponibilidade | diárias do carro devem ser confrontadas com dias da equipe | Supabase: LC-MOBILIZACAO-EXTERNA-CARRO-APOIO |
| Logística | Hospedagem | Mobilização com pernoite | dias de campo, tempo de viagem, retorno e número de pessoas | estadias = pernoites; não igualar automaticamente a dias de obra | Diretriz do Especialista / LC-MOBILIZACAO-EXTERNA-CARRO-APOIO |
| Logística | Pedágio / rota / deslocamento | Trabalho externo e deslocamento entre unidade e obra | origem, destino, distância, tempo, ida/volta, pedágios | usar dado corporativo ou fonte válida; combustível zero informado não significa custo real zero | Supabase: CORP-ROTA-* |
| Logística | Caminhão, Munck, frete, descarga e içamento | Transporte/posicionamento de módulos e contêineres | necessidade técnica, tipo de carga, acesso, capacidade e operação | custo é dependência Logística → Comercial quando esse é o fluxo corporativo | Supabase: LC-MUNCK-LOGISTICA-COMERCIAL / transporte_setor_comercial |
| Mão de obra | Fabricação interna | Componentes produzidos antes da instalação | função, produtividade, jornada, quantidade produzida, custo RH | classificar MO-FAB | Supabase: LC-MO-FAB-INST-CLASSIFICACAO |
| Mão de obra | Instalação interna | Montagem do componente no módulo/contêiner em fábrica | horas/dias, equipe e produtividade | classificar MO-INST; verificar se a composição de fabricação já contém ou não essa etapa | Supabase: LC-MO-FAB-INST-CLASSIFICACAO |
| Mão de obra | Mão de obra externa | Montagem, manutenção ou entrega no cliente | equipe, dias, viagem, permanência, carro, hospedagem e campo | classificar MO-EXT e sincronizar logística | Supabase: LC-MO-FAB-INST-CLASSIFICACAO / LC-MOBILIZACAO-EXTERNA-CARRO-APOIO |
| Projetos | Projetos executivos / ART / RRT / as built | Quando exigidos pelo TR, legislação, cliente ou solução técnica | disciplina, responsabilidade, número de documentos e escopo | não assumir projeto/ART específica sem exigência/evidência | Supabase: so156_projetos e PTS específicas |
| Manutenção | Preventiva/corretiva de módulos e sanitários | Contratos com manutenção após instalação | período, visitas, cobertura, equipe, carro de apoio, peças e insumos | percentual/quantidade deve ser convertido em ciclos físicos | Supabase: manutencao_estruturas_modulares_6m, manutencao_4_sanitarios_6m, cobertura_manutencao_30pct_unidades |
| Marcenaria / mobiliário | Chapas, fórmica, cola, bancadas e prateleiras | Mobiliário e componentes fabricados por corte/paginação | peças efetivas, paginação da chapa, faces revestidas, consumo de adesivo | área comprada ≠ área efetivamente revestida | Supabase: orcamento.paginacao.compensado_pecas_efetivas, orcamento.revestimento.formica_area_pecas, orcamento.adesivo.cola_area_revestida |

---

## 4. ASSOCIAÇÕES RECORRENTES QUE DEVEM GERAR ALERTA

O Especialista deve procurar associações entre itens. A ausência de um componente associado gera **alerta de verificação**, nunca inclusão automática.

| Item identificado | Verificar também | Motivo |
|---|---|---|
| Abertura de vão | reforço + acabamento + esquadria/equipamento | o corte gera interfaces estruturais e de acabamento |
| Porta/janela nova | abertura de vão + acabamento + fabricação + instalação | o produto isolado pode não representar a adaptação completa |
| MDF/Drywall/PIR | estrutura/fixação + acabamento de juntas/vãos | revestimento exige suporte e interfaces |
| Piso novo | preparação da base + perdas + instalação | área de compra e condição do substrato afetam custo |
| A/C | circuito dedicado + dreno + suporte + instalação | equipamento depende de infraestrutura |
| Cobertura | treliça/estrutura + telha + rufo + calha/drenagem | cobertura deve ser vista como sistema |
| Elétrica | quadro + proteção + infraestrutura + cabos + pontos + aterramento | ponto isolado pode depender de circuito novo |
| Equipe externa | carro de apoio + deslocamento + pedágio + hospedagem | recursos precisam cobrir a mesma janela de mobilização |
| Contêiner/módulo entregue em campo | transporte + descarga/posicionamento + acesso | logística é parte do fechamento do fornecimento |
| Manutenção | periodicidade + produtividade + visitas + logística + insumos | custo depende de ciclos e esforço por ciclo |
| Item fabricado | MO-FAB + eventual MO-INST | fabricação não prova instalação incluída |

---

## 5. FLUXO DO ESPECIALISTA PARA ITENS RECORRENTES

Ao identificar requisito ou condição compatível com uma família recorrente:

1. **IDENTIFICAR O GATILHO** — requisito, geometria, ambiente, disciplina ou condição de campo.
2. **CONSULTAR O MODELO/BASE** — verificar se o item já está incorporado ao produto.
3. **CONSULTAR EXCEDENTES E MEMÓRIAS** — buscar precedentes equivalentes pela aplicação, não apenas pela descrição.
4. **COMPARAR APLICABILIDADE** — dimensão, material, unidade, produtividade, local, responsabilidade e estágio de execução.
5. **RECUPERAR O MÉTODO** — fórmula, variáveis, relações e dependências.
6. **RECALCULAR PARA A SO ATUAL** — nunca copiar quantidade/preço histórico sem atualização.
7. **BUSCAR PREÇO VIGENTE** — Lista-Mãe, RH, fornecedor, Logística, Comercial ou fonte competente.
8. **CLASSIFICAR MÃO DE OBRA** — MO-FAB, MO-INST ou MO-EXT.
9. **VERIFICAR ASSOCIAÇÕES** — gerar alertas para itens correlatos ausentes.
10. **REGISTRAR PENDÊNCIAS** — não esconder informação desconhecida em verba genérica.
11. **PTS PÓS** — confrontar requisito, quantitativo, composição e valor efetivamente orçados.
12. **ELO APRENDER** — se surgir nova lógica recorrente, registrar método no Git e memória quantitativa no Supabase.

---

## 6. REGRAS DE NÃO AUTOMATISMO

- Recorrência **não significa obrigatoriedade**.
- Precedente **não significa equivalência**.
- Preço histórico **não significa preço vigente**.
- Quantidade histórica **não significa quantitativo da nova SO**.
- Mão de obra dentro de uma composição **não significa instalação incluída**.
- Transporte identificado tecnicamente **não autoriza o orçamentista a inventar valor logístico**.
- SPDA, projeto, fundação, manutenção e infraestrutura externa devem ser confirmados por requisito, solução ou responsabilidade aplicável.
- A lista de associações serve para gerar perguntas e verificações, não para inflar escopo.

---

## 7. PERSISTÊNCIA E GOVERNANÇA

O conhecimento metodológico deste catálogo reside no Git.

As memórias quantitativas, fórmulas detalhadas, valores, produtividade e precedentes permanecem no Supabase e devem ser consultados pelo `conceito_key`, aplicação e origem.

Quando surgir um novo recorrente:

`CASO → PRECEDENTE → REPETIÇÃO / EVIDÊNCIA → LEARNING_CANDIDATE → VALIDAÇÃO → CONHECIMENTO REUTILIZÁVEL`

Não promover uma regra ao Core apenas porque apareceu em uma única SO.

---

## 8. OBJETIVO COGNITIVO FINAL

O Especialista de Orçamento deve evoluir de uma busca por itens para uma busca por **sistemas de custo**.

Exemplo:

`JANELA`

não deve significar apenas “buscar preço da janela”. Deve disparar:

`DIMENSÃO → PRODUTO/EQUIVALÊNCIA → ABERTURA → REFORÇO SE NECESSÁRIO → ACABAMENTO → FABRICAÇÃO → INSTALAÇÃO → PROTEÇÃO/ GRADE SE EXIGIDA → PINTURA/ARREMATE → VALIDAÇÃO`

Da mesma forma:

`OBRA EXTERNA`

não deve significar apenas “somar mão de obra externa”. Deve disparar:

`EQUIPE → DIAS → VIAGEM → CARRO DE APOIO → PEDÁGIO → HOSPEDAGEM → PERNOITES → CAMPO → RETORNO → TRANSPORTE PRINCIPAL QUANDO APLICÁVEL`

O resultado esperado é um orçamento mais completo, explicável e auditável, com menor risco de esquecimento, duplicidade ou cópia indevida de valores históricos.
