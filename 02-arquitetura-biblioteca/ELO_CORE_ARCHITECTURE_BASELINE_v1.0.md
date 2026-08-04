# ELO Core Architecture Baseline v1.0

**Status:** Baseline normativa
**Escopo:** ELO Enterprise Integration Platform (EIP)
**Finalidade:** estabelecer as fronteiras, invariantes e vocabulário arquitetural que devem orientar a evolução documental e técnica do ELO.

## 1. Papel desta baseline

Este documento é a referência normativa para evolução da arquitetura core do ELO. Novos documentos, modelos, agentes, engines, integrações e implementações devem estender esta baseline sem redefinir conceitos já estabelecidos.

A baseline existe para reduzir deriva arquitetural, duplicação documental, incompatibilidade entre componentes e reintrodução de conceitos históricos que já foram substituídos.

## 2. Princípios invariantes

1. O ELO é uma plataforma corporativa orientada a conhecimento, contexto, raciocínio, decisão, integração e governança.
2. IA é uma capacidade substituível. Nenhum provedor ou modelo externo constitui fonte de verdade arquitetural.
3. Conhecimento corporativo é um ativo governado, versionável e rastreável.
4. Toda operação relevante deve preservar isolamento de tenant, domínio, autorização e proveniência.
5. Componentes cognitivos possuem responsabilidades distintas e não devem ser fundidos por conveniência de implementação.
6. Novas capacidades devem ser adicionadas por extensão compatível, não por criação de arquiteturas paralelas.
7. Decisões arquiteturais relevantes devem ser registradas por ADR.
8. Documentação normativa deve possuir finalidade operacional ou arquitetural verificável. Material redundante, promocional ou puramente visionário não integra a baseline.

## 3. Vocabulário canônico

### Tenant
Fronteira primária de isolamento organizacional, segurança e ownership de dados.

### Domain
Contexto de negócio pertencente a um Tenant. Substitui o uso arquitetural de `department` como fronteira central de domínio.

### Principal
Identidade autenticada, humana ou de máquina, sujeita a políticas e autorização.

### Session
Unidade delimitada de interação ou execução que mantém referências ao contexto necessário sem se tornar fonte permanente de conhecimento.

### Context
Informação situacional necessária para interpretar uma interação, tarefa ou decisão em determinado momento.

### Knowledge
Conhecimento corporativo persistente, governado, versionável e recuperável, derivado de fontes identificáveis.

### Memory
Registro cognitivo governado derivado de experiências, interações ou resultados. Memory pode referenciar Context e Knowledge, mas não redefine nenhum dos dois.

### Reasoning
Processo controlado que transforma contexto, conhecimento, memória, evidências e políticas em inferências ou resultados intermediários verificáveis.

### Evidence
Elemento verificável utilizado para sustentar uma inferência, recomendação ou decisão, mantendo referência à sua origem.

### Recommendation
Proposta de ação ou conclusão produzida a partir de raciocínio e evidências. Não equivale automaticamente a autorização ou execução.

### Decision
Registro governado de uma escolha, incluindo contexto, evidências, responsável, política aplicável, resultado e proveniência quando pertinente.

### Agent
Unidade de execução orientada a objetivo, com identidade, capacidades, ferramentas, limites de autonomia e políticas explícitas.

### Provenance
Rastreabilidade da origem, transformação, utilização e encadeamento de dados, conhecimento, evidências, inferências e decisões.

### Policy
Regra governada que condiciona acesso, comportamento, autonomia, decisão ou execução.

### Event
Fato imutável de domínio ou plataforma utilizado para integração, auditoria, observabilidade ou coordenação entre componentes.

## 4. Fronteiras cognitivas obrigatórias

O fluxo conceitual de referência é:

`Source -> Knowledge/Context -> Memory (quando aplicável) -> Reasoning -> Evidence -> Recommendation -> Decision -> Outcome`

Esse fluxo não exige implementação síncrona nem linear. Ele define responsabilidades conceituais.

Regras:

- Context não é banco de conhecimento permanente.
- Knowledge não é memória de sessão.
- Memory não substitui Knowledge.
- Reasoning não é fonte de verdade.
- Recommendation não constitui Decision.
- Decision não implica execução automática.
- Provenance deve atravessar os componentes relevantes e não ser adicionada apenas ao final do fluxo.

## 5. Isolamento e governança

Toda entidade persistente ou operação governada deve considerar, conforme aplicável:

- `tenant_id` como fronteira de isolamento;
- `domain` ou identificador canônico equivalente de domínio;
- identidade do Principal responsável;
- política e autorização aplicáveis;
- classificação e sensibilidade da informação;
- timestamps e versionamento;
- provenance e auditabilidade;
- retenção e lifecycle.

O modelo histórico baseado em `company_id` e `department` não deve ser reintroduzido como arquitetura canônica. Migrações ou adapters podem preservar compatibilidade quando necessário, sem contaminar o domínio atual.

## 6. Regras para engines e agentes

Engines e agentes devem possuir contratos explícitos de entrada, saída, erro, autorização e observabilidade.

Nenhum agente recebe autonomia implícita. Ferramentas e ações externas devem estar associadas a capacidades e políticas verificáveis.

Resultados produzidos por modelos de IA devem ser tratados como artefatos derivados sujeitos a validação, confiança calibrada e proveniência, conforme criticidade.

## 7. Compatibilidade e evolução

Uma proposta arquitetural é compatível com esta baseline quando:

1. reutiliza o vocabulário canônico existente;
2. não cria entidade equivalente com outro nome sem justificativa arquitetural;
3. preserva isolamento de Tenant e Domain;
4. mantém separação entre Context, Knowledge, Memory, Reasoning, Recommendation e Decision;
5. define provenance quando houver transformação ou decisão relevante;
6. explicita dependências e contratos;
7. registra em ADR qualquer alteração de princípio, fronteira ou responsabilidade canônica.

Alterações incompatíveis exigem ADR aprovado e nova versão da baseline.

## 8. Política documental

Antes de adicionar um documento ao repositório, aplicar os seguintes gates:

1. **Uniqueness Gate:** existe documento ou conceito equivalente?
2. **Architecture Gate:** está alinhado à baseline e ao vocabulário canônico?
3. **Maturity Gate:** aumenta implementação, governança, segurança, testabilidade, interoperabilidade ou rastreabilidade?
4. **Dependency Gate:** dependências e ownership estão explícitos?
5. **Repository Gate:** o conteúdo possui destino e função normativa claramente definidos?

Conteúdo que falhar no Uniqueness Gate deve ser fundido. Conteúdo incompatível deve ser corrigido ou descartado. Conteúdo sem ganho de maturidade não deve ser promovido a documentação normativa.

## 9. Documentos subordinados esperados

Esta baseline será detalhada, sem redefinição, por documentos específicos de:

- Tenant, Domain, IAM e Policy Enforcement;
- modelo canônico de entidades e contratos de dados;
- Context, Knowledge e Memory;
- Reasoning e Verification;
- Decision Intelligence;
- Agent Lifecycle e autonomia;
- Analytical Intelligence;
- Provenance, Evidence e Audit;
- Integration Contracts e Events;
- Evaluation, Testing e Observability;
- Production Readiness e operações.

## 10. Regra de precedência

Em caso de conflito entre documentação histórica, handbook, blueprint, roadmap, prompt, referência externa ou implementação experimental e esta baseline, a baseline prevalece até que um ADR aprove explicitamente sua alteração.

---

**Baseline:** v1.0
**Classificação:** normativa
**Evolução:** somente por mudança arquitetural deliberada e registrada.