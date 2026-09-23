# LOOP SIMBIÔNTE ELO

**Status:** V0.1 — proposta para validação  
**Domínio:** Arquitetura cognitiva / integração ELO–Supabase–GitHub  
**Branch de desenvolvimento:** `feat/skill-planejamento-multiteiner`  
**PR de referência:** #689

---

## 1. Finalidade

Definir o processo de **loop simbionte do ELO** como mecanismo fechado de percepção, recuperação de conhecimento, análise, decisão, execução, comparação com o resultado real, aprendizado e validação.

O ELO não deve funcionar apenas como uma camada que consulta conhecimento e responde. O comportamento-alvo é:

`PERCEBER → CONSULTAR → CONFRONTAR → RACIOCINAR → DECIDIR → EXECUTAR → MEDIR → APRENDER → VALIDAR → ATUALIZAR → PERCEBER`

O objetivo é criar continuidade entre:

- conhecimento persistente;
- regras e skills versionadas;
- dados operacionais atuais;
- decisões executadas;
- resultados reais;
- aprendizado validado.

---

## 2. Princípio do simbionte

O simbionte é composto por três camadas principais:

### ELO — cognição

Responsável por:

- identificar a necessidade;
- formular a pergunta correta;
- selecionar fontes relevantes;
- confrontar fontes;
- executar o raciocínio;
- calcular quando aplicável;
- explicar a decisão;
- registrar resultado e evidência.

### Supabase — memória e estado

Responsável por:

- conhecimento estruturado;
- experiências;
- conceitos;
- padrões de raciocínio;
- aprendizados;
- demanda;
- estoque;
- capacidade;
- planos;
- execução;
- resultados persistentes.

### GitHub — engenharia versionada

Responsável por:

- skills;
- regras;
- contratos;
- prompts;
- código;
- testes;
- documentação;
- histórico de alterações.

A separação não cria três autoridades concorrentes. Cada camada possui uma responsabilidade específica.

---

## 3. Loop fechado

```text
                 DEMANDA / EVENTO
                        ↓
                 [1] PERCEPÇÃO
                        ↓
                 [2] RECUPERAÇÃO
                        ↓
              SUPABASE + GITHUB
                        ↓
                [3] CONFRONTAÇÃO
                        ↓
                 DADOS ATUAIS
                        ↓
                  [4] RACIOCÍNIO
                        ↓
                   [5] DECISÃO
                        ↓
                  [6] EXECUÇÃO
                        ↓
                  [7] RESULTADO
                        ↓
             PLANEJADO × REALIZADO
                        ↓
                 [8] APRENDIZADO
                        ↓
                  [9] VALIDAÇÃO
                        ↓
             [10] PERSISTÊNCIA
                ↙              ↘
          SUPABASE           GITHUB
                ↘              ↙
                     ELO
                      ↺
```

O retorno ao ELO fecha o ciclo.

---

## 4. Estados do loop

O loop deve trabalhar com estados explícitos:

| Estado | Significado |
|---|---|
| `PERCEPÇÃO` | Demanda/evento identificado |
| `RETRIEVAL` | Fontes relevantes recuperadas |
| `CONFRONTAÇÃO` | Conhecimento e dados comparados |
| `ANÁLISE` | Relações, cálculos e impactos avaliados |
| `DECISÃO` | Ação ou orientação definida |
| `EXECUÇÃO` | Decisão aplicada ao processo |
| `RESULTADO` | Resultado real observado |
| `DESVIO` | Diferença entre planejado e realizado |
| `APRENDIZADO` | Conhecimento candidato extraído |
| `VALIDAÇÃO` | Evidência avaliada |
| `CONSOLIDAÇÃO` | Conhecimento promovido |
| `RETORNO` | Conhecimento disponível para novo ciclo |

Nem todo ciclo terá todos os estados. A execução e o resultado real podem não existir em uma análise puramente documental. Nesse caso, o estado deve permanecer explícito como não disponível.

---

## 5. Ordem de consulta

A sequência cognitiva é:

