# ELO Enterprise Method Discovery

## Purpose

Prevent the cognitive layer from imposing generic operating parameters on an organization. ELO must first discover how the tenant actually performs the task, then adapt its capabilities to that method.

## Discovery dimensions

```text
PROCESS
VOCABULARY
DATA SOURCES
RULES
PARAMETERS
FORMULAS
TEMPLATES
UNITS
APPROVALS
EXCEPTIONS
OUTPUT FORMAT
HISTORICAL OUTCOMES
```

## Operating rule

`OBSERVE -> MODEL -> EXECUTE -> VERIFY -> LEARN -> PROPOSE`

The sequence must not become `ASSUME -> STANDARDIZE -> OVERRIDE`.

## Budget example

The budget engine must inspect representative enterprise budgets before defining its domain schema. It should identify actual columns, item identifiers, units, quantity conventions, composition methods, price sources, loss/excess treatment, taxes, margins, approvals, revisions and final deliverables. If a parameter is not used by the tenant, ELO must not silently introduce it into the operational calculation.

A useful external technique can improve the cognitive mechanism without replacing the tenant method.

## Adaptation classes

- `OBSERVED`: directly evidenced in tenant operations;
- `LEARNED`: inferred from repeated tenant experience;
- `PROPOSED`: suggested improvement awaiting acceptance;
- `EXTERNAL`: external knowledge available for comparison or experimentation.

## Learning boundary

Tenant observations can improve tenant execution. Only independently generalizable, non-private principles may be proposed for canonical evolution, and every such proposal requires evidence and governance.

## General applicability

This discovery mechanism applies to every ELO capability, including database research, model selection, calculation, document generation, spreadsheet interaction, procurement, engineering workflows, automation and future domains.
