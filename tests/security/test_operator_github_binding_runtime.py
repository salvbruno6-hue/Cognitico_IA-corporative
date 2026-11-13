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
    atomic_sql = (ROOT / "supabase/migrations/20261110185000_elo_atomic_grant_audit_rpc.sql").read_text(encoding="utf-8")
    # Grant ALLOW is audited in the same DB transaction, not by a second
    # non-atomic Edge Function API call.
    assert "canonical_admin_issued_authorization_state" in atomic_sql
    assert 'supabase.rpc("elo_atomic_issue_authorization_grant"' in AUTHZ
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
    assert 'issuer_role:"CANONICAL_ADMIN",resource_id:resourceId,expires_in_seconds:expiresIn' in AUTHZ
    assert 'p_metadata:grantMetadata' in AUTHZ
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


def test_grant_lookup_pushes_resource_and_time_filters_before_limit() -> None:
    """Prevent valid grants from being hidden by ten newer unrelated/expired rows."""
    resolver = AUTHZ.split("async function resolveAuthorizationGrant(", 1)[1].split("Deno.serve(", 1)[0]
    lookup = resolver.split('supabase.from("elo_authorization_grants")', 1)[1].split("if(error)", 1)[0]
    for exact in (
        '.contains("metadata",metadataScope)',
        '.lte("issued_at",nowISO)',
        '.gt("expires_at",nowISO)',
        '.eq("session_id",sessionId)',
        '.is("revoked_at",null)',
        '.limit(10)',
    ):
        assert exact in lookup
    assert lookup.index('.contains("metadata",metadataScope)') < lookup.index(".limit(10)")
    assert 'resource_id:resourceId,tenant_id:tenantId' in resolver
    assert 'resource_id:resourceId};' in resolver
    # Keep the in-memory check as defense-in-depth against stale/malformed rows.
    assert 'metadataResourceId===resourceId' in resolver
    assert 'metadataTenantId===tenantId' in resolver

