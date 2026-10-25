# AUTHORIZATION CONTRACT

## Objetivo

Garantir que o GPT nunca converta intenção conversacional em autoridade operacional.

## Autoridade

A única autoridade de autorização deste protocolo é `elo-authz`.

## Regras

1. O GPT não pode declarar `authorization_state=VALID` por conta própria.
2. Toda autorização deve ser observada por retorno verificável de `elo-authz`.
3. A autorização deve estar vinculada ao recurso/objetivo e à operação correspondente.
4. Autorizações expiradas, ausentes, revogadas ou incompatíveis resultam em fail-closed.
5. A skill não cria grants, bindings, sessões ou permissões.
6. O fato de o usuário escrever "continue" não substitui grant técnico quando o contrato exigir autorização persistente.
7. A autorização observada deve gerar referência de evidência rastreável.

## Resultado esperado

```yaml
authorization:
  authority: elo-authz
  state: VALID|MISSING|EXPIRED|DENIED
  evidence_ref: string|null
  resource_id: string|null
  operation: string|null
```

Somente `VALID`, obtido do owner canônico, permite avançar um ciclo que exija autorização.