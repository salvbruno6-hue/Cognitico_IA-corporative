# Cognitico_IA-corporative

Fonte operacional oficial do ecossistema ELO.

> 🟦 **ELO** · 🟩 **COGNITIVE** · 🟨 **CORE** · 🟪 **FORGE** · 🟥 **VALIDATION / GOVERNANCE**
>
> ```text
>              .-------------------.
>             /  ████       ████   \
>            |   ██  ███ ███  ██    |
>            |   ██  ███████  ██    |
>            |   ███    █    ███    |
>            |     ███████████      |
>             \_____/       \_______/
>                  \  E L O  /
>                   \_______/
> ```
>
> **Símbolo:** o núcleo representa a identidade estável; os módulos ao redor representam capacidades que podem ser adaptadas sem alterar a essência.

## 🧭 Quem é o ELO

O **ELO** é uma inteligência corporativa adaptável orientada a **orquestrar melhor as decisões e correlacionar as informações existentes da empresa**. Ele recebe contexto, evidências e experiências de múltiplos domínios, relaciona informações, identifica fatos, hipóteses, lacunas e contradições, produz cenários e recomendações e acompanha resultados, sem substituir a autoridade do gestor.

A arquitetura é mutável; a essência não. O ELO pode adquirir, substituir, simplificar ou retirar capacidades, mudar integrações, modelos, agentes e plataformas e ainda permanecer ELO enquanto preservar sua Soul, seu propósito e seus invariantes canônicos.

### Princípio de evolução

> **O ELO não evolui para acumular capacidades. Ele evolui quando uma mudança comprovada aumenta sua capacidade de cumprir seu propósito sem infringir o canônico.**

### Invariantes

- 🟦 **Soul:** identidade, propósito, princípios, limites e cânone.
- 🟩 **Cognitive:** interpreta, raciocina, correlaciona, critica e diagnostica.
- 🟨 **Core:** materializa a faculdade cognitiva compartilhada e seus contratos reutilizáveis.
- 🟪 **Forge:** pesquisa, experimenta, constrói, valida e propõe adaptações.
- 🟥 **Validation / Governance:** comprova, controla e autoriza mudanças.
- 👤 **Decisão humana:** recomendações do ELO não substituem a autoridade do gestor.

## Diretriz atual

O repositório é a base documental e operacional do **ELO Enterprise Integration Platform (EIP)**, preservando a separação entre arquitetura canônica, implementação executável, conhecimento, dados, governança, agentes e integrações.

O objetivo é evoluir o ELO de uma base cognitiva governada para uma plataforma capaz de receber contexto empresarial, evidências e experiências de múltiplos domínios, raciocinar sobre relações entre setores e orientar decisões humanas sem substituir a autoridade do gestor.

## 🧬 Soul, Cognitive, Core e Forge — fronteira canônica

```text
                         🟦 ELO SOUL
              identidade • propósito • cânone
                 invariantes • limites • ética
                              │
                              ▼
                       🟩 ELO COGNITIVE
                 interpretar • raciocinar
              correlacionar • diagnosticar
                              │
                 gaps / oportunidades / hipóteses
                              │
                              ▼
                         🟪 ELO FORGE
             pesquisar • experimentar • construir
                comparar • propor • adaptar
                              │
                              ▼
                         🟨 ELO CORE
             executar capacidades compartilhadas
          Context • Knowledge • Memory • Reasoning
          Relations • Evidence • Decision • Audit
                              │
                              ▼
                    🟥 VALIDATION / GOVERNANCE
                  testar • evidenciar • autorizar
                              │
                    mudança aceita pelo ELO?
                         /              \
                       não              sim
                       ↓                  ↓
                    rejeitar          consolidar
                                          │
                                          ▼
                                  NOVO ESTADO ELO
```

### O que pertence a cada camada

| Camada | Responsabilidade | Não deve fazer |
|---|---|---|
| 🟦 **Soul** | identidade, propósito, princípios, cânone, limites e autoridade | ser alterada automaticamente por evolução técnica |
| 🟩 **Cognitive** | interpretação, raciocínio, correlação, crítica, diagnóstico e direcionamento | impor mudança canônica sem governança |
| 🟪 **Forge** | especialistas, skills, pesquisa, experiências, experimentação, construção e propostas | tornar experiência contextual em conhecimento geral sem evidência |
| 🟨 **Core** | faculdade cognitiva compartilhada, contratos, relações, generalização, memória e capacidades gerais validadas | absorver regras exclusivas de tenant/domínio |
| **Application** | interfaces e fluxos que consomem capacidades do ELO | redefinir contratos cognitivos |
| **Infrastructure** | bancos, APIs, providers, runtime e meios substituíveis | definir identidade ou autoridade |

