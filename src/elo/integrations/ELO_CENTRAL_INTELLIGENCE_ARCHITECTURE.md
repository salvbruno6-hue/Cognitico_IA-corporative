# ELO — Central de Inteligências e Casa do ELO

## Status

`NORMATIVE / ARCHITECTURAL BASELINE`

## Objetivo

Definir arquiteturalmente a capacidade de o ELO operar como uma plataforma onde usuários autenticados possam utilizar inteligências externas dentro da Casa do ELO, enquanto o próprio ELO também utiliza essas inteligências por trás dos fluxos governados.

Esta capacidade é parte da evolução da plataforma e não altera a identidade do ELO, do Cognitive Core ou da autoridade da Governance/Soul.

## Princípio de Inteligência Simbiótica

> A IA conectada fornece capacidade cognitiva especializada. O ELO fornece direção, contexto, coordenação, governança, rastreabilidade e aprendizagem corporativa.

O ELO deve maximizar o uso governado das capacidades disponíveis no ecossistema, preferindo orquestrar, especializar, combinar e avaliar inteligências existentes a replicá-las internamente.

## Dois modos de utilização

### 1. IA por trás do ELO

O usuário apresenta uma missão ao ELO. O ELO:

1. entende o objetivo;
2. decompõe a missão;
3. identifica especialistas e capacidades necessárias;
4. seleciona provider/modelo/capacidade adequados;
5. compõe contexto corporativo, memória, evidências, premissas e restrições;
6. gera instruções específicas para a missão;
7. executa através de adapters governados;
8. critica e compara os resultados;
9. consolida a resposta;
10. registra resultado e experiência;
11. utiliza a experiência em ciclos futuros quando validada e pertinente.

O usuário não precisa conhecer qual modelo foi utilizado.

### 2. IA aberta dentro da Casa do ELO

A plataforma poderá disponibilizar uma **Central de Inteligências** para usuários autorizados.

O especialista poderá abrir uma inteligência disponível dentro do ambiente ELO e utilizá-la segundo suas permissões.

Essa interface não transforma a IA externa em autoridade do ELO. O acesso permanece submetido a identidade, tenant, permissões, políticas, contratos, rastreabilidade e limites definidos pela plataforma.

## Arquitetura

```text
CASA DO ELO
│
├── Identity / Tenant / Permissions
│
├── ELO Orchestrator
│   ├── Mission Decomposer
│   ├── Specialist Selector
│   ├── Intelligence Router
│   ├── Briefing Generator
│   ├── Context Composer
│   ├── Task Coordinator
│   ├── Critic / Reviewer
│   ├── Result Comparator
│   └── Learning Loop
│
├── Central de Inteligências
│   ├── Available AIs
│   ├── Provider Catalog
│   ├── Authorized Models
│   ├── Specialist Access
│   └── Governed Launch / Invocation
│
├── ELO Interoperability Layer
│   ├── AI Gateway
│   ├── Provider Contracts
│   ├── Adapters
│   ├── Provenance
│   ├── Validation
│   └── Policy Enforcement
│
├── Corporate Context / Memory / Evidence
│
├── Experience / Learning Laboratory
│
└── ELO Core
```

## Separação de autoridade

- **Soul/Governance:** identidade, propósito, invariantes e autoridade final.
- **Cognitive:** compreensão, correlação, análise, crítica e suporte à decisão.
- **Forge:** experimentação, pesquisa, construção e proposição de evolução.
- **Core:** faculdades executáveis provider-neutral e reutilizáveis.
- **Interoperability Layer:** conexão governada com capacidades externas.
- **Central de Inteligências:** superfície de produto para descoberta e uso autorizado de inteligências.
- **IA externa:** capacidade especializada; não é memória canônica nem autoridade normativa do ELO.

## Memória e aprendizagem

Resultados produzidos por uma IA, plugin, especialista, usuário ou cálculo entram inicialmente como **experiência/observação**.

```text
USO DE IA
   ↓
EXPERIENCE
   ↓
EVIDENCE
   ↓
LEARNING CANDIDATE
   ↓
VALIDATION
   ↓
EVOLUTION GATE
   ↓
VALIDATED KNOWLEDGE / PROMOTION
```

Nenhuma resposta de provider externo pode tornar-se automaticamente conhecimento canônico.

## Aprendizagem de desempenho

O ELO deve aprender quais combinações produzem melhores resultados, sem fixar regras simplistas como `orçamento = GPT`.

A memória de desempenho deve poder relacionar:

- missão;
- domínio;
- especialista;
- provider;
- modelo;
- ferramenta/plugin;
- contexto fornecido;
- instruções/briefing;
- método;
- resultado;
- evidência;
- avaliação;
- resultado observado posteriormente.

Isso permite que o Intelligence Router evolua com evidências reais.

## Segurança e governança

- chaves e credenciais ficam somente no ambiente seguro de execução;
- nenhum segredo entra no repositório;
- providers externos não são memória canônica;
- toda chamada deve possuir identidade, tenant, request/correlation id e provenance;
- ações consequenciais permanecem sujeitas à autorização do ELO;
- usuários só acessam inteligências compatíveis com suas permissões;
- dados corporativos enviados a providers devem obedecer às políticas aplicáveis;
- adapters permanecem substituíveis;
- nenhum provider pode criar uma segunda autoridade cognitiva central.

## Evolução em duas etapas

### Etapa A — ELO utiliza IA por trás

Prioridade para integrar o Intelligence Router aos adapters existentes e validar missões reais, começando por orçamento e outros domínios de alto valor.

### Etapa B — Central de Inteligências

Após a fundação operacional, criar a experiência de produto para que especialistas autenticados possam descobrir e abrir inteligências autorizadas dentro da Casa do ELO.

A interface deve reutilizar os mesmos contratos, identidade, permissões, provenance e políticas da Etapa A; não deve criar um segundo caminho de integração.

## Regra arquitetural

A Central de Inteligências é uma **camada de produto e interoperabilidade**, não um novo Core.

O ELO deve permanecer capaz de trocar providers e modelos sem alterar sua identidade ou sua arquitetura cognitiva fundamental.

## Critério de conclusão arquitetural

A capacidade será considerada arquiteturalmente definida quando:

- houver contrato provider-neutral;
- houver adapter governado;
- houver Intelligence Router como autoridade de seleção;
- houver Central de Inteligências como superfície explicitamente prevista;
- houver identidade/permissão/tenant;
- houver provenance;
- houver separação entre experiência e conhecimento canônico;
- houver Evolution Gate para promoção de aprendizado;
- houver testes de isolamento e autorização;
- não houver duplicação de Core, memória ou autoridade.
