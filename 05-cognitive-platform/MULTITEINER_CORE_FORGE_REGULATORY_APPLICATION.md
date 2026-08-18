# ELO — Multiteiner Core → Forge Regulatory Application Contract

## Status
NORMATIVE DESIGN CONTRACT — pending formal ADR approval if required by repository governance

## 1. Objective

Transform regulatory knowledge into a controlled application model for Multiteiner projects without allowing implementation to redefine the normative meaning.

## 2. Core responsibilities

The Core must:

1. identify the work/product context;
2. identify jurisdiction;
3. identify occupancy/use;
4. identify construction stage;
5. identify systems present;
6. identify worker activities and hazards;
7. determine applicable NRs;
8. determine applicable ABNT standards;
9. determine applicable fire authority requirements;
10. determine accessibility requirements;
11. determine municipal/state requirements;
12. identify conflicts and dependencies;
13. classify each rule by authority;
14. preserve source and version;
15. produce an application contract for Forge;
16. refuse unsupported conclusions when evidence is insufficient.

## 3. Forge responsibilities

Forge must:

- instantiate the application contract;
- calculate quantities/dimensions;
- evaluate alternative layouts;
- run deterministic validation rules;
- check drawings and project parameters;
- produce checklists;
- collect evidence;
- run tests;
- report deviations;
- never silently alter the Core rule;
- escalate ambiguity or conflict back to Core.

## 4. Regulatory application matrix

| Project object | Primary sources | Secondary/related sources | Typical Forge action |
|---|---|---|---|
| Module used as workplace | NR-01, NR-08, NR-18 | NR-17, NR-24, NBR 9050, fire rules | classify use and validate base requirements |
| Construction site installation | NR-18, NR-24 | NR-10, NR-23, NR-26 | site checklist |
| Electrical installation | NR-10 | NBR 5410, NBR 5419, local utility | circuit/protection/documentation checks |
| Grounding | NR-10 | NBR 5410, NBR 5419 | verify grounding/equipotentialization design |
| SPDA | NR-18 where applicable to construction site | NBR 5419 series, local fire/building rules | verify risk analysis/design/evidence |
| Accessible module | accessibility law | NBR 9050, NBR 16537, local rules | route/accessibility validation |
| Accessible toilet | accessibility law | NBR 9050, NR-24 | layout and fixture validation |
| Circulation corridor | NBR 9050 / fire rules / NR-18 depending context | NR-24, project criteria | determine applicable dimension rather than use one universal value |
| Kitchen | NR-24 | NBR 14518, NBR 9050, fire/gas/sanitary rules | layout, ventilation, access, safety |
| Refectory | NR-24 | accessibility/fire/local sanitary rules | capacity/layout validation |
| Vestiary | NR-24 | NBR 9050, fire rules | area/equipment/layout validation |
| Sanitary facilities | NR-24 | NBR 9050, NBR 8160, NBR 5626 | count/layout/hydraulic checks |
| Water supply | NR-24 where applicable | NBR 5626, concessionaire rules | hydraulic design check |
| Sewage | NR-24 where applicable | NBR 8160, local sanitation | drainage/layout check |
| Rainwater | project/building requirements | NBR 10844, local drainage rules | roof drainage calculation |
| Emergency exit | NR-23 / applicable fire regulation | NBR 9077, NBR 10898, NBR 13434 | route and emergency systems validation |
| Fire extinguishers | NR-23 / local fire regulation | NBR 12693 | equipment selection/location check |
| Fire detection/alarm | local fire regulation | NBR 17240 | system validation when required |
| Hydrants/mangotinhos | local fire regulation | NBR 13714 | hydraulic/fire-system validation when required |
| Emergency plan | local fire regulation / organizational requirements | NBR 15219 | document/evidence check |
| Structural module | NR-18 where construction applies | NBR 6120, 6123, 8681, 8800, 6118, 6122 | structural project validation |
| Lifting/mounting | NR-11, NR-18 | equipment/manufacturer requirements | lift plan/checklist |
| Work at height | NR-35, NR-18 | project/access systems | fall-protection validation |
| Machines | NR-12 | NR-10, NR-17, NR-26 | machine safety checklist |
| PPE | NR-06 | risk assessment/NR-01 | PPE matrix/evidence |
| Ergonomic workplace | NR-17 | NBR 9050 where accessibility applies | workstation/layout evaluation |

