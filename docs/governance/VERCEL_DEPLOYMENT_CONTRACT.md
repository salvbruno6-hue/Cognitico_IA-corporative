# Contrato Universal de Deploy Vercel

## Objetivo

Impedir que um projeto web seja considerado integrado enquanto a configuração do repositório e a configuração externa do Vercel estiverem divergentes.

Este contrato é aplicável a qualquer aplicação Vercel presente neste repositório e deve ser reutilizado nos demais repositórios/projetos Vercel da organização.

## Princípios

1. **Uma fonte de código:** GitHub é a autoridade do código.
2. **Uma fonte de infraestrutura de deploy:** o projeto Vercel correspondente é a autoridade da configuração de implantação.
3. **Sem configuração implícita:** Root Directory, framework, Node e comandos críticos devem ser verificáveis.
4. **Sem `latest` em toolchain de build:** versões críticas devem ser determinísticas.
5. **Sem sucesso presumido:** merge/deploy só é considerado concluído após evidência do build e da URL.
6. **Sem correção local especulativa:** uma falha Vercel deve ser corrigida pela causa observada.
7. **Sem duplicação de projeto:** cada aplicação deve ter um único vínculo GitHub → Vercel → domínio/alias de produção.

## Contrato mínimo para aplicações Next.js

| Campo | Regra |
|---|---|
| Framework | Next.js detectado pelo Vercel |
| Root Directory | Diretório que contém o `package.json` da aplicação |
| Node.js | Versão explícita e suportada; usar 22.x como baseline deste projeto |
| Build Command | `next build` ou comando equivalente declarado no package.json |
| Install Command | padrão do gerenciador usado pelo lockfile |
| Output Directory | padrão do framework, salvo necessidade documentada |
| Ignored Build Step | automático, salvo regra documentada |
| Toolchain | versões fixadas no `package.json`/lockfile |

## Estado desejado do ELO Web

```text
GitHub main
  -> Vercel project: elo-web
  -> Root: apps/elo-web
  -> Next.js
  -> Node 22.x
  -> next build
  -> Production
  -> URL/alias validado
```

## Gate obrigatório

Uma aplicação Vercel não pode ser marcada como integrada somente porque o GitHub CI passou. O aceite requer:

- validação estrutural no GitHub;
- configuração externa do Vercel conferida;
- build Vercel observado como Ready;
- deployment de produção observado como Ready quando aplicável;
- URL acessível;
- smoke test da aplicação;
- evidência registrada no PR/deployment.

## Prevenção de recorrência

O workflow `vercel-project-governance.yml` executa a validação estrutural em todo PR e em alterações relacionadas a aplicações web.

Quando uma aplicação falhar neste gate, a correção deve ser feita antes do merge ou explicitamente registrada como GAP governado. Não é permitido contornar o gate por renome de projeto, novo alias ou criação de uma segunda aplicação Vercel.

## Limite deste contrato

O GitHub não consegue, por si só, garantir que a configuração externa do painel Vercel permaneça correta. Essa parte deve ser auditada pelo projeto Vercel e pela conexão administrativa Vercel. Portanto, este contrato separa claramente:

- **determinismo de código:** bloqueado por CI;
- **configuração de infraestrutura:** auditada no Vercel;
- **estado real do deployment:** validado por evidência.
