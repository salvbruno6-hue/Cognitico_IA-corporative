import { NextResponse } from "next/server";

const ALLOWED_ACTIONS = new Set([
  "establish_session","revoke_session","read","consult","search","inspect",
  "portal_access","authorize_area","lista_mae_insert","check_authorization_state","create_operator_binding","issue_authorization_grant",
  "authorize_strategic_write",
]);

type AuthorizationBody = {
  action?: unknown; capability?: unknown; repository?: unknown; resource_id?: unknown;
  area_code?: unknown; operation?: unknown; authorization_state?: unknown;
  identity_id?: unknown; github_user_id?: unknown; github_login?: unknown;
  operation_class?: unknown; binding_id?: unknown; expires_in_seconds?: unknown;
  strategic_action?: unknown; tenant_id?: unknown; resource_ref?: unknown;
};

function json(data: unknown,status=200){return NextResponse.json(data,{status,headers:{"Cache-Control":"no-store"}});}

export async function POST(request:Request){
  const authorization=request.headers.get("authorization")?.trim()??"";
  if(!authorization.startsWith("Bearer "))return json({authorized:false,reason:"missing_bearer"},401);
  const supabaseUrl=process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  if(!supabaseUrl)return json({authorized:false,reason:"supabase_url_not_configured"},500);
  let body:AuthorizationBody={};
  try{body=(await request.json()) as AuthorizationBody;}catch{return json({authorized:false,reason:"invalid_json"},400);}
  const action=typeof body.action==="string"&&body.action.trim()?body.action.trim():"establish_session";
  if(!ALLOWED_ACTIONS.has(action))return json({authorized:false,reason:"action_not_allowed_at_elo_web_boundary"},403);
  const upstream=await fetch(`${supabaseUrl}/functions/v1/elo-authz`,{
    method:"POST",headers:{Authorization:authorization,"Content-Type":"application/json","x-elo-request-id":request.headers.get("x-elo-request-id")?.trim()||crypto.randomUUID()},
    body:JSON.stringify({
      action,
      capability:typeof body.capability==="string"?body.capability.trim():undefined,
      repository:typeof body.repository==="string"?body.repository.trim():undefined,
      resource_id:typeof body.resource_id==="string"?body.resource_id.trim():undefined,
      area_code:typeof body.area_code==="string"?body.area_code.trim():undefined,
      operation:typeof body.operation==="string"?body.operation.trim():undefined,
      authorization_state:typeof body.authorization_state==="string"?body.authorization_state.trim():undefined,
      identity_id:typeof body.identity_id==="string"?body.identity_id.trim():undefined,
      github_user_id:body.github_user_id,
      github_login:typeof body.github_login==="string"?body.github_login.trim():undefined,
      operation_class:typeof body.operation_class==="string"?body.operation_class.trim():undefined,
      binding_id:typeof body.binding_id==="string"?body.binding_id.trim():undefined,
      expires_in_seconds:body.expires_in_seconds,
      strategic_action:typeof body.strategic_action==="string"?body.strategic_action.trim():undefined,
      tenant_id:typeof body.tenant_id==="string"?body.tenant_id.trim():undefined,
      resource_ref:typeof body.resource_ref==="string"?body.resource_ref.trim():undefined,
    }),
    cache:"no-store",
  });
  const payload=await upstream.json().catch(()=>({authorized:false,reason:"invalid_authorization_response"}));
  return json(payload,upstream.status);
}
