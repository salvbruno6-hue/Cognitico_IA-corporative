"""Humanizador de respostas do ELO.

Transforma o resultado bruto do CRL em texto no tom definido
pelo ELO_HUMAN_RESPONSE_PROTOCOL.

Camada puramente aditiva. Não altera handlers, Core ou CRL.

Refs: ELO_HUMAN_RESPONSE_PROTOCOL.
"""
from __future__ import annotations

from typing import Any


class Humanizer:
    """Converte resultado bruto do CRL em resposta humana.

    Tom: maduro, gestor, autocrítico, positivo primeiro,
    melhoria contínua, com próximo passo.
    """

    def humanize(self, result: dict[str, Any]) -> str:
        if "error" in result:
            return self._humanize_error(result)

        intent = result.get("intent")

        handlers = {
            "o_que_sabe": self._humanize_o_que_sabe,
            "confere_analise": self._humanize_confere_analise,
            "lista_abertas": self._humanize_lista_abertas,
            "status_decisao": self._humanize_status_decisao,
            "guarda_aprendizado": self._humanize_guarda_aprendizado,
            "busca_precedente": self._humanize_busca_precedente,
            "forge_consulta": self._humanize_forge_consulta,
        }

        handler = handlers.get(intent)
        if handler is None:
            return self._humanize_unknown(result)
        return handler(result)

    def _humanize_o_que_sabe(self, result: dict) -> str:
        ctx = result.get("so_context") or {}
        so_id = ctx.get("so_id") or "essa SO"
        learning = ctx.get("learning") or {}
        tags = learning.get("tags", [])
        summary = learning.get("summary", "")

        if not learning:
            return (
                f"O ELO ainda não tem registro da {so_id}.\n\n"
                "**O que ainda pode evoluir:**\n"
                "- Quando houver aprendizado registrado dessa SO, "
                "o ELO começa a reconhecer padrões aplicáveis.\n\n"
                "**Próximo passo:** se você tiver contexto dessa SO, "
                "posso registrá-lo para uso futuro."
            )

        lines = [
            f"O ELO tem registro sólido da {so_id}.",
            "",
            "**O que já sabemos:**",
        ]
        if summary:
            lines.append(f"- {summary}")
        if tags:
            for tag in tags[:6]:
                lines.append(f"- Tópico registrado: {tag}")

        lines.extend([
            "",
            "**O que ainda pode evoluir:**",
            "- Este aprendizado cobre uma SO. Outras similares ainda "
            "não têm o mesmo nível de detalhe.",
            "- O ELO ainda não cruza padrões entre SOs diferentes — "
            "isso vem quando houver mais registros.",
            "",
            "**Próximo passo:** posso detalhar qualquer ponto, se "
            "você quiser.",
        ])
        return "\n".join(lines)

    def _humanize_confere_analise(self, result: dict) -> str:
        delta = result.get("delta") or {}
        so_id = delta.get("so_id") or "essa SO"
        confidence = delta.get("overall_confidence", 0.0)

        aligned = delta.get("aligned", [])
        improvements = delta.get("improvements", [])
        corrections = delta.get("corrections", [])
        conflicts = delta.get("conflicts", [])

        if conflicts:
            headline = (
                f"A análise tem pontos que conflitam com o que o ELO "
                f"sabe sobre {so_id}."
            )
        elif corrections:
            headline = (
                f"A análise tem pontos que precisam de correção em "
                f"relação ao que o ELO sabe sobre {so_id}."
            )
        elif improvements:
            headline = (
                f"A análise está alinhada, com oportunidades de "
                f"melhoria em relação a {so_id}."
            )
        elif aligned:
            headline = (
                f"A análise está alinhada com o que o ELO sabe sobre "
                f"{so_id}."
            )
        else:
            headline = (
                f"O ELO não encontrou elementos comparáveis para "
                f"{so_id} nesta análise."
            )

        lines = [headline]

        if aligned:
            lines.append("")
            lines.append("**Pontos positivos:**")
            for item in aligned[:5]:
                lines.append(f"- {item.get('summary', '')}")

        if improvements or corrections or conflicts:
            lines.append("")
            lines.append("**Ajustes sugeridos:**")
            for item in improvements[:3]:
                lines.append(f"- {item.get('summary', '')}")
            for item in corrections[:3]:
                lines.append(f"- **Correção:** {item.get('summary', '')}")
            for item in conflicts[:3]:
                lines.append(
                    f"- **Conflito com política:** {item.get('summary', '')}"
                )

        lines.append("")
        lines.append("**O que ainda pode evoluir:**")
        if confidence < 0.5:
            lines.append(
                "- A confiança desta avaliação está baixa. Quando "
                "houver mais histórico, o ELO fica mais preciso."
            )
        else:
            lines.append(
                "- O ELO ainda não sugere valores ou ações — apenas "
                "aponta alinhamentos e divergências."
            )

        directives = delta.get("directives", [])
        if directives:
            lines.append("")
            lines.append("**O que preciso confirmar antes de prosseguir:**")
            for d in directives:
                question = d.get("question", "")
                why = d.get("why", "")
                priority = d.get("priority", "")
                marker = " 🔴" if priority == "high" else ""
                lines.append(f"-{marker} {question}")
                if why:
                    lines.append(f"  → {why}")

        recommendation = (result.get("decision_brief") or {}).get(
            "recommendation", ""
        )
        lines.append("")
        if directives:
            lines.append(
                "**Próximo passo:** responda os pontos acima e eu "
                "processo com o contexto completo."
            )
        else:
            lines.append(
                "**Próximo passo:** " + self._next_step(recommendation)
            )
        return "\n".join(lines)

    def _next_step(self, recommendation: str) -> str:
        mapping = {
            "escalar_humano_conflito_politica":
                "revisar o conflito com a área responsável antes de "
                "prosseguir.",
            "corrigir_e_revalidar":
                "ajustar os pontos apontados e submeter a análise "
                "novamente.",
            "considerar_melhorias":
                "avaliar as melhorias sugeridas — elas são opcionais.",
            "alinhado_prosseguir":
                "seguir com a análise; está consistente com o histórico.",
        }
        return mapping.get(
            recommendation, "revisar a análise e decidir o rumo."
        )

    def _humanize_lista_abertas(self, result: dict) -> str:
        count = result.get("count", 0)
        items = result.get("items", [])

        if count == 0:
            return (
                "Não há decisões abertas no momento.\n\n"
                "**O que ainda pode evoluir:**\n"
                "- O ELO ainda não distingue decisões prioritárias de "
                "rotineiras. Isso vem quando houver mais volume.\n\n"
                "**Próximo passo:** nada pendente — o ciclo está em "
                "ordem."
            )

        lines = [
            f"Há {count} decisão em aberto."
            if count == 1
            else f"Há {count} decisões em aberto.",
            "",
            "**O que está pendente:**",
        ]
        for item in items[:10]:
            dec_id = item.get("decision_id", "?")
            state = item.get("state", "?")
            lines.append(f"- {dec_id} — {state}")

        lines.extend([
            "",
            "**O que ainda pode evoluir:**",
            "- O ELO ainda não prioriza por impacto. Quando houver "
            "mais decisões, faz sentido ordenar por criticidade.",
            "",
            "**Próximo passo:** me diga qual decisão quer revisar "
            "primeiro, se precisar.",
        ])
        return "\n".join(lines)

    def _humanize_status_decisao(self, result: dict) -> str:
        if not result.get("found"):
            return (
                "Não encontrei essa decisão no histórico.\n\n"
                "**O que ainda pode evoluir:**\n"
                "- O ELO só tem registro de decisões que passaram pelo "
                "ciclo cognitivo.\n\n"
                "**Próximo passo:** confirme o identificador ou me "
                "diga o contexto."
            )

        dec_id = result.get("decision_id", "?")
        state = result.get("state", "?")
        return (
            f"A decisão {dec_id} está em '{state}'.\n\n"
            "**O que ainda pode evoluir:**\n"
            "- O ELO ainda não estima prazo para o próximo estado.\n\n"
            "**Próximo passo:** se quiser, posso detalhar o histórico "
            "dessa decisão."
        )

    def _humanize_guarda_aprendizado(self, result: dict) -> str:
        return (
            "Aprendizado registrado.\n\n"
            "**O que fizemos:** guardei o conteúdo para uso futuro em "
            "novas análises.\n\n"
            "**O que ainda pode evoluir:**\n"
            "- O ELO não valida o aprendizado antes de guardar. "
            "Curadoria manual continua importante.\n\n"
            "**Próximo passo:** o próximo registro ajuda o ELO a cruzar "
            "padrões."
        )

    def _humanize_busca_precedente(self, result: dict) -> str:
        return (
            "O ELO ainda não tem precedentes cruzados para essa "
            "busca.\n\n"
            "**O que ainda pode evoluir:**\n"
            "- Precedentes aparecem quando houver mais decisões "
            "fechadas com contexto similar.\n\n"
            "**Próximo passo:** se você identificar uma decisão "
            "anterior relacionada, posso associá-la."
        )

    def _humanize_forge_consulta(self, result: dict) -> str:
        context = result.get("forge_context") or {}
        model = context.get("model") or {}
        relationships = context.get("relationships") or {}
        discovery = context.get("governed_discovery") or {}
        if discovery.get("scope") == "cross_domain_demand_and_impacts":
            linked = discovery.get("linked_records") or {}
            not_scoped = discovery.get("not_scoped") or []
            demand_rows = linked.get("elo_sim_demanda") or []
            material_rows = linked.get("elo_sim_demanda_materiais") or []
            resource_rows = linked.get("elo_sim_demanda_recursos") or []
            decision_rows = linked.get("v_elo_pcp_decisao_externa_resumo") or []
            rule_rows = linked.get("v_elo_pcp_dialogo_regras") or []
            coverage_rows = linked.get("v_elo_pcp_cobertura_demanda_externa") or []

            lines = [
                "O Forge consultou fontes governadas para responder à demanda transversal. "
                "A síntese abaixo separa fatos observados, impactos operacionais e limites da evidência.",
                "",
                "**1. COMEÇO — o que foi consultado**",
                f"- Escopo: demanda e impactos entre domínios, sem exigir M01 ou outra entidade.",
                f"- Fontes com registros recuperados: {sum(1 for rows in linked.values() if rows)}.",
                f"- Registros recuperados nas fontes consultadas: {sum(len(rows) for rows in linked.values())}.",
            ]

            if demand_rows:
                total_qty = sum(float(row.get("quantidade") or 0) for row in demand_rows)
                priorities = [row.get("prioridade") for row in demand_rows if row.get("prioridade") is not None]
                deadlines = [row.get("prazo_dias") for row in demand_rows if row.get("prazo_dias") is not None]
                lines.extend([
                    "",
                    "**2. MEIO — fatos detalhados encontrados**",
                    f"- Demanda registrada na fonte de simulação: {len(demand_rows)} item(ns), totalizando {total_qty:g} unidade(s).",
                ])
                if deadlines:
                    lines.append(f"- Prazos registrados: de {min(deadlines)} a {max(deadlines)} dia(s).")
                if priorities:
                    lines.append(f"- Prioridades registradas: de {min(priorities)} a {max(priorities)}.")
                lines.append("- Detalhamento por demanda:")
                for row in demand_rows[:10]:
                    lines.append(
                        f"  - {row.get('demanda_id') or 'ID não informado'}: "
                        f"{row.get('descricao') or 'sem descrição'}; "
                        f"quantidade={row.get('quantidade', 'não informada')}; "
                        f"prazo={row.get('prazo_dias', 'não informado')} dia(s); "
                        f"prioridade={row.get('prioridade', 'não informada')}; "
                        f"status={row.get('status', 'não informado')}."
                    )
            else:
                lines.extend(["", "**2. MEIO — fatos detalhados encontrados**",
                              "- Não foram recuperados registros na fonte de demanda de simulação."])

            if material_rows:
                total_material = sum(float(row.get("quantidade_necessaria") or 0) for row in material_rows)
                lines.append(
                    f"- Materiais: {len(material_rows)} linha(s), com {total_material:g} unidade(s) de quantidade necessária registrada."
                )
                for row in material_rows[:10]:
                    lines.append(
                        f"  - {row.get('demanda_id') or 'demanda não informada'} → "
                        f"{row.get('material_id') or 'material não informado'}: "
                        f"{row.get('quantidade_necessaria', 'não informada')} unidade(s)."
                    )

            if resource_rows:
                total_hours = sum(float(row.get("horas_demanda_h") or 0) for row in resource_rows)
                lines.append(
                    f"- Recursos: {len(resource_rows)} linha(s), totalizando {total_hours:g} hora(s) de demanda registradas."
                )
                for row in resource_rows[:10]:
                    lines.append(
                        f"  - {row.get('demanda_id') or 'demanda não informada'} → "
                        f"{row.get('recurso_id') or 'recurso não informado'}: "
                        f"{row.get('horas_demanda_h', 'não informadas')} h."
                    )

            if decision_rows:
                decision = decision_rows[0]
                lines.extend([
                    "",
                    "**3. IMPACTOS — o que os dados permitem afirmar**",
                    f"- Estado da decisão externa: {decision.get('estado_decisao', 'não informado')}.",
                    f"- Estado de cobertura global: {decision.get('estado_cobertura_global', 'não informado')}.",
                    f"- Previsão de unidades: {decision.get('demanda_prevista_modelos', 'não informada')}.",
                    f"- Produção programada registrada: {decision.get('producao_programada_modelos', 'não informada')}.",
                    f"- Necessidade adicional de fabricação registrada: {decision.get('necessidade_adicional_fabricacao_modelos', 'não informada')}.",
                    f"- Horas planejadas de operações externas: {decision.get('horas_planejadas_externas', 'não informadas')}.",
                ])
            else:
                lines.extend(["", "**3. IMPACTOS — o que os dados permitem afirmar**",
                              "- Não há registro de resumo de decisão externa recuperado."])

            if rule_rows:
                rule = rule_rows[0]
                lines.extend([
                    "",
                    "**4. BLOQUEIOS E GAPS — o que impede uma conclusão mais forte**",
                    f"- Gate: {rule.get('gate', 'não informado')}.",
                    f"- Gap: {rule.get('gap_codigo', 'não informado')}.",
                    f"- Motivo: {rule.get('motivo', 'não informado')}.",
                    f"- Prioridade: {rule.get('prioridade', 'não informada')}.",
                    f"- Bloqueia execução: {'sim' if rule.get('bloqueia_execucao') is True else 'não' if rule.get('bloqueia_execucao') is False else 'não informado'}.",
                ])
            if not coverage_rows:
                lines.append("- A cobertura de demanda externa não apresentou registros nesta consulta.")

            if not_scoped:
                lines.extend([
                    "",
                    "**5. LIMITES — o que não deve ser inferido**",
                    "- Fontes específicas por pedido, unidade, modelo ou ordem continuam sem atribuição quando falta uma chave segura.",
                ])
                for item in not_scoped[:10]:
                    lines.append(
                        f"- {item.get('table_name')}: aprofundamento requer {item.get('reason', 'escopo seguro')}."
                    )
            else:
                lines.extend([
                    "",
                    "**5. LIMITES — o que não deve ser inferido**",
                    "- Nenhuma fonte específica ficou fora por falta de chave nesta consulta.",
                ])

            lines.extend([
                "",
                "**5A. MEMÓRIA NARRADA DO ORQUESTRADOR — como a visão foi construída**",
                "- O orquestrador parte da pergunta, identifica o domínio de demanda/impacto e consulta somente fontes autorizadas pelo catálogo.",
                "- Depois, mantém separados três níveis: **fato observado**, **padrão/sinal observado** e **projeção condicional**.",
                "- O padrão não é promovido a conhecimento aprendido nesta consulta; ele permanece uma leitura explicável dos dados recuperados.",
            ])
            if demand_rows:
                ranked = sorted(
                    demand_rows,
                    key=lambda row: (
                        -(float(row.get("prioridade")) if row.get("prioridade") is not None else -1),
                        float(row.get("prazo_dias")) if row.get("prazo_dias") is not None else float("inf"),
                    ),
                )
                lead = ranked[0]
                lead_id = lead.get("demanda_id") or "demanda sem ID"
                lead_priority = lead.get("prioridade", "não informada")
                lead_deadline = lead.get("prazo_dias", "não informado")
                lead_hours = next(
                    (
                        row.get("horas_demanda_h")
                        for row in resource_rows
                        if row.get("demanda_id") == lead.get("demanda_id")
                    ),
                    None,
                )
                lines.extend([
                    f"- **Sinal comportamental observado:** {lead_id} combina a maior prioridade disponível ({lead_priority}) com prazo de {lead_deadline} dia(s).",
                ])
                if lead_hours is not None:
                    lines.append(
                        f"- O mesmo item possui {lead_hours} hora(s) de demanda de recurso registradas; isso caracteriza pressão operacional observada, não uma previsão."
                    )
                lines.extend([
                    "",
                    "**5B. CLARIVIDÊNCIA OPERACIONAL — futuro condicionado aos padrões**",
                    "- Se esse comportamento permanecer e a cobertura continuar sem histórico comparável, a tendência esperada é de maior pressão sobre planejamento e necessidade de validação antes de ampliar fabricação ou recursos.",
                    "- Se o histórico comparável e a cobertura forem confirmados, a projeção deve ser recalculada; o orquestrador não congela uma previsão baseada apenas neste retrato.",
                    "- Se surgirem dados de estoque, reparo, produção programada ou operações externas com chaves seguras, a visão futura deve ser atualizada pela nova evidência.",
                    "- Portanto, a clarividência do ELO é **condicional, rastreável e revisável**: comportamento → padrão observado → condição futura → resultado esperado → nova evidência.",
            ])
            lines.extend([
                "",
                "**5C. ELO APRENDER — como transformar incerteza em aprendizado**",
                "- Quando o sinal ainda não é suficiente para validar um padrão, o ELO Aprender não inventa uma conclusão: identifica a lacuna e orienta a investigação.",
                "- A orientação deve ser específica: **qual assunto pesquisar, quais dados colher e por que esses dados são necessários**.",
                "- Em seguida, o ELO explicita o ganho esperado: **quais indicadores poderão ser calculados ou quais relações poderão ser validadas** com os novos dados.",
                "- Os novos dados retornam ao ciclo para confrontar o padrão inicial. Se confirmarem o comportamento nas condições comparáveis, a evidência pode avançar para validação; se contradisserem, a hipótese deve ser recalculada ou descartada.",
                "- O aprendizado somente ocorre depois da validação governada e do confronto entre expectativa e resultado posterior. A observação isolada permanece observação.",
                "",
                "**Como o ELO deve ensinar a próxima investigação:**",
                "> “Ainda não posso afirmar isso. Vamos pesquisar especificamente X e colher Y. Com esses dados poderemos validar Z e obter indicadores que hoje ainda não estão validados.”",
                "",
                "**Ciclo de aprendizado:** comportamento observado → lacuna → pesquisa orientada → novos dados → indicadores → validação → projeção condicional → resultado real → comparação → aprendizado governado.",
            ])

            lines.extend([
                "",
                "**6. FIM — conclusão executiva**",
                "- A memória desta consulta não é apenas uma lista de registros: ela registra como o orquestrador chegou à leitura, quais comportamentos observou e sob quais condições um resultado futuro pode ser esperado.",
                "- A previsão não é tratada como certeza. Ela depende da persistência dos sinais observados e pode ser alterada quando novas evidências entrarem no ciclo.",
                "- A consulta comprova registros governados de demanda, materiais e recursos, mas a decisão operacional continua dependente de cobertura, histórico comparável e vínculos seguros.",
                "",
                "**Próximo passo:** acompanhar o resultado real contra essa projeção condicionada; somente evidência posterior validada pode transformar o padrão observado em aprendizado governado.",
            ])
            return "\n".join(lines)
        linked = discovery.get("linked_records") or {}
        not_linked = discovery.get("not_linked") or []
        code = model.get("codigo") or "modelo consultado"
        name = model.get("nome") or "nome não informado"
        lines = [
            f"O Forge confirmou o **{code} — {name}** com base em fontes governadas.",
            "",
            "**O que o Forge confirma:**",
            f"- Modelo ativo: {'sim' if model.get('ativo') is True else 'não informado' if model.get('ativo') is None else 'não'}.",
        ]
        taxonomy = relationships.get("taxonomia") or []
        dimensions = relationships.get("dimensoes") or []
        kits = relationships.get("kits") or []
        kit_items = relationships.get("kit_itens") or []
        lista = relationships.get("lista_mae") or []
        structures = relationships.get("estrutura_modular") or []
        if taxonomy:
            lines.append(f"- Taxonomia: {taxonomy[0].get('codigo') or taxonomy[0].get('nome_amplo') or 'registrada'}.")
        if dimensions:
            lines.append(f"- Dimensão: {dimensions[0].get('referencia') or 'registrada'}.")
        lines.append(f"- Kits vinculados: {len(kits)}.")
        lines.append(f"- Itens de kit recuperados: {len(kit_items)}.")
        lines.append(f"- Correspondências recuperadas na Lista-Mãe: {len(lista)}.")
        model_id = context.get("entity", {}).get("model_id")
        specific_flows = [
            row for row in linked.get("fluxo_produtivo_modular", [])
            if row.get("modelo_id") == model_id
        ]
        flow_scope = discovery.get("applicability", {}).get("fluxo_produtivo_modular", [])
        family_flows = [
            item for item in flow_scope if item.get("scope") == "family_wide_modular"
        ]
        stages = linked.get("fluxo_produtivo_modular_etapas", [])
        if specific_flows:
            lines.append(f"- Fluxo produtivo específico encontrado: {len(specific_flows)}.")
            lines.append(f"- Etapas vinculadas a esse fluxo: {len(stages)}.")
        elif family_flows:
            lines.append(
                f"- Fluxo produtivo modular de referência aplicável à família de módulos: "
                f"{len(family_flows)} fluxo(s), com {len(stages)} etapa(s)."
            )
            lines.append(
                f"- O fluxo é compartilhado pela fabricação modular; isso não significa "
                f"que as {len(stages)} etapas sejam exclusivas do {code}."
            )
        else:
            lines.append("- Nenhum fluxo produtivo aplicável foi recuperado nesta consulta.")
        external_orders = linked.get("mt_ordens_montagem_externa", [])
        external_items = linked.get("mt_pedidos_venda_itens", [])
        external_team = linked.get("mt_equipe_montagem_externa", [])
        external_functions = linked.get("mt_funcoes_montagem", [])
        repair_units = linked.get("mt_unidades_modulares", [])
        repair_orders = linked.get("mt_ordens_reparo", [])
        if external_orders or external_items:
            lines.append(
                f"- Operações externas relacionadas ao {code}: {len(external_orders)} ordem(ns), "
                f"via {len(external_items)} item(ns) de pedido de venda."
            )
            if external_team:
                lines.append(f"- Equipe de montagem externa recuperada: {len(external_team)} registro(s).")
            if external_functions:
                lines.append(f"- Funções de montagem externa relacionadas: {len(external_functions)}.")
        if repair_units or repair_orders:
            lines.append(
                f"- Cobertura de reparos modulares relacionada ao {code}: "
                f"{len(repair_units)} unidade(s) e {len(repair_orders)} ordem(ns) de reparo."
            )
        if structures:
            lines.append(f"- Estrutura modular específica encontrada: {len(structures)}.")
        else:
            lines.append("- Nenhum registro de estrutura modular foi recuperado no estado atual consultado.")
        lines.extend(["", "**O que não está comprovado:**"])
        if not structures:
            lines.append(
                f"- O estado atual consultado não contém registro de estrutura modular "
                f"recuperável para o {code}; isso não autoriza concluir que a estrutura "
                f"conceitual do processo não exista."
            )
        if not specific_flows and not family_flows:
            lines.append(f"- Não foi localizado fluxo aplicável ao {code} nesta consulta.")
        if not_linked:
            names = ", ".join(str(item.get("table_name")) for item in not_linked[:8] if item.get("table_name"))
            lines.append("- Algumas fontes governadas foram descobertas, mas não foram relacionadas ao modelo sem uma chave segura: " + names + ".")
        if not external_orders and not external_items:
            lines.append(
                f"- Nenhuma ordem de operação externa foi relacionada ao {code} no estado atual consultado."
            )
        if not repair_units and not repair_orders:
            lines.append(
                f"- Nenhuma unidade/ordem de reparo foi relacionada ao {code} no estado atual consultado."
            )
        if not any([
            not structures,
            not specific_flows,
            not_linked,
            not external_orders and not external_items,
            not repair_units and not repair_orders,
        ]):
            lines.append("- Nenhuma ausência adicional foi identificada nesta consulta.")
        lines.extend([
            "",
            "**Limite da evidência:**",
            "- Relações sem chave segura não foram inferidas.",
            "- A consulta é somente leitura e não gera aprendizado ou promoção.",
            "",
            "**Próximo passo:** as fontes descobertas sem vínculo podem ser consultadas quando houver uma chave operacional que permita relacioná-las ao modelo.",
        ])
        return "\n".join(lines)

    def _humanize_error(self, result: dict) -> str:
        error = result.get("error", "desconhecido")
        suggestions = result.get("suggestions", [])

        lines = [
            "Houve um problema ao processar essa solicitação.",
            "",
            "**O que tentei:** entender o comando enviado.",
            f"**O que aconteceu:** {error}.",
            "",
            "**O ELO reconhece que isso é uma falha.** A linguagem "
            "ainda está em evolução e nem toda variação é capturada.",
            "",
            "**Próximo passo:** tente reformular usando um dos "
            "comandos documentados, ou me diga o que você queria fazer.",
        ]

        if suggestions:
            lines.append("")
            lines.append("**Comandos disponíveis:**")
            for s in suggestions[:5]:
                lines.append(f"- {s}")

        return "\n".join(lines)

    def _humanize_unknown(self, result: dict) -> str:
        return (
            "Recebi essa solicitação, mas ainda não tenho um formato "
            "definido para esse tipo de resposta.\n\n"
            "**O que ainda pode evoluir:**\n"
            "- O ELO reconhece novas intenções conforme elas aparecem.\n\n"
            "**Próximo passo:** me diga o que você esperava da resposta."
        )
