import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

const ACTION_CAPABILITY: Record<string, string> = {
  read: "READ", consult: "READ", search: "READ", inspect: "READ",
  portal_access: "PORTAL_READ",
  modify_cognitive_identity: "ADMIN", modify_core: "CANONICAL_WRITE",
  modify_canonical_memory: "CANONICAL_WRITE", modify_security_policy: "ADMIN",
  change_permissions: "ADMIN", promote_to_core: "CANONICAL_WRITE",
  merge_protected_change: "APPROVE",
};

const AREA_CAPABILITIES: Record<string, string> = {
  consult: "PORTAL_READ",
  read: "PORTAL_READ",
  stock_read: "ALMX_READ",
  stock_insert: "ALMX_INSERT",
  stock_update: "ALMX_UPDATE",
  stock_adjust: "ALMX_ADJUST",
  pcp_read: "PCP_READ",
  pcp_update: "PCP_UPDATE",
};

const CRITICAL_ACTIONS = new Set([
  "modify_cognitive_identity","modify_core","modify_canonical_memory",
  "modify_security_policy","change_permissions","promote_to_core","merge_protected_change",
]);

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json", "Cache-Control": "no-store",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "authorization, content-type, x-elo-request-id",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
    },
  });
}

async function audit(identityId: string, sessionId: string | null, action: string, resource: string | null, decision: "ALLOW"|"DENY", reason: string, requestId: string) {
  const { error } = await supabase.from("elo_authorization_audit").insert({
    identity_id: identityId, session_id: sessionId, action, resource, decision, reason, request_id: requestId,
  });
  if (error) throw new Error("authorization_audit_write_failed");
}

async function authenticate(req: Request) {
  const header = req.headers.get("Authorization") ?? "";
  const token = header.startsWith("Bearer ") ? header.slice(7).trim() : "";
  if (!token) return { ok: false as const, reason: "missing_bearer" };

  const { data, error } = await supabase.auth.getUser(token);
  if (error || !data.user) return { ok: false as const, reason: "invalid_token" };

  const email = typeof data.user.email === "string" ? data.user.email.trim().toLowerCase() : "";
  if (!email) return { ok: false as const, reason: "authenticated_email_missing" };

  const { data: identity, error: identityError } = await supabase
    .from("elo_identity_registry")
    .select("identity_id,display_name,active,provider,provider_subject,enterprise_context,authorized_email")
    .eq("auth_user_id", data.user.id).eq("active", true).maybeSingle();

  if (identityError) return { ok: false as const, reason: "identity_lookup_failed" };
  if (!identity) return { ok: false as const, reason: "operator_binding_missing" };
  if (identity.provider === "google" && String(identity.authorized_email ?? "").trim().toLowerCase() !== email) {
    return { ok: false as const, reason: "authorized_email_mismatch" };
  }

  const { data: roleRows, error: roleError } = await supabase
    .from("elo_identity_roles").select("role_id,elo_roles(code,active)").eq("identity_id", identity.identity_id);
  if (roleError) return { ok: false as const, reason: "role_lookup_failed" };

  const roles = (roleRows ?? []).map((r:any)=>r.elo_roles)
    .filter((r:any)=>r?.active===true).map((r:any)=>String(r.code));

  return {
    ok: true as const, user:data.user, email, identity, roles,
    roleIds:(roleRows ?? []).map((r:any)=>r.role_id).filter(Boolean),
  };
}

async function resolveActiveSession(identityId: string) {
  const { data, error } = await supabase.from("elo_identity_sessions")
    .select("session_id,issued_at,expires_at,revoked_at,last_seen_at")
    .eq("identity_id", identityId).is("revoked_at", null)
    .order("issued_at",{ascending:false}).limit(10);
  if (error) return { ok:false as const, reason:"session_lookup_failed" };
  const now=Date.now();
  const session=(data ?? []).find((s:any)=>{
    const i=Date.parse(String(s.issued_at)), e=Date.parse(String(s.expires_at));
    return Number.isFinite(i)&&Number.isFinite(e)&&i<=now&&e>now;
  });
  return session ? {ok:true as const,session} : {ok:false as const,reason:"active_elo_session_required"};
}

