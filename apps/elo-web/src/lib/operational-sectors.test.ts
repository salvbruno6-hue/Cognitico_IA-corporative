import { describe, expect, it } from "vitest";
import { operationalSectors } from "@/lib/operational-sectors";

describe("operational sector model", () => {
  it("includes the missing operational sectors", () => {
    expect(operationalSectors.map((sector) => sector.id)).toEqual([
      "producao",
      "almoxarifado",
      "compras",
      "qualidade",
      "expedicao",
    ]);
  });

  it("keeps production split between internal and external teams", () => {
    const production = operationalSectors.find((sector) => sector.id === "producao");
    expect(production?.teams).toEqual(["interna", "externa"]);
  });

  it("preserves cross-sector interfaces", () => {
    const names = operationalSectors.flatMap((sector) => sector.connectedSectors);
    expect(names).toContain("PCP");
    expect(names).toContain("Qualidade");
    expect(names).toContain("Expedição");
    expect(names).toContain("Almoxarifado");
  });
});
