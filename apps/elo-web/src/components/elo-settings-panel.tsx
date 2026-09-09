"use client";

import { useEffect, useState } from "react";
import {
  DEFAULT_ELO_SETTINGS,
  loadELOSettings,
  persistELOSettings,
  type ConnectorKind,
  type ELOSettings,
  type ThemeMode,
} from "@/lib/elo-settings";

type Props = {
  open: boolean;
  onClose: () => void;
  onChange: (settings: ELOSettings) => void;
};

const connectorMeta: Record<ConnectorKind, { title: string; description: string; placeholder: string }> = {
  whatsapp: {
    title: "WhatsApp",
    description: "Canal para notificações e mensagens operacionais. O segredo deve ficar no ambiente servidor, nunca no navegador.",
    placeholder: "URL/endpoint do gateway governado",
  },
  discord: {
    title: "Discord",
    description: "Canal para alertas e comunicação. A credencial deve ser armazenada como segredo do ambiente.",
    placeholder: "URL/endpoint ou webhook governado",
  },
};

export function EloSettingsPanel({ open, onClose, onChange }: Props) {
  const [settings, setSettings] = useState<ELOSettings>(DEFAULT_ELO_SETTINGS);

  useEffect(() => {
    if (open) setSettings(loadELOSettings());
  }, [open]);

  if (!open) return null;

  const update = (next: ELOSettings) => {
    setSettings(next);
    persistELOSettings(next);
    onChange(next);
  };

  const setTheme = (theme: ThemeMode) => update({ ...settings, theme });

  const setConnector = (kind: ConnectorKind, patch: Partial<ELOSettings["connectors"][ConnectorKind]>) =>
    update({
      ...settings,
      connectors: {
        ...settings.connectors,
        [kind]: { ...settings.connectors[kind], ...patch },
      },
    });

  return (
    <div className="fixed inset-0 z-[70] flex justify-end bg-slate-950/40 backdrop-blur-sm" role="dialog" aria-modal="true" aria-label="Configurações do ELO">
      <button type="button" aria-label="Fechar configurações" className="absolute inset-0 cursor-default" onClick={onClose} />
      <aside className="relative h-full w-full max-w-xl overflow-y-auto border-l border-slate-200 bg-[var(--elo-panel)] p-6 shadow-2xl">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">ELO / Preferências</p>
            <h2 className="mt-1 text-2xl font-semibold tracking-tight">Configurações</h2>
          </div>
          <button type="button" onClick={onClose} className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-600">Fechar</button>
        </div>

        <section className="mt-8 space-y-4">
          <div className="rounded-2xl border border-slate-200 p-4">
            <h3 className="font-semibold">Interface</h3>
            <p className="mt-1 text-sm text-slate-500">Preferências deste navegador. Elas não alteram regras ou autoridade do ELO.</p>
            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              <button type="button" onClick={() => setTheme(settings.theme === "dark" ? "light" : "dark")} className="flex items-center justify-between rounded-xl border border-slate-200 px-4 py-3 text-left text-sm">
                <span>Modo noturno</span>
                <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold">{settings.theme === "dark" ? "Ativo" : "Desativado"}</span>
              </button>
              <button type="button" onClick={() => update({ ...settings, soundEnabled: !settings.soundEnabled })} className="flex items-center justify-between rounded-xl border border-slate-200 px-4 py-3 text-left text-sm">
                <span>Som de alertas</span>
                <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold">{settings.soundEnabled ? "Ativo" : "Desativado"}</span>
              </button>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 p-4">
            <div>
              <h3 className="font-semibold">Canais de comunicação</h3>
              <p className="mt-1 text-sm text-slate-500">A configuração visual pode ser salva localmente; a conexão efetiva deve passar pelo gateway/connector governado.</p>
            </div>
            <div className="mt-4 space-y-3">
              {(Object.keys(connectorMeta) as ConnectorKind[]).map((kind) => {
                const connector = settings.connectors[kind];
                const meta = connectorMeta[kind];
                return (
                  <div key={kind} className="rounded-xl border border-slate-200 p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <h4 className="font-semibold">{meta.title}</h4>
                        <p className="mt-1 text-xs leading-5 text-slate-500">{meta.description}</p>
                      </div>
                      <button type="button" onClick={() => setConnector(kind, { enabled: !connector.enabled })} className="rounded-full border border-slate-200 px-3 py-1.5 text-xs font-semibold">
                        {connector.enabled ? "Ativo" : "Inativo"}
                      </button>
                    </div>
                    <label className="mt-3 block text-xs font-medium text-slate-500" htmlFor={`${kind}-endpoint`}>Endpoint</label>
                    <input
                      id={`${kind}-endpoint`}
                      value={connector.endpoint ?? ""}
                      onChange={(event) => setConnector(kind, { endpoint: event.target.value, configured: event.target.value.trim().length > 0 })}
                      placeholder={meta.placeholder}
                      className="mt-1 w-full rounded-xl border border-slate-200 bg-transparent px-3 py-2.5 text-sm outline-none focus:ring-2 focus:ring-slate-300"
                    />
                    <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
                      <span>Credencial: {connector.secretConfigured ? "configurada" : "deve ser definida no ambiente servidor"}</span>
                      <span>{connector.configured ? "Endpoint informado" : "Aguardando configuração"}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>
      </aside>
    </div>
  );
}
