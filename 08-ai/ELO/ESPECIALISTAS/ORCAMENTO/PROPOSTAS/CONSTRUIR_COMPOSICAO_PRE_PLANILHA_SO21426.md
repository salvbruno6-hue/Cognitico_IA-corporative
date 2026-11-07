# Proposta — Construir composição antes da planilha (ELO ORÇAR)

**Status:** CANDIDATO / não canônico até aprovação e Evolution Gate.
**Owner de execução:** Especialista de Orçamento, sob conferência do ELO.
**Integração:** `prompts/ELO_ORCAMENTO_EXECUTION_CONTRACT.yaml`, `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`, `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/SKILL.md`.
**Caso de regressão:** SO 214.26, **um** contêiner de 20 pés, drywall + EPS + elétrica adaptada + pintura.

## Lacuna delimitada
O fluxo já contém composição, comparação de modelo, reconciliação de memórias, gate do especialista e auditoria. Falta explicitar a **entrega de composições completas e auditáveis como pré-condição da geração da planilha**, sobretudo quando há composição parcial ou serviço complementar não cadastrado. Não criar motor, tabela, trigger ou autoridade paralela.

## Roteamento do gatilho
`elo orçar` deve ser tratado como variante de `ORÇAR` no roteamento existente. Após intake, PTS Técnica, varredura, modelo-base, delta e reconciliação, o **Especialista** executa `construir_composicao`. ELO apenas orquestra, confere e contesta. Nenhuma etapa substitui a PTS Pós nem o ciclo de aprendizado já previstos.

## Procedimento do especialista
1. Decompor escopo por **serviço/etapa executiva** e vincular cada serviço à origem documental, decisão do owner ou premissa explícita.
2. Consultar `kits`, `kit_itens`, views dos kits, `lista_mae`, composições/EXCs e `elo_orcamento_memoria`/cálculos aprendidos antes de criar. Comparar identidade, descrição, unidade, geometria, uso, condições de execução e versão.
3. Classificar cada serviço: `EXISTENTE_COMPATIVEL`, `ADAPTAVEL`, `PARCIAL`, `INEXISTENTE`, `CONFLITANTE`. Reutilizar composição completa compatível; para parcial/adaptável, preservar base e construir **somente delta**.
4. Classificar cada linha como `REUTILIZADA`, `SUBSTITUIDA`, `ADICIONADA`, `EXCLUIDA` ou `PENDENTE`; registrar relação com a linha original. Classificar parcela em `INTEGRADO_NA_COMPOSICAO`, `COMPLEMENTAR_SEPARADO`, `DUPLICIDADE`, `CONFLITO_DE_MEMORIA`, `PENDENTE_VALIDACAO`.
5. Calcular quantitativo a partir de entradas verificáveis: fórmula, unidade, dimensões, pontos, conversão, perda, arredondamento e quantidade de compra. Separar **consumo** de **embalagem adquirida**.
6. Buscar preço vigente na Lista Mãe por código **e descrição/unidade**. Zero/nulo, incompatibilidade e divergência entre kit e Lista Mãe geram GAP, nunca custo zero confirmado. Cotação externa, quando necessária, conserva fornecedor, URL, data, embalagem, preço e status provisório; não altera Lista Mãe automaticamente.
7. Recuperar mão de obra da fonte autorizada, função, diária, equipe, dias e produtividade. Distinguir MO-FAB, MO-INST e MO-EXT; evitar ratear serviço já incluso.
8. Auditar dependências condicionais (fixadores, conexões, proteção, juntas, acabamento, testes, logística), sem inclusão automática. Solicitar vistoria/especialista para incerteza material.
9. Gerar composição por serviço e quadro de reconciliação; submeter ao gate do especialista antes de liberar planilha.
10. Executar a PTS Pós, segunda varredura e reconciliação, correções, conferência ELO e aprendizado governado já previstos.

## Contrato mínimo de saída por linha
`so_id, service_id, base_model_id, base_composition_ref, source_item_ref, operation, description, unit, qty_consumption, qty_purchase, quantity_formula, quantity_inputs, quantity_evidence, unit_price, price_source, price_date, price_status, total_cost, labor_class, included_in_base, reconciliation_status, decision_ref, gap_ids, validation_status`.

**Invariantes:** `total_cost = qty_purchase × unit_price` quando unidade de compra aplicável; caso contrário documentar critério de apropriação. Não somar custos pendentes ao total fechado; exibir subtotal conhecido e lacunas. Uma parcela de execução não pode ser contada duas vezes.

## Gate pré-planilha
**PASS** somente quando: escopo reconciliado; cada linha possui origem; unidade e quantitativo verificados; preço válido ou tratamento formal autorizado; mão de obra evidenciada; dependências e duplicidades conciliadas; decisões técnicas aprovadas; nenhuma pendência crítica sem arbitragem. **BLOCKED** para conflito de código, incompatibilidade técnica, preço sem origem, serviço faltante ou dupla contagem. **REVIEW** para premissa não crítica claramente sinalizada. Apenas PASS libera planilha final; REVIEW pode gerar **prévia não final**.

## Testes de regressão SO 214.26
- Elétrica: reutilizar M01 e substituir DutoPop por eletroduto 3 m/conexões; preservar pontos aplicáveis, recalcular infraestrutura; **não assumir** compatibilidade de luva BSP com eletroduto leve; detectar divergências ELE085 e ELE078, e barramentos ELE025/ELE027.
- Drywall: área de paredes/teto de 51,78 m² é preliminar; verificar aberturas e se tratamento de juntas já consta na base.
- EPS: converter área por placa 618 × 1243 mm, documentar perda e arredondamento; não universalizar 77 placas.
- Pintura: área 51,78 m²; 7 kg de massa drywall (consumo) vs compra de embalagem de 28 kg; 6 embalagens de PVA de 25 kg **hipótese a confirmar**; 1 lata 18 L com rendimento não validado; mão de obra 1 profissional + 1 ajudante × 2 dias da tabela RH; conferir dupla contagem de juntas.
- Verificar que apenas **1 contêiner** é orçado e que cotação externa PVA não substitui preço canônico.
- Bloquear planilha final quando preço zero/ausente ou incompatibilidade permanecer; manter subtotal conhecido, não inventar total definitivo.

## Evolução e persistência
Usar estruturas existentes de orçamento, memória, evidências, decisões e associações. Nenhuma experiência isolada da SO 214.26 vira regra geral. Persistência/alteração estrutural somente após análise de esquema, testes, owner e Evolution Gate. Esta proposta é documentação de contrato operacional; não executa migração nem altera dados.
