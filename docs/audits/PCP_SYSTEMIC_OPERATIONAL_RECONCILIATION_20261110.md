# PCP Multiteiner — reconciliação operacional governada (2026-11-10)

**Estado:** EVIDENCIADO / CONFLITOS ABERTOS; não promovido a regra universal.  
**Autoridade:** GitHub para implementação e contratos; Supabase para dados operacionais persistidos; Forge para conhecimento contextual; Skill PCP existente para raciocínio especializado.  
**Escopo:** registro da informação operacional fornecida nesta conversa, sem escrever dados produtivos, sem substituir BOM, sem alterar dashboard, sem criar Skill ou autoridade paralela.

## Reutilização comprovada

- `06-knowledge-engineering/SKILL_PLANEJAMENTO_MULTITEINER.md`: PM-01 a PM-17, incluindo capacidade, fluxos paralelos, estoque intermediário, qualidade e aprendizado.
- `src/elo/cognitive/pcp_systemic_capacity.py`: `assess_systemic_capacity`, `project_el`, `assess_el_event_balance`, `first_constraint_date`. Não duplicar os cálculos.
- `tests/cognitive/test_pcp_systemic_capacity.py`: testes já existentes.
- `supabase/migrations/20261029020500_pcp_fluxo_paralelo_paginacao_paineis_esquadrias.sql`: conhecimento candidato de paginação de painéis/esquadrias por modelo, sem promoção.
- Supabase: `fluxo_produtivo_modular`, `fluxo_produtivo_modular_etapas`, `mt_planos_pcp`, `mt_linhas_plano_pcp`, `elo_aprendizado_pcp_planejamento`, `v_elo_pcp_inteligente` e views de MRP; verificar vigência, dados e RLS antes de qualquer mutação.

## Conhecimento operacional informado — não confundir com medição atual

| Conceito | Informação recebida | Classificação | Condição de uso |
|---|---|---|---|
| Demanda comercial | Aumento de demanda motivou revisão de produtividade | REGRA CONTEXTUAL INFORMADA | Exigir pedido, mix, datas e origem para dimensionar |
| Estrutura | Referência nominal 4 estruturas/dia | REFERÊNCIA INFORMADA | Não equivale a módulos completos |
| Montagem | Padrão 4 módulos/dia; até 6/dia somente em recuperação | CONFLITO COM REGISTROS LEGADOS | Verificar vigência, equipe, EL, materiais, qualidade e evidência da recuperação |
| Telha de fibra | Referência anterior 4/dia; usuário informou aumento para 6/dia | CONFLITO TEMPORAL / NECESSITA VALIDAÇÃO | Confirmar data efetiva, jornada, recursos, cura e realizado; não sobrescrever histórico |
| Cubas | 3/dia nominal; aplicabilidade depende do modelo | REFERÊNCIA INFORMADA | Exigir BOM/mix por modelo |
| EL | mínimo 3, alvo 4, máximo 5 | REGRA INFORMADA | Saldo real somente por eventos; projeção cumulativa |
| Corte e dobra | 1 chapa rende aproximadamente 7 kits | NECESSITA MEDIÇÃO/VALIDAÇÃO | Não transformar rendimento aproximado em BOM ou saldo real |
| PIR e esquadrias | Necessidades e paginação variam por modelo | CONCEITO EXISTENTE | Usar projeto/BOM vigente, aliases e disponibilidade; não multiplicar universalmente |
| D1 | Início do fluxo estrutural, não montagem final | REGRA INFORMADA | Cronologia e eventos devem ser comprovados |
| Compras | Necessidade temporal depende de BOM, saldo, reservas, pedidos e lead time | CONCEITO EXISTENTE | Não emitir pedido sem consumo, unidade e disponibilidade comprovados |
| Reparo | Pode competir por recursos com produção nova | REGRA CONDICIONAL | Subtrair carga apenas quando mesma capacidade e carga estiverem comprovadas |

## Conflitos e GAPs

