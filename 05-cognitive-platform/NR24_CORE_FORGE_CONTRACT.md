# ELO — NR-24 Core → Forge Contract

## Status
NORMATIVE architectural contract

## Purpose

Definir como o ELO deve compreender e aplicar conhecimento da NR-24 sem misturar **significado normativo** com **implementação operacional**.

A regra estrutural é:

> **Core entende e governa o significado. Forge aplica, testa e constrói.**

## 1. Authority

The canonical ELO repository is the source of truth for promoted knowledge. The external MTE publication is the authority for the NR-24 content. Forge is not an architectural authority and cannot redefine the norm.

Repository navigation rules establish that the knowledge-engineering layer handles ingestion, normalization, semantic structures, retrieval preparation, provenance and knowledge quality, while the cognitive platform handles knowledge interaction, reasoning, evidence, recommendation and decision support. fileciteturn4file0L2-L2

## 2. Knowledge object

The Core must represent an NR rule with the following minimum schema:

```text
NormativeRule {
  id
  norm_code
  chapter
  item
  title
  statement
  subject
  requirement_type
  applicability_condition
  population_basis
  threshold
  unit
  formula
  exception
  construction_date_condition
  sex_separation_condition
  local_code_dependency
  related_items[]
  source_authority
  source_url
  source_version
  provenance
  status
  interpretation_status
  supersedes[]
  superseded_by[]
}
```

## 3. Required semantic statuses

The Core must distinguish:

- `NORMATIVE` — directly supported by the norm source;
- `HISTORICAL` — previous wording retained for traceability;
- `INTERNAL_DIRECTIVE` — company-adopted rule;
- `DERIVED_CALCULATION` — mathematically derived from a normative rule;
- `APPLICATION_RESULT` — output produced by Forge;
- `EVIDENCE` — measurement/document/test supporting a result;
- `INFERENCE` — model reasoning not directly stated by the source;
- `PROPOSAL` — candidate future rule.

These statuses must not be collapsed.

## 4. Query routing

### Query contains “NR”

Route to normative knowledge first.

Examples:

- `NR-24`
- `NR 24`
- `qual a NR para vestiário?`
- `NR quantos chuveiros?`

### Query contains “Diretriz”

Route to internal directives.

### Query contains both

Use two explicit evidence sections:

1. `NORMA — NR`
2. `DIRETRIZ INTERNA`

Never merge the two into a single undifferentiated requirement.

## 5. Core reasoning sequence

For every NR-24 question:

```text
IDENTIFY CONTEXT
      ↓
IDENTIFY ESTABLISHMENT / ACTIVITY
      ↓
IDENTIFY WORKER USERS
      ↓
IDENTIFY LARGEST USER SHIFT
      ↓
IDENTIFY APPLICABLE NR-24 CHAPTER/ITEM
      ↓
CHECK CONDITIONS / EXCEPTIONS
      ↓
APPLY NORMATIVE FORMULA IF PRESENT
      ↓
SEPARATE DERIVED RESULT FROM SOURCE TEXT
      ↓
CHECK OTHER APPLICABLE REQUIREMENTS
      ↓
RETURN REQUIREMENT + BASIS + LIMITATIONS
```

## 6. No automatic compliance claim

The Core must never infer full compliance from one satisfied metric.

For example:

`area >= required area`

does not by itself mean:

`project = NR-24 compliant`.

A full compliance assessment requires all applicable requirements, evidence and other governing regulations.

## 7. Dimensioning semantics

The Core must preserve the distinction among:

- total employees;
- workers who are users of the regulated installation;
- workers in the largest shift;
- workers who need a particular installation;
- workers actually hosted in an accommodation;
- users attended simultaneously in a meal location.

The population variable must be selected from the exact normative condition instead of using a universal employee count.

## 8. Formula governance

Formulas are semantic objects, not just calculator expressions.

### Installation sanitary

`ceil(N / 20)` applies to the minimum number of sanitary installations under 24.2.2, with the applicable sex separation.

### Lavatório

`ceil(N / 10)` applies only under the exposure condition in 24.2.2.1.

### Chuveiro

`ceil(N / 10)` or `ceil(N / 20)` according to the activity condition in 24.3.5.

### Vestiário ≤ 750

`A_unit = 1.5 - N/1000`

`A_total = N * A_unit`

### Vestiário > 750

`A_total = N * 0.75`

