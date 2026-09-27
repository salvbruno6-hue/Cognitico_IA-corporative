---
artifact_id: ELO-MERGE-COORDINATOR
title: ELO Merge Coordinator
family: docs/governance
layer: governance
type: contract
owner: ELO Governance
authority: reference
status: defined
version: 0.1.0
related:
  - ELO_GOVERNED_AUTONOMOUS_ISSUE_LOOP
  - ELO_OPERATOR_GITHUB_BINDING_RUNTIME
  - AGENTS.md
  - ELO_PR_GOVERNANCE_GATE
---

# ELO Merge Coordinator

## 1. Propósito

Coordenar o merge governado de PRs que atingiram o estado
PR-ready após todos os gates obrigatórios passarem.

O coordinator NÃO decide merge. Ele consome a decisão já
expressa em:
- comentário `PR-ready` publicado por `elo-agent-loop`
- gates verdes (CI + Evolution Gate + Virtual Lab quando
  aplicável + Maintenance Coordinator)
- `elo-merge-authorized` ativa em `elo_authorization_grants`

## 2. Natureza

O coordinator é um **workflow irmão** que reage via
`workflow_run` à conclusão de outros workflows.

Ele NÃO:
- Cria autorização
- Fabrica decisão
- Substitui `elo-authz`
- Substitui o Evolution Gate
- Substitui o `elo-agent-loop`
- Bypassa branch protection
- Mergeia sem `elo-merge-authorized`
- Mergeia com review bloqueante pendente

Ele É:
- O executor da transição `PR → APPROVE_MERGE → GIT_MERGE`
  quando as condições já estão satisfeitas
- Um consumidor passivo dos gates e autorizações existentes

## 3. Fluxo

```text
workflow_run: completed
        ↓
identificar PR pelo head SHA
        ↓
PR-ready confirmado
        ↓
gates obrigatórios verificados
        ↓
review bloqueante ausente
        ↓
elo-merge-authorized válido consultado no Supabase
        ↓
merge state/branch protection permitido
        ↓
APPROVE_MERGE (derivado; não fabricado)
        ↓
GIT_MERGE via GitHub
        ↓
verificar PR merged + SHA/base
```

O coordinator deve falhar fechado: qualquer condição ausente,
indeterminada, expirada ou bloqueada interrompe a execução sem merge.

## 4. Condições obrigatórias de merge

O merge somente pode ser executado quando todas as condições abaixo forem verdadeiras:

1. A PR é aberta, não é draft e tem base `main`.
2. A PR contém o comentário operacional de `PR-ready` publicado pelo `elo-agent-loop`.
3. A cabeça da PR permanece no SHA para o qual os gates foram avaliados; qualquer novo commit exige nova avaliação.
4. Todos os checks obrigatórios do GitHub estão concluídos com sucesso.
5. Os gates ELO obrigatórios aplicáveis estão verdes, incluindo Evolution Gate e Maintenance Coordinator; Virtual Laboratory é obrigatório quando o escopo da alteração o exigir.
6. Não existe review bloqueante (`CHANGES_REQUESTED`) nem review pendente que impeça o merge segundo a proteção do repositório.
7. Existe um grant `elo-merge-authorized` válido para este repositório e operação, com `revoked_at IS NULL`, janela temporal válida e binding GitHub ativo.
8. O grant foi emitido pelo `elo-authz` sob `CANONICAL_ADMIN`; o coordinator aceita somente evidência compatível com o registro de emissão canônico.
9. O estado de merge da PR indica que o GitHub permite a integração (`mergeable`/`mergeStateStatus` compatíveis com merge).
10. A operação não exige bypass de branch protection, review, checks ou autorização.

`mergeable=true` isoladamente nunca é suficiente.

## 5. Autorização `elo-merge-authorized`

A autorização é consumida de `public.elo_authorization_grants`.

O coordinator não cria, renova, prolonga, revoga ou interpreta uma nova autorização.

A consulta deve exigir, no mínimo:

- `authorization_state = elo-merge-authorized`;
- operação de merge governado compatível com o grant;
- `repository_full_name` igual ao repositório atual;
- `revoked_at IS NULL`;
- `issued_at <= now`;
- `expires_at > now`;
- binding correspondente ativo e vinculado ao mesmo repositório;
- evidência de emissão por `CANONICAL_ADMIN` através do `elo-authz`.

A ausência de grant válido produz `WAITING_FOR_AUTHORIZATION`, nunca uma autorização implícita.

## 6. Gates e evidências

O coordinator não redefine o conteúdo dos gates. Ele consulta seus resultados existentes e usa o GitHub como superfície de estado da PR.

A regra operacional é:

