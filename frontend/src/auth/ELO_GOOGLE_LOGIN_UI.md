# ELO Google Login UI

## Objetivo

Adicionar uma porta de entrada simples para o ELO sem alterar o modelo de autorização já consolidado.

## Experiência

### Primeiro acesso

`Entrar no ELO` → `Continuar com Google` → Google OAuth → Supabase Auth → identidade ELO → sessão.

### Acessos seguintes

`Continuar com Google` → identidade existente → nova sessão → ELO.

Não criar novo cadastro quando a identidade já existir.

### Logout

`Sair` → revogar a sessão atual → retornar à tela de login.

## Segurança

A autenticação Google identifica o usuário. Ela não concede privilégios automaticamente. Role, capability, scope e policy continuam sendo avaliados pelo ELO.

A interface não recebe nem armazena client secret do Google. O provedor OAuth e as credenciais ficam na configuração segura do Supabase.

## Estados mínimos

- carregando sessão;
- não autenticado;
- redirecionamento para Google;
- autenticado;
- logout;
- erro de autenticação;
- identidade sem capability para uma operação protegida.

## Configuração necessária

Definir no runtime:

- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

Configurar no Supabase Auth o provedor Google e o redirect URI da aplicação.

## Limite desta etapa

Este componente implementa a interface e o fluxo cliente. A comprovação de login Google real depende da configuração OAuth no ambiente Supabase e de um teste de integração com uma conta autorizada.