`ELO → identificar necessidade → consultar Supabase → confrontar fonte operacional atual → consultar GitHub para regra/skill vigente → analisar → decidir → registrar → aprender`

Essa ordem não significa que o histórico tenha prioridade sobre o dado atual.

### Prioridade por natureza da informação

| Informação | Fonte de referência |
|---|---|
| Situação operacional atual | Supabase / fonte operacional vigente |
| Conhecimento persistente | Supabase |
| Experiência histórica | Supabase |
| Regra de comportamento da skill | GitHub |
| Método/fórmula documentado | GitHub + conceito correspondente |
| Código | GitHub |
| Teste | GitHub |
| Resultado executado | Supabase |
| Novo aprendizado | Supabase |
| Promoção de regra/skill | GitHub após validação |

---

## 6. Regra de confronto

Antes de uma decisão, o ELO deve separar:

`HISTÓRICO × REGRA VIGENTE × DADO ATUAL × DEMANDA ATUAL`

Cada informação deve ser classificada, quando aplicável, como:

- **DADO**;
- **FONTE VISUAL**;
- **APRENDIZADO VALIDADO**;
- **INFERÊNCIA CONTROLADA**;
- **NÃO LOCALIZADO**.

Não converter:

- histórico em dado atual;
- hipótese em fato;
- inferência em dado;
- candidato em regra consolidada.

---

## 7. Estrutura mínima da decisão

Toda decisão relevante deve poder ser reconstruída por:

`DECISÃO = ENTRADAS + FONTES + MÉTODO/REGRA + RESULTADO + IMPACTO + CONDIÇÃO DE APLICAÇÃO`

Registrar, quando disponível:

- demanda;
- valores de entrada;
- unidade;
- período;
- fonte;
- regra/skill utilizada;
- versão da skill;
- fórmula ou relação;
- resultado;
- impacto;
- premissas;
- pendências;
- status de validação.

O objetivo é preservar **o caminho da escolha**, e não somente o resultado final.

---

## 8. Planejado × realizado

Quando houver execução real, o loop deve comparar:

`PLANEJADO × REALIZADO`

Avaliar:

- quantidade;
- prazo;
- capacidade;
- consumo;
- estoque;
- sequência;
- qualidade;
- custo;
- produtividade;
- ocorrência de exceções;
- recuperação utilizada.

Se houver diferença material, abrir análise de desvio.

### Desvio

`DESVIO = REALIZADO - PLANEJADO`

A fórmula acima representa a relação conceitual. A unidade e o sentido devem ser definidos pelo indicador específico antes do cálculo.

---

## 9. Aprendizado não automático

Um resultado não deve virar regra imediatamente.

O ciclo de promoção é:

`CANDIDATO → TESTADO → VALIDADO → CONSOLIDADO`

### CANDIDATO

Hipótese ou padrão observado.

### TESTADO

Aplicado em cenário controlado ou caso comparável.

### VALIDADO

Existe evidência suficiente de que o conhecimento funciona dentro do escopo definido.

### CONSOLIDADO

Conhecimento autorizado para recuperação como regra operacional.

O histórico continua preservado mesmo quando não é promovido.

---

## 10. Condição de retorno

O loop pode retornar ao ELO quando:

- uma decisão foi registrada;
- uma execução produziu resultado;
- um desvio foi identificado;
- uma experiência foi validada;
- uma regra foi atualizada;
- uma nova demanda exige reutilização do conhecimento.

O retorno deve preservar a origem da informação.

Modelo:

`RESULTADO → EVIDÊNCIA → APRENDIZADO → STATUS → FONTE → NOVA CONSULTA`

---

## 11. Divergência entre Supabase e GitHub

Quando houver conflito:

1. identificar a informação divergente;
2. identificar a versão de cada fonte;
3. determinar qual é vigente para a situação;
4. impedir promoção automática do conhecimento conflitante;
5. registrar a divergência;
6. validar antes de consolidar.

Não ocultar divergências.

A situação corrente deve utilizar o dado operacional vigente. O comportamento da engenharia deve utilizar a regra/skill vigente no GitHub.

---

## 12. Interface com as skills especializadas

