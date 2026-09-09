"use client";

import { useMemo, useState } from "react";
import { sectors, type SectorKey } from "@/lib/sectors";
import { DEFAULT_ELO_SETTINGS, type ELOSettings } from "@/lib/elo-settings";
import { EloSettingsPanel } from "@/components/elo-settings-panel";

const navItems = ["Início", "Missões", "Projetos", "Análises", "Conectores", "Governança"];

type Props = {
  onSignOut?: () => void;
};

function MiniChart({ values, accent }: { values: number[]; accent: string }) {
  const max = Math.max(...values, 1);
  return (
    <div className="flex h-36 items-end gap-2" aria-label="Gráfico de indicadores">
      {values.map((value, index) => (
        <div key={`${value}-${index}`} className="flex flex-1 items-end justify-center">
          <div className="w-full rounded-t-md opacity-80 transition-all" style={{ height: `${Math.max(12, (value / max) * 100)}%`, backgroundColor: accent }} title={`${value}`} />
        </div>
      ))}
    </div>
  );
}

const sectorActionHelp: Record<SectorKey, string[]> = {
  planejamento: ["Nova solicitação", "Analisar orçamento", "Consultar ELO", "Abrir relatório"],
  comercial: ["Qualificar lead", "Gerar proposta", "Analisar conversão", "Identificar risco"],
  financeiro: ["Gerar relatório", "Analisar despesas", "Prever fluxo", "Ver inadimplência"],
  rh: ["Abrir vaga", "Analisar clima", "Plano de desenvolvimento", "Relatório de desempenho"],
  operacoes: ["Iniciar processo", "Verificar gargalos", "Gerar relatório", "Acompanhar fornecedor"],
  pcp: ["Programar produção", "Ver Gantt", "Analisar estoque", "Detectar gargalo"],
  ti: ["Abrir chamado", "Ver status", "Analisar vulnerabilidades", "Gerar relatório"],
};

const sectorDescriptions: Record<SectorKey, string> = {
  planejamento: "Entrada de demandas, análise, orçamento e encaminhamento governado.",
  comercial: "Oportunidades, propostas e riscos comerciais.",
  financeiro: "Leitura financeira e apoio a decisões de recursos.",
  rh: "Pessoas, desenvolvimento e indicadores organizacionais.",
  operacoes: "Coordenação operacional, incidentes e desempenho.",
  pcp: "Capacidade, programação, materiais e gargalos de produção.",
  ti: "Sistemas, suporte, disponibilidade e segurança.",
};

