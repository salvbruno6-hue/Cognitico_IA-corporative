export type ProcessViewStatus = "REFERENCE" | "CURRENT" | "DEVIATION" | "UNKNOWN";

export type ProcessViewNodeState = {
  status: ProcessViewStatus;
  evidenceCount?: number;
  lastObservedAt?: string | null;
};

export type ProcessViewRequest = {
  viewId: string;
  processId: string;
  tenantScope: string;
  requestedBy: string;
};

export type ProcessViewResponse = {
  viewId: string;
  processId: string;
  source: string;
  authority: "reference" | "canonical";
  generatedAt: string;
  nodes: Record<string, ProcessViewNodeState>;
  evidenceAvailable: boolean;
  operationalStateAvailable: boolean;
  gaps: string[];
};

/**
 * Presentation boundary only. The server must replace the reference projection
 * with governed ELO data before exposing CURRENT/DEVIATION state.
 */
export type ProcessViewProvider = (
  request: ProcessViewRequest,
) => Promise<ProcessViewResponse>;
