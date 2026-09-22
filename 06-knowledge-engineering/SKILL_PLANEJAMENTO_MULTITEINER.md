# SKILL — PLANEJAMENTO MULTITEINER

**Status:** proposta inicial para validação  
**Domínio:** Planejamento e PCP / Produção Modular  
**Base de conhecimento:** imagens de fluxo fornecidas na solicitação + estruturas existentes no Supabase  
**Fonte operacional estruturada:** Supabase  
**Fluxo de referência identificado no Supabase:** `MLT.PROD.PADRAO`

---

## 1. Finalidade

Desenvolver no ELO a habilidade de **entender planejamento como um sistema integrado**, e não apenas como uma sequência de operações.

A skill deve interpretar a relação entre:

`demanda → modelo → fluxo → etapas → dependências → capacidade → materiais → estoque → programação → execução → qualidade → exceções → recuperação → expedição → aprendizado`

O objetivo é permitir que o ELO reconstrua a lógica de planejamento apresentada nos fluxogramas e a confronte com os dados estruturados do Supabase.

---

## 2. Princípio cognitivo

O ELO deve distinguir:

- **o que acontece** — etapa/processo;
- **onde acontece** — setor/recurso;
- **quando acontece** — período/data;
- **quanto pode ser produzido** — capacidade;
- **o que precisa existir antes** — dependência;
- **o que pode ocorrer em paralelo** — fluxo paralelo;
- **o que desacopla os processos** — estoque/pulmão;
- **o que impede ou limita o fluxo** — restrição/gargalo;
- **o que acontece quando há desvio** — exceção/recuperação;
- **como se confirma a conclusão** — qualidade/liberação;
- **como o conhecimento é convertido em aprendizado** — experiência/conceito/padrão.

A skill não deve inferir uma regra operacional que não esteja sustentada por fonte, dado estruturado ou aprendizado validado.

---

## 3. Visão de planejamento representada pelas imagens

### 3.1 Fluxo integrado

A primeira imagem representa um processo integrado entre:

`Locação/Comercial → Planejamento → Almoxarifado → Compras → Produção → Reparo de módulos → Expedição`

O planejamento deve compreender que esses blocos são interdependentes.

### 3.2 Fluxo físico produtivo

A segunda imagem representa:

`Recebimento de matéria-prima → Corte e dobra → Solda → Preparação → Pintura → Estoque de estruturas → Montagem final → Expedição`

Há também um fluxo paralelo de componentes de fibra:

`Telhas de fibra + Cubas de box sanitário + Componentes complementares`

Esses fluxos devem ser analisados separadamente e depois sincronizados no ponto em que passam a ser necessários para a montagem.

---

## 4. Competências da skill

### PM-01 — Identificar a demanda

Extrair, quando disponível:

- quantidade;
- modelo;
- prazo;
- prioridade;
- pedido/origem;
- requisitos que alterem o fluxo.

Fonte estruturada principal:

- `mt_linhas_plano_pcp`;
- `v_elo_pcp_inteligente`.

### PM-02 — Identificar o fluxo aplicável

Localizar o fluxo produtivo aplicável antes de montar uma programação.

Fonte:

- `fluxo_produtivo_modular`;
- `fluxo_produtivo_modular_etapas`.

O fluxo atualmente identificado como referência é:

`MLT.PROD.PADRAO`

### PM-03 — Decompor o fluxo em etapas

Para cada etapa, reconhecer:

- ordem;
- código;
- nome;
- setor;
- processo;
- recurso;
- tempo de setup;
- tempo unitário;
- capacidade;
- unidade de capacidade;
- dependências;
- materiais;
- critérios de qualidade.

Fonte:

`fluxo_produtivo_modular_etapas`.

### PM-04 — Entender dependências

A pergunta cognitiva obrigatória é:

> O que precisa estar concluído ou disponível para esta etapa começar?

Dependências devem ser tratadas como relações de precedência, disponibilidade ou sincronização.

Não presumir dependência quando a fonte não a registrar.

### PM-05 — Entender capacidade

Relacionar:

`demanda × capacidade × período × recurso`

Fontes:

- `mt_capacidade_diaria`;
- `mt_capacidade_componentes`;
- `mt_regras_capacidade`;
- `fluxo_produtivo_modular_etapas`.

A skill deve distinguir:

- capacidade padrão;
- capacidade de recuperação;
- capacidade bloqueada;
- capacidade disponível.

