# Testes de contrato — ELO ORÇAR / composição pré-planilha

**Escopo:** testes de instrução, sem aplicação web, deploy ou Vercel. **Caso:** SO 214.26, um contêiner de 20 pés. **Status:** cenários definidos; execução funcional pelo Especialista ainda pendente.

## Critérios de aceitação

| ID | Entrada | Resultado esperado |
|---|---|---|
| T01 | "ELO ORÇAR" com SO/documentação | Roteia ao Especialista; consulta GitHub/Supabase e produz composições antes da planilha |
| T02 | Composição existente tecnicamente equivalente | Reutiliza composição e registra referência, sem criar duplicata |
| T03 | KIT-M01 com infraestrutura DutoPop incompatível | Preserva itens aplicáveis, substitui infraestrutura e explicita delta |
| T04 | Eletroduto 3 m e conexões sem quantitativo confirmado | Marca quantidade provisória; não apresenta orçamento final como validado |
| T05 | Preço zero em ELE027/ELE078 | Abre GAP; não considera preço zero como custo confirmado |
| T06 | Divergência ELE025 kit vs Lista Mãe | Marca conflito de fonte/descrição e exige reconciliação |
| T07 | Drywall 51,78 m² e memória histórica 54 m² | Recalcula pela geometria, verifica aberturas, identifica diferença |
| T08 | Massa de juntas já incluída no drywall-base | Evita segunda cobrança ou bloqueia até conciliação |
| T09 | EPS 618×1243 mm, 40 mm | Converte área, documenta perdas/arredondamento, separa estimativa de compra |
| T10 | PVA 6×25 kg a R$59,90 | Marca hipótese de consumo e cotação externa; não promove a preço oficial |
| T11 | Massa drywall 7 kg e embalagem 28 kg | Separa consumo apropriado de aquisição integral |
| T12 | Pintura com profissional + ajudante por 2 dias | Usa RH vigente e verifica se MO já consta em composição-base |
| T13 | Pedido alterado de dois para um contêiner | Não duplica quantitativos nem mão de obra |
| T14 | GAP técnico crítico ou preço sem origem | Gate BLOCKED; somente pendências e perguntas; sem planilha final |
| T15 | Premissa não crítica identificada | Gate REVIEW; apenas prévia explicitamente provisória |
| T16 | Todas as parcelas comprovadas e reconciliadas | Gate PASS; planilha final autorizada |
| T17 | PTS Pós identifica omissão/duplicidade | Retorna ao Especialista para correção e repete auditoria |
| T18 | Aprendizado isolado da SO | Registra CASE/CANDIDATO; não promove ao Core sem Evolution Gate |

## Formato de retorno nesta conversa
1. Identificação da SO, escopo e modelo-base.
2. Tabela de composições por serviço, com quantidade, unidade, preço unitário, subtotal, origem e status.
3. Memória de cálculo por quantitativo e produtividade.
4. Matriz de reconciliação: base × complemento × duplicidade × GAP.
5. Gate `PASS|REVIEW|BLOCKED` e justificativas.
6. Planilha final somente após PASS e quando solicitada; caso contrário, apresentar tabela/provisória aqui.

## Verificações estáticas sem deploy
- YAML parseável.
- Gatilho `elo orçar` mapeado a `budget_request`.
- `composition_build_pre_spreadsheet` precede `composition_pre_spreadsheet_gate`, que precede `specialist_gate` e `budget_decision`.
- Skill aponta para os IDs exatos do contrato e não assume composição/precificação.
- Saída declara `composition_build_report` e `composition_pre_spreadsheet_gate_result`.
- Não alterar Supabase, Core, preço oficial ou regra de negócio sem governança.

**Atenção:** este documento especifica testes; não atesta execução ponta a ponta. A conferência do owner e Evolution Gate continuam necessários.