def test_grant_issuance_uses_recipient_session_and_fails_closed() -> None:
    """A grant issued by an administrator targets the recipient session."""
    issuer = AUTHZ.split('const bindingId=typeof body.binding_id', 1)[1].split('if(action==="portal_access")', 1)[0]
    assert "const targetSession=await resolveActiveSession(binding.identity_id);" in issuer
    assert "if(!targetSession.ok)" in issuer
    assert 'reason:"target_elo_session_unavailable"' in issuer
    assert 'reason:"authorization_audit_write_failed"' in issuer
    assert 'targetSession.reason==="session_lookup_failed"?503:403' in issuer
    assert "p_identity_id:binding.identity_id" in issuer
    assert "p_session_id:targetSession.session.session_id" in issuer
    assert "p_issued_by_identity_id:auth.identity.identity_id" in issuer
    assert "p_issuer_session_id:session.session.session_id" in issuer
    assert 'supabase.rpc("elo_atomic_issue_authorization_grant"' in issuer
    assert 'supabase.from("elo_authorization_grants").insert' not in issuer
    assert 'audit(auth.identity.identity_id,session.session.session_id,action,repository,"ALLOW"' not in issuer


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
  constructor(name) { this.name = name; this.filters = []; this.sort = null; }
  select() { return this; }
  eq(key,value) { this.filters.push(["eq",key,value]); return this; }
  is(key,value) { this.filters.push(["eq",key,value]); return this; }
  contains(key,value) { this.filters.push(["contains",key,value]); return this; }
  lte(key,value) { this.filters.push(["lte",key,value]); return this; }
  gt(key,value) { this.filters.push(["gt",key,value]); return this; }
  order(key,options={}) { this.sort = {key,ascending:options.ascending!==false}; return this; }
  _rows() {
    const result = (tables[this.name]||[]).filter(row =>
      this.filters.every(([op,key,value]) => {
        if(op==="eq") return row[key]===value;
        if(op==="contains") return row[key] && typeof row[key]==="object"
          && Object.entries(value).every(([field,required]) => row[key][field]===required);
        if(op==="lte") return row[key] <= value;
        if(op==="gt") return row[key] > value;
        throw new Error("Unsupported mock filter: "+op);
      })
    );
    if(this.sort) {
      const {key,ascending} = this.sort;
      result.sort((a,b)=>ascending
        ? String(a[key]).localeCompare(String(b[key]))
        : String(b[key]).localeCompare(String(a[key])));
    }
    return result;
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
    elo_authorization_grants:config.noGrant ? [] : (config.grants || [{
      ...base,...(config.grant||{})
    }]),
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
  const unrelated = Array.from({length:12},(_,i)=>({
    ...base,grant_id:"other-"+i,metadata:{resource_id:"other-"+i},
    issued_at:new Date(now-1000-i).toISOString()
  }));
  await check("older exact resource survives 12 newer unrelated grants",{
    grants:[...unrelated,base]
  });
  const expired = Array.from({length:12},(_,i)=>({
    ...base,grant_id:"expired-"+i,
    issued_at:new Date(now-1000-i).toISOString(),
    expires_at:new Date(now-500).toISOString()
  }));
  await check("older exact resource survives 12 newer expired grants",{
    grants:[...expired,base]
  });
  const future = Array.from({length:12},(_,i)=>({
    ...base,grant_id:"future-"+i,
    issued_at:new Date(now+10000+i).toISOString()
  }));
  await check("older exact resource survives 12 future-issued grants",{
    grants:[...future,base]
  });
  const otherTenant = Array.from({length:12},(_,i)=>({
    ...base,grant_id:"tenant-"+i,
    operation:"continue_objective:resourceA",
    metadata:{resource_id:"resourceA",tenant_id:"other-"+i},
    issued_at:new Date(now-1000-i).toISOString()
  }));
  await check("older exact tenant survives 12 newer wrong-tenant grants",{
    grants:[...otherTenant,{...base,operation:"continue_objective:resourceA"}],
    args:{operation:"continue_objective:resourceA"}
  });
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
  process.stdout.write("27 grant resolver behavior cases passed\n");
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
    assert "27 grant resolver behavior cases passed" in result.stdout


def test_grant_issuance_behavior_with_isolated_supabase() -> None:
    """Execute the actual ELO grant-issuance branch with controlled data stores.

    This tests issuance logic, not HTTP authentication or a live Supabase
    endpoint. It must never access production or create a real grant.
    """
    import shutil
    import subprocess

    node = shutil.which("node")
    assert node is not None, "Node is required for the authorization security suite"
    issuer = "    const bindingId=typeof body.binding_id" + AUTHZ.split(
        "    const bindingId=typeof body.binding_id", 1
    )[1].split('  if(action==="portal_access")', 1)[0]
    assert issuer.rstrip().endswith("}")
    # Remove the enclosing action branch's closing brace.
    issuer = issuer.rstrip().rsplit("\n  }", 1)[0]
    assert issuer.count("const grantMetadata:Record<string,unknown>") == 1
    issuer = issuer.replace(
        "const grantMetadata:Record<string,unknown>", "const grantMetadata"
    )
    javascript = "async function issueGrant() {\n" + issuer + "\n}\n"
    harness = r"""
const assert = require("node:assert/strict");
const auth = {identity:{identity_id:"admin"}};
const session = {session:{session_id:"admin-session"}};
const action = "issue_authorization_grant";
const repository = "org/repo";
const requestId = "request-1";
let body, config, inserts, audits, targetLookups, scopesLookups;
function json(value,status=200) { return {value,status}; }
function isObjectiveContinuation(operation) {
  return operation.startsWith("continue_objective:");
}
function hasEnterpriseTenantScope(scopes,tenantId) {
  return scopes.some(scope => scope.tenant === tenantId);
}
async function getScopes(identityId) {
  scopesLookups.push(identityId);
  return config.scopeError
    ? {ok:false,reason:"scope_lookup_failed"}
    : {ok:true,scopes:[{tenant:"tenantA"}]};
}
async function resolveActiveSession(identityId) {
  targetLookups.push(identityId);
  if(config.noSession) return {ok:false,reason:"active_elo_session_required"};
  if(config.sessionLookupError) return {ok:false,reason:"session_lookup_failed"};
  return {ok:true,session:{session_id:
    identityId === "admin" ? "admin-session" : "recipient-session"
  }};
}
async function audit(identityId,sessionId,kind,repo,decision,reason,id) {
  audits.push({identityId,sessionId,kind,repo,decision,reason,id});
  if(config.auditError===decision) throw Error("audit failed");
}
const supabase={
  // Simulated RPC contract; SQL transaction rollback itself requires
  // a PostgreSQL integration test before production promotion.
  async rpc(name,args) {
    assert.equal(name,"elo_atomic_issue_authorization_grant");
    if(config.insertError||config.auditError==="ALLOW") {
      return {data:null,error:{message:"transaction rejected"}};
    }
    const payload={
      binding_id:args.p_binding_id,identity_id:args.p_identity_id,
      session_id:args.p_session_id,
      authorization_state:args.p_authorization_state,
      operation:args.p_operation,repository_full_name:args.p_repository_full_name,
      issued_by_identity_id:args.p_issued_by_identity_id,
      request_id:args.p_request_id,expires_at:args.p_expires_at,
      metadata:args.p_metadata
    };
    inserts.push(payload);
    audits.push({
      identityId:args.p_issued_by_identity_id,
      sessionId:args.p_issuer_session_id,
      decision:"ALLOW"
    });
    return {data:{grant_id:"grant-1",...payload},error:null};
  },
  from(table) {
    if(table==="elo_operator_github_bindings") {
      const filters=[];
      return {
        select() {return this;},
        eq(k,v) {filters.push([k,v]);return this;},
        async maybeSingle() {
          if(config.bindingLookupError) {
            return {data:null,error:{message:"binding error"}};
          }
          const binding={
            binding_id:"binding-1",identity_id:config.recipientId||"recipient",
            repository_full_name:"org/repo",active:true,
            github_user_id:123,github_login:"recipient",operation_class:"execute"
          };
          const valid=filters.every(([k,v])=>binding[k]===v);
          return {data:!config.noBinding&&valid?binding:null,error:null};
        }
      };
    }
    throw Error("Direct grant writes are prohibited: "+table);
  }
};
let count=0;
async function check(label,overrides={},expectedStatus=200,expectedReason=null) {
  config=overrides;
  body={
    binding_id:"binding-1",authorization_state:"elo-execution-authorized",
    operation:"execute",resource_id:"resource-A",tenant_id:"",
    expires_in_seconds:600,...(config.body||{})
  };
  inserts=[];audits=[];targetLookups=[];scopesLookups=[];
  const result=await issueGrant();
  assert.equal(result.status,expectedStatus,label+": "+JSON.stringify(result));
  assert.equal(result.value.authorized,expectedStatus===200,label);
  if(expectedReason!==null) assert.equal(result.value.reason,expectedReason,label);
  if(expectedStatus===200) {
    assert.equal(inserts.length,1,label);
    assert.equal(inserts[0].identity_id,config.recipientId||"recipient",label);
    assert.equal(inserts[0].session_id,
      config.recipientId==="admin"?"admin-session":"recipient-session",label);
    assert.equal(inserts[0].issued_by_identity_id,"admin",label);
    assert.equal(inserts[0].metadata.resource_id,body.resource_id,label);
    assert.equal(inserts[0].metadata.issuer_role,"CANONICAL_ADMIN",label);
    assert.equal(result.value.authorization_authority,"elo-authz",label);
    assert.equal(audits.length,1,label);
    assert.equal(audits[0].decision,"ALLOW",label);
    assert.equal(audits[0].identityId,"admin",label);
    assert.equal(audits[0].sessionId,"admin-session",label);
    assert.deepEqual(targetLookups,[config.recipientId||"recipient"],label);
    assert.ok(Date.parse(inserts[0].expires_at)>Date.now(),label);
  }
  if(config.noSession||config.sessionLookupError) {
    assert.equal(inserts.length,0,label);
    assert.equal(audits.length,1,label);
    assert.equal(audits[0].decision,"DENY",label);
  }
  if(config.noBinding||config.bindingLookupError||config.scopeError) {
    assert.equal(inserts.length,0,label);
    assert.equal(targetLookups.length,0,label);
  }
  count+=1;
}
(async()=>{
  await check("admin issues to another identity");
  await check("admin self-issuance",{recipientId:"admin"});
  await check("commit authorization",{body:{authorization_state:"elo-commit-authorized",operation:"commit"}});
  await check("merge authorization",{body:{authorization_state:"elo-merge-authorized",operation:"merge"}});
  await check("minimum expiry",{body:{expires_in_seconds:60}});
  await check("maximum expiry",{body:{expires_in_seconds:86400}});
  await check("continuation with correct scope",{body:{
    authorization_state:"elo-execution-authorized",
    operation:"continue_objective:objective-A",resource_id:"objective-A",tenant_id:"tenantA"
  }});
  await check("no active recipient session",{noSession:true},403,"target_elo_session_unavailable");
  await check("recipient session lookup failure",{sessionLookupError:true},503,"target_elo_session_unavailable");
  await check("audit DENY failure remains closed",{noSession:true,auditError:"DENY"},503,"authorization_audit_write_failed");
  await check("missing binding",{noBinding:true},403,"operator_binding_inactive");
  await check("binding lookup failure",{bindingLookupError:true},503,"operator_binding_lookup_failed");
  await check("no binding id",{body:{binding_id:""}},400,"binding_state_operation_expiry_required");
  await check("no resource",{body:{resource_id:""}},400,"binding_state_operation_expiry_required");
  await check("unknown state",{body:{authorization_state:"unknown"}},400,"authorization_state_not_supported");
  await check("under minimum expiry",{body:{expires_in_seconds:59}},400,"binding_state_operation_expiry_required");
  await check("over maximum expiry",{body:{expires_in_seconds:86401}},400,"binding_state_operation_expiry_required");
  await check("fractional expiry",{body:{expires_in_seconds:60.5}},400,"binding_state_operation_expiry_required");
  await check("continuation without tenant",{body:{
    operation:"continue_objective:objective-A",resource_id:"objective-A",tenant_id:""
  }},400,"binding_state_operation_resource_tenant_expiry_required");
  await check("continuation mismatched objective",{body:{
    operation:"continue_objective:objective-B",resource_id:"objective-A",tenant_id:"tenantA"
  }},400,"objective_continuation_grant_mismatch");
  await check("continuation lacks recipient tenant scope",{body:{
    operation:"continue_objective:objective-A",resource_id:"objective-A",tenant_id:"tenantB"
  }},403,"enterprise_tenant_scope_not_granted");
  await check("continuation scope lookup failure",{scopeError:true,body:{
    operation:"continue_objective:objective-A",resource_id:"objective-A",tenant_id:"tenantA"
  }},503,"scope_lookup_failed");
  await check("insert fails",{insertError:true},503,"authorization_grant_create_failed");
  await check("atomic audit failure",{auditError:"ALLOW"},503,"authorization_grant_create_failed");
  process.stdout.write(count+" grant issuance behavior cases passed\n");
})().catch(err=>{console.error(err);process.exitCode=1});
"""
    result = subprocess.run(
        [node, "-e", javascript + harness],
        capture_output=True,
        text=True,
        timeout=25,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "24 grant issuance behavior cases passed" in result.stdout


def test_active_session_lookup_filters_time_before_limit() -> None:
    """The latest 10 expired or future sessions may not mask a valid session."""
    resolver = AUTHZ.split("async function resolveActiveSession(", 1)[1].split(
        "async function establishSession(", 1
    )[0]
    lookup = resolver.split('supabase.from("elo_identity_sessions")', 1)[1].split(
        "if (error)", 1
    )[0]
    for requirement in (
        '.eq("identity_id", identityId)',
        '.is("revoked_at", null)',
        '.lte("issued_at", nowISO)',
        '.gt("expires_at", nowISO)',
        '.limit(10)',
    ):
        assert requirement in lookup
    assert lookup.index('.gt("expires_at", nowISO)') < lookup.index(".limit(10)")
    assert "Number.isFinite(i)&&Number.isFinite(e)&&i<=now&&e>now" in resolver


def test_active_session_lookup_behavior_with_isolated_supabase() -> None:
    """Execute the actual TS resolver, without creating or reading live sessions."""
    import shutil
    import subprocess

    node = shutil.which("node")
    assert node is not None, "Node is required for authorization behavior tests"
    resolver = "async function resolveActiveSession(" + AUTHZ.split(
        "async function resolveActiveSession(", 1
    )[1].split("\nasync function establishSession(", 1)[0]
    assert resolver.count("identityId: string") == 1
    assert resolver.count("(s:any)") == 1
    resolver = (
        resolver.replace("identityId: string", "identityId")
        .replace("(s:any)", "(s)")
        .replace(" as const", "")
    )
    harness = r"""
const assert = require("node:assert/strict");
const now=Date.now();
const iso = offset => new Date(now+offset).toISOString();
const base = {
  session_id:"valid",identity_id:"owner",
  issued_at:iso(-3600000),expires_at:iso(3600000),
  revoked_at:null,last_seen_at:iso(-3600000)
};
let rows=[], fail=false;
class Query {
  constructor() {this.filters=[];this.sorted=null;}
  select() {return this;}
  eq(k,v){this.filters.push(["eq",k,v]);return this;}
  is(k,v){this.filters.push(["eq",k,v]);return this;}
  lte(k,v){this.filters.push(["lte",k,v]);return this;}
  gt(k,v){this.filters.push(["gt",k,v]);return this;}
  order(k,opts={}) {this.sorted={key:k,asc:opts.ascending!==false};return this;}
  limit(n){
    if(fail) return Promise.resolve({data:null,error:{message:"db error"}});
    const filtered=rows.filter(row=>this.filters.every(([op,key,value])=>{
      if(op==="eq")return row[key]===value;
      if(op==="lte")return row[key]!=null&&row[key]<=value;
      if(op==="gt")return row[key]!=null&&row[key]>value;
      throw Error("unknown filter "+op);
    }));
    if(this.sorted) {
      const {key,asc}=this.sorted;
      filtered.sort((a,b)=>asc
        ? String(a[key]).localeCompare(String(b[key]))
        : String(b[key]).localeCompare(String(a[key])));
    }
    return Promise.resolve({data:filtered.slice(0,n),error:null});
  }
}
const supabase={from:(table)=>{
  assert.equal(table,"elo_identity_sessions");
  return new Query();
}};
async function check(label,data,expectedSession=null,expectedReason=null,identity="owner"){
  rows=data;fail=false;
  const r=await resolveActiveSession(identity);
  if(expectedSession!==null){
    assert.equal(r.ok,true,label+": "+JSON.stringify(r));
    assert.equal(r.session.session_id,expectedSession,label);
  }else{
    assert.equal(r.ok,false,label);
    assert.equal(r.reason,expectedReason,label);
  }
}
(async()=>{
  await check("valid session",[base],"valid");
  const expired=Array.from({length:13},(_,i)=>({
    ...base,session_id:"expired-"+i,issued_at:iso(-1000-i),
    expires_at:iso(-200)
  }));
  await check("13 newer expired sessions do not hide valid", [...expired,base],"valid");
  const future=Array.from({length:13},(_,i)=>({
    ...base,session_id:"future-"+i,issued_at:iso(360000+i)
  }));
  await check("13 newer future sessions do not hide valid",[...future,base],"valid");
  await check("revoked sessions excluded",[
    {...base,session_id:"revoked",issued_at:iso(-1000),revoked_at:iso(-500)},
    base
  ],"valid");
  await check("wrong identity excluded",[
    {...base,session_id:"wrong",identity_id:"other",issued_at:iso(-1000)},
    base
  ],"valid");
  await check("null expiry excluded",[
    {...base,session_id:"no-expiry",expires_at:null,issued_at:iso(-1000)},
    base
  ],"valid");
  await check("only expired denied",expired,null,"active_elo_session_required");
  await check("only future denied",future,null,"active_elo_session_required");
  await check("missing denied",[],null,"active_elo_session_required");
  rows=[base];fail=true;
  const rejected=await resolveActiveSession("owner");
  assert.equal(rejected.ok,false);
  assert.equal(rejected.reason,"session_lookup_failed");
  process.stdout.write("10 active session resolver behavior cases passed\n");
})().catch(e=>{console.error(e);process.exitCode=1});
"""
    result = subprocess.run(
        [node, "-e", resolver + "\n" + harness],
        capture_output=True,
        text=True,
        timeout=25,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "10 active session resolver behavior cases passed" in result.stdout
