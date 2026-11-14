"use client";

import { useState } from "react";
import { callELOAuthorization } from "@/auth/eloAuthorization";

const REPOSITORY = "salvbruno6-hue/Cognitico_IA-corporative";
const SHA_PATTERN = /^[0-9a-f]{40}$/i;

export function ELOAdminGrantPanel({ accessToken }: { accessToken: string }) {
  const [bindingId, setBindingId] = useState("");
  const [pr, setPr] = useState("");
  const [sha, setSha] = useState("");
  const [duration, setDuration] = useState(300);
  const [confirmed, setConfirmed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState("");
  const valid = bindingId.trim().length > 0 && /^[1-9][0-9]*$/.test(pr) && SHA_PATTERN.test(sha) && duration >= 60 && duration <= 3600 && confirmed;

  async function issueGrant() {
    if (!valid || busy) return;
    setBusy(true);
    setResult("");
    try {
      const response = await callELOAuthorization(accessToken, "issue_authorization_grant", {
        repository: REPOSITORY,
        binding_id: bindingId.trim(),
        authorization_state: "elo-merge-authorized",
        operation: `merge_pr:${pr}:${sha.toLowerCase()}`,
        resource_id: sha.toLowerCase(),
        expires_in_seconds: duration,
      });
      const issuedGrant = response.grant as { grant_id?: string; expires_at?: string } | undefined;
      setResult(`Grant emitido pelo elo-authz: ${issuedGrant?.grant_id ?? "ID indisponível"}; expira em ${issuedGrant?.expires_at ?? "horário não informado"}. A emissão não executa merge.`);
      setConfirmed(false);
    } catch (error) {
      setResult(`Autorização recusada: ${error instanceof Error ? error.message : "erro desconhecido"}`);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="rounded-2xl border border-slate-200 bg-[var(--elo-panel)] p-5 shadow-sm" aria-label="Autorização administrativa canônica">
      <h2 className="font-semibold">Autorização administrativa de merge</h2>
      <p className="mt-2 text-sm text-slate-500">Emissão pela autoridade existente elo-authz. Somente CANONICAL_ADMIN com sessão ativa e escopo válido pode autorizar. Confirme a revisão independente e os gates no GitHub antes de emitir.</p>
      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <label className="text-sm">Binding ID ativo<input className="mt-1 w-full rounded-lg border p-2" value={bindingId} onChange={e => setBindingId(e.target.value)} placeholder="UUID do vínculo existente" /></label>
        <label className="text-sm">Número da PR<input className="mt-1 w-full rounded-lg border p-2" inputMode="numeric" value={pr} onChange={e => setPr(e.target.value)} placeholder="1233" /></label>
        <label className="text-sm">SHA exato da PR<input className="mt-1 w-full rounded-lg border p-2 font-mono text-xs" value={sha} onChange={e => setSha(e.target.value.trim())} placeholder="40 caracteres hexadecimais" /></label>
        <label className="text-sm">Validade (segundos, 60–3600)<input className="mt-1 w-full rounded-lg border p-2" type="number" min={60} max={3600} value={duration} onChange={e => setDuration(Number(e.target.value))} /></label>
      </div>
      <label className="mt-4 flex items-start gap-2 text-sm"><input type="checkbox" checked={confirmed} onChange={e => setConfirmed(e.target.checked)} />Revisei os gates e confirmei aprovação independente para este SHA específico.</label>
      <button type="button" disabled={!valid || busy} onClick={() => void issueGrant()} className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:opacity-40">{busy ? "Validando no ELO…" : "Solicitar grant canônico"}</button>
      {result && <p role="status" className="mt-3 break-words text-sm">{result}</p>}
      <p className="mt-3 text-xs text-slate-500">Este formulário não cria bindings, não armazena tokens e não realiza merge. A API valida identidade, papel, sessão, repositório e vínculo no servidor.</p>
    </section>
  );
}
