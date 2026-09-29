# ELO — Simbionte: Investigação e Roteamento de Memórias de Aprendizado

**Status:** candidato para Evolution Gate  
**Owner:** ELO Cognitive / Learning  
**Executor transversal:** Simbionte

## Objetivo
Generalizar para memória a mesma disciplina usada nas descobertas Hermes: investigar experiência relacionada, preservar proveniência, resolver o Owner canônico existente e encaminhar o candidato à área governada correspondente.

## Fluxo
`MEMÓRIA → INVESTIGAR → RELACIONAR → RESOLVER OWNER → DEDUPLICAR/AGREGAR → ROUTING DECISION → ÁREA GOVERNADA → VALIDAÇÃO/EVOLUTION GATE`

Decisões possíveis: `REUSE | AGGREGATE | CANDIDATE | BLOCKED | NO_OWNER`.

## Owners iniciais
| Domínio | Tipo | Owner | Destino |
|---|---|---|---|
| ANALISE_SOLICITACOES | learning | ELO Cognitive / Solicitation Learning | `memory/solicitations_learning/` |
| ORCAMENTO | learning | ELO Budget Specialist | `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/` |
| ORCAMENTO | calculation | ELO Budget Memory | Supabase `elo_orcament_calculation_memory` |
| CORPORATIVO | learning | ELO Knowledge | `04-knowledge-handbook/` |
| EVOLUTION | experience | ELO Cognitive / Evolution Memory | `memory/evolution/` |
| FORGE | skill | ELO Forge / Specialist Skill Registry | `forge/skill-packs/` |

## Regras
- A investigação usa domínio, tipo, conceito, relações explícitas, tenant e proveniência; similaridade lexical isolada não promove equivalência.
- Se existir memória canônica equivalente no Owner resolvido, a decisão é `REUSE`; não há nova identidade.
- Memória histórica/legada pode ser evidência, mas não vira destino novo por acidente.
- Sem Owner governado, a decisão é `NO_OWNER`; o mecanismo não inventa uma área.
- Candidato não é aprendizado validado.

## Fronteiras
O mecanismo não grava Git/Supabase, não promove aprendizado, não altera Core/Soul e não substitui KnowledgeAdmission, EvolutionMemory, GovernedLearningService, SpecialistSkillResolver ou Evolution Gate. Hermes/OpenClaw podem fornecer descoberta/evidência; o Owner continua sendo ELO.
