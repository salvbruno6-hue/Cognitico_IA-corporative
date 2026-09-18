"use client";

import { useState } from "react";

type Props = { accessToken: string; displayName?: string | null; email?: string | null; onSignOut?: () => void };

const areas = [
  ["Visão geral", "Acompanhamento operacional do ELO."],
  ["Lista-Mãe · PCP", "Concepção, composição, quantidades e valores unitários."],
  ["Estoque · Almoxarifado", "Saldo físico, entradas, saídas, reservas e localização."],
  ["Modelos MLT.M01–M27", "Consulta das famílias e especificações dos módulos."],
  ["Produção / PCP", "Fluxo produtivo, capacidade, materiais e gargalos."],
  ["Qualidade", "Ocorrências, controles e evidências."],
  ["Solicitações", "Consultas comerciais e demandas."],
  ["Fluxo da empresa", "Visão ponta a ponta dos processos Multiteiner."],
] as const;

export function EloWebOperationalPortal({ accessToken, displayName, email, onSignOut }: Props) {
  const [active, setActive] = useState("Visão geral");
  const selected = areas.find(([name]) => name === active) ?? areas[0];

  return (
    <main className="min-h-screen bg-[var(--elo-bg)] text-[var(--elo-ink)]">
      <div className="flex min-h-screen">
        <aside className="hidden w-72 shrink-0 border-r border-slate-200 bg-slate-950 px-5 py-6 text-white lg:block">
          <div className="flex items-center gap-3 px-2"><div className="grid size-10 place-items-center rounded-2xl bg-white text-lg font-bold text-slate-950">E</div><div><div className="text-lg font-bold">ELO</div><div className="text-[9px] uppercase tracking-[.22em] text-white/40">Portal operacional</div></div></div>
          <div className="mt-9 px-2 text-[10px] font-semibold uppercase tracking-[.2em] text-white/35">Consulta</div>
          <nav className="mt-3 space-y-1" aria-label="Áreas operacionais">
            {areas.map(([name]) => <button key={name} type="button" onClick={() => setActive(name)} className={`w-full rounded-xl px-3 py-2.5 text-left text-sm transition ${active === name ? "bg-white font-semibold text-slate-950" : "text-white/65 hover:bg-white/10 hover:text-white"}`}>{name}</button>)}
          </nav>
          <div className="mt-8 rounded-2xl border border-white/10 bg-white/[.04] p-4 text-xs text-white/60"><div className="text-[10px] uppercase tracking-[.18em] text-white/35">Acesso</div><div className="mt-3 font-medium text-white">Consulta operacional</div><div className="mt-1">Alterações somente quando uma permissão específica estiver atribuída.</div></div>
          <a href="/terminal" className="mt-4 block rounded-xl border border-white/10 px-3 py-2.5 text-center text-sm text-white/70 hover:bg-white/10 hover:text-white">Terminal Hermes</a>
        </aside>
        <section className="min-w-0 flex-1">
          <header className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200/80 bg-[var(--elo-bg)]/95 px-5 py-4 backdrop-blur lg:px-8">
            <div><div className="text-[10px] font-semibold uppercase tracking-[.2em] text-slate-400">ELO / Portal operacional</div><h1 className="mt-1 text-xl font-semibold">{active}</h1></div>
            <div className="flex items-center gap-3"><div className="hidden text-right sm:block"><div className="text-xs font-semibold">{displayName || "Usuário ELO"}</div><div className="text-[11px] text-slate-400">{email || "Identidade Google validada"}</div></div><button type="button" onClick={onSignOut} className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-50">Sair</button></div>
          </header>
          <div className="mx-auto max-w-7xl space-y-6 p-5 lg:p-8">
            <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm lg:p-8"><div className="text-[10px] font-bold uppercase tracking-[.2em] text-slate-400">Área autorizada</div><h2 className="mt-2 text-3xl font-semibold tracking-tight">{selected[0]}</h2><p className="mt-3 max-w-3xl text-sm leading-6 text-slate-500">{selected[1]}</p></section>
            <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
              {[
                ["PCP", "Lista-Mãe", "Concepção e custo unitário dos componentes."],
                ["Almoxarifado", "Estoque", "Controle físico de materiais e movimentações."],
                ["Produtos", "MLT.M01–M27", "Consulta técnica dos modelos e módulos."],
                ["Empresa", "Fluxo integrado", "Processos conectados do pedido ao retorno."],
              ].map(([eyebrow,title,description]) => <article key={title} className="rounded-2xl border border-slate-200 bg-white p-5"><div className="text-[10px] font-bold uppercase tracking-[.16em] text-slate-400">{eyebrow}</div><h3 className="mt-2 font-semibold">{title}</h3><p className="mt-2 text-sm text-slate-500">{description}</p></article>)}
            </section>
            <section className="rounded-[2rem] border border-slate-200 bg-slate-950 p-6 text-white"><div className="text-[10px] font-bold uppercase tracking-[.2em] text-white/35">Fluxo Multiteiner</div><div className="mt-5 grid gap-2 text-sm sm:grid-cols-3 lg:grid-cols-6">{["Solicitação","Planejamento","PCP","Produção","Qualidade","Expedição / Retorno"].map((step,i) => <div key={step} className="rounded-xl border border-white/10 bg-white/[.05] p-3"><span className="text-[10px] text-white/35">0{i+1}</span><div className="mt-2 font-semibold">{step}</div></div>)}</div></section>
            <p className="text-xs text-slate-400">Sessão autenticada pelo Google/Supabase. Identidade e permissões são verificadas pelo ELO Authorization. Token de acesso: {accessToken ? "presente" : "ausente"}.</p>
          </div>
        </section>
      </div>
    </main>
  );
}