### PM-06 — Identificar restrições

Pesquisar restrições antes de afirmar que determinada programação é viável.

Fontes:

- `mt_regras_capacidade`;
- `elo_aprendizado_pcp_planejamento.restricoes`;
- `elo_aprendizado_producao_fluxo_modular.gargalos`;
- dados atuais de estoque, operações e capacidade.

### PM-07 — Reconhecer fluxo paralelo

A skill deve identificar operações que podem ocorrer independentemente do fluxo principal quando essa condição estiver documentada.

Nas imagens, a produção de componentes de fibra aparece como fluxo paralelo.

O ELO deve representar:

`Fluxo principal || Fluxo paralelo`

e posteriormente verificar o ponto de sincronização.

### PM-08 — Entender estoque intermediário/pulmão

Estoque não deve ser interpretado somente como saldo.

Deve ser analisado como possível elemento de sincronização entre operações, respeitando a evidência disponível.

Fontes:

- `mt_lotes_estoque`;
- `mt_movimentacoes_estoque`;
- `v_elo_pcp_inteligente`.

### PM-09 — Sincronizar componentes

Antes da montagem, verificar a disponibilidade dos componentes necessários.

Modelo cognitivo:

`estrutura + componentes necessários → montagem`

A skill deve apontar quais componentes estão:

- disponíveis;
- faltantes;
- em produção;
- em estoque;
- bloqueados;
- sem informação suficiente.

### PM-10 — Programar produção

Transformar a demanda em linhas planejadas e, quando aplicável, ordens de produção.

Fontes:

- `mt_planos_pcp`;
- `mt_linhas_plano_pcp`;
- `mt_ordens_producao`;
- `mt_operacoes_ordem_producao`.

### PM-11 — Acompanhar planejado × realizado

Comparar:

- quantidade planejada;
- quantidade produzida/concluída;
- início planejado;
- fim planejado;
- início real;
- fim real;
- status.

Fontes:

- `mt_ordens_producao`;
- `mt_operacoes_ordem_producao`;
- `mt_eventos_fluxo_modular`.

### PM-12 — Reconhecer qualidade como gate

A skill deve reconhecer pontos de decisão de qualidade.

Modelo:

`processo → teste/verificação → OK → liberação`

ou:

`processo → teste/verificação → falha → reparo → retorno`

Os critérios efetivamente utilizados devem vir das fontes disponíveis.

### PM-13 — Entender reparo e recuperação

Quando existir falha ou atraso, investigar a existência de:

- reparo;
- capacidade de recuperação;
- estoque disponível;
- fluxo paralelo;
- reprogramação;
- mudança de sequência.

Não escolher automaticamente uma alternativa sem evidência ou regra validada.

### PM-14 — Entender expedição como etapa do sistema

A conclusão produtiva não equivale automaticamente à entrega.

O fluxo deve distinguir:

`produção concluída → conferência/liberação → expedição`

A existência e os critérios de cada gate devem ser obtidos das fontes.

### PM-15 — Produzir aprendizado

Quando uma experiência for validada, separar:

**Experiência**

`elo_aprendizado_experiencias`

de:

**Conceito**

`elo_aprendizado_conceitos`

de:

**Padrão de raciocínio**

`elo_aprendizado_padroes_raciocinio`

de:

**Conhecimento específico de PCP**

`elo_aprendizado_pcp_planejamento`

de:

**Conhecimento específico de produção modular**

`elo_aprendizado_producao_fluxo_modular`

e conectar esses elementos por:

`elo_aprendizado_relacoes`.

---

## 5. Sequência cognitiva obrigatória

Quando a skill for acionada para analisar um planejamento:

1. **Identificar a demanda.**
2. **Identificar o modelo/produto.**
3. **Localizar o fluxo aplicável.**
4. **Decompor as etapas.**
5. **Identificar dependências.**
6. **Verificar capacidade.**
7. **Verificar restrições.**
8. **Verificar materiais e estoque.**
9. **Identificar operações paralelas.**
10. **Identificar pontos de sincronização.**
11. **Montar/avaliar a sequência planejada.**
12. **Verificar impacto em capacidade e prazo.**
13. **Acompanhar execução quando houver dados reais.**
14. **Identificar desvios.**
15. **Avaliar alternativas de recuperação documentadas.**
16. **Verificar qualidade/liberação.**
17. **Verificar condição para expedição.**
18. **Registrar aprendizado somente quando houver evidência e validação.**

