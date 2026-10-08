import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createOAuthFlow } from '../src/auth/oauthFlow.ts';
function fixture(session = null) {
  const calls = { starts: 0, exchanges: 0 };
  const auth = {
    async getSession() { return { data: { session }, error: null }; },
    async signInWithOAuth(input) { calls.starts++; calls.input = input; return { error: null }; },
    async exchangeCodeForSession() { calls.exchanges++; session = { user: { id: 'test' } }; return { data: { session }, error: null }; },
  };
  return { auth, calls, flow: createOAuthFlow(auth) };
}
test('A: starts once on the same callback origin', async () => {
  const f = fixture(); await Promise.all([f.flow.start('https://elo.test'), f.flow.start('https://elo.test')]);
  assert.equal(f.calls.starts, 1); assert.equal(f.calls.input.options.redirectTo, 'https://elo.test/auth/callback');
});
test('B/C/D/H: callback code exchanges once across remount, URL cleans, session confirms', async () => {
  const f = fixture(); let cleaned = 0;
  const first = f.flow.complete('https://elo.test/auth/callback?code=test', () => cleaned++);
  const remount = f.flow.complete('https://elo.test/auth/callback', () => cleaned++);
  assert.equal(first, remount); await remount; assert.equal(cleaned, 1); assert.equal(f.calls.exchanges, 1);
  assert.ok((await f.auth.getSession()).data.session);
});
test('E/F: valid session never starts Google, even with a callback code', async () => {
  const f = fixture({ user: { id: 'test' } }); await f.flow.start('https://elo.test');
  await f.flow.complete('https://elo.test/auth/callback?code=stale', () => {});
  assert.equal(f.calls.starts, 0); assert.equal(f.calls.exchanges, 0);
});
test('G: reload uses the persisted Supabase session', async () => {
  const f = fixture(); await f.flow.complete('https://elo.test/auth/callback?code=test', () => {});
  const reload = createOAuthFlow(f.auth); await reload.start('https://elo.test');
  await reload.complete('https://elo.test/auth/callback', () => {}); assert.equal(f.calls.starts, 0);
});
test('I: provider denial is controlled, no exchange or automatic restart', async () => {
  const f = fixture(); await assert.rejects(f.flow.complete('https://elo.test/auth/callback?error_description=Denied%25', () => {}), /Denied%/);
  assert.equal(f.calls.starts, 0); assert.equal(f.calls.exchanges, 0);
});
test('exchange failure remains controlled across repeated callback effects', async () => {
  const f = fixture(); f.auth.exchangeCodeForSession = async () => { f.calls.exchanges++; return { data: { session: null }, error: { message: 'invalid verifier' } }; };
  await assert.rejects(f.flow.complete('https://elo.test/auth/callback?code=test', () => {}), /invalid verifier/);
  await assert.rejects(f.flow.complete('https://elo.test/auth/callback', () => {}), /invalid verifier/); assert.equal(f.calls.exchanges, 1);
});
test('exchange success without persisted session is rejected', async () => {
  const f = fixture(); f.auth.exchangeCodeForSession = async () => ({ data: { session: null }, error: null });
  await assert.rejects(f.flow.complete('https://elo.test/auth/callback?code=test', () => {}), /confirmar/);
});
test('session read failure does not initiate OAuth', async () => {
  const f = fixture(); f.auth.getSession = async () => ({ data: { session: null }, error: { message: 'storage failed' } });
  await assert.rejects(f.flow.start('https://elo.test'), /storage failed/); assert.equal(f.calls.starts, 0);
});
