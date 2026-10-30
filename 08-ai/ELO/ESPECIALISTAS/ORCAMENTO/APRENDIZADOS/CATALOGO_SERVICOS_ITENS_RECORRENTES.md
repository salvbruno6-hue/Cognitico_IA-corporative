# ELO — Catálogo de Serviços e Itens Recorrentes do Especialista de Orçamento

## 1. Finalidade

Este catálogo orienta o Especialista de Orçamento a reconhecer serviços e itens recorrentes, identificar **quando são aplicáveis** e direcionar a consulta para a composição, EXC, Lista-Mãe e memória quantitativa corretas.

Regra central:

`REQUISITO/CONDIÇÃO → GATILHO → APLICAÇÃO → COMPOSIÇÃO/EXC → MEMÓRIAS ASSOCIADAS → CONFRONTO → RECÁLCULO PARA A SO ATUAL`

Nunca aplicar:

`ITEM RECORRENTE = INCLUIR AUTOMATICAMENTE`

Preço, quantidade, equipe e produtividade históricas são referências de método; devem ser validados no cenário atual.

## 2. Estados de recorrência

- **RECORRENTE VALIDADO** — regra/memória validada que pode disparar consulta confiável.
- **PRECEDENTE RECORRENTE** — método reutilizável, sujeito a revalidação de geometria, quantidade, material, produtividade e preço.
- **GATILHO DE VERIFICAÇÃO** — item frequente cuja existência depende da SO, projeto, layout, campo ou decisão comercial.
- **DEPENDÊNCIA EXTERNA** — necessidade identificada tecnicamente, com dado final vindo de outro setor/fornecedor/cliente.

## 3. Famílias recorrentes

| Família | Verificar quando | Itens/serviços associados | Alertas principais |
|---|---|---|---|
| Produto-base | fornecimento, locação ou adaptação | MLT-M / MLT-C, modelo, dimensão, configuração | comparar requisito × padrão corporativo; não escolher só pelo nome |
| Aberturas | porta, janela, A/C, integração, passagem | corte, reforço, acabamento, esquadria/equipamento | corte não equivale automaticamente a reforço |
| Forração | PIR, drywall, MDF, outros | chapa/painel, estrutura auxiliar, fixadores, acabamento | validar área, paginação, perdas, espessura e interfaces |
| Piso | LVT, cerâmico, porcelanato | preparação, material, perdas, instalação | composição pode já conter MO; confrontar antes de somar |
| Esquadrias | portas e janelas | produto, abertura, acabamento, instalação, ferragens | confrontar composição-base × memória específica de instalação |
| Proteção | grades/telas | fabricação, fixação, instalação | classificar MO pela etapa real |
| Pintura | tratamento e acabamento | preparação, primer, acabamento, consumíveis, MO | recalcular por área/substrato; não copiar total histórico |
| Elétrica | pontos, quadro, iluminação, A/C | infraestrutura, cabos, proteção, aterramento, MO | ponto isolado pode exigir circuito/infraestrutura |
| Dados | lógica/telecom | infraestrutura seca, cabos, conectores, ativos | separar passivo, ativo e interligação externa |
| SPDA/aterramento | exigência técnica/documental | captores, condutores, hastes, equipotencialização, MO | não assumir automaticamente |
| Climatização | fornecimento/preparação/manutenção | equipamento, circuito, dreno, suporte, instalação | preparação não significa fornecimento do equipamento |
| Cobertura | telhado adicional | treliças, telhas, rufos, calhas, drenagem | tratar como sistema, não itens isolados |
| Estrutura metálica | fabricação/reforços | corte, dobra, solda, preparação, montagem, perda | separar MO-FAB de MO-INST/MO-EXT |
| Hidráulica/sanitária | sanitários, copas, chuveiros | água, esgoto, interligações, caixas, acessórios | validar distância, condição de campo e responsabilidade |
| Fundação/implantação | instalação em campo | nivelamento, apoios, bases, fundação | nivelamento simples não substitui fundação exigida |
| Logística | obra/entrega externa | carro, rota, pedágio, hospedagem, combustível, Munck/frete | sincronizar dias, veículos, pernoites e responsabilidade setorial |
| Mão de obra | qualquer composição | MO-FAB, MO-INST, MO-EXT, funções, produtividade | presença de mão de obra genérica não prova etapa final incluída |
| Projetos/documentação | obrigação contratual/técnica | projeto, ART/RRT, as built, ensaio, comissionamento | não assumir sem evidência |
| Manutenção | obrigação pós-entrega/periódica | ciclos, visitas, equipe, logística, insumos | custo depende de periodicidade e produtividade |
| Marcenaria/mobiliário | bancadas/prateleiras/móveis | paginação, chapas, revestimentos, adesivos, MO | área comprada ≠ área efetivamente aplicada |

## 4. Associações que geram alerta

