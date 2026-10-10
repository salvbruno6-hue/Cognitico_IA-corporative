"use client";

import { useMemo, useState } from "react";
import type { CognitiveResponse } from "@/lib/elo-cognitive";

type Props = { onSignOut?: () => void; accessToken: string };
type AreaId = "orquestrador" | "dashboard" | "comercial" | "almoxarifado" | "compras" | "producao" | "pcp" | "expedicao" | "catalogo" | "chat" | "notificacoes" | "configuracoes";
type Area = { id: AreaId; icon: string; label: string; eyebrow: string; title: string; description: string; source: string; cards: string[]; };

const areas: Area[] = [
  { id: "orquestrador", icon: "◈", label: "Orquestrador", eyebrow: "ELO · Orquestração", title: "Orquestrador de decisões", description: "Coordena intenção, evidência, política e encaminhamento entre as áreas.", source: "Missões do ELO Cognitivo", cards: ["Missões", "Decisões", "Aprendizado"] },
  { id: "dashboard", icon: "▦", label: "Dashboard", eyebrow: "ELO · Comercial", title: "Dashboard Comercial", description: "Visão de solicitações, propostas e riscos quando houver fonte operacional conectada.", source: "Solicitações e propostas", cards: ["Solicitações", "Propostas", "Riscos"] },
  { id: "comercial", icon: "◉", label: "Comercial", eyebrow: "ELO · Comercial", title: "Comercial", description: "Solicitações, demanda sazonal e movimentação de clientes.", source: "Dados comerciais autorizados", cards: ["Solicitações", "Demanda", "Clientes"] },
  { id: "almoxarifado", icon: "□", label: "Almoxarifado", eyebrow: "ELO · Operação", title: "Almoxarifado", description: "Estoque, separação e pedidos de material com saldo rastreável.", source: "Lotes e movimentações", cards: ["Estoque", "Reservas", "Alertas"] },
  { id: "compras", icon: "⌁", label: "Compras", eyebrow: "ELO · Suprimentos", title: "Compras", description: "Cotações, fornecedores, lead time e pedidos de compra.", source: "Cotações e ordens de compra", cards: ["Cotações", "Pedidos", "Fornecedores"] },
  { id: "producao", icon: "▤", label: "Produção", eyebrow: "ELO · Produção", title: "Produção", description: "Ordens de fabricação, etapas do fluxo e inspeções.", source: "OFs e eventos de produção", cards: ["Ordens", "Etapas", "Inspeções"] },
  { id: "pcp", icon: "▧", label: "Planejamento/PCP", eyebrow: "ELO · Planejamento/PCP", title: "Planejamento/PCP", description: "O Orçamento é setor interno: solicitações, Checklist ELO, composição documentada e revisão.", source: "SO, catálogo e diretrizes", cards: ["Solicitações", "Checklist", "Orçamento"] },
  { id: "expedicao", icon: "↗", label: "Expedição", eyebrow: "ELO · Operação", title: "Expedição", description: "Programação de expedição, quarentena, retorno de ativos e campo.", source: "Expedições e devoluções", cards: ["Expedições", "Quarentena", "Retornos"] },
  { id: "catalogo", icon: "▥", label: "Catálogo", eyebrow: "ELO · Conhecimento técnico", title: "Catálogo", description: "Taxonomia, modelos, lista-mãe, BOM e diretório técnico.", source: "Taxonomia e Lista-Mãe", cards: ["Taxonomia", "Modelos", "Composição"] },
  { id: "chat", icon: "◌", label: "Chat", eyebrow: "ELO · Comunicação", title: "Chat da equipe", description: "Comunicação setorial com rastreabilidade e sem envio externo implícito.", source: "Canal autorizado", cards: ["Conversas", "Menções", "Registros"] },
  { id: "notificacoes", icon: "!", label: "Notificações", eyebrow: "ELO · Governança", title: "Notificações", description: "Pendências, evidência, autorização e resultado provenientes de eventos rastreáveis.", source: "Eventos de governança", cards: ["Pendências", "Autorizações", "Eventos"] },
  { id: "configuracoes", icon: "⚙", label: "Configurações", eyebrow: "ELO · Administração", title: "Configurações", description: "Diretrizes, escopos, integrações e limites do workspace.", source: "Perfis e políticas", cards: ["Diretrizes", "Acessos", "Integrações"] }
];

