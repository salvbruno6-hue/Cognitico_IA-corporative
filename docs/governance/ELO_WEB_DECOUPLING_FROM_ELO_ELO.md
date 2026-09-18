# ELO Web — Desacoplamento de produção de `elo_elo`

## Objetivo

O projeto oficial de produção é `apps/elo-web` / Vercel `elo-web`.

O projeto Vercel `elo_elo` é tratado como legado/dependência a ser descontinuada. Nenhuma rota, autenticação, autoridade ou execução do ELO Web pode depender da existência desse projeto.

## Inventário realizado

### 1. Núcleo cognitivo FastAPI

A implementação antiga estava em:

- `src/elo/interface/api.py`
- `src/elo/interface/contracts.py`
- `src/elo/interface/response.py`
- `src/elo/interface/session.py`
- `src/elo/cognitive/__init__.py`
- `src/elo/cognitive/symbiont_hermes_bridge.py`

O Vercel `elo_elo` expunha `POST /cognitive`.

**Estado:** MIGRADO para `apps/elo-web`.

A reconstrução foi feita nos PRs #557 e #558:

- `apps/elo-web/src/lib/elo-cognitive-core.ts`
- `apps/elo-web/src/lib/elo-cognitive.ts`
- `apps/elo-web/src/lib/elo-hermes-sandbox.ts`
- `apps/elo-web/src/app/api/cognitive/route.ts`

O fluxo atual não requer `ELO_COGNITIVE_API_URL` nem chamada ao Vercel `elo_elo`.

### 2. Hermes / Symbiont

A implementação Python anterior usava `ELO_HERMES_ENDPOINT` + `SymbiontHermesBridge`.

**Estado:** RECONSTRUÍDO no ELO Web para a missão autorizada `runtime_probe`.

O ELO Web usa o Sandbox privado da Vercel, com:

- `ELO_HERMES_GIT_TOKEN`
- `ELO_HERMES_RUNTIME_TOKEN`

O navegador não acessa Hermes diretamente.

### 3. Autorização

A autorização não pertence ao Vercel `elo_elo`.

A autoridade canônica é o Supabase Edge Function `elo-authz`.

O ELO Web chama:

`Browser → ELO Web /api/authorization → Supabase elo-authz`

**Estado:** DESACOPLADO de `elo_elo`.

### 4. Dados de cotações / custo por metro / Lista-Mãe

A implementação de #560 está nas migrations do Supabase canônico:

- `fornecedor_cotacoes`
- `fornecedor_itens_cotacao`
- `registrar_cotacao_fornecedor(...)`
- `vw_cotacoes_itens_custo`

Esses objetos são persistência/camada de dados do Supabase, não runtime do Vercel `elo_elo`.

**Estado:** CANÔNICO NO SUPABASE; não depende da existência do projeto Vercel `elo_elo`.

A regra de histórico permanece:

`cotação → fornecedor → data/origem → item → Lista-Mãe → custo`

sem sobrescrever histórico e sem criar uma nova identidade de Lista-Mãe quando o vínculo não puder ser determinado.

### 5. Core Python

O pacote `src/elo/core` contém construções como:

- orçamento governado;
- fluxo produtivo;
- aprendizado de solicitações;
- identidade/confiança;
- Evolution Gate;
- resolução de contexto;
- conhecimento/promoção;
- capacidades;
- orquestração.

Esses módulos existem no repositório canônico, mas não são chamados pelo ELO Web como um serviço Vercel externo.

**Estado:** NÃO É DEPENDÊNCIA DE RUNTIME DO ELO WEB.

Não serão simplesmente copiados para TypeScript sem contrato, evidência e validação. Cada capacidade que entrar no ELO Web deverá ser reconstruída sob a fronteira própria do Web e validada individualmente.

## Resultado do desacoplamento

A remoção do Vercel `elo_elo` não deve retirar:

- autenticação;
- autorização;
- sessão ELO;
- `/api/cognitive`;
- execução Hermes governada;
- dados Supabase;
- migrations canônicas;
- portal operacional.

## Gate de exclusão do `elo_elo`

O projeto Vercel `elo_elo` somente pode ser apagado depois de todos estes itens:

- [x] ELO Web possui Cognitive Core local.
- [x] ELO Web possui runtime Hermes governado.
- [x] ELO Web não referencia o endpoint cognitivo legado.
- [x] Autorização está no `elo-authz`.
- [x] Dados de cotação/custo por metro estão no Supabase canônico.
- [ ] PR #559 integrado em `main`.
- [ ] Build de produção do ELO Web validado após a integração.
- [ ] Fluxo Google → Supabase → ELO Authorization → Portal validado em produção.
- [ ] Verificação final de referências runtime ao `elo_elo` sem ocorrências.
- [ ] Somente então desativar/remover o projeto Vercel `elo_elo`.

## Regra

Não apagar `elo_elo` antes do gate final.

A fonte de verdade operacional do produto é o ELO Web; o `elo_elo` não pode continuar sendo uma autoridade ou dependência de runtime.