### Alojamento sanitário

`ceil(N / 10)` installation sanitary with shower per hosted workers or fraction.

### Alojamento room area

- `3.00 m² / simple bed`, including circulation and cabinet;
- `4.50 m² / bunk bed`, including circulation and cabinet;
- maximum 8 workers per room.

## 9. Forge input contract

Forge may receive:

```text
Context
NormativeRule IDs
Worker population
Shift population
Activity classification
Exposure classification
Construction date where relevant
Project dimensions
Product/module dimensions
Existing equipment quantities
Layout evidence
Local code constraints
Evidence files
Internal directives
```

Forge must not receive a free-form rule and treat it as normative without provenance.

## 10. Forge output contract

Every application result must contain:

```text
application_id
source_rule_ids[]
input_data
assumptions[]
calculation
result
unit
status
missing_information[]
validation_scope
limitations[]
evidence_required[]
internal_directives_used[]
```

## 11. Internal module rule

The conversation established an internal product datum:

`Módulo “sem bolsa” = 13.56 m² de área interna útil por unidade.`

This is **not NR-24 content**. It is an internal product parameter and can only be used by Forge when the applicable internal directive/product catalog authorizes it.

Example:

```text
NR result:
200 workers -> 260 m² minimum vestário area

Internal product parameter:
13.56 m²/module

Forge application:
ceil(260 / 13.56) = 20 modules
```

The output must be labeled `APPLICATION_RESULT`, not `NORMATIVE_REQUIREMENT`.

## 12. Historical-data protection

The 2019 CNI comparison supplied in the working knowledge contains older refeitório requirements of 1 m²/user, 1/3 of the largest shift and 75 cm/55 cm circulation. The comparison explicitly identifies those provisions as excluded in the new text.

Therefore the Core must store them as `HISTORICAL` and prevent retrieval as current NR-24 requirements unless a current authoritative source restores them.

## 13. Error correction rules

If a prior ELO response contains a statement that is not supported by the current source:

1. mark it as `UNVERIFIED` or `SUPERSEDED`;
2. identify the authoritative source;
3. replace the canonical semantic representation;
4. preserve the old answer only as historical conversation evidence if useful;
5. prevent the Forge from consuming the obsolete statement.

## 14. Conflict handling

If:

`NR requirement != Internal Directive`

the system must not silently choose the internal directive.

Required behavior:

```text
NR requirement
      ↓
conflict detected
      ↓
flag conflict
      ↓
Core decision / human specialist when required
      ↓
Forge applies only approved interpretation
```

## 15. Evidence and verification

A Forge result should be considered `VERIFIED` only when the required evidence exists, such as:

- measured area;
- dimensioned layout;
- equipment count;
- activity/exposure classification;
- construction date;
- product technical specification;
- local code check;
- applicable accessibility/fire/health requirements where relevant.

## 16. Promotion lifecycle

```text
MTE source
  ↓
Knowledge ingestion
  ↓
Normalization
  ↓
Provenance
  ↓
Core semantic interpretation
  ↓
Approved contract
  ↓
Forge implementation
  ↓
Automated tests
  ↓
Evidence
  ↓
Specialist validation
  ↓
ELO approval
  ↓
Promotion to canonical implementation
```

This follows the existing ELO Forge principle that Forge constructs and the canonical ELO architecture decides. fileciteturn14file0L2-L2

## 17. Minimum Forge test matrix for NR-24

### Test population

- 1 worker
- 10 workers
- 11 workers
- 20 workers
- 21 workers
- 30 workers
- 31 workers
- 100 workers
- 101 workers
- 200 workers
- 750 workers
- 751 workers
- >1000 workers

### Test dimensions

- sanitary installation count;
- lavatory conditional count;
- shower 1/10;
- shower 1/20;
- mictory post-2019 rule;
- vestiaire formula;
- vestiaire >750 rule;
- accommodation sanitary 1/10;
- room maximum 8;
- simple bed area;
- bunk bed area;
- water fountain 1/50;
- local code fallback.

### Boundary tests

Always test exact thresholds and `threshold + 1`, because the norm contains several piecewise rules.

## 18. Design principle

> **Norma é conhecimento governado. Aplicação é execução governada.**

The Core must know what the rule means and why it applies. Forge must know how to turn that rule into a calculation, layout, test, checklist or product configuration. Neither layer may silently assume the authority of the other.
