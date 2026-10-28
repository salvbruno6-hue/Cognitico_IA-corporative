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

test('discovery works across public and gateway-rewritten paths', async () => {
  const requestUrls = [
    endpoint + '/oauth-protected-resource',
    endpoint + '/.well-known/oauth-protected-resource',
    base + '/oauth-protected-resource',
    base + '/.well-known/oauth-protected-resource',
    base + '/elo-mcp/oauth-protected-resource',
    base + '/elo-mcp/.well-known/oauth-protected-resource',
  ];
  for (const requestUrl of requestUrls) {
    const res = await handler()(new Request(requestUrl));
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
      assert.equal(res.headers.get('WWW-Authenticate'), `Bearer realm="ELO MCP", resource_metadata="${base}/functions/v1/elo-mcp/oauth-protected-resource"`);
      assert.equal((await res.json()).error, 'unauthorized');
    }
  }
});

test('challenge stays canonical when the gateway rewrites the request origin', async () => {
  const res = await handler()(new Request('https://edge-runtime.internal/elo-mcp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'initialize', params: {} }),
  }));
  assert.equal(res.status, 401);
  assert.equal(
    res.headers.get('WWW-Authenticate'),
    `Bearer realm="ELO MCP", resource_metadata="${base}/functions/v1/elo-mcp/oauth-protected-resource"`,
  );
});

test('deploy configuration delegates authentication only for elo-mcp', () => {
  const config = readFileSync(new URL('../config.toml', import.meta.url), 'utf8');
  assert.match(config, /\[functions\.elo-mcp\]\s+verify_jwt = false/);
  assert.equal((config.match(/\[functions\./g) ?? []).length, 1);
});

test('oauth server reuses canonical ELO auth origin and consent route', () => {
  const config = readFileSync(new URL('../config.toml', import.meta.url), 'utf8');
  assert.match(config, /\[auth\]\s+site_url = "https:\/\/salvbruno6-hue\.github\.io"/);
  assert.match(config, /\[auth\.oauth_server\][\s\S]*enabled = true/);
  assert.match(config, /authorization_url_path = "\/Cognitico_IA-corporative\/oauth\/consent"/);
  assert.match(config, /allow_dynamic_registration = true/);
});

test('oauth runtime deploy preserves scoped PAT least privilege', () => {
  const workflow = readFileSync(new URL('../../.github/workflows/elo-oauth-runtime-deploy.yml', import.meta.url), 'utf8');
  assert.doesNotMatch(workflow, /supabase config push/);
  assert.match(workflow, /api\.supabase\.com\/v1\/projects\/fxbpevjrkwhbicpmecow\/config\/auth/);
  assert.match(workflow, /tomllib/);
  assert.match(workflow, /oauth_server_enabled/);
  assert.match(workflow, /oauth_server_authorization_path/);
  assert.match(workflow, /oauth_server_allow_dynamic_registration/);
});
