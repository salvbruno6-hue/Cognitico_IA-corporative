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
