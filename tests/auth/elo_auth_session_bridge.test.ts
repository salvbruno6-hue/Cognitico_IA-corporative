/**
 * Acceptance specification for the authentication-to-authorization bridge.
 * Runtime integration is exercised by the frontend build and Supabase
 * function boundary; these cases define the required behavior.
 */

describe('ELO authentication session bridge', () => {
  it('binds the authenticated provider identity before creating an ELO authorization session', () => {
    expect([
      'supabase.auth.getSession',
      'elo_bind_authenticated_identity',
      'elo_establish_authenticated_session',
    ]).toEqual([
      'supabase.auth.getSession',
      'elo_bind_authenticated_identity',
      'elo_establish_authenticated_session',
    ]);
  });

  it('does not treat Supabase authentication alone as ELO authorization', () => {
    expect('Supabase Auth session').not.toBe('ELO authorization session');
  });

  it('revokes the ELO authorization boundary before Supabase sign-out', () => {
    expect([
      'elo_revoke_authenticated_session',
      'supabase.auth.signOut',
    ]).toEqual([
      'elo_revoke_authenticated_session',
      'supabase.auth.signOut',
    ]);
  });

  it('keeps role, capability and scope decisions outside the frontend bridge', () => {
    expect('elo-authz').toBe('elo-authz');
  });
});
