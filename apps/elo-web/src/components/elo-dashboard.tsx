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

type DraftRecord = { id: string; values: Record<string,string>; source: string; updated: string };
type DraftStore = Record<string,DraftRecord[]>;
const tabKey = (area: AreaId, index: number) => `${area}:${index}`;
const editableColumns = (tab: Subtab) => tab.columns.filter(column => !["Ações","Fonte","Revisão"].includes(column));
const workflowStages = ["preparacao","corte","solda","montagem_padrao","montagem_customizada","acabamento","inspecao","reparo","pronto"];
function DraftSignals({ drafts }: { drafts: DraftStore }) {
  const commercial = drafts[tabKey("comercial",0)] ?? [];
  const stock = drafts[tabKey("almoxarifado",0)] ?? [];
  const production = drafts[tabKey("producao",1)] ?? [];
  const alerts = [
    ...commercial.filter(row => row.values.Status === "APROVADO").map(row => `Solicitação ${row.values.SO || "sem SO"} aprovada em rascunho: revisar Projeto e OF; nada foi criado.`),
    ...stock.filter(row => row.values.Quantidade === "0").map(row => `Estoque zero informado para ${row.values.Modelo || row.values.Família || "item sem identificação"}; confirmar saldo na fonte.`),
    ...production.filter(row => row.values.Etapa === "pronto").map(row => `Ordem ${row.values.Referência || "sem referência"} na etapa pronto: revisar inspeção antes de concluir.`),
  ];
  return alerts.length ? <div className="elo-panel p-4"><h3 className="font-semibold">Sinais para revisão</h3><ul className="mt-2 space-y-2 text-sm text-amber-200">{alerts.map((alert,index)=><li key={index}>• {alert}</li>)}</ul><p className="mt-2 text-xs text-white/45">Derivado somente dos rascunhos desta sessão; não é alerta canônico nem acionamento automático.</p></div> : null;
}
function GenericArea({ area, onMission, drafts, onSave, onDelete }: { area: Area; onMission: (text: string) => void; drafts: DraftStore; onSave: (key: string,record: DraftRecord) => void; onDelete: (key: string,id: string) => void }) {
  const tabs = moduleTabs[area.id] ?? [];
  const [selected,setSelected] = useState(0);
  const [query,setQuery] = useState("");
  const [editing,setEditing] = useState<DraftRecord | null>(null);
  const [reviewing,setReviewing] = useState(false);
  const [notice,setNotice] = useState("");
  const [kanbanTarget,setKanbanTarget] = useState<{id:string;stage:string}|null>(null);
  const [analysis,setAnalysis] = useState<string[]>([]);
  const active = tabs[Math.min(selected,tabs.length-1)];
  const key = tabKey(area.id,selected);
  const records = drafts[key] ?? [];
  const filtered = records.filter(row => !query || Object.values(row.values).some(value=>value.toLocaleLowerCase("pt-BR").includes(query.toLocaleLowerCase("pt-BR"))));
  const allDrafts = Object.values(drafts).flat();
  function startNew() {
    const columns = editableColumns(active);
    setEditing({id:crypto.randomUUID(),values:Object.fromEntries(columns.map(column=>[column,""])),source:"",updated:""});
    setReviewing(false);setNotice("");
  }
  function review() {
    if(!editing)return;
    const columns = editableColumns(active);
    if(!editing.source.trim() || !columns.some(column=>editing.values[column]?.trim())) { setNotice("Preencha ao menos um dado e identifique a fonte antes da revisão."); return; }
    const so=editing.values.SO?.trim();
    if(so && !/^\\d{3}\\.\\d{2}$/.test(so)){setNotice("Use SO 000.AA, informada pelo analista.");return;}
    const numeric=columns.filter(column=>/^(Qtd|Quantidade|Lead time|Prazo|Estoque livre|Disponível)$/.test(column));
    if(numeric.some(column=>editing.values[column] && (!Number.isFinite(Number(editing.values[column])) || Number(editing.values[column])<0))){setNotice("Quantidades e prazos informados devem ser números não negativos.");return;}
    setNotice("");setReviewing(true);
  }
  function commit() { if(!editing)return;onSave(key,{...editing,updated:new Date().toISOString()});setEditing(null);setReviewing(false);setNotice("Rascunho salvo somente nesta sessão. Nenhuma operação externa foi executada."); }
  function moveKanban() {
    if(!kanbanTarget)return;
    const record=records.find(row=>row.id===kanbanTarget.id);
    if(record)onSave(key,{...record,values:{...record.values,Etapa:kanbanTarget.stage},updated:new Date().toISOString()});
    setKanbanTarget(null);setNotice("Etapa movida no rascunho da sessão. Nenhuma OF foi alterada no banco.");
  }
  const total = allDrafts.length;
  return <div className="space-y-5">
    <section className="elo-panel p-5 md:p-6"><div className="flex flex-wrap items-start justify-between gap-3"><div><h2 className="text-2xl font-semibold">{area.title}</h2><p className="mt-2 text-sm text-white/60">{area.description}</p></div><span className="elo-badge">Rascunhos locais · {total} registro(s) na sessão</span></div><div className="mt-5 flex gap-2 overflow-x-auto pb-2" role="tablist" aria-label={area.title}>{tabs.map((tab,index)=><button key={tab.title} type="button" role="tab" aria-selected={selected===index} onClick={()=>{setSelected(index);setQuery("");setEditing(null);setReviewing(false);setNotice("");}} className={`elo-subtab ${selected===index?"active":""}`}>{tab.title}</button>)}</div></section>
    {area.id==="orquestrador" && <section className="elo-panel p-4"><div className="flex flex-wrap gap-2">{["Gerar insights","Analisar gargalos","Simular decisão"].map(label=><button key={label} type="button" onClick={()=>{
  const commercial=drafts[tabKey("comercial",0)]??[];
  const stock=drafts[tabKey("almoxarifado",0)]??[];
  const purchases=drafts[tabKey("compras",0)]??[];
  const production=drafts[tabKey("producao",1)]??[];
  const expedition=drafts[tabKey("expedicao",0)]??[];
  const lines:string[]=[];
  if(label==="Gerar insights"){
    commercial.filter(row=>row.values.Status==="APROVADO").forEach(row=>lines.push(`Comercial: ${row.values.SO||"SO não informada"} em rascunho aprovado; projeto/OF dependem de revisão e autorização.`));
    stock.filter(row=>row.values.Quantidade==="0").forEach(row=>lines.push(`Almoxarifado: saldo zero informado para ${row.values.Modelo||row.values.Família||"item"}; confirmar no registro de estoque.`));
    expedition.filter(row=>row.values.Status==="QUARENTENA").forEach(row=>lines.push(`Expedição: ${row.values.AF||"AF não informada"} em quarentena informada; disponibilidade não presumida.`));
  }else if(label==="Analisar gargalos"){
    purchases.filter(row=>row.values.Status==="PENDENTE").forEach(row=>lines.push(`Compras: ${row.values.Pedido||"pedido"} pendente; lead time ${row.values["Lead time"]||"não informado"}; não há prazo de entrega comprovado.`));
    production.filter(row=>row.values.Etapa && row.values.Etapa!=="pronto").forEach(row=>lines.push(`Produção: ${row.values.Referência||"ordem"} na etapa ${row.values.Etapa}; capacidade não comprovada.`));
  }else{
    lines.push(`Comercial: ${commercial.length} rascunho(s) para qualificação de demanda.`);
    lines.push(`PCP: avaliar capacidade e checklist antes de converter demanda; ${production.length} ordem(ns) em rascunho.`);
    lines.push(`Compras e Almoxarifado: ${purchases.length} pedido(s) e ${stock.length} saldo(s) informados; cobertura não calculável sem vínculos e fonte validada.`);
    lines.push(`Produção e Expedição: ${production.length} ordem(ns) e ${expedition.length} expedição(ões) em rascunho; nenhum acionamento ocorreu.`);
  }
  setAnalysis(lines.length?lines:["Nenhum dado suficiente nesta sessão para afirmar um insight ou gargalo. Informe registros e fontes nos setores."]);
  setNotice(`${label}: prévia local baseada apenas nos registros informados; nenhum agente, compra ou OF foi acionado.`);
}} className="elo-button">{label}</button>)}</div>{analysis.length>0&&<div className="mt-4 space-y-2 text-sm" role="status">{analysis.map((line,index)=><p key={index} className="rounded-lg bg-white/5 p-3">{line}</p>)}</div>}</section>}
    {area.id==="dashboard" && <div className="grid gap-3 sm:grid-cols-3">{[
      ["Solicitações em rascunho",(drafts[tabKey("comercial",0)]??[]).length],
      ["Ordens em rascunho",(drafts[tabKey("producao",1)]??[]).length],
      ["Compras em rascunho",(drafts[tabKey("compras",0)]??[]).length],
    ].map(([label,value])=><div key={label} className="elo-panel p-4"><p className="text-xs text-white/50">{label}</p><strong className="mt-2 block text-2xl">{value}</strong><p className="mt-1 text-xs text-white/40">Apenas nesta sessão; não é KPI operacional.</p></div>)}</div>}
    {area.id==="dashboard" && (()=>{const stock=drafts[tabKey("almoxarifado",0)]??[];const production=drafts[tabKey("producao",1)]??[];const commercial=drafts[tabKey("comercial",0)]??[];const models=[...new Set([...stock.map(row=>row.values.Modelo),...production.map(row=>row.values.Modelo),...commercial.map(row=>row.values.Modelo)].filter(Boolean))];return <section className="elo-panel p-5"><h3 className="font-semibold">Capacidade informada por modelo · rascunhos</h3><p className="mt-1 text-xs text-white/45">Estoque, produção e solicitações são apresentados separadamente. Disponibilidade e prazo não são inferidos sem vínculo, status e fonte canônicos.</p><div className="mt-4 overflow-x-auto"><table className="elo-table"><thead><tr><th>Modelo</th><th>Estoque informado</th><th>Ordens em rascunho</th><th>Solicitações em rascunho</th><th>Cobertura / risco</th></tr></thead><tbody>{models.length===0?<tr><td colSpan={5} className="text-center text-white/45">Sem dados informados. Gráficos e indicadores aguardam evidência.</td></tr>:models.map(model=><tr key={model}><td>{model}</td><td>{stock.filter(row=>row.values.Modelo===model).reduce((sum,row)=>sum+(Number(row.values.Quantidade)||0),0)}</td><td>{production.filter(row=>row.values.Modelo===model).length}</td><td>{commercial.filter(row=>row.values.Modelo===model).length}</td><td>Não calculável sem demanda e disponibilidade comprovadas</td></tr>)}</tbody></table></div></section>})()}
    <DraftSignals drafts={drafts}/>
    {notice&&<p role="status" className="rounded-lg border border-amber-400/30 bg-amber-400/10 p-3 text-sm text-amber-200">{notice}</p>}
    {active && <section className="elo-panel p-5" role="tabpanel"><div className="flex flex-wrap items-center justify-between gap-3"><div><h3 className="font-semibold">{active.title}</h3><p className="mt-1 text-xs text-white/45">{records.length} registro(s) informados nesta sessão · Fonte canônica: {area.source}</p></div><div className="flex flex-wrap gap-2">{active.action&&<button type="button" onClick={startNew} className="elo-button">＋ {active.action}</button>}{area.id==="orquestrador"&&<button type="button" onClick={()=>onMission("Analisar lacunas e evidências disponíveis sem acionar agentes ou executar decisões.")} className="elo-button">Consultar ELO</button>}</div></div>
      {area.id==="producao" && selected===1 && <div className="mt-4 flex gap-2 overflow-x-auto pb-2">{workflowStages.map(stage=><div key={stage} className="min-w-32 rounded-lg border border-white/10 p-2"><strong className="text-xs">{stage.replaceAll("_"," ")}</strong><p className="mt-1 text-xs text-white/40">{records.filter(row=>row.values.Etapa===stage).length} rascunho(s)</p>{records.filter(row=>row.values.Etapa===stage).map(row=><button key={row.id} type="button" onClick={()=>setKanbanTarget({id:row.id,stage})} className="mt-2 block w-full rounded-md bg-white/5 p-2 text-left text-xs">{row.values.Referência||"Sem referência"}</button>)}</div>)}</div>}
      {kanbanTarget && <div className="mt-3 rounded-lg border border-violet-400/30 p-3 text-sm"><p>Alterar etapa apenas no rascunho:</p><select value={kanbanTarget.stage} onChange={e=>setKanbanTarget({...kanbanTarget,stage:e.target.value})} className="elo-input mt-2">{workflowStages.map(stage=><option key={stage} value={stage}>{stage.replaceAll("_"," ")}</option>)}</select><div className="mt-2 flex gap-2"><button type="button" onClick={moveKanban} className="elo-button">Confirmar movimento local</button><button type="button" onClick={()=>setKanbanTarget(null)} className="elo-subtab">Cancelar</button></div></div>}
      <label className="mt-4 block max-w-sm text-xs text-white/50">Filtrar registros<input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Buscar nesta tela" className="elo-input mt-2"/></label>
      <div className="mt-4 overflow-x-auto rounded-xl border border-white/10"><table className="elo-table"><thead><tr>{active.columns.map(column=><th key={column}>{column}</th>)}{active.action&&<th>Revisar</th>}</tr></thead><tbody>{filtered.length===0?<tr><td colSpan={active.columns.length+(active.action?1:0)} className="text-center text-white/45">Nenhum registro. Não há volume ou indicador canônico presumido.</td></tr>:filtered.map(row=><tr key={row.id}>{active.columns.map(column=><td key={column}>{column==="Fonte"?row.source:column==="Ações"?"—":row.values[column]||"—"}</td>)}{active.action&&<td><div className="flex gap-2"><button type="button" onClick={()=>{setEditing(row);setReviewing(false);}} className="elo-subtab">Editar</button><button type="button" onClick={()=>{if(window.confirm("Remover este rascunho desta sessão?"))onDelete(key,row.id);}} className="elo-subtab">Remover</button></div></td>}</tr>)}</tbody></table></div>
    </section>}
    {editing&&<section className="elo-panel p-5"><h3 className="font-semibold">{reviewing?"Revisar antes de salvar":"Preencher rascunho"} · {active.title}</h3><p className="mt-1 text-xs text-white/45">Este formulário não escreve no Supabase, não cria AF/OF e não envia mensagem.</p>{reviewing?<div className="mt-4 space-y-2 text-sm">{editableColumns(active).map(column=><p key={column}><strong>{column}:</strong> {editing.values[column]||"Não informado"}</p>)}<p><strong>Fonte:</strong> {editing.source}</p><div className="flex gap-2"><button type="button" onClick={commit} className="elo-button">Confirmar rascunho local</button><button type="button" onClick={()=>setReviewing(false)} className="elo-subtab">Corrigir</button></div></div>:<div className="mt-4 grid gap-3 sm:grid-cols-2">{editableColumns(active).map(column=><label key={column} className="text-xs text-white/70">{column}{column==="Status"||column==="Etapa"?<select value={editing.values[column]??""} onChange={e=>setEditing({...editing,values:{...editing.values,[column]:e.target.value}})} className="elo-input mt-1"><option value="">Selecione</option>{(column==="Etapa"?workflowStages:["PENDENTE","EM_ANDAMENTO","APROVADO","PRODUCAO","REPARO","CONCLUIDO","ENTREGUE","QUARENTENA"]).map(option=><option key={option} value={option}>{option}</option>)}</select>:<input value={editing.values[column]??""} onChange={e=>setEditing({...editing,values:{...editing.values,[column]:e.target.value}})} placeholder={column==="SO"?"000.AA":column} className="elo-input mt-1"/>}</label>)}<label className="text-xs text-white/70 sm:col-span-2">Fonte e evidência<input value={editing.source} onChange={e=>setEditing({...editing,source:e.target.value})} placeholder="Documento, responsável ou registro de origem" className="elo-input mt-1"/></label><div className="flex gap-2 sm:col-span-2"><button type="button" onClick={review} className="elo-button">Revisar dados</button><button type="button" onClick={()=>setEditing(null)} className="elo-subtab">Cancelar</button></div></div>}</section>}
    <p className="text-xs text-white/45">Rascunhos são temporários e desaparecem ao recarregar a página. Integrações e decisões externas exigem fonte canônica, permissão e confirmação separada.</p>
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
    {stage === "revisao" && <section className="elo-panel p-5"><h3 className="font-semibold">Revisão do analista · SO {so}</h3><p className="mt-2 text-sm text-white/60">Analista: {analyst} · Modelo: {model}</p><p className="mt-2 whitespace-pre-wrap text-sm text-white/60">Fonte: {source}</p><p className="mt-3 text-sm text-white/60">Checklist: {checklist.filter(item=>criteria[item]?.status&&criteria[item]?.evidence.trim()).length}/{checklist.length} critérios documentados.</p><div className="mt-4 rounded-xl border border-white/10 p-4">{groups.map(group=><p key={group.id} className="flex justify-between text-sm"><span>{group.label} ({budget[group.id]?.length??0} itens)</span><span>{money(subtotal(group.id))}</span></p>)}<p className="mt-3 flex justify-between border-t border-white/10 pt-3 font-semibold"><span>Total geral</span><span>{money(groups.reduce((sum,group)=>sum+subtotal(group.id),0))}</span></p>{groups.map(group=><div key={group.id} className="mt-4 border-t border-white/10 pt-3"><h4 className="text-sm font-semibold">{group.label}</h4>{(budget[group.id]??[]).length===0?<p className="text-xs text-white/40">Sem itens</p>:(budget[group.id]??[]).map(line=><p key={line.id} className="mt-1 text-xs text-white/60">{line.description||"Descrição pendente"} · {line.quantity||"Qtd pendente"} {line.unit} × {line.price!==""?money(Number(line.price)):"Preço pendente"} · Fonte: {line.source||"pendente"} · Cotação: {line.date||"pendente"}</p>)}</div>)}</div>{!amountsReady && <p className="mt-3 rounded-lg border border-amber-400/30 bg-amber-400/10 p-3 text-sm text-amber-200">Orçamento incompleto: informe ao menos um item de modelo base e preencha fonte, data, unidade, quantidade e preço de cada item. O total parcial não é um orçamento aprovado.</p>}<div className="mt-5 flex flex-wrap gap-2"><button type="button" onClick={()=>go("solicitacao")} className="elo-subtab">Editar dados</button><button type="button" onClick={()=>go("orcamento")} className="elo-subtab">Editar orçamento</button><button type="button" onClick={()=>onMission(`Revisar SO ${so}, modelo ${model}. Fonte: ${source}. Checklist: ${JSON.stringify(criteria)}. Itens informados: ${JSON.stringify(budget)}. Indicar lacunas e riscos, sem executar ou publicar orçamento.`)} className="elo-button">Consultar ELO para revisão</button></div><p className="mt-3 text-xs text-white/45">Esta consulta envia os dados preenchidos ao ELO Cognitivo. Nenhuma ordem, compra, mensagem ou publicação é disparada por esta tela.</p></section>}
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
  const [drafts,setDrafts] = useState<DraftStore>({});
  const saveDraft = (key: string,record: DraftRecord) => setDrafts(previous=>({...previous,[key]:[record,...(previous[key]??[]).filter(item=>item.id!==record.id)]}));
  const deleteDraft = (key: string,id: string) => setDrafts(previous=>({...previous,[key]:(previous[key]??[]).filter(item=>item.id!==id)}));
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

  return <main className="min-h-screen bg-[var(--elo-bg)] text-[var(--elo-ink)]">
    <header className="sticky top-0 z-20 flex h-14 items-center justify-between border-b border-white/10 bg-[#0a1628]/95 px-4 backdrop-blur-xl">
      <div className="flex items-center gap-3"><div className="grid size-10 place-items-center bg-gradient-to-br from-violet-500 to-blue-500 text-xl font-black text-white" style={{clipPath:"polygon(50% 0%,100% 25%,100% 75%,50% 100%,0 75%,0 25%)"}}>E</div><div><span className="text-sm font-bold">ELO Orquestrador</span><p className="text-[10px] text-white/40">Workspace operacional · Multiteiner</p></div></div>
      <div className="flex items-center gap-2"><span className="hidden text-xs text-white/45 sm:inline">Acesso autorizado</span><button type="button" onClick={onSignOut} className="elo-subtab" aria-label="Encerrar sessão">Sair</button></div>
    </header>
    <nav className="sticky top-14 z-20 flex gap-1 overflow-x-auto border-b border-white/10 bg-[#0a1628] px-3 py-1" aria-label="Áreas do workspace">{areas.map(item=><button type="button" key={item.id} onClick={()=>{setAreaId(item.id);setNotice(null);setResult(null);}} aria-current={item.id===areaId?"page":undefined} className={`elo-subtab ${item.id===areaId?"active":""}`}><span className="mr-1">{item.icon}</span><span>{item.label}</span></button>)}</nav>
    <div className="mx-auto max-w-[1500px] space-y-5 px-4 py-5 md:px-6"><div><h1 className="text-xl font-semibold">{area.label}</h1><p className="text-sm text-white/40">{area.description}</p></div>
      {notice && <div role="status" className="rounded-xl border border-violet-400/30 bg-violet-400/10 p-3 text-sm text-violet-200">{notice}</div>}
      {areaId==="pcp"?<PCPWorkspace onMission={runMission}/>:<GenericArea key={areaId} area={area} onMission={runMission} drafts={drafts} onSave={saveDraft} onDelete={deleteDraft}/>}
      <section className="elo-panel p-5"><div className="flex items-center justify-between"><div><h3 className="font-semibold">🧠 ELO Assistente</h3><p className="mt-1 text-xs text-white/45">Consulta cognitiva contextual; não executa ações externas sem autorização.</p></div><span className="elo-badge">{busy?"Processando":"Pronto"}</span></div><div className="mt-4 flex gap-2"><input value={mission} onChange={e=>setMission(e.target.value)} onKeyDown={e=>{if(e.key==="Enter")void runMission(mission);}} disabled={busy} placeholder="Digite sua pergunta ao ELO…" className="elo-input min-w-0 flex-1"/><button type="button" disabled={busy||!mission.trim()} onClick={()=>void runMission(mission)} className="elo-button disabled:opacity-40">Enviar</button></div></section>
      {result&&<CognitiveResult result={result}/>}
    </div>
  </main>;
}
