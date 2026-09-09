"use client";

import { useMemo, useState } from "react";
import { getProcess, processes, type ProcessId, type ProcessNode } from "@/lib/processes";

type ProcessNavigationProps = {
  accent: string;
};

function nodeClass(node: ProcessNode) {
  if (node.kind === "gate") return "border-dashed";
  if (node.kind === "output") return "font-semibold";
  return "";
}

export function ProcessNavigation({ accent }: ProcessNavigationProps) {
  const [processId, setProcessId] = useState<ProcessId>("planning-demand");
  const process = useMemo(() => getProcess(processId), [processId]);

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm" aria-label="Navegação de processos">
      <div className="flex flex-col gap-4 border-b border-slate-100 pb-5 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">Processo ELO</div>
          <h2 className="mt-1 text-xl font-semibold tracking-tight">Planejamento conectado ao fluxo operacional</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
            Esta camada apresenta a estrutura de processo documentada. Não representa telemetria operacional atual.
          </p>
        </div>
        <div className="flex gap-2" role="tablist" aria-label="Processos de planejamento">
          {processes.map((item) => {
            const active = item.id === processId;
            return (
              <button
                key={item.id}
                type="button"
                role="tab"
                aria-selected={active}
                onClick={() => setProcessId(item.id)}
                className="rounded-xl border px-3 py-2 text-xs font-semibold transition"
                style={active ? { borderColor: accent, backgroundColor: `${accent}12`, color: accent } : undefined}
              >
                {item.title}
              </button>
            );
          })}
        </div>
      </div>

      <div className="mt-5 grid gap-4 xl:grid-cols-[1.6fr_0.8fr]">
        <div>
          <div className="mb-3 flex items-center justify-between gap-3">
            <div>
              <h3 className="font-semibold">{process.title}</h3>
              <p className="text-xs text-slate-400">{process.summary}</p>
            </div>
            <span className="rounded-full bg-amber-50 px-2.5 py-1 text-[11px] font-semibold text-amber-700">REFERÊNCIA · DRAFT</span>
          </div>

          <div className="flex flex-col gap-2" role="list" aria-label={`Etapas do ${process.title}`}>
            {process.nodes.map((node, index) => (
              <div key={node.id} className="flex items-stretch gap-3" role="listitem">
                <div className="flex w-7 shrink-0 flex-col items-center">
                  <span className="grid size-7 place-items-center rounded-full border border-slate-200 bg-slate-50 text-[11px] font-semibold text-slate-500">{index + 1}</span>
                  {index < process.nodes.length - 1 && <span className="mt-1 h-full w-px bg-slate-200" aria-hidden="true" />}
                </div>
                <div className={`mb-2 min-w-0 flex-1 rounded-xl border border-slate-200 px-3 py-3 ${nodeClass(node)}`}>
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="font-medium text-slate-800">{node.label}</div>
                    <span className="rounded-full bg-slate-50 px-2 py-1 text-[10px] font-semibold uppercase tracking-wide text-slate-400">{node.kind}</span>
                  </div>
                  <div className="mt-1 text-[11px] uppercase tracking-wide text-slate-400">{node.status}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <aside className="space-y-4">
          <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Conexões com setores</div>
            <div className="mt-3 flex flex-wrap gap-2">
              {process.connectedSectors.map((sector) => (
                <span key={sector} className="rounded-lg bg-white px-2.5 py-1.5 text-xs text-slate-600 shadow-sm ring-1 ring-slate-200">{sector}</span>
              ))}
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-4">
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Governança da representação</div>
            <div className="mt-3 space-y-2 text-xs leading-5 text-slate-500">
              <div><strong className="text-slate-700">Fonte:</strong> {process.source}</div>
              <div><strong className="text-slate-700">Autoridade:</strong> {process.authority}</div>
              <div><strong className="text-slate-700">Estado:</strong> {process.status}</div>
              <div>Estado atual, evidência e desvio devem vir de dados governados do ELO.</div>
            </div>
          </div>
        </aside>
      </div>
    </section>
  );
}
