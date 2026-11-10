from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTHZ = (ROOT / "supabase/functions/elo-authz/index.ts").read_text(encoding="utf-8")
MIGRATION = (ROOT / "supabase/migrations/20260919220335_elo_operator_github_binding_runtime.sql").read_text(encoding="utf-8")


def test_binding_is_persistent_and_repository_scoped() -> None:
    assert "elo_operator_github_bindings" in MIGRATION
    assert "identity_id uuid not null" in MIGRATION
    assert "github_user_id bigint not null" in MIGRATION
    assert "repository_full_name text not null" in MIGRATION
    assert "unique (identity_id, repository_full_name)" in MIGRATION
    assert "unique (github_user_id, repository_full_name)" in MIGRATION


def test_authorization_states_are_explicit_and_expiring() -> None:
    for state in (
        "elo-execution-authorized",
        "elo-commit-authorized",
        "elo-merge-authorized",
    ):
        assert state in MIGRATION
    assert "elo_authorization_grants" in MIGRATION
    assert "expires_at timestamptz not null" in MIGRATION
    assert "revoked_at timestamptz" in MIGRATION


def test_authorization_audit_remains_canonical():
    assert 'supabase.from("elo_authorization_audit").insert' in AUTHZ
    assert "authorization_authority:" in AUTHZ


def test_codex_cannot_emit_authorization_states():
    workflow = (ROOT / ".github/workflows/elo-agent-loop.yml").read_text(encoding="utf-8")
    assert "ELO_DECISION=APPROVE_COMMIT" in workflow
    assert "authorization_state:" not in workflow
    assert "create_operator_binding" not in workflow
    assert "issue_authorization_grant" not in workflow


def test_canonical_issuer_is_required_for_binding_and_grants():
    assert 'action==="create_operator_binding" || action==="issue_authorization_grant"' in AUTHZ
    assert 'auth.roles.includes("CANONICAL_ADMIN")' in AUTHZ
    assert "canonical_admin_created_operator_binding" in AUTHZ
    assert "canonical_admin_issued_authorization_state" in AUTHZ
    assert "expires_in_seconds" in AUTHZ
    assert "86400" in AUTHZ


def test_web_boundary_exposes_only_canonical_issuer_actions():
    route = Path("apps/elo-web/src/app/api/authorization/route.ts").read_text(encoding="utf-8")
    assert '"create_operator_binding","issue_authorization_grant"' in route


def test_collaborator_and_visitor_tiers_are_separated():
    migration = Path("supabase/migrations/20260919220406_elo_access_tiers.sql").read_text(encoding="utf-8")
    assert "'COLABORADOR'" in migration
    assert "'VISITANTE'" in migration
    assert "'LISTA_MAE_INSERT'" in migration
    assert "FOR INSERT" in migration
    assert "FOR UPDATE" not in migration
    assert "FOR DELETE" not in migration


def test_collaborator_has_no_github_binding_by_definition():
    migration = Path("supabase/migrations/20260919220406_elo_access_tiers.sql").read_text(encoding="utf-8")
    assert "No identity is auto-provisioned by this migration." in migration
    assert "no GitHub repository binding" in migration


def test_authorization_grant_is_resource_bound() -> None:
    assert 'const metadataResourceId=String(metadata.resource_id??"").trim();' in AUTHZ
    assert 'metadataResourceId===resourceId' in AUTHZ
    assert 'grantMetadata:Record<string,unknown>={issuer_role:"CANONICAL_ADMIN",resource_id:resourceId}' in AUTHZ
    assert 'resource_id:resourceId' in AUTHZ
    assert "evidence_ref" in AUTHZ


def test_authorization_state_check_requires_candidate_resource() -> None:
    assert "authorization_state_operation_repository_resource_required" in AUTHZ
    assert "resolveAuthorizationGrant(auth.identity.identity_id,session.session.session_id,state,operation,repository,resourceId,tenantId)" in AUTHZ


def test_objective_continuation_grant_is_enterprise_tenant_bound() -> None:
    assert 'operation.startsWith("continue_objective:")' in AUTHZ
    assert 'metadata.tenant_id' in AUTHZ
    assert 'metadataTenantId===tenantId' in AUTHZ
    assert 'grantMetadata.tenant_id=tenantId' in AUTHZ
    assert 'hasEnterpriseTenantScope(targetScopes.scopes,tenantId)' in AUTHZ
    assert 'hasEnterpriseTenantScope(scopes.scopes,tenantId)' in AUTHZ
    assert 'operation!==`continue_objective:${resourceId}`' in AUTHZ
    assert 'state!=="elo-execution-authorized"' in AUTHZ


