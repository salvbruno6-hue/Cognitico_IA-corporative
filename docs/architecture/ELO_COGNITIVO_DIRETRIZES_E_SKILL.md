# ELO Cognitivo — Diretrizes e Skill Boundary

**Status:** CANONICAL REFERENCE  
**Natureza:** contrato de identidade, autoridade e fronteira cognitiva  
**Owner:** ELO Cognitivo  
**Version:** 1.0

## 1. Finalidade

O ELO Cognitivo é a autoridade normativa do sistema: identidade, cânone, princípios, invariantes, limites de autonomia, governança e regras de evolução.

Este documento não cria uma nova camada nem substitui o `ELO_BOOTSTRAP.md`, contratos cognitivos ou documentos de governança existentes. Ele define somente a referência operacional para a relação entre identidade, Core, Forge, Simbionte e skills.

## 2. Diretrizes

1. Preservar identidade, princípios e invariantes do ELO.
2. Manter autoridade normativa separada da faculdade compartilhada do Core.
3. Governar os limites de autonomia, autorização, segurança, proveniência e evolução.
4. Não delegar autoridade canônica a Hermes, OpenClaw, plugins, bibliotecas, aplicações ou infraestrutura.
5. Não transformar experiência contextual em cânone sem evidência, generalização e Evolution Gate.
6. Exigir que conflitos permaneçam identificáveis e preservem proveniência.
7. Impedir criação de segunda autoridade para Core, Memory, Router, Skill Registry ou Evolution Gate.
8. Manter separação entre `DOCUMENTED`, `CONTRACTED`, `IMPLEMENTED`, `TESTED`, `VERIFIED` e `EVOLUTION-GATED`.
9. Uma autorização técnica ou acesso a infraestrutura não equivale a autoridade ELO.
10. Alterações estruturais, de segurança, identidade ou governança exigem o caminho de autorização correspondente.

## 3. Skill Boundary do ELO Cognitivo

O ELO Cognitivo **não deve possuir uma skill operacional de domínio que concorra com o Forge**. Sua função é governar o contrato pelo qual skills são criadas, executadas, avaliadas e eventualmente promovidas.

A função normativa é:

`DEFINE AUTHORITY → DEFINE INVARIANTS → AUTHORIZE BOUNDARIES → GOVERN EVIDENCE → CONTROL PROMOTION`

Skills concretas permanecem no Forge e são registradas pelo `forge/SPECIALIST_SKILL_REGISTRY.md`. O ELO Cognitivo define o que é permitido e quais condições devem ser satisfeitas; não duplica a implementação das skills.

## 4. Relação com Core

`ELO Cognitivo → governa → Core`

`Core → materializa → mecanismos cognitivos compartilhados`

O ELO Cognitivo não deve reimplementar no próprio documento ou camada aquilo que pertence ao Core. O Core também não pode redefinir a identidade ou os invariantes do ELO Cognitivo.

## 5. Relação com Simbionte

`ELO Cognitivo → autoriza e governa → Simbionte → observa/refina → candidato → Evolution Gate`

A Simbionte pode explorar mecanismos e propor adaptações, mas não redefine a identidade do ELO, não cria autoridade paralela e não promove diretamente para Core.

## 6. Relação com skills e aprendizado

Caminho canônico:

`SOURCE → EVIDENCE → FORGE SKILL → TEST → EMPIRICAL VALIDATION → CONTEXTUAL EXPERIENCE → GENERALIZATION → EVOLUTION GATE → OPTIONAL CORE PROMOTION`

Uma skill bem-sucedida em uma execução não é automaticamente aprendizado generalizado. A promoção depende do mecanismo de governança já existente.

## 7. Regra de não duplicidade

Antes de criar qualquer artefato atribuído ao ELO Cognitivo, verificar se sua finalidade já pertence a:

- `ELO_BOOTSTRAP.md`;
- contratos cognitivos;
- `09-governance/`;
- `src/elo/core/`;
- Forge Specialist Skill Registry;
- memória/evolução da Simbionte.

Se a finalidade já estiver coberta, este documento deve apontar para a fonte canônica em vez de reproduzi-la.

## 8. Fontes canônicas relacionadas

- `ELO_BOOTSTRAP.md` — identidade e separação das camadas.
- `forge/SPECIALIST_SKILL_REGISTRY.md` — skills e especialistas.
- `src/elo/core/README.md` — faculdade compartilhada do Core.
- `docs/architecture/ELO_HERMES_SYMBIONT_CONTRACT.md` — fronteira de execução e evolução.
- `09-governance/GOVERNANCE_MASTER.md` — governança.

Este arquivo é uma referência de fronteira e não uma nova fonte normativa concorrente.
