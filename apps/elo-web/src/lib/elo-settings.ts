export type ThemeMode = "light" | "dark";

export type ConnectorKind = "whatsapp" | "discord";

export type ConnectorSettings = {
  enabled: boolean;
  configured: boolean;
  label: string;
  endpoint?: string;
  secretConfigured?: boolean;
};

export type ELOSettings = {
  theme: ThemeMode;
  soundEnabled: boolean;
  notificationsEnabled: boolean;
  connectors: Record<ConnectorKind, ConnectorSettings>;
};

export const DEFAULT_ELO_SETTINGS: ELOSettings = {
  theme: "light",
  soundEnabled: true,
  notificationsEnabled: true,
  connectors: {
    whatsapp: {
      enabled: false,
      configured: false,
      label: "WhatsApp",
      secretConfigured: false,
    },
    discord: {
      enabled: false,
      configured: false,
      label: "Discord",
      secretConfigured: false,
    },
  },
};

const STORAGE_KEY = "elo-web-settings-v1";

export function loadELOSettings(): ELOSettings {
  if (typeof window === "undefined") return DEFAULT_ELO_SETTINGS;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return DEFAULT_ELO_SETTINGS;
    const parsed = JSON.parse(raw) as Partial<ELOSettings>;
    return {
      ...DEFAULT_ELO_SETTINGS,
      ...parsed,
      connectors: {
        ...DEFAULT_ELO_SETTINGS.connectors,
        ...(parsed.connectors ?? {}),
      },
    };
  } catch {
    return DEFAULT_ELO_SETTINGS;
  }
}

export function persistELOSettings(settings: ELOSettings) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
}