def test_objective_continuation_runtime_uses_canonical_enterprise_tenant() -> None:
    prefinalize = Path("apps/elo-web/src/app/api/elo/chat/prefinalize/route.ts").read_text(encoding="utf-8")
    real_test = Path("apps/elo-web/src/app/api/elo/admin/objective-continuity-test/route.ts").read_text(encoding="utf-8")
    assert 'tenant_id: tenantId' in prefinalize
    assert 'const TEST_TENANT_ID = "MULTITEINER"' in real_test
    assert 'tenant_id: TEST_TENANT_ID' in real_test


def test_grant_lookup_is_bound_to_active_elo_session() -> None:
    """Grants from a different session must not pass the canonical lookup."""
    resolver = AUTHZ.split("async function resolveAuthorizationGrant(", 1)[1].split("Deno.serve(", 1)[0]
    lookup = resolver.split('supabase.from("elo_authorization_grants")', 1)[1].split("if(error)", 1)[0]
    assert '.eq("identity_id",identityId)' in lookup
    assert '.eq("session_id",sessionId)' in lookup
    assert '.eq("authorization_state",state)' in lookup
    assert '.eq("operation",operation)' in lookup
    assert '.eq("repository_full_name",repository)' in lookup
    assert '.is("revoked_at",null)' in lookup
    assert 'metadataResourceId===resourceId' in resolver
    assert 'metadataTenantId===tenantId' in resolver
    assert "issued<=now&&expires>now" in resolver
    assert 'reason:"authorization_state_not_granted"' in resolver


def test_grant_issuance_uses_recipient_session_and_fails_closed() -> None:
    """A grant issued by an administrator targets the recipient session."""
    issuer = AUTHZ.split('const bindingId=typeof body.binding_id', 1)[1].split('if(action==="portal_access")', 1)[0]
    assert "const targetSession=await resolveActiveSession(binding.identity_id);" in issuer
    assert "if(!targetSession.ok)" in issuer
    assert 'reason:"target_elo_session_unavailable"' in issuer
    assert 'reason:"authorization_audit_write_failed"' in issuer
    assert 'targetSession.reason==="session_lookup_failed"?503:403' in issuer
    assert "identity_id:binding.identity_id,session_id:targetSession.session.session_id" in issuer
    assert "identity_id:binding.identity_id,session_id:session.session.session_id" not in issuer
    assert 'issued_by_identity_id:auth.identity.identity_id' in issuer
    assert 'audit(auth.identity.identity_id,session.session.session_id,action,repository,"ALLOW"' in issuer