export function EloDashboard({ onSignOut }: Props) {
  const [sectorKey, setSectorKey] = useState<SectorKey>("planejamento");
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [settings, setSettings] = useState<ELOSettings>(DEFAULT_ELO_SETTINGS);
  const [activeNav, setActiveNav] = useState("Início");
  const [mission, setMission] = useState("");
  const [notice, setNotice] = useState<string | null>(null);
  const sector = useMemo(() => sectors.find((item) => item.key === sectorKey) ?? sectors[0], [sectorKey]);
  const actions = sectorActionHelp[sectorKey];

  function handleSettingsChange(next: ELOSettings) {
    setSettings(next);
    document.documentElement.dataset.theme = next.theme;
  }

  function handleMission() {
    const request = mission.trim();
    if (!request) return;
    setNotice(`Solicitação preparada para o setor ${sector.label}. A execução deve seguir o fluxo governado do ELO.`);
    setMission("");
    if (settings.soundEnabled && typeof window !== "undefined") {
      try {
        const AudioContextClass = window.AudioContext ?? (window as typeof window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
        if (AudioContextClass) {
          const context = new AudioContextClass();
          const oscillator = context.createOscillator();
          const gain = context.createGain();
          oscillator.frequency.value = 660;
          gain.gain.value = 0.025;
          oscillator.connect(gain);
          gain.connect(context.destination);
          oscillator.start();
          oscillator.stop(context.currentTime + 0.06);
          void context.close();
        }
      } catch {
        // Audio is optional; never block the operational interaction.
      }
    }
  }

  function handleQuickAction(action: string) {
    setNotice(`${action}: ação encaminhada para o workspace ${sector.label}.`);
  }

  return (
    <main className="min-h-screen bg-[var(--elo-bg)] text-[var(--elo-ink)]" data-theme={settings.theme}>
      <div className="flex min-h-screen flex-col lg:flex-row">
        <aside className="w-full border-b border-white/10 bg-[var(--elo-sidebar)] p-4 text-white lg:min-h-screen lg:w-72 lg:border-b-0 lg:border-r">
          <div className="mb-8 flex items-center gap-3 px-2">
            <div className="grid size-10 place-items-center rounded-full border border-white/40 text-lg font-semibold">C</div>
            <div>
              <div className="text-xl font-semibold tracking-wide">ELO</div>
              <div className="text-[10px] uppercase tracking-[0.24em] text-white/50">Inteligência corporativa</div>
            </div>
          </div>

          <nav aria-label="Navegação principal" className="space-y-1">
            {navItems.map((item) => (
              <button key={item} onClick={() => setActiveNav(item)} className={`w-full rounded-xl px-4 py-3 text-left text-sm transition ${activeNav === item ? "bg-white/10 font-medium text-white" : "text-white/70 hover:bg-white/10 hover:text-white"}`}>
                {item === "Início" ? "⌂" : "•"} {item}
              </button>
            ))}
          </nav>

          <div className="mt-8 border-t border-white/10 pt-5">
            <label htmlFor="sector" className="mb-2 block px-2 text-xs font-medium uppercase tracking-wider text-white/40">Setor atual</label>
            <div className="space-y-2">
              {sectors.map((item) => (
                <button key={item.key} type="button" onClick={() => { setSectorKey(item.key); setActiveNav("Início"); setNotice(null); }} className={`w-full rounded-xl border px-3 py-2.5 text-left text-sm transition ${sectorKey === item.key ? "border-white/20 bg-white/15 text-white" : "border-white/5 bg-white/5 text-white/65 hover:bg-white/10 hover:text-white"}`}>
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          <button type="button" onClick={() => setSettingsOpen(true)} className="mt-5 flex w-full items-center justify-between rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white/80 hover:bg-white/10 hover:text-white" aria-label="Abrir configurações">
            <span>⚙ Configurações</span>
            <span className="text-xs text-white/40">Interface · Canais</span>
          </button>
        </aside>

        <section className="flex min-w-0 flex-1 flex-col">
          <header className="flex items-center justify-between gap-4 border-b border-slate-200 bg-[var(--elo-panel)]/90 px-5 py-4 backdrop-blur lg:px-8">
            <div>
              <div className="text-xs text-slate-400">ELO / {activeNav}</div>
              <h1 className="text-2xl font-semibold tracking-tight">{sector.label}</h1>
            </div>
            <div className="flex items-center gap-2">
              <button type="button" onClick={() => setSettingsOpen(true)} className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-50">⚙</button>
              <button type="button" onClick={() => onSignOut?.()} className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-slate-800">Sair</button>
              <div className="hidden text-sm text-slate-500 sm:block">Bruno</div>
              <div className="grid size-9 place-items-center rounded-full bg-slate-200 text-sm font-semibold text-slate-700">B</div>
            </div>
          </header>

          <div className="flex-1 space-y-6 p-5 lg:p-8">
            {notice && <div className="rounded-xl border border-slate-200 bg-[var(--elo-panel)] px-4 py-3 text-sm text-slate-600" role="status">{notice}</div>}

            <div className="grid gap-4 xl:grid-cols-[1.4fr_1fr]">
              <section className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-6 shadow-sm">
                <p className="mb-2 text-sm font-medium" style={{ color: sector.accent }}>ELO • {sector.label}</p>
                <h2 className="max-w-2xl text-3xl font-semibold tracking-tight">{sector.subtitle}</h2>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">{sectorDescriptions[sectorKey]}</p>
                <div className="mt-6 flex flex-wrap gap-3">
                  <button onClick={() => handleQuickAction("Criar missão")} className="rounded-xl px-4 py-3 text-sm font-semibold text-white shadow-sm" style={{ backgroundColor: sector.accent }}>Criar missão</button>
                  <button onClick={() => handleQuickAction("Analisar dados")} className="rounded-xl border border-slate-200 bg-transparent px-4 py-3 text-sm font-semibold text-slate-700">Analisar dados</button>
                </div>
              </section>

              <section className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm">
                <label htmlFor="mission" className="mb-2 block text-sm font-medium text-slate-700">Pergunte ou solicite algo</label>
                <div className="flex gap-2 rounded-xl border border-slate-200 bg-slate-50 p-2">
                  <input id="mission" value={mission} onChange={(event) => setMission(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter") handleMission(); }} placeholder={`Ex.: analise a carteira de ${sector.label.toLowerCase()}`} className="min-w-0 flex-1 bg-transparent px-2 text-sm outline-none" />
                  <button onClick={handleMission} aria-label="Enviar missão" className="rounded-lg px-4 py-2 text-sm font-semibold text-white" style={{ backgroundColor: sector.accent }}>➤</button>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-2 text-xs text-slate-500">
                  <div className="rounded-lg bg-slate-50 p-3">Governança ativa</div>
                  <div className="rounded-lg bg-slate-50 p-3">Dados via camada governada</div>
                </div>
              </section>
            </div>

            <section aria-label="Indicadores principais" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {sector.metrics.map((metric) => (
                <article key={metric.label} className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm">
                  <p className="text-xs font-medium text-slate-500">{metric.label}</p>
                  <div className="mt-2 flex items-end justify-between gap-2">
                    <strong className="text-2xl tracking-tight">{metric.value}</strong>
                    <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600">Referência</span>
                  </div>
                </article>
              ))}
            </section>

            <section className="grid gap-4 xl:grid-cols-[1.5fr_0.8fr]">
              <article className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm">
                <div className="mb-5 flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold">{sector.chartTitle}</h3>
                    <p className="text-xs text-slate-400">Referência visual — não representa telemetria atual</p>
                  </div>
                  <span className="rounded-lg bg-slate-50 px-3 py-2 text-xs text-slate-500">Referência</span>
                </div>
                <MiniChart values={sector.chartValues} accent={sector.accent} />
              </article>

              <article className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm">
                <h3 className="font-semibold">Ações do setor</h3>
                <p className="mt-1 text-xs text-slate-400">Atalhos de interação; execução real passa pelo fluxo governado.</p>
                <div className="mt-4 space-y-2">
                  {actions.map((action) => (
                    <button key={action} onClick={() => handleQuickAction(action)} className="flex w-full items-center justify-between rounded-xl border border-slate-200 px-3 py-3 text-left text-sm transition hover:bg-slate-50">
                      <span>{action}</span><span className="text-slate-400">→</span>
                    </button>
                  ))}
                </div>
              </article>
            </section>

            <footer className="flex flex-col gap-2 border-t border-slate-200 pt-5 text-xs text-slate-400 sm:flex-row sm:items-center sm:justify-between">
              <span>ELO • Inteligência para um futuro melhor.</span>
              <span>Simbionte · Hermes · Conectores · Governança</span>
            </footer>
          </div>
        </section>
      </div>

      <EloSettingsPanel open={settingsOpen} onClose={() => setSettingsOpen(false)} onChange={handleSettingsChange} />
    </main>
  );
}