## 5. Example — electrical module

Input:

```text
product = modular building
use = workplace
voltage = low voltage
location = identified municipality/state
installation = fixed or temporary as classified
metal structure = yes/no
SPDA = applicable/under evaluation
```

Core output:

```text
NR-10 = applicable
NBR 5410 = applicable to low-voltage installation
NBR 5419 = evaluate/apply according to lightning-protection scope and current edition
local utility requirements = verify
fire requirements = verify where applicable
```

Forge output:

```text
- single-line diagram check
- circuit protection check
- conductor/installation check
- grounding/equipotentialization check
- SPD/interface check
- identification/signage check
- inspection/test evidence
```

## 6. Example — accessible module

Core must first identify whether the module/space is subject to accessibility requirements.

Forge then validates, according to the applicable standard/project:

- accessible route;
- access door;
- circulation;
- turning/approach areas;
- ramp where required;
- accessible sanitary fixture layout;
- grab bars and accessories where applicable;
- visual/tactile signage where required;
- connection to accessible external route.

The Forge must not reduce accessibility to “wheelchair width”.

## 7. Example — kitchen

Core classification:

```text
use = professional kitchen / food preparation
workers = known
public = yes/no
food preparation = yes
cooking equipment = yes/no
gas = yes/no
exhaust = yes
```

Potential source set:

```text
NR-24
NBR 14518
NBR 9050 when accessibility applies
NR-10 + NBR 5410 for electrical installation
NBR 5626 / 8160 for water/sewage
fire regulation + applicable fire NBRs
local sanitary regulation
local gas/concessionaire rules when gas exists
```

Forge must calculate/check each subsystem independently and then run an integrated conflict check.

## 8. Integrated validation rule

A module is not considered “compliant” merely because every isolated checklist is green.

The Forge must perform:

```text
individual requirements
        ↓
integrated layout
        ↓
accessibility check
        ↓
fire/egress check
        ↓
electrical/hydraulic/gas interfaces
        ↓
structural interfaces
        ↓
operational circulation
        ↓
jurisdictional requirements
        ↓
professional review
        ↓
FINAL STATUS
```

## 9. Conflict examples

### Accessibility vs circulation
Do not choose a corridor width from memory. Identify whether the corridor is:
- accessible route;
- fire exit route;
- ordinary circulation;
- service route;
- material route.

### Fire route vs equipment layout
A kitchen equipment arrangement cannot obstruct a required emergency route merely because the equipment fits geometrically.

### Electrical vs metal module
A metal module requires Core analysis of grounding/equipotentialization, protective measures and interfaces. “Metal box = ground” is not a valid rule.

### SPDA vs grounding
SPDA grounding, protective grounding and equipotentialization must be analyzed as related but distinct functions under the applicable standards.

## 10. Evidence model

Every Forge conclusion should produce:

- source identifier;
- rule identifier;
- project identifier;
- input parameters;
- calculation;
- drawing/layout reference;
- test/inspection result;
- reviewer/responsible professional when applicable;
- timestamp;
- software/rule version;
- final status.

## 11. Statuses

- `NOT_EVALUATED`
- `APPLICABLE`
- `NOT_APPLICABLE`
- `COMPLIANT`
- `COMPLIANT_WITH_REMARKS`
- `NON_COMPLIANT`
- `INSUFFICIENT_EVIDENCE`
- `CONFLICT_REQUIRES_CORE_DECISION`
- `REQUIRES_RESPONSIBLE_TECHNICAL_REVIEW`

## 12. Hard rule

Forge cannot turn:

`internal guideline → regulatory requirement`

or:

`historical rule → current requirement`

or:

`calculated result → quoted normative text`.

The provenance chain must remain explicit.