def test_grant_resolver_behavior_with_isolated_supabase() -> None:
    """Execute the actual TS grant resolver under Node with a fake Supabase API.

    Unlike source-assertion tests, this executes the implementation on allowed
    and denied grants. No live credential, network connection or write is used.
    """
    import shutil
    import subprocess

    node = shutil.which("node")
    assert node is not None, "Node is required for security behavior tests"
    resolver = "async function resolveAuthorizationGrant(" + AUTHZ.split(
        "async function resolveAuthorizationGrant(", 1
    )[1].split("\nDeno.serve(", 1)[0]
    # The existing function has a small, known TS-only surface.
    assert resolver.count(":string") == 7
    assert resolver.count("(g:any)") == 1
    resolver = (
        resolver.replace(":string", "")
        .replace("(g:any)", "(g)")
        .replace(" as Record<string,unknown>", "")
        .replace(" as const", "")
    )
    harness = r"""
const assert = require("node:assert/strict");
const now = Date.now();
const base = {
  grant_id:"grant1", binding_id:"binding1", identity_id:"identityA",
  session_id:"sessionA", authorization_state:"elo-execution-authorized",
  operation:"execute", repository_full_name:"org/repo",
  issued_at:new Date(now-60000).toISOString(),
  expires_at:new Date(now+60000).toISOString(), revoked_at:null,
  metadata:{resource_id:"resourceA",tenant_id:"tenantA"}
};
const binding = {
  binding_id:"binding1",identity_id:"identityA",
  repository_full_name:"org/repo",active:true,
  github_user_id:123,github_login:"user",operation_class:"execute"
};
let tables = {};
let dbErrors = {};
class Query {
  constructor(name) { this.name = name; this.filters = []; }
  select() { return this; }
  eq(key,value) { this.filters.push([key,value]); return this; }
  is(key,value) { this.filters.push([key,value]); return this; }
  order() { return this; }
  _rows() {
    return (tables[this.name]||[]).filter(row =>
      this.filters.every(([key,value]) => row[key] === value)
    );
  }
  limit(n) {
    const error = dbErrors[this.name] || null;
    return Promise.resolve({data:error?null:this._rows().slice(0,n),error});
  }
  maybeSingle() {
    const error = dbErrors[this.name] || null;
    return Promise.resolve({data:error?null:(this._rows()[0]||null),error});
  }
}
const supabase = {from:(name)=>new Query(name)};
function isObjectiveContinuation(operation) {
  return operation.startsWith("continue_objective:");
}
async function check(label, config={},expected=null) {
  tables = {
    elo_authorization_grants:config.noGrant ? [] : [{
      ...base,...(config.grant||{})
    }],
    elo_operator_github_bindings:config.noBinding ? [] : [{
      ...binding,...(config.binding||{})
    }]
  };
  dbErrors = config.errors || {};
  const args = {
    identityId:"identityA",sessionId:"sessionA",
    state:"elo-execution-authorized",operation:"execute",
    repository:"org/repo",resourceId:"resourceA",tenantId:"tenantA",
    ...(config.args||{})
  };
  const result = await resolveAuthorizationGrant(
    args.identityId,args.sessionId,args.state,args.operation,
    args.repository,args.resourceId,args.tenantId
  );
  if (expected === null) {
    assert.equal(result.ok,true,label+": "+JSON.stringify(result));
    assert.equal(result.grant.grant_id,"grant1",label);
    assert.equal(result.binding.binding_id,"binding1",label);
  } else {
    assert.equal(result.ok,false,label);
    assert.equal(result.reason,expected,label);
  }
}
(async () => {
  await check("valid same identity and session");
  await check("valid objective scope",{
    grant:{operation:"continue_objective:resourceA"},
    args:{operation:"continue_objective:resourceA"}
  });
  const denied = "authorization_state_not_granted";
  await check("wrong session",{args:{sessionId:"sessionB"}},denied);
  await check("missing grant session",{grant:{session_id:null}},denied);
  await check("wrong recipient identity",{args:{identityId:"identityB"}},denied);
  await check("wrong resource",{args:{resourceId:"resourceB"}},denied);
  await check("missing resource metadata",{grant:{metadata:{}}},denied);
  await check("wrong repository",{args:{repository:"other/repo"}},denied);
  await check("wrong state",{args:{state:"elo-commit-authorized"}},denied);
  await check("wrong operation",{args:{operation:"merge"}},denied);
  await check("expired",{grant:{expires_at:new Date(now-1000).toISOString()}},denied);
  await check("not yet issued",{grant:{issued_at:new Date(now+1000).toISOString()}},denied);
  await check("revoked",{grant:{revoked_at:new Date(now-1000).toISOString()}},denied);
  await check("missing grant",{noGrant:true},denied);
  await check("objective wrong tenant",{
    grant:{operation:"continue_objective:resourceA"},
    args:{operation:"continue_objective:resourceA",tenantId:"tenantB"}
  },denied);
  await check("objective missing tenant",{
    grant:{operation:"continue_objective:resourceA"},
    args:{operation:"continue_objective:resourceA",tenantId:""}
  },denied);
  await check("binding inactive",{binding:{active:false}},"operator_binding_inactive");
  await check("binding wrong identity",{binding:{identity_id:"identityB"}},"operator_binding_inactive");
  await check("binding wrong repo",{binding:{repository_full_name:"other/repo"}},"operator_binding_inactive");
  await check("binding missing",{noBinding:true},"operator_binding_inactive");
  await check("lookup failure",{errors:{elo_authorization_grants:{message:"db"}}},"authorization_grant_lookup_failed");
  await check("binding lookup failure",{errors:{elo_operator_github_bindings:{message:"db"}}},"operator_binding_lookup_failed");
  await check("unsupported state",{args:{state:"unknown"}},"authorization_state_not_supported");
  process.stdout.write("23 grant resolver behavior cases passed\n");
})().catch(error=>{console.error(error);process.exitCode=1});
"""
    result = subprocess.run(
        [node, "-e", resolver + "\n" + harness],
        capture_output=True,
        text=True,
        timeout=25,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "23 grant resolver behavior cases passed" in result.stdout
