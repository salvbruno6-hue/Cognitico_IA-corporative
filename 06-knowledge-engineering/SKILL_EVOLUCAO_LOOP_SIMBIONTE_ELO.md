# SKILL_EVOLUCAO_LOOP_SIMBIONTE_ELO

**Versão:** V0.1 — candidata  
**Status:** CANDIDATO / EM VALIDAÇÃO  
**Natureza:** Skill de evolução e governança do Loop Simbionte existente

## 1. Finalidade

Conduzir a evolução controlada do Loop Simbionte ELO a partir de evidências reais, regras existentes, experiências, aprendizados, automações, contratos e estado operacional.

A Skill transforma uma lacuna identificada em: evidência estruturada; diagnóstico do GAP; hipótese de evolução; alteração mínima necessária; teste; validação; decisão pelo Evolution Gate; promoção governada, quando autorizada; atualização do artefato canônico correspondente.

**Princípio:** Evidência antes de evolução; validação antes de promoção.

## 2. Limites arquiteturais

Esta Skill **não é um novo Loop Simbionte**. O Evolution Gate é uma etapa de governança dentro da Skill.

### Não criar
- novo Loop Simbionte;
- segundo Loop de aprendizado;
- segundo Evolution Gate;
- novo registry de automações;
- nova memória cognitiva;
- novo banco de relações;
- novo mecanismo de promoção automática;
- nova autoridade paralela de aprendizagem.

### Reutilizar
- Loop Simbionte ELO existente;
- contrato do ciclo de execução;
- Learning Governance existente;
- Evolution Gate como etapa de governança;
- experiências, conceitos, padrões, especializações e relações existentes;
- automações e seus registros/execuções;
- eventos de evolução;
- auditoria;
- estruturas de planejamento e execução;
- GitHub como autoridade de engenharia/versionamento;
- Supabase como autoridade de persistência cognitiva/operacional;
- ELO como autoridade de orquestração cognitiva.

## 3. Fluxo

RETRIEVE → EVIDÊNCIA → CONFRONTAÇÃO → GAP → EVOLUÇÃO → TESTE → VALIDAÇÃO → EVOLUTION GATE → PROMOÇÃO → ATUALIZAÇÃO

A Skill não deve pular uma etapa sem registrar a razão.

## 4. RETRIEVE — reconstrução do estado

Recuperar, conforme aplicabilidade:
- objetivo e contexto da demanda;
- estado atual e pendências;
- experiências, conceitos, padrões, especializações e relações;
- automações e suas execuções;
- eventos de evolução;
- dados operacionais, planejamento, execução e resultados;
- documentação, contratos, Skills, testes e implementação no GitHub;
- histórico relevante de issues/PRs.

Ausência de registro não é evidência positiva. Quando necessário, registrar **NÃO LOCALIZADO**.

## 5. EVIDÊNCIA — classificação

| Classe | Significado |
|---|---|
| DADO | dado operacional ou persistido verificável |
| FONTE | informação diretamente localizada em fonte documental |
| EXPERIÊNCIA | registro de experiência executada |
| APRENDIZADO VALIDADO | conhecimento já validado |
| REGRA | regra ou contrato vigente |
| INFERÊNCIA CONTROLADA | conclusão explicitamente derivada de evidências |
| HIPÓTESE | proposta ainda não validada |
| NÃO LOCALIZADO | informação necessária não encontrada |

Não converter inferência em dado nem hipótese em aprendizado sem validação.

## 6. CONFRONTAÇÃO

Cada evidência deve ser confrontada com contrato, regra, Skill, implementação, automação, persistência, testes e resultado observado.

Pergunta central: **o comportamento necessário já existe, existe parcialmente, existe apenas como contrato/documentação ou não existe?**

Classificação: REUSE, EXTEND, SUPERSEDE, CONFLICT ou NEW.

NEW somente quando a arquitetura existente não puder atender ao requisito sem criar duplicação semântica.

## 7. GAP

A Skill deve produzir:

| Componente | Evidência | Estado atual | GAP | Causa | Ação necessária | Fonte |
|---|---|---|---|---|---|---|

Tipos de GAP: DOCUMENTAL, CONTRATUAL, DADO, INTEGRAÇÃO, PERSISTÊNCIA, EXECUÇÃO, TESTE, VALIDAÇÃO, GOVERNANÇA e PROMOÇÃO.

Sem evidência suficiente, o GAP permanece NÃO LOCALIZADO.

## 8. EVOLUÇÃO

A evolução deve ser mínima e orientada pelo GAP.

Prioridade: REUSE → EXTEND → RELATE → REFACTOR/MIGRATE → CREATE.

Toda proposta deve responder: o que muda; por que muda; qual evidência exige a mudança; qual componente canônico será alterado; qual componente não deve ser criado; como será testado; como será revertido; qual resultado é esperado.

## 9. TESTE

Contrato mínimo: REQUISITO → CONTRATO → IMPLEMENTAÇÃO → TESTE → RESULTADO.

O teste deve verificar comportamento esperado, limites, ausência de duplicação, preservação de autoridade, rastreabilidade, proveniência, não inferência, regressão e reprodutibilidade quando aplicável.