const checklist = ["Modelo e escopo", "Materiais e adaptações", "Elétrica", "Água, esgoto e drenagem", "Implantação e logística", "Acessibilidade e uso", "Padrão × excedente", "Riscos e responsabilidades", "Alternativas e lacunas"];

function StateCard({ label }: { label: string }) {
  return <article className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-4 shadow-sm"><p className="text-xs text-slate-500">{label}</p><strong className="mt-3 block text-base">Sem dado conectado</strong><p className="mt-2 text-xs leading-5 text-slate-500">Aguardando fonte canônica e permissão de acesso.</p></article>;
}

type Subtab = { title: string; columns: string[]; action?: string };
const moduleTabs: Partial<Record<AreaId, Subtab[]>> = {
  orquestrador: [
    { title: "Agentes por setor", columns: ["Agente", "Setor", "Última orientação", "Estado"] },
    { title: "Recomendações ativas", columns: ["Prioridade", "Recomendação", "Fonte", "Impacto", "Revisão"] },
    { title: "Governança e KPIs", columns: ["Indicador", "Fonte", "Período", "Estado"] },
  ],
  dashboard: [
    { title: "Capacidade por modelo", columns: ["Modelo", "Estoque livre", "Em produção", "Em reparo", "OF estoque", "Disponível", "Prazo", "Risco"] },
    { title: "Disponibilidade × demanda", columns: ["Modelo", "Disponibilidade", "Demanda", "Cobertura", "Fonte"] },
    { title: "Demanda sazonal", columns: ["Mês", "Quantidade", "Modelos", "Fonte"] },
  ],
  comercial: [
    { title: "Solicitações", columns: ["SO", "Cliente", "Família", "Modelo", "Quantidade", "Status", "Prioridade", "Necessidade", "Ações"], action: "Nova solicitação" },
    { title: "Demanda sazonal", columns: ["Mês", "Quantidade", "Modelos mais solicitados", "Fonte"], action: "Editar demanda" },
    { title: "Movimentação de clientes", columns: ["Cliente", "Modelo", "Quantidade", "Fornecimento", "Devolução"], action: "Nova movimentação" },
  ],
  almoxarifado: [
    { title: "Estoque", columns: ["Família", "Modelo", "Quantidade", "Status", "Origem", "Ações"], action: "Novo item" },
    { title: "Pedidos de material", columns: ["Pedido", "Solicitante", "Material", "Quantidade", "Status", "Prioridade", "Projeto/OF"], action: "Novo pedido" },
  ],
  compras: [
    { title: "Pedidos de compra", columns: ["Pedido", "Fornecedor", "Descrição", "Quantidade", "Lead time", "Status", "AF/Projeto"], action: "Novo pedido" },
  ],
  producao: [
    { title: "Oficinas", columns: ["Etapa", "OF/AF", "Cliente", "Modelo", "Quantidade", "Estado"] },
    { title: "Ordens em produção", columns: ["Referência", "Cliente", "Modelo", "Status", "Etapa", "Ações"], action: "Nova OF" },
    { title: "Serviços externos", columns: ["Título", "AF", "Status", "Fornecedor", "Saída", "Retorno"], action: "Novo serviço" },
  ],
  expedicao: [
    { title: "Expedições", columns: ["AF", "Cliente", "Modelo", "Quantidade", "Status", "Quarentena", "Retorno", "Disponível"], action: "Nova expedição" },
  ],
  catalogo: [
    { title: "Taxonomia", columns: ["Modelo", "Família", "Tamanho", "Área", "Uso", "Capacidade", "Dificuldade", "Acessibilidade"] },
    { title: "Lista Mãe", columns: ["COD_ITEM", "Descrição", "Aplicação", "Unidade", "Valor", "Curva", "Modelos"], action: "Novo item" },
    { title: "BOM", columns: ["Código", "Descrição", "Unidade", "Quantidade", "Valor unitário", "Valor total", "Centro de custo"], action: "Novo item" },
    { title: "Diretório", columns: ["Documento", "Tipo", "Origem", "Versão", "Acesso"] },
  ],
  chat: [{ title: "Conversas", columns: ["Remetente", "Setor", "Destinatário", "Mensagem", "Data"], action: "Nova mensagem" }],
  notificacoes: [{ title: "Alertas", columns: ["Data", "Prioridade", "Setor", "Mensagem", "Fonte", "Leitura"] }],
  configuracoes: [
    { title: "Integrações", columns: ["Serviço", "Fonte", "Escopo", "Estado"] },
    { title: "Usuários e setores", columns: ["Usuário", "Setor", "Permissão", "Origem"] },
    { title: "Backup e logs", columns: ["Recurso", "Escopo", "Política", "Disponibilidade"] },
  ],
};