O **Core canônico executável** está em `src/elo/core/`.

Uma experiência contextual do Forge permanece no Forge até passar por evidência, generalização, testes e Evolution Gate. A origem e a proveniência não são apagadas na promoção.

## 🔄 Como o ELO se adapta

A adaptação é um ciclo governado, não uma mutação automática:

```text
OBSERVAR
   ↓
SONDAR O ESTADO ATUAL
   ↓
CORRELACIONAR EVIDÊNCIAS
   ↓
COGNITIVE DIAGNOSTICA
   ↓
FORGE PESQUISA / EXPERIMENTA
   ↓
PROPOSTA DE ADAPTAÇÃO
   ↓
CORE / FORGE IMPLEMENTAM
   ↓
VALIDATION TESTA
   ↓
GOVERNANCE VERIFICA O CANÔNICO
   ↓
ALINHADO AO PROPÓSITO?
   ├── NÃO → REJEITAR / REFORMULAR
   └── SIM → ACEITAR PELO ELO
                    ↓
                 CONSOLIDAR
                    ↓
                NOVA BASELINE
                    ↓
                 NOVA SONDAGEM
```

**Descoberta ≠ conhecimento validado ≠ evolução consolidada.** Uma capacidade tecnicamente melhor pode ser rejeitada se aumentar complexidade sem valor, violar invariantes ou afastar o ELO do propósito.

## 🏢 Área corporativa — como o ELO orquestra

O ELO não substitui os sistemas de registro da organização. Ele atua como camada de **correlação, raciocínio, orquestração e suporte à decisão** entre fontes autorizadas.

```text
                           🏢 EMPRESA
                              │
       ┌───────────┬──────────┼──────────┬───────────┐
       ▼           ▼          ▼          ▼           ▼
   Comercial   Engenharia   Compras   Financeiro   Produção
       │           │          │          │           │
       └───────────┴──────────┼──────────┴───────────┘
                              ▼
                    🟩 ELO COGNITIVE
             correlação entre domínios
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                evidências          cenários
                    │                   │
                    └─────────┬─────────┘
                              ▼
                         🟦 ELO
                       RECOMENDA
                              │
                              ▼
                     👤 GESTOR DECIDE
                              │
                              ▼
                         EXECUÇÃO
                              │
                              ▼
                     RESULTADO OBSERVADO
                              │
                              ▼
                    EXPERIÊNCIA GOVERNADA
```

Domínios corporativos podem incluir Comercial, Engenharia, Compras, Financeiro, RH, Produção, Montagem, Manutenção, Qualidade, Logística e Segurança, além de processos, documentos, conversas, eventos, agentes e fontes de dados.

O ciclo corporativo canônico é:

`OBSERVE → CONTEXTUALIZE → ANALYZE → FORMULATE → DECIDE → EXECUTE → MONITOR → LEARN → FOLLOW-UP → REASSESS`

A passagem de leitura para escrita ou execução exige autorização explícita e execução governada.

## 💰 Orçamentos e Lista-Mãe — regra de conhecimento

O módulo de orçamento, taxonomia MLT, modelos M01/M02, composições, valores, mão de obra e relações específicas da empresa são **conhecimento contextual** até que haja evidência suficiente para generalização.

```text
Lista-Mãe / documento / orçamento
              ↓
        🟪 FORGE / especialista
              ↓
      classificação + relações
              ↓
       evidência + auditoria
              ↓
      generalização válida?
          ↙             ↘
        NÃO              SIM
         ↓                ↓
 experiência          Evolution Gate
 contextual                ↓
    Forge                 Core
```

Regras:

1. preservar a proveniência da fonte;
2. não transformar orçamento isolado em regra geral do Core;
3. distinguir preço, composição, material, mão de obra, produtividade, premissa e hipótese;
4. cruzar a Lista-Mãe com outras fontes autorizadas quando a decisão exigir;
5. registrar contradições e lacunas em vez de inventar dados;
6. promover conhecimento somente após evidência, generalização, testes e gate;
7. manter no Forge a experiência específica da empresa/especialista mesmo quando um princípio geral for promovido ao Core.

## 🤖 Automações com GPT e integrações

