# CONTRATO — CICLO DE EXECUÇÃO DO ELO

**Status:** V0.1 — proposta para validação  
**Domínio:** Loop simbionte ELO / integração ELO–Supabase–GitHub  
**Base:** LOOP_SIMBIONTE_ELO.md

## 1. Finalidade

Definir a unidade mínima rastreável de um ciclo do ELO.

O contrato não executa decisões nem promove conhecimento. Ele define quais informações precisam existir para que uma execução possa ser reconstruída, comparada e posteriormente validada.

## 2. Estrutura obrigatória

IDENTIDADE → ENTRADA → DEMANDA/EVENTO → FONTES → DADOS ATUAIS → SKILL/REGRA + VERSÃO → ANÁLISE → DECISÃO → IMPACTO → EXECUÇÃO → RESULTADO → DESVIO → EVIDÊNCIA → APRENDIZADO → STATUS DE VALIDAÇÃO

## 3. Campos e significado

| Bloco | Conteúdo mínimo |
|---|---|
| IDENTIDADE | identificador do ciclo e data/hora |
| ENTRADA | pergunta, demanda ou evento que iniciou o ciclo |
| DEMANDA/EVENTO | origem e contexto da necessidade |
| FONTES | fontes consultadas e proveniência |
| DADOS ATUAIS | valores efetivamente usados na análise |
| SKILL/REGRA + VERSÃO | comportamento de engenharia aplicado |
| ANÁLISE | relações, cálculos, confrontações e premissas |
| DECISÃO | conclusão ou ação definida |
| IMPACTO | efeito esperado e condição de aplicação |
| EXECUÇÃO | ação efetivamente realizada, quando existir |
| RESULTADO | resultado real observado ou NÃO LOCALIZADO |
| DESVIO | diferença entre planejado e realizado, quando aplicável |
| EVIDÊNCIA | documentos, registros ou resultados que sustentam o ciclo |
| APRENDIZADO | conhecimento candidato extraído do ciclo |
| STATUS DE VALIDAÇÃO | candidato, testado, validado ou consolidado |

## 4. Regra de completude

Um ciclo só pode ser marcado como FECHADO quando:

1. a entrada estiver identificada;
2. as fontes estiverem registradas;
3. a análise estiver registrada;
4. a decisão/conclusão estiver registrada;
5. o resultado estiver disponível ou explicitamente marcado como NÃO LOCALIZADO;
6. a evidência estiver registrada;
7. o status de validação estiver definido.

Caso contrário: STATUS = INCOMPLETO

## 5. Regra de evidência

O contrato deve preservar a distinção:

DADO × FONTE VISUAL × APRENDIZADO VALIDADO × INFERÊNCIA CONTROLADA × NÃO LOCALIZADO

É proibido transformar:
- histórico em dado atual;
- hipótese em fato;
- inferência em dado;
- candidato em regra consolidada.

## 6. Planned × Realizado

DESVIO = REALIZADO - PLANEJADO

A unidade, indicador e sentido da diferença devem ser definidos antes do cálculo.

Quando não existir execução real, não criar resultado por inferência.

## 7. Persistência

O contrato reconhece as responsabilidades:

- Supabase: estado operacional, execução, resultado e aprendizado persistente;
- GitHub: skill, regra, contrato, teste e versionamento;
- ELO: execução cognitiva, confronto, análise, decisão e registro.

A tabela elo_evolution_events pode representar eventos de evolução, mas sua utilização como persistência completa do ciclo ainda depende de validação do modelo de dados. Não presumir que ela substitua um registro dedicado de execução.

## 8. Gate de aprendizado

CANDIDATO → TESTADO → VALIDADO → CONSOLIDADO

O ciclo não promove conhecimento automaticamente.

A evidência deve acompanhar qualquer proposta de promoção.

## 9. Estado V0.1

Este contrato é CANDIDATO / NÃO CONSOLIDADO.

Próxima validação:

ENTRADA → FONTES → ANÁLISE → DECISÃO → RESULTADO → EVIDÊNCIA → APRENDIZADO

Somente após testar essa sequência com um caso real ou controlado o contrato poderá ser promovido.