---

## 6. Mapeamento para o Supabase

| Necessidade cognitiva | Fonte principal |
|---|---|
| Fluxo | `fluxo_produtivo_modular` |
| Etapas | `fluxo_produtivo_modular_etapas` |
| Plano | `mt_planos_pcp` |
| Demanda planejada | `mt_linhas_plano_pcp` |
| Roteiro | `mt_operacoes_roteiro` |
| Ordem de produção | `mt_ordens_producao` |
| Operações da ordem | `mt_operacoes_ordem_producao` |
| Capacidade diária | `mt_capacidade_diaria` |
| Capacidade de componentes | `mt_capacidade_componentes` |
| Regras de capacidade | `mt_regras_capacidade` |
| Estoque | `mt_lotes_estoque` |
| Movimentação | `mt_movimentacoes_estoque` |
| Eventos | `mt_eventos_fluxo_modular` |
| Visão integrada | `v_elo_pcp_inteligente` |
| Aprendizado de planejamento | `elo_aprendizado_pcp_planejamento` |
| Aprendizado de produção | `elo_aprendizado_producao_fluxo_modular` |
| Experiências | `elo_aprendizado_experiencias` |
| Conceitos | `elo_aprendizado_conceitos` |
| Padrões de raciocínio | `elo_aprendizado_padroes_raciocinio` |
| Relações | `elo_aprendizado_relacoes` |

---

## 7. Regra de evidência

A skill deve classificar cada afirmação como:

- **DADO** — existe registro estruturado;
- **FONTE VISUAL** — está representado nas imagens/fluxogramas fornecidos;
- **APRENDIZADO VALIDADO** — existe conhecimento de aprendizado com validação;
- **INFERÊNCIA CONTROLADA** — relação derivada explicitamente de dados existentes;
- **NÃO LOCALIZADO** — a informação necessária não foi encontrada.

Não converter uma inferência em dado.

Não converter uma experiência histórica em regra universal sem validação.

---

## 8. Regra de planejamento

O ELO não deve perguntar apenas:

> “Qual é a próxima operação?”

Deve perguntar:

> “Qual é a próxima decisão de planejamento considerando demanda, dependências, capacidade, materiais, estoque, paralelismo, restrições e sincronização?”

Essa é a mudança central de comportamento desta skill.

---

## 9. Estrutura de saída

Quando aplicada a um cenário, a skill deve poder produzir:

### A. Demanda
- quantidade;
- modelo;
- prazo;
- prioridade.

### B. Fluxo
- fluxo identificado;
- etapas;
- sequência;
- operações paralelas.

### C. Capacidade
- capacidade disponível;
- demanda;
- diferença;
- restrições;
- possível gargalo.

### D. Materiais/estoque
- componentes necessários;
- disponibilidade;
- faltas;
- estoque intermediário relevante.

### E. Programação
- sequência;
- datas;
- ordens;
- dependências.

### F. Controle
- planejado × realizado;
- desvios;
- qualidade;
- status.

### G. Recuperação
- desvio identificado;
- alternativas documentadas;
- impacto da alternativa.

### H. Liberação
- condições de qualidade;
- condição de montagem;
- condição de expedição.

### I. Aprendizado
- experiência;
- decisão;
- evidência;
- conceito extraído;
- relação criada;
- condição de aplicabilidade.


---

## Integração ELO ↔ Supabase ↔ GitHub

A arquitetura de planejamento deve separar três responsabilidades:

**ELO**
- executa o raciocínio;
- identifica o que precisa saber;
- consulta conhecimento contextual;
- calcula;
- compara conhecimento histórico com dados atuais;
- registra a decisão e sua evidência.

**Supabase**
- mantém o estado e o conhecimento persistente de PCP;
- armazena demanda, estoque, capacidade, planos, execução e aprendizado estruturado;
- fornece conceitos, experiências e padrões de raciocínio conforme status de validação.

**GitHub**
- mantém a definição versionada da skill;
- documenta regras, contratos, prompts e testes;
- registra mudanças e governança de engenharia;
- não substitui o estado operacional do Supabase.

### Ordem de consulta

`ELO → Supabase (conhecimento/dados relevantes) → GitHub (skill/regra vigente) → dados atuais → cálculo → análise → decisão → validação → registro → aprendizado`