O loop simbionte é uma camada transversal.

Uma skill especializada não cria um loop próprio isolado. Ela participa do loop comum.

Exemplo para Planejamento Multiteiner:

`DEMANDA → ELO → SKILL PCP → SUPABASE/GITHUB → ANÁLISE → PLANEJAMENTO → EXECUÇÃO → RESULTADO → APRENDIZADO → ELO`

Exemplo para Orçamento:

`SO → ELO → PTS TÉCNICA → ESPECIALISTA → ORÇAMENTO → PTS PÓS → APRENDIZADO → ELO`

O conhecimento especializado retorna para a memória do simbionte.

---

## 13. Contrato mínimo de execução

Quando uma skill participar do loop, deve conseguir informar:

```text
ENTRADA
FONTE
CONTEXTO
REGRA/SKILL
VERSÃO
ANÁLISE
DECISÃO
IMPACTO
EXECUÇÃO
RESULTADO
EVIDÊNCIA
STATUS DE VALIDAÇÃO
APRENDIZADO
```

Campos não disponíveis devem permanecer como **NÃO LOCALIZADO**, quando essa classificação for aplicável.

---

## 14. Critério de fechamento de ciclo

Um ciclo é considerado fechado quando existe:

1. demanda ou evento identificado;
2. fonte utilizada registrada;
3. análise realizada;
4. decisão ou conclusão registrada;
5. resultado disponível ou explicitamente marcado como não disponível;
6. aprendizado identificado quando houver evidência;
7. status de validação definido;
8. persistência realizada na camada apropriada.

Sem esses elementos, o ciclo deve ser tratado como **INCOMPLETO**, e não como aprendizado consolidado.

---

## 15. Primeiro ciclo de validação

A V0.1 deve ser validada inicialmente sobre a cadeia de Planejamento Multiteiner:

`DEMANDA → FLUXO → ETAPAS → DEPENDÊNCIAS → CAPACIDADE → ESTOQUE → PARALELISMO → SINCRONIZAÇÃO → PROGRAMAÇÃO → EXECUÇÃO → RECUPERAÇÃO → QUALIDADE → EXPEDIÇÃO → APRENDIZADO`

Para cada ponto, verificar:

- fonte existente;
- dado disponível;
- regra existente;
- cálculo necessário;
- resultado esperado;
- evidência;
- estado de validação.

A skill `SKILL_PLANEJAMENTO_MULTITEINER.md` permanece a camada especializada; este documento define o loop transversal.

---

## 16. Governança de evolução

Toda alteração do loop deve seguir:

`DIAGNÓSTICO → EVIDÊNCIA → ANÁLISE → CORREÇÃO → TESTE → VALIDAÇÃO → EVOLUTION GATE → MERGE → APRENDIZADO`

O merge não representa apenas publicação de código. Representa a promoção de uma alteração de engenharia após validação.

O aprendizado persistente deve registrar a versão que originou a decisão.

---

## 17. Estado V0.1

Esta arquitetura é **proposta inicial para validação**.

Não declara que o loop já esteja operacional ponta a ponta.

### Confirmado nesta etapa

- existência da skill de Planejamento Multiteiner em desenvolvimento;
- integração conceitual ELO ↔ Supabase ↔ GitHub;
- separação entre memória persistente e engenharia versionada;
- cadeia de promoção de conhecimento;
- necessidade de comparar planejado × realizado;
- regra de preservação de evidência e proveniência.

### Ainda a validar

- mecanismo técnico de execução automática do loop;
- persistência completa da decisão com versão da skill;
- ligação operacional entre resultado real e aprendizado;
- testes automatizados do ciclo;
- promoção automática ou assistida de aprendizados;
- tratamento técnico de divergências entre versões.

---

## 18. Regra central

> **O ELO deve aprender com a execução, mas somente transformar execução em conhecimento operacional após evidência e validação.**

O loop simbionte não termina na resposta.

Ele termina quando o resultado pode voltar ao sistema como conhecimento rastreável — ou quando fica explicitamente registrado por que ainda não pode fazê-lo.
