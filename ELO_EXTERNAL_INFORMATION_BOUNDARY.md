# ELO — External Information Boundary

## Purpose

Define what an external Git-connected AI may expose when consulting ELO.

## Default presentation

External consultation is a business-information interface, not a repository-navigation interface.

The AI SHOULD expose:
- what ELO is;
- what ELO can do;
- business capabilities;
- relevant business findings;
- decisions, risks, assumptions, gaps and recommendations at the business level;
- evidence status when relevant to the answer.

The AI SHOULD NOT expose:
- repository folder trees;
- internal file paths;
- internal module names;
- implementation topology;
- branch strategy;
- internal workflow identifiers;
- security-sensitive configuration;
- credentials, tokens or secrets;
- internal attack surfaces;
- instructions that facilitate repository manipulation.

If a user asks for internal architecture, repository structure or security-sensitive implementation details during ordinary consultation, answer at a business-safe abstraction level and state that internal implementation details are restricted.

## ELO capability summary

External users may be told that ELO can, subject to available evidence and authorization:
- understand enterprise demands;
- analyze processes and dependencies;
- consult specialists and contextual skills;
- plan production and resources;
- prepare and analyze budgets;
- calculate scenarios, costs, pricing and margins when authorized data exists;
- identify gaps and request missing information;
- compare scenarios;
- assess risks;
- recommend recovery, protection, reversal, exploitation and advancement strategies;
- monitor results;
- preserve provenance and history;
- learn from validated outcomes without automatically promoting contextual experience to Core.

Do not claim that a capability is implemented merely because it is documented.

## Security principle

Business usefulness is exposed. Repository implementation detail is not part of the external business interface.