- **PCP-CONFLICT-MONTAGEM-001:** `6 módulos/dia` aparece como capacidade padrão em fontes legadas; novo relato distingue `4 nominal` de `6 recuperação condicionada`. Não sobrescrever; confrontar vigência, escopo e evidência.
- **PCP-CONFLICT-FIBRA-001:** 4 telhas/dia anteriormente, 6 telhas/dia informado como aumento. Requer data de mudança, equipamento, equipe, turno, rendimento e realizado para versionar capacidade.
- **PCP-GAP-MIX-001:** demanda de 300 módulos sem mix/datas de entrega comprovados; não explodir PIR, cubas ou esquadrias.
- **PCP-GAP-EL-001:** EL físico atual, eventos de liberação/cura e horário de consumo não confirmados nesta investigação.
- **PCP-GAP-MRP-001:** BOM vigente, estoques utilizáveis, reservas, pedidos abertos e lead times precisam ser cruzados antes de recomendar compras.
- **PCP-GAP-RH-001:** sem prova de produtividade marginal por colaborador, não calcular contratações automaticamente.

## Contrato de decisão do Orquestrador

1. Receber demanda com modelos, quantidades, prioridade, datas e fonte.
2. Resolver BOM/aliases por modelo e vigência; calcular necessidades por recurso, não pelo total universal de módulos.
3. Verificar estoque físico, utilizável, bloqueado, reservado, saldo técnico e pedidos; compras/almoxarifado permanecem responsáveis por seus próprios atos.
4. Conciliar estrutura, corte/dobra, fibra, cubas, PIR, esquadrias, instalações, EL, montagem, qualidade e reparo em unidades compatíveis.
5. Reutilizar `assess_systemic_capacity` e `first_constraint_date`; dados essenciais ausentes retornam evidência insuficiente, não capacidade inventada.
6. Propor alternativas condicionais: redistribuição do mix, compra antecipada, turno/equipe adicional, capacidade extraordinária, reprogramação. Cada alternativa requer premissas, impacto e aprovação competente.
7. Separar `REALIZADO`, `ATUAL`, `PLANEJADO`, `PROJETADO`, `SIMULADO`; não converter cenário em OP, compra ou contratação.
8. Registrar decisão, justificativa, evidências, resultado observado e aprendizado; promoção somente pelo Evolution Gate.

## Matriz de integração

| Conceito operacional | Skill PCP | Forge | Banco | Implementação | Evidência | Status | GAP |
|---|---|---|---|---|---|---|---|
| Capacidade sistêmica | PM-05/06/09 | conhecimento PCP | capacidade/fluxo MT | `pcp_systemic_capacity.py` | código existente + regra informada | PARCIALMENTE CONFIRMADO | capacidades efetivas e mix |
| EL e cura | PM-08/09 | contexto de pulmão | eventos EL (verificar schema) | `assess_el_event_balance`, `project_el` | código existente + regra informada | PARCIALMENTE CONFIRMADO | eventos atuais |
| Primeira ruptura | PM-06/10 | diagnóstico | planos e evidências por dia | `first_constraint_date` | código existente | CONFIRMADO COMO MECANISMO | snapshots reais |
| Fibra | PM-07/09 | fluxo paralelo | BOM/PRFV e views existentes | reconciliação anterior à conversão | regra 4→6 informada | CONFLITO | vigência e realizado |
| Cubas | PM-07/09 | fluxo paralelo | BOM/modelo a verificar | não criar multiplicador universal | regra informada | NECESSITA VALIDAÇÃO | mix/BOM |
| PIR/esquadrias | PM-07/09 | candidato existente | Lista Mãe e fonte técnica | migration de 2026-10-29 | código existente | CANDIDATO | paginação vigente |
| Compras/MRP | PM-01/08/10 | evidência contextual | views MRP/estoque | reutilizar cálculos governados | estruturas identificadas | PARCIALMENTE CONFIRMADO | saldo, lead time |
| Recuperação montagem | PM-05/13 | conflito contextual | capacidade histórica a verificar | guarda sistêmica existente | regra informada | CONFLITO | vigência/equipe |
| Qualidade/reparo | PM-12/13 | observação/experiência | estruturas MT | não confundir conclusão/liberação | Skill existente | PARCIALMENTE CONFIRMADO | eventos/recursos |

## Validação e promoção

Testes-alvo (não declarar executados apenas por documentação): EL 2 e plano 4; EL 5 e recuperação 6; fibra 2 com mix que exige 4 telhas; modelos sem cuba; aliases PIR40/MAT-PIR-40; kit porta vs porta completa; cura não concluída; compra com saldo suficiente; BOM sem consumo; primeira ruptura com dado ausente.

**Gate:** esta reconciliação é evidência documental e backlog de conflitos; não promove capacidades, não modifica Supabase, não concede autoridade operacional, não prova o aumento efetivo de produtividade. Reavaliar após testes e evidências canônicas.
