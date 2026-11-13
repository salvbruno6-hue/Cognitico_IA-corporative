import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import vm from 'node:vm';
import ts from 'typescript';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { sectors } from '../src/lib/sectors.ts';
import { workspaceAreas, isEvidenceBacked } from '../src/lib/workspace.ts';
import { callWorkspaceTool } from '../src/lib/elo-workspace-mcp.ts';
const require = createRequire(import.meta.url);
function loadComponent(path, overrides = {}) {
  const source = readFileSync(new URL(path, import.meta.url), 'utf8');
  const code = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX } }).outputText;
  const module = { exports: {} };
  vm.runInNewContext(code, { module, exports: module.exports, require: name => overrides[name] ?? require(name), process });
  return module.exports;
}
test('reference navigation has all twelve areas and one unified planning/PCP area', () => {
  assert.deepEqual(workspaceAreas.map(area => area.key), ['orquestrador', 'dashboard', 'comercial', 'almoxarifado', 'compras', 'producao', 'pcp', 'expedicao', 'catalogo', 'chat', 'notificacoes', 'configuracoes']);
  assert.equal(workspaceAreas.filter(area => /planejamento|pcp/i.test(area.label)).length, 1);
  assert.equal(sectors.filter(sector => /planejamento|pcp/i.test(sector.label)).length, 1);
});
test('every area renders its own content, preserves real identity and explains integration gaps', () => {
  const { EloDashboard } = loadComponent('../src/components/elo-dashboard.tsx', {
    '@/lib/workspace': { workspaceAreas, isEvidenceBacked },
    '@/lib/elo-settings': { DEFAULT_ELO_SETTINGS: {}, loadELOSettings: () => ({}), persistELOSettings() {} },
    '@/components/elo-operational-data': { EloOperationalData: () => React.createElement('p', null, 'Catalog test') },
    '@/components/elo-workspace-tool': { EloWorkspaceTool: ({ title }) => React.createElement('h2', null, title) },
  });
  for (const area of workspaceAreas) {
    const html = renderToStaticMarkup(React.createElement(EloDashboard, { accessToken: 'test', displayName: 'Samuel', initialArea: area.key }));
    assert.ok(html.includes(area.label), area.key);
    assert.ok(html.includes(area.description), area.key);
    assert.match(html, /Samuel/);
    assert.match(html, /Integração pendente/);
    assert.doesNotMatch(html, /Bruno|Agentes Conectados|100% confiança|simulação concluída/);
  }
});
test('catalog loads all nine existing allowed sources without seeded counts', () => {
  const { EloOperationalData, catalogTables } = loadComponent('../src/components/elo-operational-data.tsx');
  assert.equal(catalogTables.length, 9);
  const html = renderToStaticMarkup(React.createElement(EloOperationalData, { accessToken: 'test' }));
  for (const table of catalogTables) assert.ok(html.includes(table.label));
  assert.match(html, /Consultando Lista-Mãe/);
  assert.doesNotMatch(html, /474|registros carregados/);
});
test('echo without sources cannot be presented as evidenced cognitive analysis', () => {
  assert.equal(isEvidenceBacked({ sources: [], provenance: { evidence_refs: [] } }), false);
  assert.equal(isEvidenceBacked({ sources: [{ source_id: 'source' }] }), true);
  assert.equal(isEvidenceBacked({ provenance: { evidence_refs: ['ref'] } }), true);
});
test('adapter reuses authenticated MCP with request correlation and preserves pending state', async () => {
  const original = globalThis.fetch;
  let sent;
  globalThis.fetch = async (url, request) => {
    sent = { url, request, body: JSON.parse(request.body) };
    return { ok: true, status: 200, json: async () => ({ jsonrpc: '2.0', id: sent.body.id, result: { content: [{ type: 'text', text: JSON.stringify({ ready: false, next_question: 'Qual a fonte?', requests: [] }) }] } }) };
  };
  try {
    const result = await callWorkspaceTool('https://example.test/', 'session-token', 'elo_pcp_dados_pendentes');
    assert.equal(sent.url, 'https://example.test/functions/v1/elo-mcp');
    assert.equal(sent.request.headers.Authorization, 'Bearer session-token');
    assert.equal(sent.body.method, 'tools/call');
    assert.equal(result.ready, false);
    assert.equal(result.next_question, 'Qual a fonte?');
    assert.ok(!('service_role' in sent.request.headers));
  } finally { globalThis.fetch = original; }
});
test('adapter does not expose generic SQL/table/write tools', async () => {
  await assert.rejects(callWorkspaceTool('https://example.test', 'test', 'elo_read'), /não disponível/);
  await assert.rejects(callWorkspaceTool('https://example.test', 'test', 'execute_sql'), /não disponível/);
});
test('adapter rejects denial, MCP failures, mismatched request and malformed results', async () => {
  const original = globalThis.fetch;
  try {
    for (const fixture of [{ status: 403 }, { status: 200, error: { message: 'private internal SQL error' } }, { status: 200, id: 'wrong', result: {} }, { status: 200, invalidText: true }]) {
      globalThis.fetch = async (_url, request) => {
        const id = JSON.parse(request.body).id;
        return { ok: fixture.status === 200, status: fixture.status, json: async () => ({ jsonrpc: '2.0', id: fixture.id ?? id, error: fixture.error, result: fixture.result ?? { content: [{ type: 'text', text: fixture.invalidText ? 'broken' : '{}' }] } }) };
      };
      await assert.rejects(callWorkspaceTool('https://example.test', 'test', 'elo_status'), error => !error.message.includes('SQL'));
    }
  } finally { globalThis.fetch = original; }
});
