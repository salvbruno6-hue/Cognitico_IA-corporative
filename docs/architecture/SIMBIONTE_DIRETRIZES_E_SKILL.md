# ELO — Diretrizes e Skill da Simbionte

**Status:** FORGE / EVOLUTION LAB / CANDIDATE-ONLY  
**Natureza:** contrato operacional complementar  
**Owner:** ELO Cognitivo  
**Shared faculty:** Core  
**Promotion gate:** Evolution_Gate  
**Version:** 1.0

## 1. Finalidade

A Simbionte é a natureza cognitiva de associação, observação, adaptação, experimentação e refinamento do ELO. Ela não constitui um novo componente arquitetural, uma segunda memória, um segundo Core, um segundo orquestrador ou uma autoridade paralela.

Sua finalidade é transformar experiência observada em melhoria testável de uma capacidade ELO já existente, preservando contexto, mecanismo, justificativa, evidência, resultado, falha e refinamento.

## 2. Diretrizes

1. **Partir do ELO existente.** Toda adaptação deve procurar primeiro uma capability, skill, mecanismo ou contrato já existente.
2. **Não duplicar finalidade.** Se existir artefato com o mesmo objetivo, a Simbionte deve reutilizá-lo, fortalecê-lo ou refatorá-lo; não criar uma versão semanticamente equivalente.
3. **Separar fonte de autoridade.** Hermes, OpenClaw, plugins, bibliotecas, documentos e outros provedores são fontes de experiência/evidência ou meios de execução; não são autoridade canônica do ELO.
4. **Preservar proveniência.** Toda experiência deve manter origem, revisão, contexto, escopo e resultado.
5. **Refinar, não copiar.** O mecanismo externo deve ser decomposto e adaptado ao contrato ELO; código ou estrutura externa não se torna canônica por semelhança.
6. **Medir ganho.** Toda adaptação deve possuir baseline, hipótese, métrica, resultado e análise de regressão.
7. **Iterar.** Resultado insuficiente produz diagnóstico e nova versão candidata; não produz promoção automática.
8. **Preservar falhas.** Experimentos malsucedidos permanecem como evidência histórica e não podem ser apagados para produzir uma narrativa de sucesso.
9. **Respeitar limites.** A Simbionte não altera Soul, Core, autoridade, autorização, segurança, identidade, tenant boundary ou Evolution Gate por conta própria.
10. **Aprender sob governança.** Uma melhoria só pode ser considerada aprendizado generalizável após evidência, repetição, compatibilidade, governança e Evolution Gate.

## 3. Skill operacional da Simbionte

A skill canônica de adaptação refinada é `SIMBIONTE-ADAPT-001`, definida em `forge/skill-packs/SIMBIONTE_REFINED_ADAPTATION_SKILL.yaml`.

Fluxo obrigatório:

`OBSERVE → INTERPRET → DECOMPOSE → EXTRACT_MECHANISM → IDENTIFY_EXISTING_OWNER → CHECK_COMPATIBILITY → ADAPT → GOVERN → TEST → MEASURE → DIAGNOSE → REFINE → RETEST`

### Saída mínima

- capability ELO existente relacionada;
- mecanismo identificado;
- adaptação proposta;
- justificativa técnica;
- baseline;
- hipótese de ganho;
- experimento controlado;
- resultado e métricas;
- regressão/riscos;
- proveniência;
- estado de aprendizado;
- próximo refinamento, quando necessário.

## 4. Estados

`OBSERVED → EVIDENCED → ASSOCIATED → HYPOTHESIS → ADAPTED → TESTED → REFINED → LEARNING_CANDIDATE → GOVERNED_LEARNING → EVOLUTION_GATE → VALIDATED_LEARNING`

Nenhum estado intermediário equivale a promoção canônica.

## 5. Limites de não duplicidade

A Simbionte não deve criar:

- nova Memory Authority;
- novo Core;
- novo Reasoning Engine;
- novo Router;
- novo Skill Registry;
- novo Evolution Gate;
- nova autoridade de governança;
- uma segunda implementação apenas por existir Hermes/OpenClaw.

Quando houver sobreposição aparente, a primeira ação é **resolver a relação com o artefato existente**, classificando-a como `REUSE`, `STRENGTHEN`, `REFACTOR` ou `DEPRECATE`. `CREATE` exige demonstração de ausência de owner adequado e generalização comprovável.

