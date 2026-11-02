import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { runInNewContext } from 'node:vm';

function loadResolver(supabase) {
  const full = readFileSync(new URL('../functions/elo-authz/index.ts', import.meta.url), 'utf8');
  const start = full.indexOf('async function resolveAuthorizationGrant');
  const end = full.indexOf('\n\nDeno.serve', start);
  assert.notEqual(start, -1, 'resolver must exist');
  assert.notEqual(end, -1, 'resolver boundary must exist');
  const source = `${full.slice(start, end)}\nglobalThis.resolveAuthorizationGrant = resolveAuthorizationGrant;`;
  const context = { supabase, Date };
  runInNewContext(stripTypeScriptTypes(source), context);
  return context.resolveAuthorizationGrant;
}

function queryChain(rows, { binding = null } = {}) {
  const filters = [];
  let requireNull = null;
  const chain = {
    select() { return this; },
    eq(column, value) { filters.push([column, value]); return this; },
    is(column, value) { requireNull = [column, value]; return this; },
    order() { return this; },
    async limit() {
      const data = rows.filter((row) => {
        for (const [column, value] of filters) {
          if (column in row && row[column] !== value) return false;
        }
        if (requireNull && row[requireNull[0]] !== requireNull[1]) return false;
        return true;
      });
      return { data, error: null };
    },
    async maybeSingle() { return { data: binding, error: null }; },
  };
  return chain;
}

function runtime(grants) {
  const binding = {
    binding_id: 'binding-1',
    identity_id: 'identity-1',
    github_user_id: 123,
    github_login: 'operator',
    repository_full_name: 'salvbruno6-hue/Cognitico_IA-corporative',
    operation_class: 'OPERATIONAL',
    active: true,
  };
  return {
    from(table) {
      if (table === 'elo_authorization_grants') return queryChain(grants);
      if (table === 'elo_operator_github_bindings') return queryChain([], { binding });
      throw new Error(`unexpected table ${table}`);
    },
  };
}

const now = Date.now();
const baseGrant = {
  grant_id: 'grant-1',
  binding_id: 'binding-1',
  identity_id: 'identity-1',
  session_id: 'session-1',
  authorization_state: 'elo-execution-authorized',
  operation: 'continue_objective:ELO-OBJ-1',
  repository_full_name: 'salvbruno6-hue/Cognitico_IA-corporative',
  issued_at: new Date(now - 60_000).toISOString(),
  expires_at: new Date(now + 60_000).toISOString(),
  revoked_at: null,
  metadata: { resource_id: 'ELO-OBJ-1' },
};

async function resolve(grants, sessionId = 'session-1', resourceId = 'ELO-OBJ-1') {
  return loadResolver(runtime(grants))(
    'identity-1',
    sessionId,
    'elo-execution-authorized',
    'continue_objective:ELO-OBJ-1',
    'salvbruno6-hue/Cognitico_IA-corporative',
    resourceId,
  );
}

function assertDenied(result, reason) {
  assert.equal(result.ok, false);
  assert.equal(result.reason, reason);
}

test('accepts only an active grant bound to the active session and exact resource', async () => {
  const result = await resolve([baseGrant]);
  assert.equal(result.ok, true);
  assert.equal(result.grant.grant_id, 'grant-1');
});

test('rejects a grant issued for another active session', async () => {
  const result = await resolve([baseGrant], 'session-2');
  assertDenied(result, 'authorization_grant_session_mismatch');
});

test('rejects a legacy grant without resource binding metadata', async () => {
  const result = await resolve([{ ...baseGrant, metadata: {} }]);
  assertDenied(result, 'authorization_grant_resource_missing');
});

test('rejects a grant bound to another resource', async () => {
  const result = await resolve([{ ...baseGrant, metadata: { resource_id: 'ELO-OBJ-OTHER' } }]);
  assertDenied(result, 'authorization_grant_resource_mismatch');
});

test('expired grants fail closed', async () => {
  const result = await resolve([{ ...baseGrant, expires_at: new Date(now - 1_000).toISOString() }]);
  assertDenied(result, 'authorization_state_not_granted');
});

test('revoked grants fail closed through the canonical revoked_at query filter', async () => {
  const result = await resolve([{ ...baseGrant, revoked_at: new Date(now - 1_000).toISOString() }]);
  assertDenied(result, 'authorization_state_not_granted');
});
