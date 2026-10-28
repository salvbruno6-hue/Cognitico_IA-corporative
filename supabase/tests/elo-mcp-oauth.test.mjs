// ELO MCP discovery and fail-closed authentication; no live credentials used.
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { runInNewContext } from 'node:vm';
import { test } from 'node:test';
import assert from 'node:assert/strict';

const base = 'https://fxbpevjrkwhbicpmecow.supabase.co';
const endpoint = `${base}/functions/v1/elo-mcp`;
const source = readFileSync(new URL('../functions/elo-mcp/index.ts', import.meta.url), 'utf8').replace(/^import .*;\n/gm, '');

function handler() {
  let serve;
  const client = {
    auth: { getUser: async () => ({ data: { user: null }, error: new Error('invalid') }) },
    from: () => ({ insert: async () => ({ error: null }) }),
  };
  runInNewContext(stripTypeScriptTypes(source), {
    Deno: { env: { get: key => key === 'SUPABASE_URL' ? base : 'test-only' }, serve: fn => { serve = fn; } },
    createClient: () => client, Response, Request, URL, crypto,
    fetch: () => { throw new Error('Unauthenticated request reached authorization or data'); },
  });
  return serve;
}

test('discovery works without a bearer token at both supported paths', async () => {
  for (const suffix of ['/oauth-protected-resource', '/.well-known/oauth-protected-resource']) {
    const res = await handler()(new Request(endpoint + suffix));
    assert.equal(res.status, 200);
    const metadata = await res.json();
    assert.equal(metadata.resource, endpoint);
    assert.deepEqual(metadata.authorization_servers, [base + '/auth/v1']);
  }
});

test('missing and invalid tokens cannot initialize, list or call tools', async () => {
  for (const method of ['initialize', 'tools/list', 'tools/call']) {
    for (const headers of [{}, { Authorization: 'Bearer invalid' }]) {
      const res = await handler()(new Request(endpoint, {
        method: 'POST', headers,
        body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params: { name: 'elo_status' } }),
      }));
      assert.equal(res.status, 401);
      assert.match(res.headers.get('WWW-Authenticate'), /resource_metadata="https:\/\/.+\/oauth-protected-resource"/);
      assert.equal((await res.json()).error, 'unauthorized');
    }
  }
});

test('deploy configuration delegates authentication only for elo-mcp', () => {
  const config = readFileSync(new URL('../config.toml', import.meta.url), 'utf8');
  assert.match(config, /\[functions\.elo-mcp\]\s+verify_jwt = false/);
  assert.equal((config.match(/\[functions\./g) ?? []).length, 1);
});
