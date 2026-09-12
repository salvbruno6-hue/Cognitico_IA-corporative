"use client";

import { useId, useState } from "react";
import type { CognitiveResponse } from "@/lib/elo-cognitive";

type Props = {
  accessToken: string;
  sector: string;
  domain: string;
  workspace: string;
  activeSurface: string;
  onResult: (result: CognitiveResponse) => void;
  onNotice: (notice: string | null) => void;
  onBusyChange: (busy: boolean) => void;
};

const RUNTIME_PROBE_MESSAGE = "Executar probe governado do runtime Hermes e retornar Evidence/Outcome.";

export function GovernedMissionPanel({
  accessToken,
  sector,
  domain,
  workspace,
  activeSurface,
  onResult,
  onNotice,
  onBusyChange,
}: Props) {
  const inputId = useId();
  const [mission, setMission] = useState("");
  const [runtimeProbe, setRuntimeProbe] = useState(false);

  async function submit(message: string, probe = false) {
    const request = message.trim();
    if (!request) {
      onNotice("Descreva a missão antes de enviar.");
      return;
    }

    onBusyChange(true);
    onNotice(null);

    try {
      const context: Record<string, unknown> = {
        sector,
        surface: activeSurface,
        workspace,
        source: "elo-web",
      };

      if (probe) {
        context.hermes_mission = {
          mission_class: "runtime_probe",
          authorized_capabilities: ["hermes:runtime_probe"],
          method: "runtime_probe",
          constraints: {
            read_only: true,
            bounded: true,
            no_canonical_mutation: true,
          },
          evidence_requirements: ["execution", "outcome"],
        };
      }

      const response = await fetch("/api/cognitive", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        cache: "no-store",
        body: JSON.stringify({
          message: request,
          tenant_id: process.env.NEXT_PUBLIC_ELO_TENANT_ID?.trim() || "multiteiner",
          domain,
          context,
        }),
      });

      const payload = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(
          typeof payload?.message === "string"
            ? payload.message
            : "O ELO não conseguiu processar a missão.",
        );
      }

      onResult(payload as CognitiveResponse);
      setMission("");
      setRuntimeProbe(false);
      onNotice(
        probe
          ? "Probe Hermes encaminhada pelo boundary cognitivo. Nenhuma mutação canônica foi autorizada."
          : "Missão processada pelo ELO Cognitivo.",
      );
    } catch (error) {
      onNotice(error instanceof Error ? error.message : "Não foi possível processar a missão.");
    } finally {
      onBusyChange(false);
    }
  }

  return (
    <section
      aria-labelledby={`${inputId}-title`}
      className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-4 shadow-sm sm:p-5"
    >
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <h3 id={`${inputId}-title`} className="font-semibold text-slate-900">
              Missão ELO
            </h3>
            <span className="rounded-full border border-slate-200 px-2 py-1 text-[10px] font-semibold uppercase tracking-wide text-slate-500">
              Governada
            </span>
          </div>
          <p className="mt-1 text-xs leading-5 text-slate-500">
            Intenção → Cognitivo → Symbiont → Hermes → Evidence/Outcome. O browser não acessa o runtime diretamente.
          </p>
        </div>

        <button
          type="button"
          aria-pressed={runtimeProbe}
          onClick={() => setRuntimeProbe((value) => !value)}
          className={`min-h-10 shrink-0 rounded-xl border px-3 py-2 text-xs font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-500 focus-visible:ring-offset-2 ${
            runtimeProbe
              ? "border-slate-900 bg-slate-900 text-white"
              : "border-slate-200 bg-white text-slate-700 hover:border-slate-300"
          }`}
        >
          {runtimeProbe ? "Probe Hermes selecionado" : "Testar Hermes"}
        </button>
      </div>

      {runtimeProbe && (
        <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-4">
          <div className="flex items-center justify-between gap-3">
            <div>
              <div className="text-xs font-semibold text-slate-800">runtime_probe</div>
              <p className="mt-1 text-xs leading-5 text-slate-500">
                Somente leitura · capacidade pré-autorizada · Evidence/Outcome obrigatórios · sem mutação canônica.
              </p>
            </div>
            <span className="rounded-full bg-white px-2 py-1 text-[10px] font-semibold text-slate-500">
              READ ONLY
            </span>
          </div>
          <button
            type="button"
            onClick={() => void submit(RUNTIME_PROBE_MESSAGE, true)}
            className="mt-3 min-h-10 rounded-lg bg-slate-900 px-3 py-2 text-xs font-semibold text-white transition hover:bg-slate-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-500 focus-visible:ring-offset-2"
          >
            Executar probe
          </button>
        </div>
      )}

      <form
        className="mt-4 flex flex-col gap-2 rounded-xl border border-slate-200 bg-slate-50 p-2 sm:flex-row"
        onSubmit={(event) => {
          event.preventDefault();
          void submit(mission);
        }}
      >
        <label htmlFor={inputId} className="sr-only">
          Missão para {sector}
        </label>
        <input
          id={inputId}
          value={mission}
          onChange={(event) => setMission(event.target.value)}
          maxLength={1000}
          placeholder={`Solicite algo para ${sector.toLowerCase()}…`}
          className="min-h-10 min-w-0 flex-1 rounded-lg bg-transparent px-2 text-sm text-slate-900 outline-none placeholder:text-slate-400 focus-visible:ring-2 focus-visible:ring-slate-300"
        />
        <button
          type="submit"
          disabled={!mission.trim()}
          className="min-h-10 rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-500 focus-visible:ring-offset-2"
        >
          Enviar missão
        </button>
      </form>

      <div className="mt-4 grid grid-cols-1 gap-2 text-xs text-slate-500 sm:grid-cols-3">
        <div className="rounded-lg bg-slate-50 p-3">Browser → API Cognitive</div>
        <div className="rounded-lg bg-slate-50 p-3">Symbiont → Hermes</div>
        <div className="rounded-lg bg-slate-50 p-3">Evidence → Evolution Gate</div>
      </div>
    </section>
  );
}