function GenericArea({ area, onOpenPCP, onMission }: { area: Area; onOpenPCP: () => void; onMission: (text: string) => void }) {
  const tabs = moduleTabs[area.id] ?? [];
  const [selected, setSelected] = useState(0);
  const [query, setQuery] = useState("");
  const [notice, setNotice] = useState("");
  const active = tabs[Math.min(selected, tabs.length - 1)];
  return <div className="space-y-5">
    <section className="elo-panel p-5 md:p-6">
      <div className="flex flex-wrap items-start justify-between gap-3"><div><p className="text-xs font-bold uppercase tracking-[.18em] text-violet-300">{area.eyebrow}</p><h2 className="mt-2 text-2xl font-semibold">{area.title}</h2><p className="mt-2 text-sm text-white/60">{area.description}</p></div><span className="elo-badge">Fonte: {area.source}</span></div>
      <div className="mt-5 flex gap-2 overflow-x-auto pb-2" role="tablist" aria-label={area.title}>{tabs.map((tab, index) => <button key={tab.title} type="button" role="tab" aria-selected={selected === index} onClick={() => { setSelected(index); setQuery(""); setNotice(""); }} className={`elo-subtab ${selected === index ? "active" : ""}`}>{tab.title}</button>)}</div>
    </section>
    {active && <section className="elo-panel p-5" role="tabpanel">
      <div className="flex flex-wrap items-center justify-between gap-3"><div><h3 className="font-semibold">{active.title}</h3><p className="mt-1 text-xs text-white/45">Sem registros operacionais autorizados nesta tela.</p></div><div className="flex flex-wrap gap-2">{active.action && <button type="button" onClick={() => setNotice(`${active.action}: requer fonte, política de acesso e formulário governado antes de salvar.`)} className="elo-button">＋ {active.action}</button>}{area.id === "orquestrador" && <button type="button" onClick={() => onMission("Analisar evidências e gargalos disponíveis, explicitando lacunas e sem executar ações externas.")} className="elo-button">🔍 Analisar gargalos</button>}</div></div>
      {notice && <p className="mt-3 rounded-lg border border-amber-400/30 bg-amber-400/10 p-3 text-sm text-amber-200" role="status">{notice}</p>}
      <label className="mt-4 block max-w-sm text-xs text-white/50">Filtrar registros<input value={query} onChange={e => setQuery(e.target.value)} placeholder="Buscar por código, cliente ou status" className="elo-input mt-2" /></label>
      <div className="mt-4 overflow-x-auto rounded-xl border border-white/10"><table className="elo-table"><thead><tr>{active.columns.map(column => <th key={column}>{column}</th>)}</tr></thead><tbody><tr><td colSpan={active.columns.length} className="text-center text-white/45">Nenhum registro vinculado. A busca “{query || "todos"}” não gera dados fictícios.</td></tr></tbody></table></div>
      <p className="mt-4 text-xs text-white/45">Os botões mostram o fluxo previsto; escritas, importações e sincronizações permanecem bloqueadas até a integração canônica e a revisão do analista.</p>
    </section>}
    {area.id === "pcp" && <button type="button" onClick={onOpenPCP} className="elo-button">Abrir Planejamento/PCP</button>}
  </div>;
}

type Stage = "solicitacao" | "checklist" | "orcamento" | "revisao";
type Criterion = { status: "" | "padrao" | "excedente" | "risco" | "na"; evidence: string };
type BudgetLine = { id: string; description: string; quantity: string; unit: string; price: string; source: string; date: string };
const initialCriterion = (): Criterion => ({ status: "", evidence: "" });
const emptyLine = (): BudgetLine => ({ id: crypto.randomUUID(), description: "", quantity: "", unit: "", price: "", source: "", date: "" });
const money = (value: number) => value.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

