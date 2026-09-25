# ELO Forge — Modelo de Execução do Construtor

## Finalidade

Este documento fecha o modelo operacional do Forge como plano construtor do ELO Cognitivo.

O Forge recebe um objetivo explícito, lê as restrições canônicas aplicáveis, constrói uma solução candidata, testa, mede, compara, corrige e prepara a promoção. Ele não cria autoridade canônica paralela.

## Ciclo canônico de construção

```
OBJETIVO
  ↓
CONTRATO / RESTRIÇÕES CANÔNICAS
  ↓
ESCOPO DE CONSTRUÇÃO
  ↓
PLANO
  ↓
CONSTRUÇÃO
  ↓
TESTE
  ↓
EVIDÊNCIA
  ↓
COMPARAÇÃO COM O CÂNONE
  ↓
DIVERGÊNCIA?
  ├─ não → VALIDAR
  └─ sim
       ↓
   CLASSIFICAR
       ├─ ajustável → CORRIGIR → TESTAR
       ├─ melhoria canônica → CANDIDATO ARQUITETURAL
       └─ incompatível → ISOLAR / REJEITAR
  ↓
VALIDAÇÃO
  ↓
PACOTE DE PROMOÇÃO
  ↓
PR / PROMOÇÃO CANÔNICA
```

## Princípios de execução

1. **Objetivo antes da implementação.**
2. **Cânone antes da conveniência.**
3. **Evidência antes da promoção.**
4. **Teste antes da decisão de compatibilidade.**
5. **Divergência explícita.**
6. **Mudança reversível sempre que tecnicamente possível.**
7. **Nenhum artefato de Forge torna-se canônico apenas por existir.**
8. **Conhecimento externo é evidência, não autoridade.**
9. **Dados operacionais não são promovidos como arquitetura.**
10. **Toda construção relevante deixa rastreabilidade suficiente para reprodução e auditoria.**

## Resultado mínimo de uma construção

Toda construção encerrada deve conseguir responder:

- qual objetivo foi atendido;
- qual contrato canônico foi aplicado;
- o que foi construído;
- como foi testado;
- quais evidências foram obtidas;
- quais divergências apareceram;
- quais correções foram realizadas;
- qual decisão foi tomada;
- qual é o caminho de promoção ou rejeição;
- qual é o caminho de reversão.

## Limite

O Forge constrói. O CORE governa. O COGNITIVE interpreta e utiliza capacidades. A promoção continua sujeita ao Evolution Gate.
