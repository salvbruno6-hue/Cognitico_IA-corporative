# ELO Security, Tenant and Policy Enforcement

**Status:** Documento normativo
**Dependência:** ELO Core Architecture Baseline v1.0
**Escopo:** isolamento organizacional, autenticação, autorização, políticas e controle de execução para o ELO Enterprise Integration Platform (EIP).

## 1. Objetivo

Este documento define a camada normativa de segurança e enforcement do ELO para garantir que usuários, agentes, sessões, conhecimento e execuções respeitem fronteiras organizacionais, políticas e níveis de autonomia.

## 2. Princípios

1. Nenhum acesso é implícito.
2. Nenhuma execução crítica é autônoma sem política explícita.
3. Tenant é a fronteira primária de isolamento.
4. Domain é a fronteira de contexto de negócio dentro do Tenant.
5. Principal é a identidade sujeita a autenticação e autorização.
6. Agentes são sujeitos a identidade, escopo, política e auditoria.
7. Acesso, leitura, escrita, execução e automação seguem menor privilégio.
8. Provenance e auditoria devem acompanhar ações relevantes.

## 3. Conceitos canônicos

### Tenant
Fronteira organizacional superior. Tudo o que é persistido, recuperado ou executado no ELO deve poder ser atribuído a um Tenant quando aplicável.

### Domain
Subfronteira de negócio do Tenant. `domain` é o identificador canônico para contexto de negócio. O uso arquitetural de `department` não deve ser reintroduzido como fronteira central.

### Principal
Identidade autenticada, humana ou de máquina, que solicita acesso, consulta, transformação ou execução.

### Policy
Regra governada que condiciona acesso, escopo, autorização, autonomia e execução.

### Authorization
Decisão de permitir ou negar uma ação a um Principal, agente ou serviço, com base em Policy, escopo e contexto.

### Role
Agrupamento de permissões.

### Permission
Capacidade específica de realizar uma ação sobre um recurso, conjunto de recursos ou classe de operações.

### Classification
Nível de sensibilidade ou restrição da informação. Ao menos os níveis público, interno, confidencial e restrito devem ser considerados na modelagem do ELO.

## 4. Modelo de enforcement

A cadeia normativa de referência é:

`Principal -> Authentication -> Tenant Resolution -> Domain Resolution -> Policy Evaluation -> Authorization -> Execution`

Regras:

- Tenant deve ser resolvido antes da liberação de qualquer dado ou contexto sensível.
- Domain deve restringir o contexto de operação quando o recurso estiver associado a um domínio específico.
- Policy deve ser aplicada antes de leitura, escrita, execução e integração externa.
- Resultados produzidos por agente ou modelo de IA não podem ultrapassar a política que os originou.

## 5. Isolamento de dados e contexto

O ELO deve impedir, por padrão, que um Tenant acesse dados, sessão, memória privada, conhecimento reservado ou contexto operacional de outro Tenant.

Quando houver compartilhamento explícito, ele deve ocorrer por política, contrato e escopo definidos, com auditoria suficiente para reconstrução posterior.

A solução histórica baseada em `company_id` e `department` pode existir apenas como compatibilidade transitória, nunca como modelo canônico principal.

## 6. Sessão, memória e autorização

- Session herda o Tenant do Principal ou do sistema que a criou.
- Memory não pode ser compartilhada entre Tenants sem política explícita.
- Context recuperado para uma resposta deve respeitar Tenant, Domain, classificação e finalidade.
- Knowledge consultado por um agente deve obedecer às permissões desse agente e do Principal que o acionou, quando aplicável.

## 7. Controle de agentes

Todo agente deve possuir:

- identidade;
- versão;
- responsável;
- capabilities;
- ferramentas autorizadas;
- políticas aplicáveis;
- limites de autonomia;
- trilha de auditoria.

Nenhum agente pode alterar seus próprios limites, permissões ou política sem fluxo governado.

## 8. Níveis de autonomia

O ELO adota os seguintes níveis de autonomia como referência de governança:

1. Informar.
2. Sugerir.
3. Recomendar.
4. Executar com aprovação.
5. Automação controlada.

A autonomia só aumenta quando a política, o contexto e a criticidade permitirem.

## 9. Criticidade e aprovação humana

Ações que afetem segurança, finanças, contratos, compliance, exclusões, integrações externas ou dados sensíveis exigem aprovação humana ou mecanismo equivalente definido em policy.

A ausência de aprovação explícita deve ser interpretada como negação em ações críticas.

## 10. Auditoria mínima

Toda operação governada deve registrar, quando aplicável:

- Principal;
- Tenant;
- Domain;
- recurso acessado;
- action;
- policy aplicada;
- decisão de autorização;
- timestamp;
- provenance;
- resultado;
- erro ou recusa, se houver.

## 11. Contratos esperados

Este documento deve ser detalhado, sem mudança de princípio, por contratos específicos de:

- autenticação;
- autorização;
- RBAC e, quando necessário, ABAC;
- classificação da informação;
- políticas de agentes;
- isolamento de sessão e memória;
- auditoria e rastreabilidade;
- execução aprovada;
- integração segura.

## 12. Critério de compatibilidade

Uma implementação é compatível com este documento quando:

- resolve Tenant antes de expor contexto ou dados;
- aplica Domain como restrição de negócio;
- valida policy antes de executar;
- mantém trilha de auditoria;
- preserva isolamento entre Tenants;
- evita dependência de `department` como fronteira principal;
- não permite autonomia implícita.

## 13. Regra de precedência

Em caso de conflito entre protótipo, documentação histórica, blueprint, prompt ou implementação experimental e este documento, prevalece este documento até que um ADR aprove alteração explícita.

---

**Baseline associada:** ELO Core Architecture Baseline v1.0
**Classificação:** normativa
**Evolução:** por ADR e revisão arquitetural controlada.