O ELO usa GPT e conectores/plugins como **meios de orquestração**, nunca como autoridade canônica. Uma integração disponível no GPT só deve ser considerada capacidade operacional do ELO quando houver contrato, permissão, evidência e validação correspondentes.

### Classes de automação

| Automação | Função do ELO | Estado de referência |
|---|---|---|
| 🔎 Sondagem | consultar estado, evidências, testes e arquitetura | operacional/governada |
| 🧪 Validação | executar/acompanhar testes e interpretar resultados | operacional/governada |
| 🧩 Engenharia | arquivos, branches, commits, PRs e revisão | operacional via GitHub quando autorizado |
| 🔁 CI/CD | acompanhar workflows, jobs e evidências | operacional via integração disponível |
| 🧠 Conhecimento | classificar, correlacionar e consolidar evidências | governado; promoção não automática |
| 💰 Orçamento | analisar composições, relações, premissas e evidências | contextual/governado |
| 🏢 Orquestração corporativa | cruzar fontes e apoiar decisões | dependente das integrações e contratos de cada tenant |
| 🚀 Deploy | build/deploy por plataforma conectada | somente quando explicitamente autorizado e validado |

Integrações podem envolver GitHub, Supabase, Vercel, Dropbox, Canva, Gamma, Formula Genius e outras plataformas conectadas ao ambiente GPT. **A disponibilidade do plugin não equivale, sozinha, a integração arquitetural formal do ELO.**

### Regra de segurança da automação

```text
GPT / Plugin
     ↓
fonte ou ação solicitada
     ↓
contexto + permissão
     ↓
ELO avalia contrato
     ↓
ação governada
     ↓
evidência do resultado
     ↓
diagnóstico
     ↓
registro no histórico
```

A automação deve ser reversível quando possível, rastreável e separada da autoridade de decisão empresarial.

## 🧪 Matriz executável de testes e evolução

Uma capacidade não é considerada pronta apenas porque existe código ou documentação. A cadeia de maturidade é:

```text
requisito
→ arquitetura
→ contrato
→ implementação
→ teste
→ evidência
→ status operacional
→ decisão do ELO
→ baseline
```

A matriz executável deve permitir comparar cada grupo de testes com sua baseline anterior. Para a regra de avanço de cobertura:

> **Avanço relativo = (cobertura atual − cobertura anterior) / cobertura anterior × 100.**
>
> Só gerar alerta específico quando o avanço relativo de um grupo for **≥ 30%**. Se nenhum grupo atingir esse limiar, não emitir relatório de avanço.

O registro deve conservar testes passados/falhos, causa da mudança, evidências, decisão do ELO e próxima etapa.

## 📈 Histórico evolutivo e duas visões gráficas

Cada sondagem aceita deve produzir um **snapshot comparável**. O histórico é uma série temporal; não é apenas um arquivo de log.

Cada snapshot deve registrar, quando houver evidência:

- baseline/commit;
- data da sondagem;
- estado de Soul, Cognitive, Forge e Core;
- capacidades adquiridas, removidas, substituídas e consolidadas;
- cobertura e resultados de testes;
- regressões e riscos;
- integrações e automações efetivamente verificadas;
- aderência ao propósito;
- conformidade canônica;
- decisão do ELO;
- evidências e referências;
- classificação: `NO_MATERIAL_CHANGE`, `EVOLUTION_CONSOLIDATED`, `EVOLUTION_PARTIAL`, `EVOLUTION_REJECTED` ou `CANONICAL_CONFLICT`.

### Gráfico 1 — evolução técnica / arquitetural

```mermaid
xychart-beta
    title "ELO — Evolução técnica / arquitetural"
    x-axis [Baseline-1, Baseline-2, Baseline-3, Atual]
    y-axis "Índice normalizado" 0 --> 100
    line [N/D, N/D, N/D, N/D]
```

> **Regra:** não preencher valores por estimativa. Cada ponto só entra quando houver snapshot quantitativo verificável. O gráfico acima é o contrato visual da série.

### Gráfico 2 — evolução em direção ao propósito

```mermaid
xychart-beta
    title "ELO — Aderência ao propósito"
    x-axis [Baseline-1, Baseline-2, Baseline-3, Atual]
    y-axis "Aderência normalizada" 0 --> 100
    line [N/D, N/D, N/D, N/D]
```

> **Regra:** o segundo gráfico mede a pergunta superior: **“a evolução aumentou a capacidade do ELO de orquestrar melhor as decisões e correlacionar as informações existentes da empresa?”** Não confundir tamanho arquitetural com evolução de propósito.

