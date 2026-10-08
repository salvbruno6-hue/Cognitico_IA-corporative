import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import vm from 'node:vm';
import ts from 'typescript';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { sectors } from '../src/lib/sectors.ts';
const require = createRequire(import.meta.url);
function loadComponent(path, overrides = {}) {
  const source = readFileSync(new URL(path, import.meta.url), 'utf8');
  const code = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX } }).outputText;
  const module = { exports: {} };
  vm.runInNewContext(code, { module, exports: module.exports, require: name => overrides[name] ?? require(name), process });
  return module.exports;
}
test('one planning/PCP sector appears in sector navigation', () => {
  assert.equal(sectors.filter(sector => /planejamento|pcp/i.test(sector.label)).length, 1);
  assert.equal(sectors.find(sector => sector.key === 'planejamento').label, 'Planejamento/PCP');
});
test('workspace presents one analysis action and actual authenticated display name', () => {
  const { EloDashboard } = loadComponent('../src/components/elo-dashboard.tsx', { '@/components/elo-operational-data': { EloOperationalData: () => null } });
  const html = renderToStaticMarkup(React.createElement(EloDashboard, { accessToken: 'test', displayName: 'Samuel' }));
  assert.match(html, /Planejamento\/PCP/);
  assert.match(html, /Samuel/);
  assert.match(html, /Consultar ELO/);
  assert.doesNotMatch(html, /Bruno|Hermes|Automações do setor|Governança|Conectores|Programar produção/);
  assert.match(html, /disabled=""/);
});
test('catalog starts loading rather than presenting invented rows or counts', () => {
  const { EloOperationalData } = loadComponent('../src/components/elo-operational-data.tsx');
  const html = renderToStaticMarkup(React.createElement(EloOperationalData, { accessToken: 'test' }));
  assert.match(html, /Consultando Lista-Mãe/);
  assert.match(html, /Modelos/);
  assert.match(html, /Kits/);
  assert.doesNotMatch(html, /474|registros carregados/);
});
