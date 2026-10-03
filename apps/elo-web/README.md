# ELO Web

Superfície web mínima para validação da autenticação e da sessão operacional do ELO.

## Fluxo de teste atual

`Google OAuth → Supabase authenticated session → ELO Authorization establish_session → tela de confirmação`

O navegador **não** emite grants de execução, commit ou merge.

## O que permanece nesta fase

- login Google;
- callback OAuth em `/auth/callback`;
- sessão autenticada do Supabase;
- chamada governada `establish_session`;
- revogação da sessão no logout;
- tela mínima para confirmar o resultado.

## O que foi retirado da superfície de teste

- Terminal Hermes;
- Portal Operacional;
- operações de Lista-Mãe/Almoxarifado;
- views de governança do Symbiont;
- rotas e componentes de teste que não são necessários para validar a autenticação.

Esses itens não são necessários para o primeiro teste de sessão e não devem participar do diagnóstico atual.

## Fronteira

```text
Google
  ↓
Supabase Auth
  ↓
ELO Web
  ↓
/api/authorization
  ↓
elo-authz
  ↓
sessão ELO
```

O ELO Web não é autoridade de governança. A autorização continua no `elo-authz`.

## Vercel

Projeto: `elo-web`

Root Directory:

`apps/elo-web`

Framework:

`Next.js`

Build:

`next build`

Valores públicos do Supabase podem ser usados somente para o fluxo de autenticação. Nenhuma credencial de Hermes ou segredo de infraestrutura deve ser exposto ao navegador.
