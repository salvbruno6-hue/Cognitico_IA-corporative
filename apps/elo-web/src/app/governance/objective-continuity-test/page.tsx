"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { callELOAuthorization } from "@/auth/eloAuthorization";

type TestResult = {
  authorized?: boolean;
  code?: string;
  reason?: string;
  objective_id?: string;
  workstream_id?: string;
  operation?: string;
  grant?: {
    authorization_state?: string;
    grant_id?: string;
    expires_at?: string;
    authorization_authority?: string;
  };
  cycle?: {
    decision?: string;
    checkpoint_version?: number;
    progress_token?: string;
    next_action?: string;
    human_required?: boolean;
    should_continue_automatically?: boolean;
    authorization_authority?: string;
    authorization_evidence_ref?: string;
    next_trigger?: unknown;
    final_message?: string;
  };
};

function getSupabaseClient() {
  try { return createClient(); } catch { return null; }
}

export default function ObjectiveContinuityTestPage() {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [ready, setReady] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<TestResult | null>(null);

  useEffect(() => {
    let live = true;
    const supabase = getSupabaseClient();
    if (!supabase) {
      setError("Cliente Supabase do ELO não está configurado.");
      return () => { live = false; };
    }
    void supabase.auth.getSession().then(async ({ data, error: sessionError }) => {
      if (!live) return;
      if (sessionError || !data.session) {
        setError("Sessão ELO ausente. Abra o ELO principal e autentique-se primeiro.");
        return;
      }
      try {
        await callELOAuthorization(data.session.access_token, "establish_session");
        if (!live) return;
        setAccessToken(data.session.access_token);
        setReady(true);
      } catch (authorizationError) {
        if (live) setError(authorizationError instanceof Error ? authorizationError.message : "Não foi possível validar a sessão ELO.");
      }
    });
    return () => { live = false; };
  }, []);

  async function runTest() {
    if (!accessToken || busy) return;
    setBusy(true);
    setError(null);
    setResult(null);
    try {
      const response = await fetch("/api/elo/admin/objective-continuity-test", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
        cache: "no-store",
      });
      const payload = await response.json().catch(() => null) as TestResult | null;
      if (!response.ok || !payload) {
        throw new Error(payload?.reason || payload?.code || "O teste governado não pôde ser concluído.");
      }
      setResult(payload);
    } catch (runError) {
      setError(runError instanceof Error ? runError.message : "Falha ao executar o teste governado.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-slate-100">
      <section className="mx-auto max-w-4xl rounded-3xl border border-white/10 bg-white/[0.04] p-7 shadow-2xl">
        <div className="flex flex-col justify-between gap-4 md:flex-row md:items-start">
          <div>
            <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">ELO · Governança</div>
            <h1 className="mt-2 text-2xl font-semibold">Teste real · Objective Continuity</h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">Este harness não cria autoridade. Ele usa sua sessão autenticada, solicita um grant curto ao elo-authz e executa um ciclo no endpoint canônico de prefinalização.</p>
          </div>
          <a href="/" className="rounded-xl border border-white/10 px-4 py-2 text-sm text-slate-300 hover:bg-white/5">Voltar ao ELO</a>
        </div>

        <div className="mt-6 grid gap-3 sm:grid-cols-3">
          <div className="rounded-2xl border border-white/10 p-4"><div className="text-xs text-slate-500">Sessão</div><div className="mt-1 font-semibold">{ready ? "CANONICAL_ADMIN validada" : "Aguardando"}</div></div>
          <div className="rounded-2xl border border-white/10 p-4"><div className="text-xs text-slate-500">Grant</div><div className="mt-1 font-semibold">elo-execution-authorized · 5 min</div></div>
          <div className="rounded-2xl border border-white/10 p-4"><div className="text-xs text-slate-500">Limite</div><div className="mt-1 font-semibold">1 ciclo por acionamento</div></div>
        </div>

        {error && <div className="mt-5 rounded-2xl border border-rose-500/20 bg-rose-500/10 p-4 text-sm text-rose-200" role="alert">{error}</div>}

        <button type="button" onClick={() => void runTest()} disabled={!ready || busy} className="mt-6 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-950 disabled:cursor-not-allowed disabled:opacity-40">
          {busy ? "Executando pelo ELO…" : "Executar teste governado"}
        </button>

        {result && <section className="mt-7 space-y-4">
          <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/10 p-5">
            <div className="text-xs font-semibold uppercase tracking-[0.16em] text-emerald-300">Ciclo executado</div>
            <div className="mt-2 text-xl font-semibold">{result.cycle?.decision ?? "SEM DECISÃO"}</div>
            <div className="mt-2 text-sm text-emerald-100/80">Checkpoint {result.cycle?.checkpoint_version ?? "—"} · continuidade automática {String(result.cycle?.should_continue_automatically ?? false)}</div>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <article className="rounded-2xl border border-white/10 p-5"><h2 className="font-semibold">Autorização</h2><dl className="mt-3 space-y-2 text-sm text-slate-300"><div><dt className="text-slate-500">Estado</dt><dd>{result.grant?.authorization_state ?? "—"}</dd></div><div><dt className="text-slate-500">Autoridade</dt><dd>{result.grant?.authorization_authority ?? "—"}</dd></div><div><dt className="text-slate-500">Expira</dt><dd>{result.grant?.expires_at ?? "—"}</dd></div></dl></article>
            <article className="rounded-2xl border border-white/10 p-5"><h2 className="font-semibold">Handoff</h2><dl className="mt-3 space-y-2 text-sm text-slate-300"><div><dt className="text-slate-500">Objetivo</dt><dd>{result.objective_id ?? "—"}</dd></div><div><dt className="text-slate-500">Próxima ação</dt><dd>{result.cycle?.next_action ?? "—"}</dd></div><div><dt className="text-slate-500">Evidência authz</dt><dd className="break-all">{result.cycle?.authorization_evidence_ref ?? "—"}</dd></div></dl></article>
          </div>
          {result.cycle?.final_message && <pre className="whitespace-pre-wrap rounded-2xl border border-white/10 bg-black/20 p-5 text-sm leading-6 text-slate-300">{result.cycle.final_message}</pre>}
        </section>}
      </section>
    </main>
  );
}