async function establishSession(identityId:string) {
  const existing=await resolveActiveSession(identityId);
  if(existing.ok) {
    const refreshedAt=new Date().toISOString();
    const {error}=await supabase.from("elo_identity_sessions").update({last_seen_at:refreshedAt}).eq("session_id",existing.session.session_id);
    if(error) return {ok:false as const,reason:"session_refresh_failed"};
    return {ok:true as const,session:{...existing.session,last_seen_at:refreshedAt},reused:true};
  }
  if(existing.reason!=="active_elo_session_required") return existing;
  const now=new Date(), expires=new Date(now.getTime()+8*60*60*1000);
  const {data,error}=await supabase.from("elo_identity_sessions").insert({
    identity_id:identityId,issued_at:now.toISOString(),expires_at:expires.toISOString(),
    revoked_at:null,last_seen_at:now.toISOString()
  }).select("session_id,issued_at,expires_at,revoked_at,last_seen_at").single();
  if(error||!data) return {ok:false as const,reason:"session_create_failed"};
  return {ok:true as const,session:data,reused:false};
}

async function revokeSession(identityId:string) {
  const {data,error}=await supabase.from("elo_identity_sessions").update({revoked_at:new Date().toISOString()})
    .eq("identity_id",identityId).is("revoked_at",null).select("session_id");
  return error ? {ok:false as const,reason:"session_revoke_failed"} : {ok:true as const,revoked:data?.length??0};
}

async function hasCapability(roleIds:string[], code:string) {
  if(!roleIds.length) return {ok:true as const,granted:false};
  const {data,error}=await supabase.from("elo_role_capabilities")
    .select("capability_id,elo_capabilities(code,active)").in("role_id",roleIds);
  if(error) return {ok:false as const,reason:"capability_lookup_failed"};
  return {ok:true as const,granted:(data??[]).some((r:any)=>r.elo_capabilities?.active===true&&r.elo_capabilities?.code===code)};
}

async function getScopes(identityId:string) {
  const {data,error}=await supabase.from("elo_identity_scopes")
    .select("elo_scopes(scope_id,scope_type,scope_key,description,active)").eq("identity_id",identityId);
  if(error) return {ok:false as const,reason:"scope_lookup_failed"};
  return {ok:true as const,scopes:(data??[]).map((r:any)=>r.elo_scopes).filter((s:any)=>s?.active===true)};
}

async function resolveAuthorizationGrant(identityId:string, sessionId:string, state:string, operation:string, repository:string) {
  const allowed = new Set([
    "elo-execution-authorized",
    "elo-commit-authorized",
    "elo-merge-authorized",
  ]);
  if(!allowed.has(state)) return {ok:false as const,reason:"authorization_state_not_supported"};

  const {data,error}=await supabase.from("elo_authorization_grants")
    .select("grant_id,binding_id,authorization_state,operation,repository_full_name,issued_at,expires_at,revoked_at")
    .eq("identity_id",identityId)
    .eq("authorization_state",state)
    .eq("operation",operation)
    .eq("repository_full_name",repository)
    .is("revoked_at",null)
    .order("issued_at",{ascending:false})
    .limit(10);

  if(error) return {ok:false as const,reason:"authorization_grant_lookup_failed"};

  const now=Date.now();
  const grant=(data??[]).find((g:any)=>{
    const issued=Date.parse(String(g.issued_at));
    const expires=Date.parse(String(g.expires_at));
    return Number.isFinite(issued)&&Number.isFinite(expires)&&issued<=now&&expires>now;
  });
  if(!grant) return {ok:false as const,reason:"authorization_state_not_granted"};

  const {data:binding,error:bindingError}=await supabase.from("elo_operator_github_bindings")
    .select("binding_id,identity_id,github_user_id,github_login,repository_full_name,operation_class,active")
    .eq("binding_id",grant.binding_id).eq("identity_id",identityId)
    .eq("repository_full_name",repository).eq("active",true).maybeSingle();

  if(bindingError) return {ok:false as const,reason:"operator_binding_lookup_failed"};
  if(!binding) return {ok:false as const,reason:"operator_binding_inactive"};

  return {ok:true as const,grant,binding};
}

