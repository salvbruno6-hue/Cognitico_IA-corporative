// Browser consent must reach the canonical authorization handler via supabase-js.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { runInNewContext } from 'node:vm';

function handler() {
  let handle;
  const source = readFileSync(new URL('../functions/elo-authz/index.ts', import.meta.url), 'utf8')
    .replace(/^import .*;\n/gm, '');
  runInNewContext(stripTypeScriptTypes(source), {
    Deno: { env: { get: () => 'test-only' }, serve: fn => { handle = fn; } },
    createClient: () => ({ auth: { getUser: async () => ({ data: { user: null }, error: new Error('invalid') }) } }),
    Request, Response, URL, crypto,
  });
  return handle;
}

function assertSDKHeaders(response) {
  const allowed = response.headers.get('access-control-allow-headers').toLowerCase().split(',').map(x => x.trim());
  for (const header of ['authorization', 'apikey', 'x-client-info', 'content-type', 'x-elo-request-id']) {
    assert(allowed.includes(header), `CORS must allow ${header}`);
  }
}

test('supabase-js consent preflight permits SDK headers', async () => {
  const response = await handler()(new Request('https://example.test/elo-authz', {
    method: 'OPTIONS', headers: {
      Origin: 'https://salvbruno6-hue.github.io',
      'Access-Control-Request-Method': 'POST',
      'Access-Control-Request-Headers': 'authorization,apikey,x-client-info,content-type',
    },
  }));
  assert.equal(response.status, 204);
  assertSDKHeaders(response);
});

test('SDK headers never replace missing or invalid user authentication', async () => {
  for (const authorization of ['', 'Bearer invalid']) {
    const response = await handler()(new Request('https://example.test/elo-authz', {
      method: 'POST', headers: { apikey: 'public-key', 'x-client-info': 'supabase-js', authorization },
      body: JSON.stringify({ purpose: 'oauth_consent' }),
    }));
    assert.equal(response.status, 401);
    assertSDKHeaders(response);
    assert.equal((await response.json()).authorized, false);
  }
});
