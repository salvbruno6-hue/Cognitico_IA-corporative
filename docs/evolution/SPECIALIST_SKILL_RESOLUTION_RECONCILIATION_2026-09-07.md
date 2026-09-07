# ELO — Specialist Skill Resolution Reconciliation — 2026-09-07

## Objetivo
Reconciliar a proposta do PR #407 com a `main` atual sem criar uma segunda autoridade para Skills.

## Diagnóstico
A `main` possui o Forge Specialist Skill Registry como fonte canônica, porém a capacidade executável de resolver um `domain_family` para um `skill_id` não estava presente em `src/elo/core`. O PR #407 adicionava essa capacidade, mas seu branch estava divergente da `main` atual e também carregava alterações históricas adicionais.

## Correção
Foi incorporado somente o núcleo necessário da capacidade em uma nova implementação reconciliada:

- `SpecialistSkillResolver` consome snapshot explícito do Registry do Forge;
- resolução exige `domain_family` exato;
- maturidade mínima é validada contra uma ordem determinística;
- autorização permanece externa ao resolver, por callback explícito;
- ausência de Skill resulta em `GAP`;
- ausência de candidato autorizado resulta em `BLOCKED`;
- seleção entre candidatos autorizados usa desempate determinístico por maturidade e `skill_id`;
- `skill_from_registry_record()` adapta registros do Registry sem criar nova fonte de verdade;
- nenhuma persistência, promoção, mutação de Core, Soul ou Supabase é realizada pelo resolver.

## Integração Supabase
A varredura live confirma que o Supabase possui estruturas de identidade, capabilities e scopes para autorização, mas não possui uma tabela canônica de Specialist Skills. Portanto, o resolver não cria tabela paralela no Supabase. O Registry do Forge permanece a fonte de verdade da Skill; a autorização continua no caminho canônico de identidade/capability/scope.

## Testes adicionados
`tests/test_specialist_skill_resolution_reconcile.py` cobre:

1. resolução exata por domínio e maturidade;
2. ausência de domínio registrado → `GAP`;
3. maturidade mínima desconhecida → `BLOCKED`;
4. autorização externa negada → `BLOCKED`;
5. adaptação de registro canônico com validação de identidade.

## Regra de governança
`SpecialistSkillResolver` é resolução, não autoridade. Não registra Skill, não concede permissão, não promove conhecimento e não altera o Registry do Forge.

## Critério de fechamento
A alteração só poderá chegar à `main` após CI completo na branch e revisão da integração com `GPTDecisionHandoff`, `SpecialistFeedback` e `EvolutionGate`.
