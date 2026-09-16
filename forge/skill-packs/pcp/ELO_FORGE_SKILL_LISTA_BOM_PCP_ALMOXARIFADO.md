# ELO-FORGE — Skill: Lista BOM → PCP → Almoxarifado

**Skill ID:** `ELO-FORGE-PCP-BOM-ALMOX-001`  
**Domain family:** `PCP`  
**Related domains:** `PROCUREMENT`, `LOGISTICS`, `DATA_ANALYSIS`  
**Maturity:** `DEFINED`  
**Version:** `1.0.0`  
**Status:** `FORGE_CANDIDATE`  
**Authority:** Forge construction; canonical production authority remains `mt_*` after validation/promotion.

## 1. Purpose

Define the governed behavior for using `lista_bom` as the material-requirement layer that transforms kit composition into planned material demand for PCP and the corresponding request/separation need for Almoxarifado.

The purpose is not merely to catalog materials. The skill must answer:

> Given the production plan for a model/module and its kits, how much of each material/component is required in the planning period, how much is already available/reserved, and what remains to be supplied to production?

## 2. Scope

Applies to modular/container production, including standard and configured models, and to kits such as:

- Kit Estrutura;
- Kit Montagem;
- Kit Elétrico;
- Kit Hidrossanitário;
- other validated production kits.

The skill covers the transformation:

`MODELO → KIT → KIT_ITENS → LISTA_BOM → DEMANDA PCP → NECESSIDADE → ALMOXARIFADO / COMPRAS`

## 3. Technical boundaries

- `lista_mae` remains the master catalog of items/materials.
- `kit_itens` remains the composition/link between a kit and its items.
- `lista_bom` is the planning/explosion layer for production material requirements.
- `lista_bom` must not become a second master material catalog.
- `lista_bom` must not create a parallel PCP authority outside the `mt_*` architecture.
- Existing tables must be reused/consolidated where compatible; duplicate production structures must not be created.
- No consumption, time, capacity, stock, cost or productivity value may be invented.

## 4. Prerequisites

Before calculating requirements, the system must have, to the degree required by the calculation:

1. a valid production model;
2. a valid kit associated with the model/configuration;
3. validated kit items;
4. a master item/material reference in `lista_mae` where applicable;
5. a production quantity and planning period;
6. unit of measure;
7. validated consumption per module/unit;
8. stock and reservation information when netting against inventory.

Missing information remains `GAP` and blocks automatic calculation of the affected line.

## 5. Authorized inputs

- Model/product;
- production quantity planned for the period;
- kit;
- kit item;
- consumption per module/unit;
- unit of measure;
- available stock;
- reserved stock;
- already allocated production quantity;
- validated safety/coverage parameters, if they exist in the authoritative PCP model.

## 6. Authorized sources and provenance

Primary sources:

- `lista_mae`;
- `kits`;
- `kit_itens`;
- authoritative `mt_*` PCP/production structures;
- validated stock/inventory structures;
- validated production demand/plan.

Every imported or migrated value must preserve provenance. Historical values must not be silently overwritten.

## 7. Core procedure

### 7.1 Determine planned production

Example structure:

`MLT.M01 = 15 modules × 4 weekly cycles = 60 modules in the planning period`

The numerical example is illustrative only and must not be stored as a company standard unless separately validated.

### 7.2 Explode kit consumption

For each applicable kit item:

`gross_requirement = planned_quantity × consumption_per_unit`

Example concept:

`60 M01 × 1 quadro elétrico/M01 = 60 quadros elétricos`

For a cable:

`60 M01 × validated_meters_of_cable_per_M01 = required meters`

If the material is managed in rolls/reels, the system must not assume a roll length. It must use the validated packaging/roll conversion for that item.

### 7.3 Net against inventory

When stock data is authorized:

`net_requirement = gross_requirement − available_stock − applicable_reserved_stock`

The exact treatment of reservations, quarantine, blocked stock and safety stock must follow the authoritative inventory/PCP rules.

### 7.4 Generate PCP/Almoxarifado requirement

The result must distinguish at least:

- gross requirement;
- available stock;
- reserved/allocated quantity;
- net requirement;
- unit;
- source kit;
- source model;
- planning period;
- status/evidence.

The operational consequence is a material requirement that PCP can send to Almoxarifado for separation/availability and, where applicable, to Procurement for replenishment.

