# ELO Core — Diretrizes e Skill Boundary

**Status:** CANONICAL REFERENCE  
**Natureza:** contrato de fronteira e operação  
**Owner:** ELO Cognitivo  
**Version:** 1.0

## 1. Finalidade

O Core é a faculdade cognitiva compartilhada e executável do ELO. Ele materializa mecanismos cognitivos canônicos, conhecimento generalizado validado, parâmetros gerais, padrões, relações, heurísticas e capacidades reutilizáveis.

Este documento não cria uma nova definição de Core. Ele consolida, em formato de referência operacional, as fronteiras já estabelecidas em `src/elo/core/README.md`, evitando duplicação semântica.

## 2. Diretrizes

1. O Core permanece provider-neutral e reutilizável.
2. O Core não contém regra de negócio específica de empresa, especialista ou domínio.
3. O Core não substitui a identidade/cânone do ELO Cognitivo.
4. O Core não recebe diretamente experiência contextual do Forge.
5. Conhecimento generalizado só entra após validação, generalização e governança.
6. Contratos cognitivos permanecem estáveis diante da substituição de aplicações, infraestrutura ou provedores.
7. Integrações externas usam contratos/adapters apropriados, nunca acoplamento que transforme o provedor em autoridade.
8. O Core não cria uma segunda autoridade de Memory, Router, Reasoning ou Evolution Gate.

## 3. Skill Boundary do Core

O Core **não possui uma skill de especialista paralela ao Forge**. Skills são representadas pelo mecanismo canônico de `forge/SPECIALIST_SKILL_REGISTRY.md`.

A função do Core em relação às skills é:

`CONSUME VALIDATED MECHANISM → EXPOSE SHARED CAPABILITY → ENFORCE CONTRACT → ACCEPT GOVERNED PROMOTION`

O Core pode fornecer mecanismos compartilhados para skills e receber uma capacidade somente pelo caminho de promoção governado. Ele não deve criar uma segunda Skill Registry.

## 4. Relação com Forge e Simbionte

`Forge/Skill → Evidence → Test → Generalization → Evolution Gate → Core`

A Simbionte pode propor refinamentos e associar experiência a capacidades existentes, mas não escreve diretamente no Core nem transforma uma experiência externa em mecanismo canônico.

## 5. Regra de não duplicidade

Antes de qualquer nova capability ou skill, verificar:

- capability existente no Core;
- contrato cognitivo existente;
- skill existente no Forge;
- mecanismo equivalente já validado;
- experiência/candidato existente na Simbionte;
- autoridade já responsável pelo objetivo.

Se o objetivo já possui owner, preferir `REUSE`, `STRENGTHEN` ou `REFACTOR`. Não criar artefato equivalente apenas para acomodar uma nova fonte externa.

## 6. Fontes canônicas relacionadas

- `src/elo/core/README.md` — definição e fronteiras do Core.
- `forge/SPECIALIST_SKILL_REGISTRY.md` — registro canônico de skills.
- `ELO_BOOTSTRAP.md` — identidade e separação Cognitivo/Core/Forge.
- `docs/architecture/ELO_HERMES_SYMBIONT_CONTRACT.md` — fronteira ELO–Simbionte–Hermes.

Este arquivo é uma referência de fronteira; não substitui esses documentos nem cria nova autoridade.