function PCPWorkspace({ onMission }: { onMission: (text: string) => void }) {
  const [stage, setStage] = useState<Stage>("solicitacao");
  const [so, setSO] = useState("");
  const [analyst, setAnalyst] = useState("");
  const [source, setSource] = useState("");
  const [model, setModel] = useState("");
  const [criteria, setCriteria] = useState<Record<string, Criterion>>({});
  const [budget, setBudget] = useState<Record<string, BudgetLine[]>>({ base: [], excedentes: [], maoObra: [] });
  const [notice, setNotice] = useState("");
  const validSO = /^\\d{3}\\.\\d{2}$/.test(so.trim());
  const readyForChecklist = validSO && analyst.trim().length > 0 && source.trim().length > 0;
  const complete = checklist.every(item => { const row = criteria[item]; return row?.status && row.evidence.trim(); });
  const canBudget = readyForChecklist && complete && model.trim().length > 0;
  const groups = [
    { id: "base", label: "Modelo base" },
    { id: "excedentes", label: "Excedentes individualizados" },
    { id: "maoObra", label: "Mão de obra separada" },
  ];
  const rows = Object.values(budget).flat();
  const validLine = (line: BudgetLine) => line.description.trim() && line.source.trim() && line.date && Number(line.quantity) > 0 && Number(line.price) >= 0 && line.price !== "" && line.unit.trim();
  const amountsReady = budget.base.length > 0 && rows.every(validLine);
  const subtotal = (group: string) => (budget[group] ?? []).reduce((sum, line) => sum + (validLine(line) ? Number(line.quantity) * Number(line.price) : 0), 0);
  function go(next: Stage) {
    setNotice("");
    if (next !== "solicitacao" && !readyForChecklist) { setStage("solicitacao"); setNotice("Informe SO, analista e fonte antes de abrir o Checklist ELO."); return; }
    if ((next === "orcamento" || next === "revisao") && !canBudget) { setStage("checklist"); setNotice("Registre o modelo e a situação com evidência em todos os critérios antes do Orçamento."); return; }
    setStage(next);
  }
  function updateLine(group: string, id: string, key: keyof BudgetLine, value: string) {
    setBudget(previous => ({ ...previous, [group]: (previous[group] ?? []).map(line => line.id === id ? { ...line, [key]: value } : line) }));
  }
  function addLine(group: string) { setBudget(previous => ({ ...previous, [group]: [...(previous[group] ?? []), emptyLine()] })); }
  function removeLine(group: string, id: string) { setBudget(previous => ({ ...previous, [group]: (previous[group] ?? []).filter(line => line.id !== id) })); }
  return <div className="space-y-5">
    <section className="elo-panel p-5 md:p-6"><p className="text-xs font-bold uppercase tracking-[.18em] text-violet-300">ELO · Planejamento/PCP</p><h2 className="mt-2 text-2xl font-semibold">Solicitação → Checklist ELO → Orçamento → Revisão</h2><p className="mt-2 text-sm text-white/60">Orçamento é um setor dentro de Planejamento/PCP. O analista informa a numeração SO 000.AA; nenhuma ação externa é automática.</p><div className="mt-5 flex gap-2 overflow-x-auto">{(["solicitacao","checklist","orcamento","revisao"] as Stage[]).map((item,index) => <button type="button" key={item} onClick={() => go(item)} className={`elo-subtab ${stage === item ? "active" : ""}`}>{index+1}. {item === "solicitacao" ? "Solicitação" : item === "checklist" ? "Checklist ELO" : item === "orcamento" ? "Orçamento" : "Revisão"}</button>)}</div></section>
    {notice && <div role="alert" className="rounded-lg border border-amber-400/30 bg-amber-400/10 p-3 text-sm text-amber-200">{notice}</div>}
    {stage === "solicitacao" && <section className="elo-panel p-5"><h3 className="font-semibold">Identificação e fonte da SO</h3><p className="mt-1 text-sm text-white/50">Sem identificador presumido e sem quantidade padrão.</p><div className="mt-4 grid gap-4 md:grid-cols-2">
      <label className="text-sm">Número da SO <input value={so} onChange={e=>setSO(e.target.value)} placeholder="000.AA" aria-invalid={so.length>0&&!validSO} className="elo-input mt-2 font-mono" /></label>
      <label className="text-sm">Analista de Orçamento <input value={analyst} onChange={e=>setAnalyst(e.target.value)} placeholder="Responsável pela numeração" className="elo-input mt-2" /></label>
      <label className="text-sm md:col-span-2">Documento, trecho ou informação explícita de origem <textarea value={source} onChange={e=>setSource(e.target.value)} placeholder="Identifique a fonte e os quantitativos declarados, se houver." className="elo-input mt-2 min-h-24" /></label>
    </div><button type="button" disabled={!readyForChecklist} onClick={()=>go("checklist")} className="elo-button mt-5 disabled:opacity-40">Abrir Checklist ELO →</button></section>}
    {stage === "checklist" && <section className="elo-panel p-5"><h3 className="font-semibold">Checklist ELO · antes do Orçamento</h3><p className="mt-1 text-sm text-white/50">Critérios técnicos, enquadramento do modelo, padrão versus excedente, riscos e regras aplicadas.</p><label className="mt-4 block text-sm">Enquadramento do modelo <input value={model} onChange={e=>setModel(e.target.value)} placeholder="Modelo identificado na fonte; não presumir M01" className="elo-input mt-2" /></label><div className="mt-4 overflow-x-auto"><table className="elo-table"><thead><tr><th>Critério</th><th>Classificação</th><th>Evidência / regra / risco</th></tr></thead><tbody>{checklist.map(item => { const row = criteria[item] ?? initialCriterion(); return <tr key={item}><td className="font-semibold">{item}</td><td><select value={row.status} onChange={e=>setCriteria(previous=>({...previous,[item]:{...row,status:e.target.value as Criterion["status"]}}))} className="elo-input min-w-40"><option value="">A revisar</option><option value="padrao">Padrão</option><option value="excedente">Excedente</option><option value="risco">Risco / pendência</option><option value="na">Não se aplica</option></select></td><td><input value={row.evidence} onChange={e=>setCriteria(previous=>({...previous,[item]:{...row,evidence:e.target.value}}))} placeholder="Fonte ou justificativa, inclusive para N/A" className="elo-input min-w-64" /></td></tr>; })}</tbody></table></div><div className="mt-5 flex flex-wrap gap-2"><button type="button" onClick={()=>go("solicitacao")} className="elo-subtab">← Dados da SO</button><button type="button" disabled={!canBudget} onClick={()=>go("orcamento")} className="elo-button disabled:opacity-40">Abrir Orçamento →</button></div></section>}
    {stage === "orcamento" && <section className="elo-panel p-5"><h3 className="font-semibold">Composição do Orçamento</h3><p className="mt-1 text-sm text-white/50">Modelo base + excedentes + mão de obra, subtotais e total geral. Sem BDI. Quantidades, preços, fonte e data vêm do analista.</p>{groups.map(group => <div key={group.id} className="mt-5 rounded-xl border border-white/10 p-4"><div className="flex items-center justify-between gap-2"><h4 className="font-semibold">{group.label}</h4><button type="button" onClick={()=>addLine(group.id)} className="elo-button">＋ Item</button></div>{(budget[group.id]??[]).length===0 && <p className="mt-3 text-sm text-white/40">Nenhum item informado.</p>}{(budget[group.id]??[]).map(line=><div key={line.id} className="mt-3 grid gap-2 rounded-lg border border-white/10 p-3 md:grid-cols-6"><input aria-label="Descrição" value={line.description} onChange={e=>updateLine(group.id,line.id,"description",e.target.value)} placeholder="Descrição" className="elo-input md:col-span-2" /><input aria-label="Quantidade" type="number" min="0.001" step="any" value={line.quantity} onChange={e=>updateLine(group.id,line.id,"quantity",e.target.value)} placeholder="Qtd" className="elo-input" /><input aria-label="Unidade" value={line.unit} onChange={e=>updateLine(group.id,line.id,"unit",e.target.value)} placeholder="Un." className="elo-input" /><input aria-label="Preço unitário" type="number" min="0" step="0.01" value={line.price} onChange={e=>updateLine(group.id,line.id,"price",e.target.value)} placeholder="Preço unit." className="elo-input" /><input aria-label="Data da cotação" type="date" value={line.date} onChange={e=>updateLine(group.id,line.id,"date",e.target.value)} className="elo-input" /><input aria-label="Fonte" value={line.source} onChange={e=>updateLine(group.id,line.id,"source",e.target.value)} placeholder="Fonte / cotação" className="elo-input md:col-span-5" /><button type="button" onClick={()=>removeLine(group.id,line.id)} className="elo-subtab">Remover</button></div>)}<p className="mt-3 text-right text-sm">Subtotal: {money(subtotal(group.id))}</p></div>)}<div className="mt-5 text-right text-lg font-semibold">Total geral: {money(groups.reduce((sum,group)=>sum+subtotal(group.id),0))}</div><div className="mt-5 flex gap-2"><button type="button" onClick={()=>go("checklist")} className="elo-subtab">← Checklist</button><button type="button" onClick={()=>go("revisao")} className="elo-button">Conferir resultado →</button></div></section>}
    {stage === "revisao" && <section className="elo-panel p-5"><h3 className="font-semibold">Revisão do analista · SO {so}</h3><p className="mt-2 text-sm text-white/60">Analista: {analyst} · Modelo: {model}</p><p className="mt-2 whitespace-pre-wrap text-sm text-white/60">Fonte: {source}</p><p className="mt-3 text-sm text-white/60">Checklist: {checklist.filter(item=>criteria[item]?.status&&criteria[item]?.evidence.trim()).length}/{checklist.length} critérios documentados.</p><div className="mt-4 rounded-xl border border-white/10 p-4">{groups.map(group=><p key={group.id} className="flex justify-between text-sm"><span>{group.label} ({budget[group.id]?.length??0} itens)</span><span>{money(subtotal(group.id))}</span></p>)}<p className="mt-3 flex justify-between border-t border-white/10 pt-3 font-semibold"><span>Total geral</span><span>{money(groups.reduce((sum,group)=>sum+subtotal(group.id),0))}</span></p></div>{!amountsReady && <p className="mt-3 rounded-lg border border-amber-400/30 bg-amber-400/10 p-3 text-sm text-amber-200">Orçamento incompleto: informe ao menos um item de modelo base e preencha fonte, data, unidade, quantidade e preço de cada item. O total parcial não é um orçamento aprovado.</p>}<div className="mt-5 flex flex-wrap gap-2"><button type="button" onClick={()=>go("solicitacao")} className="elo-subtab">Editar dados</button><button type="button" onClick={()=>go("orcamento")} className="elo-subtab">Editar orçamento</button><button type="button" onClick={()=>onMission(`Revisar SO ${so}, modelo ${model}. Fonte: ${source}. Checklist: ${JSON.stringify(criteria)}. Itens informados: ${JSON.stringify(budget)}. Indicar lacunas e riscos, sem executar ou publicar orçamento.`)} className="elo-button">Consultar ELO para revisão</button></div><p className="mt-3 text-xs text-white/45">Esta consulta envia os dados preenchidos ao ELO Cognitivo. Nenhuma ordem, compra, mensagem ou publicação é disparada por esta tela.</p></section>}
  </div>;
}

