"use client";

import { useEffect, useMemo, useState, type FormEvent } from "react";
import { callELOAuthorization, type ELOAuthorizationResult } from "@/auth/eloAuthorization";

type Props = { accessToken:string; displayName?:string|null; email?:string|null; onSignOut?:()=>void };
type Area = { name:string; description:string; code?:string; operations?:string[] };

const areas:Area[]=[
 {name:"Visão geral",description:"Acompanhamento operacional do ELO."},
 {name:"Lista-Mãe · PCP",description:"Concepção, composição, quantidades e valores unitários.",code:"PCP-LISTA-MAE",operations:["pcp_read","pcp_update"]},
 {name:"Estoque · Almoxarifado",description:"Saldo físico, entradas, saídas, reservas e localização.",code:"GESTAO-ALMOXARIFADO",operations:["stock_read","stock_insert","stock_update","stock_adjust"]},
 {name:"Modelos MLT.M01–M27",description:"Consulta das famílias e especificações dos módulos."},
 {name:"Produção / PCP",description:"Fluxo produtivo, capacidade, materiais e gargalos."},
 {name:"Qualidade",description:"Ocorrências, controles e evidências."},
 {name:"Solicitações",description:"Consultas comerciais e demandas."},
 {name:"Fluxo da empresa",description:"Visão ponta a ponta dos processos Multiteiner."},
];

const listaMaeFields: Array<{name:string; label:string; required:boolean}> = [
  {name:"cod_item",label:"Código do item",required:true},
  {name:"cod_produt",label:"Código do produto",required:false},
  {name:"descricao_oficial",label:"Descrição oficial",required:true},
  {name:"aplicacao",label:"Aplicação",required:false},
  {name:"un",label:"Unidade",required:false},
  {name:"valor_unitario",label:"Valor unitário",required:false},
  {name:"curva",label:"Curva",required:false},
  {name:"modelos_aplicaveis",label:"Modelos aplicáveis",required:false},
];