```text
PR_READY
AND
REQUIRED_CHECKS_PASS
AND
EVOLUTION_GATE_PASS
AND
MAINTENANCE_COORDINATOR_PASS
AND
VIRTUAL_LAB_PASS (quando aplicável)
AND
REVIEWS_CLEAR
AND
ELO_MERGE_AUTHORIZED
AND
BRANCH_PROTECTION_PERMITS
→ APPROVE_MERGE → GIT_MERGE
```

Quando um gate aplicável não puder ser determinado de forma confiável,
o resultado é `WAITING_FOR_EVIDENCE` e não merge.

## 7. Revalidação e idempotência

Cada execução deve reconsultar o estado atual da PR e do grant antes do merge.

Uma autorização ou avaliação anterior não é reutilizada depois de um novo commit.

Se a PR já estiver `MERGED`, o coordinator não executa uma segunda operação e apenas registra `ALREADY_MERGED`.

Se a PR estiver fechada sem merge, o coordinator encerra com `NOT_MERGEABLE`.

## 8. Branch protection

O coordinator usa exclusivamente as capacidades normais do GitHub para realizar o merge.

Ele não usa endpoints ou opções de bypass, não desativa proteção,
não ignora checks e não remove reviews obrigatórias.

Se o GitHub responder que a PR não pode ser mesclada, o coordinator
registra a condição e termina sem merge.

## 9. Segurança do workflow irmão

O `workflow_run` possui acesso potencial a segredos e permissões de escrita.
Por isso:

- o coordinator não faz checkout nem executa código da branch da PR;
- os scripts executados pertencem ao próprio workflow ou usam comandos
  determinísticos do runner;
- o conteúdo da PR é tratado como dado não confiável;
- segredos são usados somente para a consulta autorizada ao Supabase e para
  a operação GitHub governada;
- nenhum dado retornado pela PR pode criar ou alterar uma autorização.

## 10. Estados operacionais

O coordinator deve produzir estados observáveis, pelo menos:

- `WAITING_FOR_PR_READY`
- `WAITING_FOR_GATES`
- `WAITING_FOR_AUTHORIZATION`
- `WAITING_FOR_REVIEWS`
- `WAITING_FOR_BRANCH_PROTECTION`
- `WAITING_FOR_EVIDENCE`
- `APPROVE_MERGE`
- `MERGED`
- `ALREADY_MERGED`
- `NOT_MERGEABLE`
- `BLOCKED`

Esses estados são evidência operacional; não constituem uma nova autoridade cognitiva.

## 11. Falha fechada

Em caso de erro de consulta, timeout, resposta inconsistente, segredo ausente,
grant inválido, gate desconhecido ou estado de proteção indeterminado,
o coordinator não tenta uma alternativa de merge.

A correção deve ocorrer no sistema que é proprietário da condição ausente.

## 12. Auditoria

Cada tentativa deve registrar, no log do workflow, pelo menos:

- PR e repository;
- head SHA avaliado;
- resultado de PR-ready;
- checks/gates observados;
- estado das reviews;
- estado de merge do GitHub;
- grant encontrado e sua expiração, sem expor credenciais;
- decisão operacional;
- resultado final da operação GitHub.

Segredos, tokens e material de autenticação nunca devem ser registrados.

## 13. Relação com as autoridades existentes

```text
ELO / Governança
      ↓ define gates e decisão
elo-authz
      ↓ emite elo-merge-authorized
Supabase
      ↓ persiste evidência
GitHub Actions / Merge Coordinator
      ↓ consome evidência e executa
GitHub
      ↓ aplica branch protection e integra PR
main
```

Nenhuma etapa acima pode criar uma segunda autoridade para substituir a anterior.

## 14. Limites

O coordinator não:

- cria ou altera grants;
- emite `APPROVE_MERGE` como decisão cognitiva independente;
- altera `elo-agent-loop.yml`;
- altera gates existentes;
- fecha Issue como substituto do post-merge loop;
- altera branch protection;
- faz merge de PR sem todas as condições obrigatórias;
- transforma ausência de evidência em PASS.

## 15. Resultado pós-merge

Após um merge efetivo, o coordinator verifica:

1. `merged=true` na PR;
2. existência do merge commit quando aplicável;
3. base `main` correta;
4. head SHA esperado integrado conforme a estratégia de merge;
5. ausência de erro na confirmação.

O pós-merge verification não transforma o merge em conclusão automática da Issue.

## 16. Governança

Este contrato é uma referência operacional subordinada aos contratos canônicos de governança do ELO.

Em caso de conflito, prevalecem a autoridade canônica, a proteção do repositório,
o `elo-authz` e os gates existentes.
