"use client";

import { useMemo, useState } from "react";
import { ProcessNavigation } from "@/components/process-navigation";
import { sectors, type SectorKey } from "@/lib/sectors";

const navItems = ["Missões", "Projetos", "Processos", "Análises", "Conectores", "Governança"];

function MiniChart({ values, accent }: { values: number[]; accent: string }) {
  const max = Math.max(...values);
  return (
    <div className="flex h-36 items-end gap-2" aria-label="Gráfico de indicadores">
      {values.map((value, index) => (
        <div key={`${value}-${index}`} className="flex flex-1 items-end justify-center">
          <div
            className="w-full rounded-t-md opacity-80 transition-all"
            style={{ height: `${Math.max(12, (value / max) * 100)}%`, backgroundColor: accent }}
            title={`${value}`}
          />
        </div>
      ))}
    </div>
  );
}

export function EloDashboard() {
  const [sectorKey, setSectorKey] = useState<SectorKey>("planejamento");
  const [showProcesses, setShowProcesses] = useState(true);
  const sector = useMemo(() => sectors.find((item) => item.key === sectorKey) ?? sectors[0], [sectorKey]);

  return (
    <main className="min-h-screen bg-[var(--elo-bg)] text-[var(--elo-ink)]">
      <div className="flex min-h-screen flex-col lg:flex-row">
        <aside className="w-full border-b border-white/10 bg-[var(--elo-sidebar)] p-4 text-white lg:min-h-screen lg:w-64 lg:border-b-0 lg:border-r">
          <div className="mb-8 flex items-center gap-3 px-2">
            <div className="grid size-10 place-items-center rounded-full border border-white/40 text-lg font-semibold">C</div>
            <div>
              <div className="text-xl font-semibold tracking-wide">ELO</div>
              <div className="text-[10px] uppercase tracking-[0.24em] text-white/50">Inteligência corporativa</div>
            </div>
          </div>

          <nav aria-label="Navegação principal" className="space-y-1">
            <button className="w-full rounded-xl bg-white/10 px-4 py-3 text-left text-sm font-medium">⌂ Início</button>
            {navItems.map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => item === "Processos" && setShowProcesses(true)}
                className={`w-full rounded-xl px-4 py-3 text-left text-sm transition ${item === "Processos" && showProcesses ? "bg-white/10 font-medium text-white" : "text-white/70 hover:bg-white/10 hover:text-white"}`}
              >
                {item}
              </button>
            ))}
          </nav>

          <div className="mt-10 border-t border-white/10 pt-5">
            <label htmlFor="sector" className="mb-2 block px-2 text-xs font-medium uppercase tracking-wider text-white/40">Setor atual</label>
            <select
              id="sector"
              value={sectorKey}
              onChange={(event) => setSectorKey(event.target.value as SectorKey)}
              className="w-full rounded-xl border border-white/10 bg-white/10 px-3 py-3 text-sm text-white outline-none focus:ring-2 focus:ring-white/30"
            >
              {sectors.map((item) => <option key={item.key} value={item.key} className="text-slate-900">{item.label}</option>)}
            </select>
          </div>
        </aside>

        <section className="flex min-w-0 flex-1 flex-col">
          <header className="flex items-center justify-between gap-4 border-b border-slate-200 bg-white/85 px-5 py-4 backdrop-blur lg:px-8">
            <div>
              <div className="text-xs text-slate-400">ELO / Workspace</div>
              <h1 className="text-2xl font-semibold tracking-tight">{sector.label}</h1>
            </div>
            <div className="flex items-center gap-3">
              <span className="hidden text-sm text-slate-500 sm:block">Bruno</span>
              <div className="grid size-9 place-items-center rounded-full bg-slate-200 text-sm font-semibold text-slate-700">B</div>
            </div>
          </header>

          <div className="flex-1 space-y-6 p-5 lg:p-8">
            <div className="grid gap-4 xl:grid-cols-[1.4fr_1fr]">
              <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <p className="mb-2 text-sm font-medium" style={{ color: sector.accent }}>ELO • {sector.label}</p>
                <h2 className="max-w-2xl text-3xl font-semibold tracking-tight">{sector.subtitle}</h2>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">Transforme uma intenção em missão, análise ou processo governado pelo ELO.</p>
                <div className="mt-6 flex gap-3">
                  <button className="rounded-xl px-4 py-3 text-sm font-semibold text-white shadow-sm" style={{ backgroundColor: sector.accent }}>Criar missão</button>
                  <button className="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700">Analisar dados</button>
                </div>
              </section>

              <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <label htmlFor="mission" className="mb-2 block text-sm font-medium text-slate-700">Pergunte ou solicite algo</label>
                <div className="flex gap-2 rounded-xl border border-slate-200 bg-slate-50 p-2">
                  <input id="mission" placeholder={`Ex.: analise a carteira de ${sector.label.toLowerCase()}`} className="min-w-0 flex-1 bg-transparent px-2 text-sm outline-none" />
                  <button aria-label="Enviar missão" className="rounded-lg px-4 py-2 text-sm font-semibold text-white" style={{ backgroundColor: sector.accent }}>➤</button>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-2 text-xs text-slate-500">
                  <div className="rounded-lg bg-slate-50 p-3">Governança ativa</div>
                  <div className="rounded-lg bg-slate-50 p-3">Evidências registradas</div>
                </div>
              </section>
            </div>

            {showProcesses && sectorKey === "planejamento" && <ProcessNavigation accent={sector.accent} />}

            <section aria-label="Indicadores principais" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {sector.metrics.map((metric) => (
                <article key={metric.label} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                  <p className="text-xs font-medium text-slate-500">{metric.label}</p>
                  <div className="mt-2 flex items-end justify-between gap-2">
                    <strong className="text-2xl tracking-tight">{metric.value}</strong>
                    <span className="rounded-full bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-700">{metric.delta}</span>
                  </div>
                </article>
              ))}
            </section>

            <section className="grid gap-4 xl:grid-cols-[1.5fr_0.8fr]">
              <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="mb-5 flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold">{sector.chartTitle}</h3>
                    <p className="text-xs text-slate-400">Visão operacional do setor</p>
                  </div>
                  <span className="rounded-lg bg-slate-50 px-3 py-2 text-xs text-slate-500">Últimos 7 períodos</span>
                </div>
                <MiniChart values={sector.chartValues} accent={sector.accent} />
              </article>

              <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <h3 className="font-semibold">Ações rápidas</h3>
                <div className="mt-4 space-y-2">
                  {sector.quickActions.map((action) => (
                    <button key={action} className="flex w-full items-center justify-between rounded-xl border border-slate-200 px-3 py-3 text-left text-sm transition hover:bg-slate-50">
                      <span>{action}</span>
                      <span className="text-slate-400">→</span>
                    </button>
                  ))}
                </div>
              </article>
            </section>

            <footer className="flex flex-col gap-2 border-t border-slate-200 pt-5 text-xs text-slate-400 sm:flex-row sm:items-center sm:justify-between">
              <span>ELO • Inteligência para um futuro melhor.</span>
              <span>Governança · Segurança · Simbionte · Hermes · Conectores · Múltiplas IAs</span>
            </footer>
          </div>
        </section>
      </div>
    </main>
  );
}
