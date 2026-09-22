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
