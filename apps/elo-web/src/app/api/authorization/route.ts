import { NextResponse } from "next/server";

const ALLOWED_ACTIONS = new Set([
  "establish_session","revoke_session","read","consult","search","inspect",
  "portal_access","authorize_area",
]);

type AuthorizationBody = { action?: unknown; capability?: unknown; repository?: unknown; area_code?: unknown; operation?: unknown; };

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
    body:JSON.stringify({action,capability:typeof body.capability==="string"?body.capability.trim():undefined,repository:typeof body.repository==="string"?body.repository.trim():undefined,area_code:typeof body.area_code==="string"?body.area_code.trim():undefined,operation:typeof body.operation==="string"?body.operation.trim():undefined}),
    cache:"no-store",
  });
  const payload=await upstream.json().catch(()=>({authorized:false,reason:"invalid_authorization_response"}));
  return json(payload,upstream.status);
}
