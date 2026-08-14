# ELO-ORG Test Matrix

## Objective

Prove that ELO-ORG is a bounded organizational member, not a second Cognitive Core, and that its structural assertions can be safely consumed by ELO.

## Contract tests

| ID | Scenario | Expected |
|---|---|---|
| ORG-001 | member identity/version | PASS when stable identity and version are returned |
| ORG-002 | capability discovery | PASS when only declared capabilities are exposed |
| ORG-003 | provenance required | BLOCKED when a structural assertion has no provenance |
| ORG-004 | tenant isolation | BLOCKED on unauthorized cross-tenant access |
| ORG-005 | domain scope | BLOCKED on unauthorized cross-domain access |
| ORG-006 | conflicting structural assertion | CONFLICTING; never silently overwrite |
| ORG-007 | temporal validity | PASS only when effective interval is respected |
| ORG-008 | unavailable member | BLOCKED; no synthetic PASS |
| ORG-009 | malformed result | BLOCKED; no silent coercion |
| ORG-010 | contract incompatibility | BLOCKED until compatible version/migration exists |

## Organizational-model tests

| ID | Scenario | Expected |
|---|---|---|
| ORG-011 | Commercial vs Licitações | distinct domains and semantics |
| ORG-012 | Licitações -> Orçamento | explicit requirement relation |
| ORG-013 | Comercial -> Orçamento | explicit commercial request relation |
| ORG-014 | Orçamento -> Projeto | cost/technical dependency represented without collapsing domains |
| ORG-015 | Projeto -> Produção | production dependency preserved |
| ORG-016 | Compras -> Produção | supply dependency preserved |
| ORG-017 | PCP -> Produção | planning/programming relationship preserved |
| ORG-018 | Produção -> Logística | fulfillment/dispatch relationship preserved |
| ORG-019 | Result -> Learning | outcome is evidence for evolution, not structural ownership |
| ORG-020 | full cross-domain chain | all relations retain source, target, type, provenance and validity |

## Acceptance rule

Documentation alone cannot mark a scenario PASS. A scenario becomes PASS only after executable or independently reproducible evidence is attached. `DEFINED` is not `PASS`.
