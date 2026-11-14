# ELO Web — Central de Autorizações: contrato de implantação (GAP #1236)

## Evidências verificadas em 2026-11-14

- `apps/elo-web/src/components/elo-dashboard.tsx` contém a navegação `Governança`, mas não tinha painel de decisões.
- `apps/elo-web/src/app/api/authorization/route.ts` é o boundary server-side que encaminha operações ao `elo-authz`; não é uma nova autoridade.
- `supabase/functions/elo-authz/index.ts` exige `authorization_state`, `operation`, `repository` e `resource_id` para `check_authorization_state`.
- Consulta de inventário no Supabase canônico encontrou `public.elo_authorization_audit` e `public.elo_authorization_grants`; **não identificou** tabela de fila de pedidos/notificações com os nomes pesquisados. Isso não comprova ausência de uma fonte externa/canônica.
- Uma sessão Google/ELO estabelecida não equivale a um grant de merge.

## Entrega desta PR

- Superfície visual em `Governança`, integrada ao dashboard existente.
- Consulta explícita **somente leitura** de grant `elo-merge-authorized` para `operation=merge`, `repository=salvbruno6-hue/Cognitico_IA-corporative`, `resource_id=pr:<numero>@<sha40>`.
- Estado de erro/negação fail-closed; nenhuma contagem de solicitações inventada; nenhum botão de aprovação ativo.

## GAP de integração — não implementar por inferência

Antes de disponibilizar inbox, notificações ou decisões:
1. Identificar o owner canônico da **solicitação** e seu estado (não confundir `grants` emitidos com pedidos pendentes).
2. Definir contrato mínimo read-only de listagem paginada, filtrada por identidade/escopo, com `request_id`, PR, SHA, motivo, expiração, gates e proveniência.
3. Validar identidade CANONICAL_ADMIN, sessão ELO e GitHub binding no servidor antes de qualquer decisão; não usar `user_metadata` ou confiança no frontend.
4. Definir mecanismo de aprovação/rejeição no owner `elo-authz` e exigir revisão independente, idempotência, auditoria e prevenção de replay.
5. Garantir dependências de #1171, #1173, #1175, #1177 conforme aplicáveis e os gates atuais antes de liberar merge.
6. Realizar teste de ponta a ponta com solicitações reais; validar estados vazios, falha de rede, sessão expirada, grant inválido e mudança de HEAD.

## Restrições

- Sem novo banco, nova tabela, novo fluxo OAuth ou autoridade paralela nesta PR.
- Sem merge, emissão de grant ou deploy por esta interface.
- Não afirmar que contagem de grants = contagem de solicitações.
- PR permanece Draft até validação e governança.
