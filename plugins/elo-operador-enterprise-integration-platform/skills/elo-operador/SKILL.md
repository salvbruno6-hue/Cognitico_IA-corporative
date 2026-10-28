---
name: elo-operador
description: Consulte o banco ELO no Supabase e o sistema cognitivo no GitHub para verificar evidências, estado das fontes, memória e implementação, sem depender do frontend ELO.
---

# ELO Operador

## Fontes e escopo

- Banco: projeto Supabase `Elo-forge`, ID `fxbpevjrkwhbicpmecow`.
- Sistema: `salvbruno6-hue/Cognitico_IA-corporative`, branch canônico `main`.
- Reutilize as ferramentas dos conectores autenticados Supabase e GitHub declarados neste plugin.
- Não exija abrir páginas do ELO, Vercel, GitHub Pages ou autenticar o ELO-MCP para este fluxo.
- Este modo consulta fontes por acesso delegado do usuário; não representa uma sessão de runtime autorizada por `elo-authz`. Não simule `elo_status`, gates ou permissões.

## Limites

Esta versão executa somente consultas. No GitHub, use busca e leitura de arquivos, commits, issues, PRs e checks. No Supabase, use leitura de metadados, logs e SELECTs estritamente de consulta. Para várias consultas relacionadas, use transação READ ONLY quando suportada. Nunca execute DML, DDL, funções com efeitos colaterais, migrations, deploy, merge, grants ou promoção de conhecimento neste fluxo.

Os conectores podem expor ferramentas de escrita: a presença delas não autoriza seu uso por esta habilidade. A instrução de leitura não altera as permissões técnicas das contas. Não use acesso administrativo para contornar RLS, tenant, scopes ou decisões de negócio; se a consulta depender de autorização canônica não comprovada, relate o GAP e pare essa consulta. Não leia segredos, tokens ou dados pessoais desnecessários.

## Fluxo

1. Identifique objetivo, fonte e escopo. Para uma análise integrada, consulte ambas as fontes antes da conclusão.
2. No GitHub, leia `AGENTS.md`, as regras de navegação e os contratos pertinentes antes de interpretar o sistema. Busque implementações existentes em vez de inventar capacidades.
3. No banco, confirme o projeto. Inspecione o schema e as fontes consultivas existentes antes de SELECTs limitados e pertinentes ao pedido. Preserve contexto e proveniência.
4. GitHub é a fonte operacional canônica; Supabase fornece memória e evidências persistentes consultivas. O ELO permanece o orquestrador cognitivo. Conflitos geram GAP e investigação, nunca prevalência silenciosa.
5. Para "status do ELO", apresente separadamente conectividade do banco, evidências persistentes e estado observado no repositório. Não converta esses resultados em prova de saúde do runtime ou de acesso a todas as tabelas.
6. Não estime dados faltantes, não promova experiências a regras e não denomine indicador como KPI formal sem definição e evidência.
7. Se um conector não estiver disponível, informe qual está ausente. Não substitua por páginas do ELO nem invente resultados.

## Retorno

Informe evidências com projeto/tabela ou arquivo/branch/commit, lacunas, análise e próxima ação autorizada. Relacione os achados das duas fontes sem criar autoridade paralela.