A ordem acima é cognitiva, não uma licença para usar conhecimento histórico contra um dado atual. Para a situação corrente, **dado operacional atual** prevalece; para comportamento da skill, **regra versionada no GitHub** prevalece; para conhecimento estruturado e memória persistente, **Supabase** é a fonte.

### Governança da informação

| Tipo | Fonte |
|---|---|
| Demanda atual | Supabase / dados operacionais |
| Estoque atual | Supabase / movimentos e lotes |
| Capacidade atual | Supabase / capacidade e regras |
| Plano PCP atual | Supabase |
| Execução real | Supabase |
| Fórmula e método analítico da Skill | GitHub + conceito correspondente no Supabase |
| Experiência histórica | Supabase |
| Padrão de raciocínio validado | Supabase + Skill no GitHub |
| Código/teste/contrato | GitHub |
| Decisão executada | Supabase, com referência ao comportamento/versão da Skill |
| Aprendizado novo | Supabase, promovido a regra/skill somente após validação |

### Regra de versionamento cruzado

Toda decisão de planejamento derivada dessa skill deve, quando possível, registrar:
- `skill_id`/nome da skill;
- versão da skill;
- conceito/regra consultado;
- valores de entrada;
- fórmula aplicada;
- resultado;
- impacto;
- fonte dos dados;
- status de validação.

Quando houver alteração do método no GitHub, o aprendizado persistido no Supabase deve continuar identificando a versão anterior para preservar rastreabilidade histórica.

### Regra de promoção

`CANDIDATO → TESTADO → VALIDADO → CONSOLIDADO`

Somente conhecimento marcado como **VALIDADO/CONSOLIDADO** pode ser recuperado como regra operacional automática. Candidatos servem para análise e teste e devem ser identificados como tal.

### Regra de divergência

Se GitHub e Supabase apresentarem versões diferentes da mesma regra:
1. não esconder a divergência;
2. identificar qual versão está vigente;
3. bloquear promoção automática da regra conflitante;
4. registrar a pendência;
5. validar antes de consolidar.

## 12. Motor analítico de demanda e planejamento PCP

O planejamento deve converter dados em decisão por uma cadeia analítica rastreável:

`DEMANDA → CAPACIDADE → CARGA → UTILIZAÇÃO → RESTRIÇÃO → GARGALO → BOM → NECESSIDADE BRUTA → ESTOQUE DISPONÍVEL → NECESSIDADE LÍQUIDA → LEAD TIME → DATA DE NECESSIDADE → DATA DE PEDIDO → DATA DE ENTREGA → RISCO → IMPACTO → DECISÃO → CONTINGÊNCIA`

### 12.1 Fórmulas-base

| Código | Fórmula | Finalidade |
|---|---|---|
| NL | `NL = D - (EA - ES)` | Necessidade líquida considerando estoque de segurança. |
| NM | `NM = NecessidadeProduto × ConsumoUnitário` | Converter demanda de produto em demanda de componente pela BOM. |
| NLM | `NLM = NM - (EM - ESM)` | Necessidade líquida de material. |
| COB | `COB = EstoqueDisponível / ConsumoPorPeríodo` | Transformar estoque físico em cobertura temporal. |
| ICL | `ICL = COB / LeadTime` | Comparar cobertura com tempo de reposição. |
| DP | `DP = DN - LeadTime` | Determinar a data-limite de pedido. |
| DE | `DE = DP + LeadTime` | Projetar a data de entrega. |
| RUP | `RUP = DE > DN` | Detectar risco de chegada após a necessidade. |
| ATR | `ATR = DE - DN` | Medir atraso potencial. |
| CAP | `CAP = TDA / CT` | Estimar capacidade a partir de tempo disponível e ciclo. |
| UTI | `UTI = Demanda / Capacidade` | Medir pressão da demanda sobre o recurso. |
| GARG | `GARG = argmax(Carga_i / Capacidade_i)` | Identificar o recurso mais pressionado. |
| WIP | `ΔWIP = Entrada - Saída` | Identificar acumulação de estoque em processo. |
| SETUP | `TsetupTotal = Σ(Tsetup_j)` | Medir capacidade consumida por trocas/setup. |

### 12.2 Regras de cálculo