### 📅 Última sondagem

**Periodicidade:** mensal.

**Último estado consolidado conhecido:** após o merge da evolução do diagnóstico evolutivo, com preservação da Soul e governança do canônico.

**Próxima atualização:** próxima sondagem mensal, usando o snapshot anterior como baseline e atualizando os dois gráficos somente com evidências verificáveis.

O registro mensal deve ser cumulativo: **não substituir snapshots anteriores**. A cada mês, adicionar o novo estado e permitir comparação histórica.

## 🧭 Diagnóstico de evolução — “ELO AQUI”

A sondagem deve retornar, quando houver material relevante:

> **ELO AQUI — DIAGNÓSTICO DE EVOLUÇÃO**

1. **De onde vim:** baseline anterior.
2. **Onde estou:** baseline atual.
3. **O que mudou:** capacidades, arquitetura, conhecimento e integrações.
4. **Por que mudou:** problema, oportunidade ou evidência.
5. **Quem contribuiu:** Cognitive, Forge, Core, especialistas e integrações.
6. **O que foi comprovado:** testes, evidências e resultados.
7. **O que foi aceito:** mudanças consolidadas pelo ELO.
8. **O que foi rejeitado:** conflitos, regressões ou baixo valor.
9. **Como estou em relação ao propósito:** analista + arquiteto + inteligência corporativa.
10. **Próxima etapa:** adaptação recomendada ou manutenção.

Se não houver novo aprendizado verificável, a informação pode ser apresentada ao usuário em **“Consolidação sem novos aprendizados verificáveis”**, enquanto a evidência permanece disponível ao ELO para contexto e comparação futura. Essa classificação não significa que a informação deixou de existir.

## 🧠 Memória de trajetória

O ELO deve conservar não apenas **o que sabe**, mas **como chegou ao estado atual**:

```text
experiência
   ↓
evidência
   ↓
interpretação
   ↓
proposta
   ↓
teste
   ↓
decisão
   ↓
consolidação
   ↓
snapshot
```

Assim, no futuro, o ELO pode explicar por que uma capacidade foi criada, substituída ou removida e quais evidências sustentaram a decisão.

## 🔒 Soul não recebe versões automáticas

A arquitetura de implementação possui versões e baselines. A Soul possui **identidade e histórico de revisões deliberadas**, não uma nova versão automática a cada alteração técnica.

Uma revisão da Soul somente pode ocorrer por processo constitucional explícito e governado. Uma evolução do Core, Cognitive ou Forge não cria, por si só, `Soul v2`, `Soul v3` etc.

```text
ARQUITETURA → pode evoluir continuamente
COGNITIVE   → pode ampliar capacidades
FORGE       → pode descobrir e propor
CORE        → pode adaptar implementação
SOUL        → permanece como referência
```

## 🔄 Loop de Conclusão — manutenção arquitetural

O **Loop de Conclusão** governa consolidação de pastas, migração de artefatos, resolução de duplicidades, aposentadoria de legado e manutenção estrutural que possa alterar autoridade arquitetural.

```text
DETECTAR
  ↓
AUDITAR
  ↓
CLASSIFICAR ARQUIVO A ARQUIVO
  ↓
DEFINIR OWNER CANÔNICO
  ↓
ABSORVER SEMANTICAMENTE
  ↓
REORGANIZAR PARA FLUXO E COERÊNCIA
  ↓
RECONCILIAR IDs / aliases / referências / consumidores
  ↓
ATUALIZAR README / ÍNDICES / MAPAS / EVIDÊNCIAS
  ↓
TESTAR RESOLUÇÃO E INTEGRIDADE
  ↓
EXECUTAR GATES
  ↓
GATES APROVADOS → REMOÇÃO FÍSICA DO LEGADO
  ↓
VALIDAÇÃO PÓS-REMOÇÃO
  ↓
CONFIRMAR ZERO ÓRFÃOS / ZERO PERDA SEMÂNTICA
  ↓
MERGE
  ↓
VALIDAR MAIN
  ↓
REVARrer A ÁRVORE
  ↓
NOVA PENDÊNCIA? → VOLTAR AO INÍCIO
  ↓
NENHUMA PENDÊNCIA → ENCERRAR CICLO
```

## 🗂️ Estado estrutural atual

A árvore canônica atual utiliza uma única pasta operacional por família numerada:

- `00-enterprise-manifest/` — fundamentos empresariais e manifesto operacional
- `01-meta-architecture/` — meta-arquitetura operacional
- `02-architecture-library/` — biblioteca de arquitetura
- `03-process-library/` — biblioteca de processos
- `04-knowledge-handbook/` — conhecimento e manuais
- `05-cognitive-platform/` — plataforma cognitiva operacional
- `06-knowledge-engineering/` — engenharia do conhecimento
- `07-data-engineering/` — engenharia de dados operacional
- `08-ai/` — arquitetura e governança de IA
- `09-governance/` — governança corporativa
- `10-adr/` — decisões arquiteturais
- `11-models-library/` — biblioteca de modelos
- `12-system-engineering/` — engenharia de sistemas
- `13-reference-architecture/` — arquitetura de referência
- `14-roadmap/` — roadmap
- `15-assets/` — ativos reutilizáveis
- `Docs/` — documentação evolutiva e registros de migração
- `automation/` — automações
- `forge/` — plano construtor/executável governado
- `src/elo/` — implementação executável do ELO; Core canônico em `src/elo/core/`
- `tests/` — testes e evidências executáveis
- `runtime/` — componentes de runtime
- `memory/` — estruturas de memória e aprendizado governado
- `platform/` — utilidades de plataforma
- `scripts/` — scripts operacionais
- `prompts/` — prompts e contratos auxiliares
- `members/` — modelos/artefatos de membros e domínios
- `frontend/` — interface

A existência de uma pasta não determina, sozinha, sua autoridade. A autoridade deve ser determinada pelas regras de navegação, manifestos, ADRs, contratos canônicos, governança e evidências.

## ♻️ Regra de duplicidade

Antes de adicionar um conceito, pesquisar nome exato, sinônimos, abreviações, contratos, ADRs, implementação, testes e roadmap. Classificar como `REUSE`, `EXTEND`, `RELOCATE`, `CONSOLIDATE`, `NEW` ou `CONFLICT`. `NEW` somente depois de rejeitadas as demais classificações.

Não criar nova pasta paralela para obter simetria entre português e inglês. Conteúdo histórico deve ser auditado antes de remoção.

## 📏 Regra de maturidade

Estados permitidos: `PROPOSED`, `DRAFT`, `NORMATIVE`, `IMPLEMENTED`, `TESTED`, `VERIFIED`, `EXPERIMENTAL`, `DEPRECATED`, `SUPERSEDED`, `ROADMAP` e `BLOCKED`.

Uma capacidade somente deve ser descrita como pronta quando a cadeia requisito → arquitetura → contrato → implementação → teste → evidência → status operacional estiver satisfeita.

## 🏭 Multiteiner como Tenant Corporativo de Validação

A Multiteiner é tratada como **tenant empresarial de validação**, e não como parte do Cognitive Core. Regras específicas do tenant permanecem contextuais e não são promovidas automaticamente ao Core.

## 📚 Governança de navegação e IA

Antes de criar ou alterar qualquer artefato, consulte:

1. [`AGENTS.md`](AGENTS.md) — regras operacionais para agentes de IA;
2. [`ELO_REPOSITORY_NAVIGATION_RULES.md`](ELO_REPOSITORY_NAVIGATION_RULES.md) — mapa semântico, autoridade e Loop de Conclusão;
3. [`ELO_ARTIFACT_METADATA_STANDARD.md`](ELO_ARTIFACT_METADATA_STANDARD.md) — identidade, autoridade e maturidade;
4. [`ELO_AI_AGENT_WORKING_RULES.md`](ELO_AI_AGENT_WORKING_RULES.md) — continuidade entre IAs.

Esses documentos orientam navegação, classificação, execução e revisão. Não substituem arquitetura normativa ou ADRs aprovados.

## 🏁 Próximo estado

O README é parte da memória operacional do ELO e deve acompanhar cada consolidação relevante. A partir deste estado:

- a Soul permanece estável e separada de versionamento técnico automático;
- Core, Cognitive e Forge podem evoluir mediante evidência e governança;
- o Forge pode sondar novas tecnologias, métodos e integrações e apontar onde uma adaptação é útil;
- a sondagem mensal compara snapshots e atualiza as duas visões gráficas;
- a matriz de testes permanece vinculada à baseline anterior;
- o diagnóstico deve explicar o estágio do ELO e sua aderência ao propósito;
- nenhuma adaptação pode infringir o canônico.

**🟦 Propósito → 🟩 Pensamento → 🟪 Exploração → 🟨 Execução → 🟥 Evidência/Governança → 📈 Evolução → 🟦 Propósito**