function CognitiveResult({ result }: { result: CognitiveResponse }) {
  return <section className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm"><div className="flex flex-wrap items-start justify-between gap-3"><div><h3 className="font-semibold">Resultado da missão</h3><p className="mt-1 text-xs text-slate-500">request {result.request_id.slice(0, 8)} · {Math.round(result.confidence * 100)}% de confiança</p></div><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{result.provenance.validation_status ?? "processada"}</span></div><div className="mt-4 space-y-3 text-sm">{Object.entries(result.response).map(([key, value]) => <div key={key}><p className="text-xs font-bold uppercase tracking-wide text-slate-500">{key}</p><p className="mt-1 whitespace-pre-wrap leading-6">{typeof value === "string" ? value : JSON.stringify(value, null, 2)}</p></div>)}</div></section>;
}

export function EloDashboard({ onSignOut, accessToken }: Props) {
  const [areaId, setAreaId] = useState<AreaId>("pcp");
  const [mission, setMission] = useState("");
  const [notice, setNotice] = useState<string | null>(null);
  const [result, setResult] = useState<CognitiveResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const area = useMemo(() => areas.find((item) => item.id === areaId) ?? areas[0], [areaId]);

  async function runMission(text: string) {
    const message = text.trim();
    if (!message || busy) return;
    setBusy(true); setNotice(null); setResult(null);
    try {
      const response = await fetch("/api/cognitive", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: `Bearer ${accessToken}` }, cache: "no-store", body: JSON.stringify({ message, tenant_id: process.env.NEXT_PUBLIC_ELO_TENANT_ID?.trim() || "multiteiner", domain: area.id, context: { area: area.label, surface: "operational-workspace", source: "elo-web" } }) });
      const payload = await response.json().catch(() => null);
      if (!response.ok) throw new Error(typeof payload?.message === "string" ? payload.message : "Não foi possível processar a missão pelo ELO Cognitivo.");
      setResult(payload as CognitiveResponse);
      setNotice("Missão processada pelo ELO Cognitivo. Execução externa permanece atrás do boundary governado.");
      setMission("");
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Não foi possível processar a missão.");
    } finally { setBusy(false); }
  }

  return <main className="min-h-screen bg-[var(--elo-bg)] text-[var(--elo-ink)]"><div className="min-h-screen lg:grid lg:grid-cols-[244px_minmax(0,1fr)]">
    <aside className="bg-[var(--elo-sidebar)] p-5 text-white lg:min-h-screen"><div className="flex items-center gap-3 px-2"><div className="grid size-10 place-items-center rounded-xl border border-white/30 font-bold text-teal-200">E</div><div><p className="text-xl font-semibold tracking-wide">ELO</p><p className="text-[10px] uppercase tracking-[.22em] text-white/50">Multiteiner</p></div></div><div className="mt-9 px-2 text-xs uppercase tracking-[.14em] text-white/45">Planejamento/PCP</div><p className="mt-2 px-2 text-xs text-white/60">Orçamento é setor interno</p><button type="button" onClick={() => setAreaId("pcp")} className={`mt-4 w-full rounded-xl px-4 py-3 text-left text-sm font-semibold ${areaId === "pcp" ? "bg-white/15 text-white" : "text-white/70 hover:bg-white/10"}`}>▧ Fluxo de solicitações</button><div className="mt-8 border-t border-white/10 pt-5"><p className="mb-2 px-2 text-xs uppercase tracking-[.14em] text-white/45">Acesso</p><p className="px-2 text-sm text-white/75">Sessão ELO autorizada</p><button type="button" onClick={onSignOut} className="mt-5 w-full rounded-xl border border-white/15 px-4 py-3 text-left text-sm font-semibold text-white/85 hover:bg-white/10">Encerrar sessão</button></div></aside>
    <section className="min-w-0"><header className="border-b border-slate-200 bg-[var(--elo-panel)] px-5 py-4 lg:px-8"><div className="flex flex-wrap items-center justify-between gap-4"><div><p className="text-xs text-slate-500">ELO / Workspace operacional</p><h1 className="text-2xl font-semibold tracking-tight">{area.label}</h1></div><span className="rounded-full border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600">Cognitivo ativo</span></div><nav className="mt-4 flex gap-2 overflow-x-auto pb-1" aria-label="Áreas do workspace">{areas.map((item) => <button key={item.id} type="button" onClick={() => { setAreaId(item.id); setNotice(null); setResult(null); }} aria-current={item.id === areaId ? "page" : undefined} className={`shrink-0 rounded-lg border px-3 py-2 text-xs font-semibold transition ${item.id === areaId ? "border-teal-700 bg-teal-700 text-white" : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50"}`}><span className="mr-1.5">{item.icon}</span>{item.label}</button>)}</nav></header>
      <div className="space-y-5 p-5 lg:p-8">{notice && <div role="status" className="rounded-xl border border-slate-200 bg-[var(--elo-panel)] px-4 py-3 text-sm text-slate-700">{notice}</div>}
        {areaId === "pcp" ? <PCPWorkspace onMission={runMission} /> : <GenericArea key={areaId} area={area} onOpenPCP={() => setAreaId("pcp")} onMission={runMission} />}
        <section className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm"><div className="flex flex-wrap items-start justify-between gap-4"><div><h3 className="font-semibold">Missão ELO</h3><p className="mt-1 text-sm text-slate-500">Consulta ao ELO Cognitivo no contexto da área aberta.</p></div><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{busy ? "Processando" : "Pronto"}</span></div><div className="mt-4 flex gap-2 rounded-xl border border-slate-200 bg-slate-50 p-2"><input value={mission} onChange={(event) => setMission(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter") void runMission(mission); }} placeholder={`Solicite uma análise para ${area.label.toLowerCase()}…`} disabled={busy} className="min-w-0 flex-1 bg-transparent px-2 text-sm outline-none" /><button type="button" onClick={() => void runMission(mission)} disabled={busy} className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50">Enviar</button></div></section>
        {result && <CognitiveResult result={result} />}
      </div></section></div></main>;
}