## 8. Evidence handling

Each calculation line must be classified according to available evidence:

- `FACT`: validated source value;
- `COMMITMENT`: approved production/demand commitment;
- `AVAILABILITY`: stock physically/systemically available;
- `ASSUMPTION`: explicitly identified assumption;
- `ESTIMATE`: estimate, never represented as fact;
- `HYPOTHESIS`: testable hypothesis;
- `GAP`: required information unavailable;
- `CONFLICT`: incompatible authoritative evidence requiring arbitration.

A GAP or CONFLICT must not be silently converted into a quantity.

## 9. Decision boundaries

The skill may calculate and expose material requirements. It may not autonomously:

- alter the master material catalog;
- redefine kit composition;
- invent consumption factors;
- invent roll/packaging conversion;
- change stock balances;
- approve purchases;
- change the canonical PCP architecture;
- promote a Forge candidate to Core.

Such changes require the appropriate authoritative process and, when architectural ambiguity exists, user arbitration.

## 10. Required conceptual data relationship

```text
LISTA_MAE
   │
   └── master item/material
          │
          ▼
      KIT_ITENS
          │
          └── item + consumo por unidade
                    │
                    ▼
                LISTA_BOM
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   DEMANDA / PLANO PCP     ESTOQUE
          │                   │
          └─────────┬─────────┘
                    ▼
            NECESSIDADE LÍQUIDA
                    │
             ┌──────┴──────┐
             ▼             ▼
       ALMOXARIFADO     COMPRAS
```

## 11. Example of expected behavior

For an MLT.M01 electrical kit, if the validated BOM states a certain consumption of cable 2.5 mm² per module and one validated electrical panel per module, and the PCP plan is 60 M01 for the period, the skill calculates:

- required cable = `60 × validated cable consumption per M01`;
- required electrical panels = `60 × validated panels per M01`;
- other electrical components = `60 × their validated consumption per M01`.

If inventory contains part of the requirement, the net requirement is calculated using the authoritative stock/reservation rules.

The skill must never infer how many meters are on a cable roll merely from the phrase “rolo”. Packaging conversion must come from a validated source.

## 12. Uncertainty and escalation

Escalate when:

- a kit has no validated item composition;
- an item has no validated consumption;
- units are incompatible;
- packaging/roll conversion is missing;
- stock source conflicts with another authoritative source;
- the same item appears with conflicting consumption factors;
- it is unclear which `mt_*` table is authoritative for a specific PCP relation.

In the last case, do not create or alter the relationship automatically. Present the ambiguity and request arbitration.

## 13. Outputs

The skill should produce a traceable requirement set suitable for PCP and Almoxarifado, with:

`model → kit → item → consumption/unit → planned quantity → gross requirement → stock/reservation → net requirement → unit → provenance → status`

## 14. Test references

Initial tests to be defined in the Forge construction line:

1. single model / single kit / single item;
2. multiple kit items;
3. monthly production explosion;
4. unit conversion;
5. stock netting;
6. reserved stock netting;
7. missing consumption = GAP;
8. missing roll conversion = GAP;
9. conflicting consumption = CONFLICT;
10. traceability from requirement back to kit and master item.

No test result is considered empirical validation until executed against validated data.

## 15. Contextual company overlay

Multiteiner production context:

- kits represent what composes the module;
- production/operation structures represent what must be executed;
- labor/resources execute operations;
- `lista_bom` represents the material-demand explosion required to support PCP execution and Almoxarifado supply.

This overlay is contextual and is not, by itself, a generalized Core rule.

## 16. Learning candidates

Potential future learning candidates, only after empirical validation:

- recurring consumption deviations by model/kit;
- systematic material shortages;
- recurrent packaging/roll conversion patterns;
- forecast-vs-actual material consumption;
- recurring kit completeness failures.

## 17. Promotion candidates

No direct promotion to Core is authorized by this file.

A candidate may be proposed only after:

`SOURCE → EVIDENCE → FORGE SKILL → TEST → EMPIRICAL VALIDATION → CONTEXTUAL EXPERIENCE → GENERALIZATION → EVOLUTION GATE`

## 18. Historical lineage

This skill records the arbitrated requirement that the BOM layer must transform kit composition into PCP material demand and an Almoxarifado supply signal. It does not authorize immediate database schema changes. Physical schema reconciliation remains a separate validation step.
