# ELO Cognitive Layer

## Objetivo

Definir a camada cognitiva da EIP, responsável por contexto, conhecimento, raciocínio, decisão, aprendizagem e orquestração de agentes.

## Escopo

- context engine
- knowledge engine
- reasoning engine
- decision engine
- learning engine
- agent orchestration
- retrieval and grounding
- governed execution routing
- **Simbionte**, como natureza cognitiva de absorção, aprendizagem, experimentação, generalização e adaptação

## Ownership canônico

Cada conceito possui um único owner semântico. O nome do arquivo não cria uma autoridade nova.

| Responsabilidade | Owner canônico |
|---|---|
| ciclo de execução cognitiva | `execution_loop.py` |
| decomposição e planejamento de tarefa | `reasoning/task_planning.py` |
| seleção de capacidade/modelo/ferramenta | `routing/` |
| avaliação de experiência | `learning/experience_evaluation.py` |
| evidência de desempenho histórico | `learning/performance_evidence.py` |
| descoberta da metodologia empresarial | `learning/methodology.py` |
| memória e avaliação da memória | `memory/` |
| contexto | `context/` |
| conhecimento | `knowledge/` |
| decisão | `decision/` |
| natureza Simbionte | conjunto cognitivo existente de `learning/`, `memory/`, `reasoning/`, `knowledge/` e evolução governada; não cria um novo owner estrutural |

### Regra de nomenclatura

Não criar arquivos ou pastas novos apenas para substituir um nome existente, nem usar nomes semelhantes para a mesma responsabilidade. Antes de criar um artefato, localizar o owner semântico e aplicar, nesta ordem: `REUSE → EXTEND → CONSOLIDATE → RELOCATE → CREATE`.

Nomes semelhantes são permitidos somente quando representam responsabilidades comprovadamente diferentes. Por exemplo, `execution_loop.py` coordena o ciclo completo; `routing/execution_routing.py` decide a rota de execução. Eles não são autoridades concorrentes.

Tecnologias, frameworks e padrões externos devem ser tratados como referências/adaptações dentro do owner ELO correspondente, nunca como novas autoridades arquiteturais.

## Princípio Simbionte

**Simbionte é uma natureza do ELO Cognitivo. Não é pilar, camada, núcleo, autoridade ou componente arquitetural independente.**

O Cognitive recebe do Forge conhecimento, experiência, mecanismos recuperados e evidências; a natureza Simbionte permite absorver, relacionar, experimentar, aprender, testar e generalizar esse material. A eventual necessidade de evolução é avaliada pelo Cognitive e qualquer alteração estrutural permanece subordinada à governança do Core.

```text
FORGE
  ↓ conhecimento / experiência / mecanismos
COGNITIVE
  ↓
SIMBIONTE (natureza)
  ├── absorver
  ├── relacionar
  ├── aprender
  ├── experimentar
  ├── testar
  └── generalizar
          ↓
      avaliação cognitiva
          ↓
         CORE
      governança estrutural
```

## Princípios

- conhecimento governado antes de geração
- contexto antes de inferência
- decisão antes de ação
- rastreabilidade antes de autonomia
- adaptação antes de automação total
- IA como componente integrado, nunca como fonte de verdade isolada
- experiência verificada pode gerar evidência de aprendizagem, mas não altera o Canon automaticamente
- evidência específica de tenant permanece isolada do conhecimento canônico
- aprendizagem não redefine a tricotomia nem suas invariantes estruturais

## Relação com a EIP

A camada cognitiva não substitui os domínios de negócio. Ela os amplia com interpretação, síntese, recomendação e automação governada.

## Fluxo básico

```text
Input / Request
  ↓
Context Engine
  ↓
Knowledge / Retrieval
  ↓
Reasoning / Method
  ↓
Capability
  ↓
Execution Routing
  ↓
Decision / Verification
  ↓
Experience
  ↓
Learning Candidate
  ↓
Simbionte / assimilação cognitiva
  ↓
Governed Evolution
```

## Regras

- a camada cognitiva deve consumir configuração validada e políticas de segurança
- qualquer uso de IA externa deve passar por governança e observabilidade
- resultados cognitivos devem ser rastreáveis a contexto, evidências e origem
- nenhuma nova estrutura cognitiva deve ser criada sem auditoria de duplicidade e definição explícita de owner
- o conhecimento recuperado do Forge é alimento para a natureza Simbionte, não autorização estrutural
- a natureza Simbionte não pode alterar Soul, criar autoridade paralela ou promover mudança estrutural fora do Core
