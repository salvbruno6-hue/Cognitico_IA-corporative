# Hermes Security + MCP — Native ELO Adaptation

## Objective

Extract reusable mechanisms demonstrated by Hermes and implement them as native ELO capabilities. Hermes remains an external evidence/provider source and is not a canonical dependency.

## Security mechanism extracted

From the Hermes `oss-forensics` skill: evidence-first claims, explicit fact/hypothesis separation, source-lane boundaries, rejection of fabricated evidence, static analysis instead of executing investigated repository code, and secret redaction.

Native ELO implementation: `elo.cognitive.security_forensics.SecurityObservation`.

Guarantees:
- evidence is mandatory;
- provenance is mandatory;
- facts and hypotheses remain distinct;
- secret-bearing metadata is rejected rather than persisted;
- classification reuses the canonical `SymbiontPatternIntake` and Evolution Gate;
- the capability does not execute target code or mutate canonical knowledge.

## MCP mechanism extracted

From the Hermes FastMCP skill: narrow typed tool surfaces, explicit parameters, early unsafe-input validation, read-only-first operation, bounded testing, and local contract validation before integration.

The ELO already owns the canonical MCP contract `symbiont_mcp_contracts.py`. The native addition is therefore a resolver, not a second MCP protocol:
`elo.forge.mcp_capability_resolver.MCPCapabilityResolver`.

Guarantees:
- tenant isolation;
- explicit authorization;
- fail-closed state validation;
- bounded tool-call requests;
- provider-neutral selection;
- no provider receives canonical authority.

## Mandatory test envelope

1. Security: missing evidence -> reject.
2. Security: secret metadata -> reject.
3. Security: valid observation -> canonical Evolution Gate classification.
4. MCP: wrong tenant -> block.
5. MCP: missing authorization -> block.
6. MCP: excessive calls -> block.
7. MCP: discovered-only capability -> fail closed.
8. MCP: tested capability within bounds -> allow.

## Potencialização para o ELO

Security increases the system's ability to distinguish evidence from inference and to operate fail-closed under suspicious input. MCP increases the system's ability to select external tools through explicit authorization, tenant scope and bounded execution without transferring ELO authority to the provider.

## Scope

This pair does not deploy a new MCP server, does not grant credentials, does not reopen public Supabase RPC execution, and does not promote external mechanisms directly into Core. Promotion remains subject to the existing Evolution Gate and governed PR process.
