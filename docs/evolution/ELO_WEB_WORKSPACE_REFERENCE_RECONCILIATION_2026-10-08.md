---
id: ELO-WEB-WORKSPACE-REFERENCE-20261008
name: Operational workspace reference reconciliation
type: reference
layer: system
owner: ELO Web experience layer
status: draft
authority: reference
related: [AGENTS.md, ELO_REPOSITORY_NAVIGATION_RULES.md, apps/elo-web/README.md]
---

# Requirement and authority

User requested the entire operational workspace to reflect the uploaded `Texto colado(8).txt`, including a single Planejamento/PCP area. Attachment SHA-256: `0b7c2138f6b930f205420d6aac4494be75a0fc5c0396f9df81b2624f96efc300`. The attachment is a UX/functional reference, not a security contract or a source of real operational data. Its localStorage stores, seeds, random quantities, hardcoded agents, automatic approvals and Google Sheets placeholders are not admitted as canonical implementations.

Inspected main: `a253db3238ee5830104f8e740e3ef5531d7ee1cb`. Changes extend PR #955 instead of creating a competing workspace or architecture. GitHub owns implementation/contracts; live Supabase observations establish which memory/data and endpoints exist. No Core, authorization, learning, schema or deployment function is created.

# Complete reference mapping

| Reference area | Experience implementation | Existing source/boundary | Outstanding gate |
|---|---|---|---|
| Orquestrador | Request field; pending inputs; improvement communication; external-decision view | Existing `/api/cognitive` and `elo-mcp` tools | The local cognitive implementation echoes ordinary requests without evidence. UI must not render that echo as evidenced analysis. General reasoning/runtime integration remains a GAP. |
| Dashboard Comercial | Dedicated area; existing demand-crossing view; KPI/demand/coverage topics | `elo_pcp_demanda_crossing_status`; `mt_definicoes_kpi`, `mt_snapshots_kpi`, `mt_demanda_historico`, `mt_previsoes_demanda`, `mt_balanco_demanda` | KPI queries/calculations/metas and direct operational table access are not admitted. No illustrative charts or zeros for unknown periods. |
| Comercial | Dedicated solicitation/budget, clients/orders, seasonality and movements sections | `elo_orcamentos`, MT sales/client/demand/lease/return tables | Budget is not a solicitation authority. A complete SO lifecycle/write contract is not supplied by the attachment. SO number remains assigned by the budget analyst. No auto approval or automatic OF creation. |
| Almoxarifado | Dedicated material/module stock and material-request sections | MT stock/movement/unit/need tables | No generic client exposure of these tables or unvalidated material-request/approval contract. |
| Compras | Dedicated orders, suppliers/quotations and lead-time sections | MT purchase tables; `fornecedores`, `fornecedor_itens_cotacao` | Authorized operational reader/writer and safe joins are required; do not derive lead time without dates. |
| Produção | Dedicated orders/stages, repair and external-service sections | MT production/operation/repair/external-assembly tables; `fluxo_produtivo_modular_etapas` | No stock or stage mutation. Canonical ordered stages and operation links must drive a later kanban. External assembly is not all subcontracted services. |
| PCP | Labelled Planejamento/PCP; shared catalog plus existing pending/decision/demand tools; budget/plan/capacity/kanban topics | Same existing MCP tools and MT planning/operation tables | One sector in the UX does not grant capabilities or change cognitive domain contracts. Drag/drop and creation remain unavailable pending authorized operations. |
| Expedição | Dedicated shipments/return/quarantine/availability sections | MT shipment, return and inspection tables | Return cannot imply release or availability; governed read/write and inspection linkage required. |
| Catálogo | Nine searchable tables via the existing gateway | `taxonomia`, `dimensoes`, `modelos`, `modelo_apresentacao`, `kits`, `kit_itens`, `lista_mae`, `estrutura_modular`, `estrutura_modular_itens` | BOM versioning and document directory require their own existing sources/authorized access; kits are not silently relabelled BOM. Queries are limited to 500 loaded rows, not asserted global totals. |
| Chat | Existing PCP collection dialogue; explicit response/source and required fields | `elo_pcp_orquestrador_dialogo`, private canonical dialogue store | This is ELO dialogue, not team messaging. No collaborator-message contract found. Replies are submitted in events, never automatically retried; uncertain outcomes require checking dialogue state. Session resume/history is not implemented by this view. |
| Notificações | Existing pending-data view | `elo_pcp_dados_pendentes` | No read receipt/seen mutation contract found; no fabricated notification feed. Absence of this queue is not absence of all alerts. |
| Configurações | Theme/preferences, own identity/roles | Existing settings helper and `elo_status` | No client-generated user permissions, global backup/import or Sheets synchronization. |