1. Não calcular uma fórmula quando faltar uma variável necessária; registrar **NÃO LOCALIZADO**.
2. Registrar sempre os valores de entrada, unidade, período, fonte e resultado.
3. Não tratar exemplo didático como regra universal sem validação operacional.
4. Dados atuais de demanda, estoque, capacidade e prazo comandam a decisão operacional; histórico serve para recuperar padrões de raciocínio e conhecimento validado.
5. Quando `DE > DN`, abrir análise de contingência e impacto na produção.
6. Quando produtos ou rotas possuírem capacidades diferentes, não aplicar uma capacidade média única sem segmentação.
7. O cálculo deve distinguir claramente **dado**, **fonte visual**, **aprendizado validado**, **inferência controlada** e **NÃO LOCALIZADO**.

### 12.3 Modelo de decisão

A decisão de planejamento deve ser explicável como:

`DECISÃO = DADOS DE ENTRADA + FÓRMULA/RELAÇÃO + RESULTADO + IMPACTO + CONDIÇÃO DE APLICAÇÃO`

O objetivo não é apenas produzir um número, mas recuperar **o caminho da escolha**.

### 12.4 Fonte cognitiva no Supabase

O conhecimento-base desta camada foi registrado como **candidato** no domínio `planejamento_pcp`, especialização `planejamento_pcp_planejamento`, nas estruturas:

- `elo_aprendizado_conceitos`;
- `elo_aprendizado_pcp_planejamento`.

A fonte de aprendizagem é composta pelos casos didáticos **GlassVibe** e **Urnas Eternidade**, fornecidos para a construção da Skill. Esse registro não substitui dados operacionais atuais.

### 12.5 Regra de consulta ELO → Supabase → GitHub

A interação entre os três componentes deve obedecer:

`ELO → identificar necessidade de conhecimento → consultar Supabase → confrontar com fonte operacional atual → consultar GitHub para regra/skill/código vigente → analisar → decidir → registrar evidência/resultado → aprender`

**Supabase** é a autoridade cognitiva/persistente para conhecimento estruturado, experiências, conceitos, padrões de raciocínio e dados operacionais de PCP.

**GitHub** é a autoridade de engenharia para skills, regras documentadas, contratos, prompts, código, testes e histórico de mudanças.

**ELO** é a camada cognitiva de execução: faz a pergunta certa, seleciona as fontes relevantes, confronta conhecimento histórico com dados atuais, calcula, explica a decisão e registra o resultado.

Nenhuma das três fontes deve ser tratada como substituta automática das demais.

### 12.6 Fluxo de governança

`DEMANDA → RETRIEVAL SUPABASE → REGRA/SKILL GITHUB → DADOS ATUAIS → CÁLCULO → ANÁLISE → DECISÃO → VALIDAÇÃO → REGISTRO → APRENDIZADO`

Quando houver divergência:

1. dado operacional atual prevalece para a situação corrente;
2. regra/skill vigente no GitHub define o comportamento de engenharia;
3. conhecimento do Supabase orienta o raciocínio histórico e estruturado;
4. a divergência deve ser registrada como evidência/pendência, nunca ocultada.

### 12.7 Estado de validação

Os cálculos acima estão registrados como **CANDIDATO / não consolidado**. A promoção para regra operacional exige validação dos casos, das variáveis disponíveis no Supabase e da aplicação em cenários reais de PCP.

---

## 10. Limites atuais identificados

A estrutura do Supabase já possui o domínio `planejamento_pcp` e as especializações:

- `planejamento_pcp_planejamento`;
- `planejamento_pcp_programacao`.

Também existem as estruturas de conhecimento específicas de PCP e produção modular.

Na consulta realizada, entretanto, não foram encontrados padrões de raciocínio associados diretamente à especialização de planejamento PCP. Portanto, esta skill **não deve declarar que tais padrões já estão consolidados**.

A próxima etapa de engenharia é transformar os elementos das imagens e os registros existentes em padrões de raciocínio validados, mantendo a distinção entre fonte visual, dado operacional e aprendizado.

---

## 11. Estado desta versão

Esta é a **V0.1 — modelo cognitivo inicial**.

Ainda não representa uma regra operacional final.

O próximo ciclo deve validar, um a um:

`demanda → fluxo → etapa → dependência → capacidade → estoque → paralelismo → sincronização → programação → execução → recuperação → qualidade → expedição → aprendizado`

Somente após essa validação a habilidade deverá ser promovida de modelo cognitivo para conhecimento operacional consolidado.