export function EloWebOperationalPortal({accessToken,displayName,email,onSignOut}:Props){
 const [active,setActive]=useState("Visão geral");
 const [authz,setAuthz]=useState<ELOAuthorizationResult|null>(null);
 const [loading,setLoading]=useState(true);
 const [error,setError]=useState<string|null>(null);
 const [insertMessage,setInsertMessage]=useState<string|null>(null);
 const [insertError,setInsertError]=useState<string|null>(null);
 const [saving,setSaving]=useState(false);
 useEffect(()=>{let live=true; void callELOAuthorization(accessToken,"portal_access").then(r=>{if(live)setAuthz(r);}).catch(e=>{if(live)setError(e instanceof Error?e.message:"Não foi possível carregar as permissões.");}).finally(()=>{if(live)setLoading(false);}); return()=>{live=false;};},[accessToken]);
 const selected=areas.find(a=>a.name===active)??areas[0];
 const grantedScopes=useMemo(()=>new Set(((authz?.scopes??[]) as Array<{scope_key?:string}>).map(s=>String(s.scope_key??""))),[authz]);
 const grantedCaps=useMemo(()=>new Set(((authz?.capabilities??[]) as Array<{code?:string}>).map(c=>String(c.code??""))),[authz]);
 const operationCapability:Record<string,string>={stock_read:"ALMX_READ",stock_insert:"ALMX_INSERT",stock_update:"ALMX_UPDATE",stock_adjust:"ALMX_ADJUST",pcp_read:"PCP_READ",pcp_update:"PCP_UPDATE"};
 const allowed=(a:Area,o:string)=>!!a.code&&grantedScopes.has(a.code)&&grantedCaps.has(operationCapability[o]??"");
 const canInsertListaMae=grantedCaps.has("LISTA_MAE_INSERT");
 const insertListaMae=async(e:FormEvent<HTMLFormElement>)=>{
  e.preventDefault();
  setInsertMessage(null);
  setInsertError(null);
  setSaving(true);
  const form=new FormData(e.currentTarget);
  const rawValue=String(form.get("valor_unitario")??"").trim();
  const value=rawValue===""?null:Number(rawValue.replace(",","."));
  if(value!==null&&!Number.isFinite(value)){setInsertError("Valor unitário inválido.");setSaving(false);return;}
  try{
   const baseUrl=process.env.NEXT_PUBLIC_SUPABASE_URL;
   if(!baseUrl) throw new Error("URL do Supabase não configurada.");
   const response=await fetch(baseUrl+"/functions/v1/elo-data-gateway",{
    method:"POST",
    headers:{Authorization:"Bearer "+accessToken,"Content-Type":"application/json"},
    body:JSON.stringify({
     operation:"lista_mae_insert",
     repository:"salvbruno6-hue/Cognitico_IA-corporative",
     data:{
      cod_item:String(form.get("cod_item")??"").trim(),
      cod_produt:String(form.get("cod_produt")??"").trim()||null,
      descricao_oficial:String(form.get("descricao_oficial")??"").trim(),
      aplicacao:String(form.get("aplicacao")??"").trim()||null,
      un:String(form.get("un")??"").trim()||null,
      valor_unitario:value,
      curva:String(form.get("curva")??"").trim()||null,
      modelos_aplicaveis:String(form.get("modelos_aplicaveis")??"").trim()||null
     }
    })
   });
   const result=await response.json().catch(()=>null);
   if(!response.ok||result?.ok!==true) throw new Error(result?.error??result?.reason??"Não foi possível inserir o item.");
   e.currentTarget.reset();
   setInsertMessage("Item "+String(result.data?.cod_item??"")+" inserido na Lista-Mãe.");
  }catch(err){setInsertError(err instanceof Error?err.message:"Falha na inserção.");}
  finally{setSaving(false);}
 };
 return <main className="min-h-screen bg-[var(--elo-bg)] text-[var(--elo-ink)]"><div className="flex min-h-screen">
  <aside className="hidden w-72 shrink-0 border-r border-slate-200 bg-slate-950 px-5 py-6 text-white lg:block">
   <div className="flex items-center gap-3 px-2"><div className="grid size-10 place-items-center rounded-2xl bg-white text-lg font-bold text-slate-950">E</div><div><div className="text-lg font-bold">ELO</div><div className="text-[9px] uppercase tracking-[.22em] text-white/40">Portal operacional</div></div></div>
   <div className="mt-9 px-2 text-[10px] font-semibold uppercase tracking-[.2em] text-white/35">Consulta</div>
   <nav className="mt-3 space-y-1" aria-label="Áreas operacionais">{areas.map(a=><button key={a.name} type="button" onClick={()=>setActive(a.name)} className={`w-full rounded-xl px-3 py-2.5 text-left text-sm transition ${active===a.name?"bg-white font-semibold text-slate-950":"text-white/65 hover:bg-white/10 hover:text-white"}`}>{a.name}</button>)}</nav>
   <div className="mt-8 rounded-2xl border border-white/10 bg-white/[.04] p-4 text-xs text-white/60"><div className="text-[10px] uppercase tracking-[.18em] text-white/35">Acesso</div><div className="mt-3 font-medium text-white">{loading?"Validando permissões…":"Consulta operacional"}</div><div className="mt-1">{error??"Alterações somente quando uma permissão específica estiver atribuída."}</div></div>
   <a href="/terminal" className="mt-4 block rounded-xl border border-white/10 px-3 py-2.5 text-center text-sm text-white/70 hover:bg-white/10 hover:text-white">Terminal Hermes</a>
  </aside>
  <section className="min-w-0 flex-1"><header className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200/80 bg-[var(--elo-bg)]/95 px-5 py-4 backdrop-blur lg:px-8"><div><div className="text-[10px] font-semibold uppercase tracking-[.2em] text-slate-400">ELO / Portal operacional</div><h1 className="mt-1 text-xl font-semibold">{active}</h1></div><div className="flex items-center gap-3"><div className="hidden text-right sm:block"><div className="text-xs font-semibold">{displayName||"Usuário ELO"}</div><div className="text-[11px] text-slate-400">{email||"Identidade Google validada"}</div></div><button type="button" onClick={onSignOut} className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-50">Sair</button></div></header>
   <div className="mx-auto max-w-7xl space-y-6 p-5 lg:p-8"><section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm lg:p-8"><div className="text-[10px] font-bold uppercase tracking-[.2em] text-slate-400">Área autorizada</div><h2 className="mt-2 text-3xl font-semibold tracking-tight">{selected.name}</h2><p className="mt-3 max-w-3xl text-sm leading-6 text-slate-500">{selected.description}</p></section>
    <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">{[["PCP","Lista-Mãe","Concepção e custo unitário dos componentes."],["Almoxarifado","Estoque","Controle físico de materiais e movimentações."],["Produtos","MLT.M01–M27","Consulta técnica dos modelos."],["Empresa","Fluxo integrado","Processos conectados do pedido ao retorno."]].map(([e,t,d])=><article key={t} className="rounded-2xl border border-slate-200 bg-white p-5"><div className="text-[10px] font-bold uppercase tracking-[.16em] text-slate-400">{e}</div><h3 className="mt-2 font-semibold">{t}</h3><p className="mt-2 text-sm text-slate-500">{d}</p></article>)}</section>
    {selected.code&&<section className="rounded-[2rem] border border-slate-200 bg-white p-6"><div className="text-[10px] font-bold uppercase tracking-[.2em] text-slate-400">Gestão / permissões</div><div className="mt-2 flex flex-wrap items-center gap-3"><span className="rounded-lg bg-slate-100 px-3 py-1 text-xs font-semibold">{selected.code}</span>{(selected.operations??[]).map(o=><span key={o} className={`rounded-lg px-3 py-1 text-xs font-semibold ${allowed(selected,o)?"bg-slate-900 text-white":"bg-slate-100 text-slate-400"}`}>{o}{allowed(selected,o)?" · autorizado":" · consulta/sem alteração"}</span>)}</div></section>}
    {active==="Lista-Mãe · PCP"&&canInsertListaMae&&<section className="rounded-[2rem] border border-slate-200 bg-white p-6">
      <div className="text-[10px] font-bold uppercase tracking-[.2em] text-slate-400">Operação autorizada · Lista-Mãe</div>
      <h3 className="mt-2 text-xl font-semibold">Inserir novo item</h3>
      <p className="mt-2 text-sm text-slate-500">Disponível somente para identidades com <span className="font-semibold">LISTA_MAE_INSERT</span>. UPDATE e DELETE não são oferecidos.</p>
      <form onSubmit={insertListaMae} className="mt-5 grid gap-4 md:grid-cols-2">
        {listaMaeFields.map(({name,label,required})=><label key={name} className="text-xs font-semibold text-slate-600">{label}{required?" *":""}<input name={name} required={required} type={name==="valor_unitario"?"number":"text"} step={name==="valor_unitario"?"0.01":undefined} className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm font-normal outline-none focus:border-slate-400" /></label>)}
        <div className="md:col-span-2 flex flex-wrap items-center gap-3">
          <button type="submit" disabled={saving} className="rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50">{saving?"Inserindo…":"Inserir na Lista-Mãe"}</button>
          {insertMessage&&<span className="text-sm font-medium text-slate-600">{insertMessage}</span>}
          {insertError&&<span className="text-sm font-medium text-red-600">{insertError}</span>}
        </div>
      </form>
    </section>}
    <section className="rounded-[2rem] border border-slate-200 bg-slate-950 p-6 text-white"><div className="text-[10px] font-bold uppercase tracking-[.2em] text-white/35">Fluxo Multiteiner</div><div className="mt-5 grid gap-2 text-sm sm:grid-cols-3 lg:grid-cols-6">{["Solicitação","Planejamento","PCP","Produção","Qualidade","Expedição / Retorno"].map((step,i)=><div key={step} className="rounded-xl border border-white/10 bg-white/[.05] p-3"><span className="text-[10px] text-white/35">0{i+1}</span><div className="mt-2 font-semibold">{step}</div></div>)}</div></section>
    <p className="text-xs text-slate-400">Google valida a identidade; o ELO Authorization valida e entrega as permissões. Lista-Mãe permanece no PCP. Estoque permanece no Almoxarifado. Nenhuma permissão de escrita é inferida pelo frontend.</p>
   </div></section></div></main>;
}