## 6. Relação com os artefatos canônicos

- Memória da experiência: `docs/evolution/SIMBIONTE_MEMORY.md`.
- Associação harmônica: `docs/evolution/SIMBIONTE_HARMONIC_ASSOCIATION_2026-09-07.md`.
- Intake de laboratório: `docs/evolution/SIMBIONTE_LAB_INTAKE_2026-09-06.md`.
- Skill formal: `forge/skill-packs/SIMBIONTE_REFINED_ADAPTATION_SKILL.yaml`.
- Registro geral de skills: `forge/SPECIALIST_SKILL_REGISTRY.md`.
- Contrato ELO–Hermes: `docs/architecture/ELO_HERMES_SYMBIONT_CONTRACT.md`.

Este arquivo não substitui nem replica o conteúdo normativo desses artefatos; define apenas a diretriz de operação conjunta da Simbionte.

## 7. Critério de evolução

A Simbionte somente entrega um candidato para aprendizado governado quando houver:

`proveniência + contexto + baseline + mecanismo + adaptação + experimento + resultado + métricas + regressão + generalização + risco + owner`

**Regra final:** a Simbionte observa e refina; o ELO Cognitivo governa; o Core incorpora somente o que for validado e promovido pelo caminho canônico.


## 3.1 Pré-intake de criação de Skill dentro do fluxo existente

Antes de propor uma nova Skill, a própria `SIMBIONTE-ADAPT-001` deve reconciliar:

1. `existing_owner`: existe owner/capability/skill adequada?
2. componentes requeridos: `FOUND | PARTIAL | MISSING`;
3. prontidão da base para intake.

Disposições:

`REUSE` → owner identificado pelo `SpecialistSkillResolver` canônico; não criar duplicidade.  
`DEVELOP_FIRST` → componente ou evidência obrigatória ausente, parcial, bloqueada ou não comprovada.  
`READY_FOR_INTAKE` → componentes e evidências mínimas completas e nenhum owner existente identificado independentemente.

### Evidência mínima de prontidão

Cada componente requerido deve declarar, além de `FOUND | PARTIAL | MISSING`:

- documentação: `FOUND | PARTIAL | MISSING`;
- teste: `TESTED | PARTIAL | UNTESTED | FAILED`;
- autorização: `COMPATIBLE | BLOCKED | UNKNOWN`; quando `COMPATIBLE`, a evidência deve identificar a autoridade canônica `elo-authz` e possuir referência de evidência;
- compatibilidade: `COMPATIBLE | CONFLICT | UNKNOWN`;
- baseline: `PRESENT | MISSING`;
- medição: `PRESENT | MISSING`;
- regressão: `PASS | FAIL | UNKNOWN`.

O `readiness_score` representa **cobertura de evidência do pré-intake**, não qualidade global, maturidade ou probabilidade de sucesso. A qualidade e a generalização continuam sendo avaliadas no laboratório e no Evolution Gate.

`existing_owner` fornecido manualmente não é suficiente para `REUSE` quando a resolução canônica não foi executada. O owner precisa ser independentemente resolvido pelo `SpecialistSkillResolver` quando essa verificação for necessária.

A avaliação é somente evidência de pré-intake. Não cria Skill, Registry, Capability, autorização ou aprendizado e não substitui o Evolution Gate.

O mecanismo é implementado dentro de `SymbiontPatternIntake`, reutilizando o `SpecialistSkillResolver`; não existe um segundo resolver de pré-intake.


### 3.2 Fronteira de autorização no pré-intake

O pré-intake não cria nem resolve autorização. A decisão autorizativa deve vir da autoridade canônica existente, `elo-authz`, e ser transportada como evidência verificável para o componente avaliado.

Para um componente ser considerado `authorization_status=COMPATIBLE`, são obrigatórios:

- `authorization_authority=elo-authz`;
- `authorization_evidence_ref` não vazio.

Ausência, bloqueio ou autoridade diferente de `elo-authz` impede a suficiência da evidência. O `SymbiontPatternIntake` não interpreta role, sessão, capability ou scope e não substitui a decisão de `elo-authz`.

Essa fronteira mantém a separação: `elo-authz` autoriza; `SpecialistSkillResolver` resolve owner; `SymbiontPatternIntake` avalia evidência de pré-intake; o Evolution Gate governa evolução.
