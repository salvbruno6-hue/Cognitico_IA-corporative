"use client";

import { useState } from "react";
import { getOperationalSector, operationalSectors, type OperationalSectorId } from "@/lib/operational-sectors";

type Props = { accent: string };

export function OperationalSectorNavigation({ accent }: Props) {
  const [sectorId, setSectorId] = useState<OperationalSectorId>("producao");
  const sector = getOperationalSector(sectorId);

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm" aria-label="Setores operacionais">
      <div className="flex flex-col gap-4 border-b border-slate-100 pb-5">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">Operação conectada</div>
          <h2 className="mt-1 text-xl font-semibold tracking-tight">Produção, abastecimento, qualidade e expedição</h2>
          <p className="mt-2 max-w-4xl text-sm leading-6 text-slate-500">
            Cada setor é apresentado como parte do mesmo fluxo ELO. Estado operacional, indicadores e evidências deverão ser alimentados por contratos governados.
          </p>
        </div>
        <div className="flex flex-wrap gap-2" role="tablist" aria-label="Setores operacionais">
          {operationalSectors.map((item) => {
            const active = item.id === sectorId;
            return (
              <button
                key={item.id}
                type="button"
                role="tab"
                aria-selected={active}
                onClick={() => setSectorId(item.id)}
                className="rounded-xl border px-3 py-2 text-xs font-semibold transition"
                style={active ? { borderColor: accent, backgroundColor: `${accent}12`, color: accent } : undefined}
              >
                {item.label}
              </button>
            );
          })}
        </div>
      </div>

      <div className="mt-5 grid gap-4 xl:grid-cols-[1.25fr_1fr_1fr]">
        <article className="rounded-xl border border-slate-200 bg-slate-50 p-4">
          <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Função</div>
          <h3 className="mt-2 text-lg font-semibold">{sector.label}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-600">{sector.purpose}</p>
          {sector.teams && (
            <div className="mt-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Equipes</div>
              <div className="mt-2 flex flex-wrap gap-2">
                {sector.teams.map((team) => (
                  <span key={team} className="rounded-lg bg-white px-2.5 py-1.5 text-xs font-medium capitalize text-slate-600 ring-1 ring-slate-200">
                    Equipe {team}
                  </span>
                ))}
              </div>
            </div>
          )}
        </article>

        <article className="rounded-xl border border-slate-200 bg-white p-4">
          <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Entradas</div>
          <div className="mt-3 space-y-2">
            {sector.inputs.map((input) => (
              <div key={input} className="rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-600">{input}</div>
            ))}
          </div>
        </article>

        <article className="rounded-xl border border-slate-200 bg-white p-4">
          <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Saídas</div>
          <div className="mt-3 space-y-2">
            {sector.outputs.map((output) => (
              <div key={output} className="rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-600">{output}</div>
            ))}
          </div>
        </article>
      </div>

      <div className="mt-4 rounded-xl border border-slate-200 bg-white p-4">
        <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Conexões</div>
        <div className="mt-3 flex flex-wrap gap-2">
          {sector.connectedSectors.map((item) => (
            <span key={item} className="rounded-lg border border-slate-200 px-3 py-2 text-xs text-slate-600">{item}</span>
          ))}
        </div>
      </div>
    </section>
  );
}