Se o teste necessário não existir ou não puder ser executado, a validação não está concluída.

## 10. VALIDAÇÃO

Registrar evidência usada; versão da Skill; versão do contrato/regra; entrada; resultado esperado; resultado observado; divergência; impacto; confiança; aplicabilidade; limitações.

Uma execução isolada não generaliza uma regra.

## 11. EVOLUTION GATE

O Evolution Gate é uma **etapa da Skill**, não uma nova autoridade.

Estados de evolução:

OBSERVED → EVIDENCED → ASSOCIATED → HYPOTHESIS → TESTED → REFINED → LEARNING_CANDIDATE → GOVERNED_LEARNING → EVOLUTION_GATE → VALIDATED_LEARNING

O Gate verifica: evidência suficiente; proveniência preservada; teste executado; reprodutibilidade quando aplicável; ausência de conflito de autoridade; aplicabilidade delimitada; confiança suficiente; regressão avaliada; impacto conhecido; referência ao artefato a atualizar.

Saídas mínimas: PASS, PASS_WITH_LIMITATIONS, HOLD ou FAIL.

O Gate não executa automaticamente promoção canônica sem a autoridade de governança correspondente.

## 12. PROMOÇÃO

Estados: CANDIDATO → TESTADO → VALIDADO → CONSOLIDADO.

Critério: evidência ∧ critérios ∧ autoridade.

Não promover com evidência insuficiente, conflito não resolvido, teste ausente, regressão não resolvida, aplicabilidade indefinida ou autoridade ausente.

## 13. ATUALIZAÇÃO

Após validação e governança, atualizar somente o artefato canônico correspondente: Skill, contrato, regra, documentação, código, experiência, evento de evolução ou relações.

Preservar origem, versão, data, escopo, aplicabilidade, limitações, status de validação e evidência utilizada.

## 14. Integração das automações

As automações existentes são mecanismos de execução, não autoridade de aprendizagem.

Funções relevantes incluem captura de experiência, derivação de padrões, relacionamento de conceitos, recalculo de especialização, atualização de orientação, avaliação de progressão, verificação de integridade e ELO Scan Orchestrator.

Regra: **AUTOMAÇÃO EXECUTA → ELO INTERPRETA/VALIDA → GOVERNANÇA DECIDE**.

Não: AUTOMAÇÃO EXECUTA → APRENDIZADO É PROMOVIDO.

## 15. Planejado × Realizado

Quando houver dados operacionais: DESVIO = REALIZADO − PLANEJADO.

Registrar planejado, realizado, desvio, unidade, período, fonte, causa conhecida, impacto, correção e resultado da correção.

Sem dados reais: PLANEJADO × REALIZADO = NÃO LOCALIZADO. Não criar dados artificiais.

## 16. Persistência do ciclo

Verificar evidência dos elementos: IDENTIDADE → ENTRADA → DEMANDA/EVENTO → FONTES → DADOS ATUAIS → SKILL + VERSÃO → ANÁLISE → DECISÃO → IMPACTO → EXECUÇÃO → RESULTADO → DESVIO → EVIDÊNCIA → APRENDIZADO → STATUS DE VALIDAÇÃO.

Não assumir que a existência de tabelas significa que o ciclo completo está persistido.

## 17. Aplicação às pendências

Para cada pendência: verificar evidência; verificar se componente já existe; classificar REUSE/EXTEND/NEW; verificar teste; verificar execução; verificar resultado; aplicar Evolution Gate.

## 18. Critérios de encerramento

Uma evolução somente é concluída quando existir: requisito identificado; evidência rastreável; GAP classificado; solução confrontada com a arquitetura; implementação/documentação adequada; teste; resultado; validação; Evolution Gate; atualização canônica autorizada; verificação pós-atualização; registro de aprendizado quando aplicável.

Definição: **CONCLUÍDO = EVIDÊNCIA + TESTE + VALIDAÇÃO + GOVERNANÇA + ATUALIZAÇÃO VERIFICADA**.

## 19. Estado inicial conhecido

| Componente | Estado |
|---|:---:|
| Integração das automações ao Loop completo | PENDENTE |
| Estrutura Planejado × Realizado | MODELO EXISTENTE |
| Dados operacionais para teste | PENDENTE |
| Persistência completa do ciclo | PENDENTE |
| Planejado × Realizado | PENDENTE |
| Promoção automática | PENDENTE |
| Evolution Gate | PENDENTE — desenvolver primeiro |

A existência de automações, modelos ou tabelas não constitui prova de integração funcional.

## 20. Regra de não inferência

Sem suporte suficiente: **NÃO LOCALIZADO**.

Apenas hipótese: **HIPÓTESE**.

Implementação sem validação: **IMPLEMENTADO / NÃO VALIDADO**.

Teste sem evidência operacional: **TESTADO EM CENÁRIO CONTROLADO**.

Evidência + teste + validação + governança: **VALIDADO**.

## 21. Princípio final

A Skill não existe para afirmar que o Loop evoluiu. Ela existe para demonstrar, por evidência, quando e por que o Loop pode evoluir.

EVIDÊNCIA + CONFRONTAÇÃO + TESTE + VALIDAÇÃO + GOVERNANÇA = EVOLUÇÃO AUTORIZADA