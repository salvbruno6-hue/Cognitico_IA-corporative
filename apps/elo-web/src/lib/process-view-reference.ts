import type { ProcessViewRequest, ProcessViewResponse } from "./process-view-contract";

/**
 * Temporary structural adapter for the existing canonical process reference.
 * It must not be interpreted as live operational telemetry.
 */
export function buildReferenceProcessView(request: ProcessViewRequest): ProcessViewResponse {
  return {
    viewId: request.viewId,
    processId: request.processId,
    source: "ELO-PROC-MULTITEINER-001",
    authority: "reference",
    generatedAt: new Date().toISOString(),
    nodes: {},
    evidenceAvailable: false,
    operationalStateAvailable: false,
    gaps: [
      "Governed ELO process/view API contract not connected yet",
      "Current operational state unavailable",
      "Evidence state unavailable",
    ],
  };
}