# Evidence and source separation

Live project `fxbpevjrkwhbicpmecow` was consulted read-only through metadata, columns, enabled `elo_aprendizado_fontes` and deployed Edge Function source. `elo-mcp` v9 is active and matches the relevant tool contracts. Both the generic MCP reader and data gateway allow nine catalog tables; this change preserves those allowlists. The memory source registry contains additional enabled sources, but that does not authorize generic browser access to them. MT tenant authorization is still unresolved in the preceding main audit; this PR does not bypass it using a service key, permissive client RLS or a new privileged reader.

The experience mapping in `src/lib/workspace.ts` grants no permissions. It records sources and GAPs as UI context, not a new data/authorization authority. Operational data never comes from the reference seed/localStorage. Browser persistence is limited to existing preferences. Display name metadata is presentation-only.

# Validation

- 15/15 Node tests passed: eight OAuth regressions and seven workspace/catalog/evidence/MCP adapter tests.
- Twelve areas rendered through React SSR; distinct section content and unified Planning/PCP navigation asserted.
- MCP contract tests verify bearer forwarding, request/response correlation, deny/error/malformed-result handling and preservation of pending states; they prohibit generic SQL/table/write tool selection.
- These tests use explicit synthetic fixtures; they do not assert production tool success or authenticated operational reads.
- Next production build and its TypeScript validation passed. Only canonical routes were emitted; temporary verification route is absent.
- ESLint remains unavailable because the incumbent application lacks `eslint.config`.
- Impeccable detector: existing Arial font warning in incumbent globals.css; no other findings. Reference palette and UI identities are retained rather than introducing unrelated typography work.
- Live desktop/mobile browser verification was not completed: cloud browser could not reach the local dev server; local Playwright browser download failed in this environment. The temporary local verification route is removed and must never be committed or deployed.
- No real dialogue reply, operational insert/update/delete, grant or schema modification was performed by verification.

## Follow-up evidence: canonical application reconciliation

Maintenance run `37775327439` passed technically but left PR #955 in `WAITING_FOR_EVIDENCE`: the reconciler recognized the historical `frontend/` case, not the official application registry. The existing `docs/governance/AUTHORIZED_VERCEL_PROJECTS.json` declares `apps/elo-web` under ELO-VRC-001 and explicitly deprecates `frontend/`.

The existing reconciler now consumes that unchanged registry for application ownership. It preserves executable candidates in the audit; they must resolve to the registered application, the independently mapped Core or the explicitly deprecated frontend. An unclassified executable or explicit parallel owner remains unresolved/blocked. Changes to the registry itself, mixed application/Core/backend changes, malformed registries and other app targets cannot use this evidence. This is GOVERNANCE + TEST supporting the workspace implementation, not a new approval authority; CI, specialist/acceptance, review and merge authorization gates remain in force.

31 targeted governance tests passed, including eight additional application-boundary regressions. Local reconciliation of the full PR resolves `apps/elo-web`, source of truth = existing Vercel registry, decision = REUSE. The ELO Web legacy dependency guard also runs; obsolete variable-name prose in the README was removed rather than weakening the guard.

The public preview loaded its Google sign-in screen. A login started at the commit preview returned to the different legacy project domain; a fresh tab at the original preview still showed login. This is an observed callback-domain mismatch, not proof of a successful session or a restored production loop. Preview redirect admission/configuration needs investigation before authenticated browser acceptance. No authorization code is recorded in this evidence.

# Remaining governance/runtime work

Full functional equivalence is NOT claimed. Prioritize canonical reasoning/evidence integration (RUN-01), authorized scoped operational readers, safe joins and current empty-table states, then existing write contracts/approval gates. Team messaging, notification receipts and directory integration require an architecture decision when no canonical owner/contract exists; do not create a parallel store. The canonical grant inventory contains only expired execution/commit/merge records (expiry 2026-09-19). No self-authorization is issued and this PR cannot be reported as merged or production-complete on technical validation alone.
