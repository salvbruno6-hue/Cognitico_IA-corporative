import { describe, expect, it } from "vitest";
import { processes } from "@/lib/processes";

describe("process navigation model", () => {
  it("exposes the initial planning processes from the canonical reference", () => {
    expect(processes.map((process) => process.id)).toEqual(["planning-demand", "planning-modular"]);
    expect(processes.every((process) => process.source === "ELO-PROC-MULTITEINER-001")).toBe(true);
  });

  it("keeps process state separate from current operational telemetry", () => {
    expect(processes.every((process) => process.status === "draft")).toBe(true);
    expect(processes.flatMap((process) => process.nodes).every((node) => node.status === "REFERENCE" || node.status === "A_VALIDAR")).toBe(true);
  });
});