Deno.serve(async(req:Request)=>{
  if(req.method==="OPTIONS") return new Response(null,{status:204,headers:{"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"authorization, content-type, x-elo-request-id","Access-Control-Allow-Methods":"POST, OPTIONS"}});
  if(req.method!=="POST") return json({error:"method_not_allowed"},405);
  const requestId=req.headers.get("x-elo-request-id")?.trim()||crypto.randomUUID();
  const auth=await authenticate(req);
  if(!auth.ok) return json({authorized:false,reason:auth.reason,request_id:requestId},auth.reason==="missing_bearer"||auth.reason==="invalid_token"?401:403);

  let body:any={}; try{body=await req.json();}catch{return json({authorized:false,reason:"invalid_json",request_id:requestId},400);}
  const action=typeof body.action==="string"&&body.action.trim()?body.action.trim():"read";
  const repository=typeof body.repository==="string"?body.repository.trim():"";

  if(action==="establish_session") {
    const established=await establishSession(auth.identity.identity_id);
    if(!established.ok){try{await audit(auth.identity.identity_id,null,action,null,"DENY",established.reason,requestId);}catch{return json({authorized:false,reason:"authorization_audit_write_failed",request_id:requestId},503);}return json({authorized:false,reason:established.reason,request_id:requestId},403);}
    try{await audit(auth.identity.identity_id,established.session.session_id,action,null,"ALLOW","authenticated_identity_session_established",requestId);}catch{return json({authorized:false,reason:"authorization_audit_write_failed",request_id:requestId},503);}
    return json({authorized:true,action,identity_id:auth.identity.identity_id,session_id:established.session.session_id,reused:established.reused,display_name:auth.identity.display_name,email:auth.email,provider:auth.identity.provider,request_id:requestId,authorization_authority:"elo-authz"});
  }

  if(action==="revoke_session") {
    const revoked=await revokeSession(auth.identity.identity_id);
    if(!revoked.ok)return json({authorized:false,reason:revoked.reason,request_id:requestId},503);
    try{await audit(auth.identity.identity_id,null,action,null,"ALLOW","authenticated_identity_sessions_revoked",requestId);}catch{return json({authorized:false,reason:"authorization_audit_write_failed",request_id:requestId},503);}
    return json({authorized:true,action,revoked:revoked.revoked,identity_id:auth.identity.identity_id,request_id:requestId,authorization_authority:"elo-authz"});
  }

  const session=await resolveActiveSession(auth.identity.identity_id);
  if(!session.ok) {
    try{await audit(auth.identity.identity_id,null,action,repository||null,"DENY",session.reason,requestId);}catch{}
    return json({authorized:false,reason:session.reason,request_id:requestId},403);
  }

  if(action==="check_authorization_state") {
    const state=typeof body.authorization_state==="string"?body.authorization_state.trim():"";
    const operation=typeof body.operation==="string"?body.operation.trim():"";
    if(!state||!operation||!repository)return json({authorized:false,reason:"authorization_state_operation_repository_required",request_id:requestId},400);

    const grant=await resolveAuthorizationGrant(auth.identity.identity_id,session.session_id,state,operation,repository);
    if(!grant.ok){
      try{await audit(auth.identity.identity_id,session.session.session_id,action,repository,"DENY",grant.reason,requestId);}catch{}
      return json({authorized:false,reason:grant.reason,authorization_state:state,operation,repository,request_id:requestId},403);
    }

    try{await audit(auth.identity.identity_id,session.session.session_id,action,repository,"ALLOW","explicit_authorization_state_verified",requestId);}
    catch{return json({authorized:false,reason:"authorization_audit_write_failed",request_id:requestId},503);}

    return json({
      authorized:true,
      action,
      authorization_state:state,
      operation,
      repository,
      identity_id:auth.identity.identity_id,
      session_id:session.session.session_id,
      binding_id:grant.binding.binding_id,
      github_user_id:grant.binding.github_user_id,
      github_login:grant.binding.github_login,
      operation_class:grant.binding.operation_class,
      grant_id:grant.grant.grant_id,
      expires_at:grant.grant.expires_at,
      request_id:requestId,
      authorization_authority:"elo-authz"
    });
  }

  if(action==="portal_access") {
    const cap=await hasCapability(auth.roleIds,"PORTAL_READ");
    const scopes=await getScopes(auth.identity.identity_id);
    if(!cap.ok||!scopes.ok)return json({authorized:false,reason:(!cap.ok?cap.reason:scopes.reason),request_id:requestId},403);
    if(!cap.granted)return json({authorized:false,reason:"portal_read_not_granted",request_id:requestId},403);
    try{await audit(auth.identity.identity_id,session.session.session_id,action,null,"ALLOW","portal_identity_scope_capability_verified",requestId);}catch{return json({authorized:false,reason:"authorization_audit_write_failed",request_id:requestId},503);}
    const caps=await supabase.from("elo_role_capabilities").select("elo_capabilities(code,name,description,active)").in("role_id",auth.roleIds);
    return json({authorized:true,action,identity_id:auth.identity.identity_id,email:auth.email,display_name:auth.identity.display_name,roles:auth.roles,scopes:scopes.scopes,capabilities:(caps.data??[]).map((r:any)=>r.elo_capabilities).filter((c:any)=>c?.active===true),session_id:session.session.session_id,request_id:requestId,authorization_authority:"elo-authz"});
  }

  if(action==="authorize_area") {
    const areaCode=typeof body.area_code==="string"?body.area_code.trim():"";
    const operation=typeof body.operation==="string"?body.operation.trim():"";
    const capabilityCode=AREA_CAPABILITIES[operation];
    if(!areaCode||!capabilityCode)return json({authorized:false,reason:"area_and_supported_operation_required",request_id:requestId},400);
    const scopes=await getScopes(auth.identity.identity_id);
    if(!scopes.ok)return json({authorized:false,reason:scopes.reason,request_id:requestId},403);
    const allowed=scopes.scopes.some((s:any)=>s.scope_key===areaCode);
    if(!allowed){try{await audit(auth.identity.identity_id,session.session.session_id,action,areaCode,"DENY","area_scope_not_granted",requestId);}catch{}return json({authorized:false,reason:"area_scope_not_granted",area_code:areaCode,operation,request_id:requestId},403);}
    const cap=await hasCapability(auth.roleIds,capabilityCode);
    if(!cap.ok||!cap.granted){try{await audit(auth.identity.identity_id,session.session.session_id,action,areaCode,"DENY","area_capability_not_granted",requestId);}catch{}return json({authorized:false,reason:"area_capability_not_granted",area_code:areaCode,operation,capability:capabilityCode,request_id:requestId},403);}
    try{await audit(auth.identity.identity_id,session.session.session_id,action,areaCode,"ALLOW","area_scope_and_capability_verified",requestId);}catch{return json({authorized:false,reason:"authorization_audit_write_failed",request_id:requestId},503);}
    return json({authorized:true,action,area_code:areaCode,operation,capability:capabilityCode,identity_id:auth.identity.identity_id,session_id:session.session.session_id,request_id:requestId,authorization_authority:"elo-authz"});
  }

  const requestedCapability=typeof body.capability==="string"?body.capability.trim():"";
  const capability=ACTION_CAPABILITY[action];
  if(!capability||(requestedCapability&&requestedCapability!==capability))return json({authorized:false,reason:"capability_not_canonical_for_action",request_id:requestId},403);

  if(repository){
    const scopes=await getScopes(auth.identity.identity_id);
    if(!scopes.ok)return json({authorized:false,reason:scopes.reason,request_id:requestId},403);
    if(!scopes.scopes.some((s:any)=>s.scope_key===repository))return json({authorized:false,reason:"repository_out_of_scope",request_id:requestId},403);
  }
  if(CRITICAL_ACTIONS.has(action)&&!auth.roles.includes("CANONICAL_ADMIN"))return json({authorized:false,reason:"canonical_authority_required",request_id:requestId},403);

  const cap=await hasCapability(auth.roleIds,capability);
  if(!cap.ok||!cap.granted)return json({authorized:false,reason:cap.ok?"capability_not_granted":cap.reason,capability,request_id:requestId},403);
  try{await audit(auth.identity.identity_id,session.session.session_id,action,repository||null,"ALLOW","identity_session_scope_and_capability_verified",requestId);}catch{return json({authorized:false,reason:"authorization_audit_write_failed",request_id:requestId},503);}
  return json({authorized:true,role:auth.roles[0]??null,roles:auth.roles,identity_id:auth.identity.identity_id,session_id:session.session.session_id,display_name:auth.identity.display_name,email:auth.email,provider:auth.identity.provider,enterprise_context:auth.identity.enterprise_context,action,capability,repository:repository||null,request_id:requestId,authorization_authority:"elo-authz"});
});