| Item identificado | Verificar também | Motivo |
|---|---|---|
| Abertura de vão | reforço + acabamento + esquadria/equipamento | o corte cria interfaces estruturais e de acabamento |
| Porta/janela | abertura + acabamento + produto + instalação | o valor do produto pode não incluir adaptação/instalação |
| MDF/Drywall/PIR | estrutura + fixação + acabamento | revestimento exige suporte e interfaces |
| Piso | preparação + perdas + instalação | área e substrato afetam custo |
| A/C | circuito + dreno + suporte + instalação | equipamento depende de infraestrutura |
| Cobertura | estrutura + telha + rufo + calha/drenagem | solução deve ser tratada como sistema |
| Elétrica | quadro + proteção + infraestrutura + cabos + pontos + aterramento | ponto isolado pode depender de circuito novo |
| Equipe externa | carro + rota + pedágio + hospedagem/pernoite | recursos devem cobrir a mesma janela de mobilização |
| Entrega de módulo/contêiner | transporte + descarga/posicionamento | logística integra o fechamento comercial conforme responsabilidade |
| Item fabricado | MO-FAB + verificar MO-INST | fabricação não prova instalação incluída |
| Memória específica existente | confrontar composição-base | impede omissão ou duplicidade por texto-resumo ambíguo |

## 5. Fluxo obrigatório para itens recorrentes

1. **Identificar o gatilho** — requisito, geometria, ambiente, disciplina ou condição de campo.
2. **Consultar modelo/base** — verificar o que já está incorporado.
3. **Consultar EXCs, composições e memórias** — buscar equivalência pela aplicação, não apenas pela descrição.
4. **Abrir a composição-base** — identificar componentes efetivamente precificados.
5. **Classificar etapas** — material, MO-FAB, MO-INST, MO-EXT, acabamento, transporte etc.
6. **Localizar memórias específicas** — instalação, montagem, acabamento, logística, manutenção ou outra etapa complementar.
7. **Confrontar evidências** — decidir integrado, complementar, duplicado, conflitante ou pendente.
8. **Comparar aplicabilidade** — dimensão, material, unidade, produtividade, local, responsabilidade e estágio.
9. **Recuperar método** — fórmula, variáveis, relações e dependências.
10. **Recalcular para a SO atual** — não copiar quantidade/preço histórico.
11. **Buscar preço vigente** — Lista-Mãe, RH, fornecedor, Logística, Comercial ou fonte competente.
12. **Verificar associações** — gerar alertas para correlatos ausentes.
13. **Registrar pendências** — não esconder lacunas em verba genérica.
14. **PTS Pós** — repetir varredura e reconciliação sobre o orçamento efetivamente fechado.
15. **Revisão de aprendizado** — confrontar respostas do owner com evidências.
16. **ELO APRENDER** — persistir método e memória conforme governança.

## 6. Regra de confronto composição × memória

Hierarquia de evidência para decidir se uma etapa está incluída:

1. componentes efetivamente precificados;
2. memória específica da etapa;
3. vínculo EXC ↔ memória;
4. decisão explícita validada do especialista/orçamentista;
5. texto-resumo genérico.

Classificações:

- `INTEGRADO_NA_COMPOSIÇÃO`;
- `COMPLEMENTAR_SEPARADO`;
- `DUPLICIDADE`;
- `CONFLITO_DE_MEMÓRIA`;
- `PENDENTE_DE_VALIDAÇÃO`.

**Texto-resumo não prevalece sobre a estrutura da composição.**

### Caso de referência — porta metálica

- `MC-PORTA-EXTERNA-CORTEN-800X2100` — R$ 600,22: materiais + fabricação + acabamento;
- `MC-INSTALACAO-PORTA-METALICA` — R$ 118,15: instalação específica;
- conclusão: a existência da memória específica impede presumir instalação embutida nos R$ 600,22 sem linha inequívoca dessa etapa na composição-base.

## 7. Regras de não automatismo

- Recorrência **não significa obrigatoriedade**.
- Precedente **não significa equivalência**.
- Preço histórico **não significa preço vigente**.
- Quantidade histórica **não significa quantitativo da nova SO**.
- Mão de obra dentro de composição **não significa instalação incluída**.
- Transporte identificado tecnicamente **não autoriza inventar valor logístico**.
- Associação serve para gerar verificação, não para inflar escopo.
- Memória específica não deve ser somada sem verificar duplicidade; também não deve ser excluída por texto-resumo sem confronto.

## 8. Persistência e governança

O método e as regras de aplicação deste catálogo residem no Git.

Memórias quantitativas, fórmulas detalhadas, valores, produtividade e precedentes residem no Supabase e devem ser consultados por `conceito_key`, aplicação, origem e evidência.

`CASO → PRECEDENTE → REPETIÇÃO/EVIDÊNCIA → LEARNING_CANDIDATE → VALIDAÇÃO → CONHECIMENTO REUTILIZÁVEL`

Uma única SO não promove regra ao Core.

## 9. Objetivo cognitivo

O Especialista deve evoluir de busca por itens para busca por **sistemas de custo e etapas executivas**.

Exemplo:

`PORTA → PRODUTO/COMPOSIÇÃO → ABERTURA → ACABAMENTO → FABRICAÇÃO → MEMÓRIA ESPECÍFICA DE INSTALAÇÃO → CONFRONTO → CUSTO FINAL`

Exemplo:

`OBRA EXTERNA → EQUIPE → DIAS → VIAGEM → CARRO → PEDÁGIO → HOSPEDAGEM → PERNOITES → CAMPO → RETORNO → TRANSPORTE PRINCIPAL QUANDO APLICÁVEL`

O resultado esperado é um orçamento completo, explicável e auditável, com menor risco de esquecimento, duplicidade ou exclusão indevida de parcelas.
