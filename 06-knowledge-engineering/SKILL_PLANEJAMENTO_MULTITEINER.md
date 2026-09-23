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

Localizar somente o segmento do fluxo produtivo necessário para a meta atual antes de montar uma programação. O ELO não deve percorrer todo o fluxo Multiteiner quando a meta puder ser respondida por um subfluxo comprovado.

A seleção do caminho deve considerar a meta, os dados disponíveis e as dependências comprovadas. Ausência de dados não autoriza inventar o caminho.

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

### PM-16 — Avaliar suficiência orientada à meta

A Skill não exige banco de dados completo para responder. Exige dados suficientes para o objetivo analisado.

Classificar cada requisito como:

- **ESSENCIAL** — necessário para concluir o objetivo ou um subobjetivo definido;
- **CONDICIONAL** — necessário somente se a análise avançar para determinado subfluxo;
- **COMPLEMENTAR** — aprofunda a resposta, mas sua ausência não impede o cálculo ou conclusão já sustentados.

Estados obrigatórios:

- `DADOS_SUFICIENTES` — dados suficientes para a meta;
- `RESPOSTA_PARCIAL` — parte da meta pode ser respondida e outra parte permanece bloqueada;
- `ANALISE_BLOQUEADA` — falta evidência essencial para qualquer resposta útil daquela meta;
- `DADOS_NAO_LOCALIZADOS` — nenhuma evidência relevante foi localizada;
- `DIVERGENCIA_DE_FONTES` — fontes relevantes apresentam valores conflitantes;
- `CAUSA_NAO_LOCALIZADA` — o desvio é calculável, mas a causa não possui evidência causal explícita;
- `EVIDENCIA_VALIDADA` — resultado validado segundo o gate canônico.

Regra central:

> **dados ausentes não bloqueiam por si só; bloqueia somente a ausência da evidência necessária ao próximo resultado pretendido.**

### PM-17 — Delimitar o caminho analítico

A sequência operacional deve ser orientada pela meta:

`META → ESCOPO → DADOS LOCALIZADOS → DADOS AUSENTES → SUFICIÊNCIA → CÁLCULOS → CONFRONTAÇÃO → CONCLUSÃO → LIMITAÇÕES → PRÓXIMA EVIDÊNCIA`

O caminho pode parar quando a meta já estiver sustentada. Só deve expandir para capacidade, materiais, qualidade, execução, campo ou aprendizado quando a pergunta exigir essas dimensões.

Sem evidência causal, a Skill pode calcular o desvio, mas não deve declarar sua causa.

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


## 22. Integração com o Loop Simbionte — fronteira PCP → evidência

A Skill PCP permanece independente do Symbiont.

A separação obrigatória é:

`PCP / Comercial / Engenharia → EVIDÊNCIA → SYMBIONT → aprender/adaptar → EVOLUTION GATE`

O PCP calcula e analisa seus próprios resultados sem importar, chamar ou persistir diretamente em mecanismos do Symbiont.

### 22.1 Owners

| Responsabilidade | Owner |
|---|---|
| análise, fórmulas e diagnóstico PCP | `SKILL_PLANEJAMENTO_MULTITEINER` + mecanismos PCP existentes |
| dados operacionais e conhecimento persistente | Supabase |
| transformação de resultado em evidência | `pcp_evidence_bridge.py` |
| handoff governado | `DecisionLifecycle → SymbiontSkillRuntime` |
| observação/confrontação | `SymbiontLabAdapter` |
| aprender/adaptar | mecanismos canônicos do Symbiont |
| decisão de evolução | `EvolutionGate` |

### 22.2 Regra de independência

O módulo analítico PCP deve continuar executável sem Symbiont.

O Symbiont não deve conhecer detalhes das fórmulas PCP para funcionar.

O domínio entrega somente uma evidência estruturada na fronteira:

`resultado PCP → evidência`

A ponte `pcp_evidence_bridge.py` é um adapter de tradução, não um novo motor de aprendizado.

### 22.3 Fluxo canônico

```
                     ELO
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
      PCP         Comercial      Engenharia
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                   EVIDÊNCIA
                      │
                      ▼
                  SYMBIONT
                      │
               ┌──────┴──────┐
               ▼             ▼
            aprender       adaptar
               │             │
               └──────┬──────┘
                      ▼
                EVOLUTION GATE
```

O fluxo preserva a autonomia dos domínios e concentra no Symbiont apenas a governança da evidência, aprendizagem/adaptação e evolução.

### 22.4 Regra contra duplicação

`MECANISMO EXISTENTE → REUSAR`

`CONHECIMENTO PCP EXCLUSIVO → EXECUTAR NO KERNEL PCP`

`RESULTADO DO DOMÍNIO → TRANSFORMAR EM EVIDÊNCIA`

`EVIDÊNCIA → HANDOFF CANÔNICO`

`CONFLITO → EVOLUTION GATE`

Não criar:
- novo Lifecycle;
- novo Adapter de aprendizagem;
- nova memória;
- novo Router;
- novo Evolution Gate;
- nova autoridade para decisão já pertencente a outro mecanismo.

### 22.5 Evidência não é aprendizado

A produção de evidência não promove conhecimento.

A ponte deve somente transportar:
- resultado;
- fonte;
- versão;
- evidências;
- baseline;
- experimento;
- resultado observado;
- regressão;
- generalização;
- risco;
- owner existente.

A promoção continua dependente da governança canônica.

### 22.6 Regra de independência testável

O teste arquitetural deve confirmar que:
1. `pcp_symbiont_integration.py` não importa `DecisionLifecycle`, `SymbiontSkillRuntime` ou `SymbiontLabObservation`;
2. as fórmulas PCP podem ser executadas sem o runtime Symbiont;
3. o bridge pode encaminhar a evidência ao handoff canônico;
4. o Evolution Gate continua sendo o owner da decisão de evolução.

## 23. Fluxo de implementação da Skill com o Loop Simbionte

A implementação da Skill deve ser executada em ciclos controlados, sem transformar a própria Skill em autoridade de aprendizagem.

### 23.1 Ordem obrigatória

`ATIVAR → RETRIEVE → EVIDENCIAR → CONFRONTAR → EXECUTAR → OBSERVAR → VALIDAR → GATE → REGISTRAR → EVOLUIR`

### 23.2 Gate 1 — ATIVAR

Identificar:
- Skill: `SKILL_PLANEJAMENTO_MULTITEINER`;
- versão/commit vigente;
- domínio: PCP / Produção Modular;
- objetivo do ciclo;
- identificador da demanda ou cenário.

Nenhuma fórmula ou regra nova é promovida nesta etapa.

### 23.3 Gate 2 — RETRIEVE

Consultar obrigatoriamente:

1. GitHub — Skill, código e testes vigentes;
2. Supabase — dados operacionais e conhecimento persistente;
3. mecanismos ELO existentes que respondam à mesma pergunta.

Para o ciclo PCP, o ponto de partida atual é `v_elo_pcp_inteligente`.

### 23.4 Gate 3 — EVIDENCIAR

Classificar cada informação como:

`DADO | FONTE VISUAL | APRENDIZADO VALIDADO | INFERÊNCIA CONTROLADA | NÃO LOCALIZADO`

Campos ausentes permanecem `NÃO LOCALIZADO`. Não preencher lacunas por plausibilidade.

### 23.5 Gate 4 — CONFRONTAR

Para cada decisão, identificar se já existe mecanismo equivalente.

Regra:

`MECANISMO EXISTENTE → REUSAR`

`CONHECIMENTO PCP EXCLUSIVO → EXECUTAR`

`SOBREPOSIÇÃO → CONFRONTAR RESULTADOS`

`DIVERGÊNCIA → REGISTRAR E BLOQUEAR PROMOÇÃO`

### 23.6 Gate 5 — EXECUTAR

Aplicar o kernel PCP somente quando as variáveis necessárias estiverem disponíveis e executar o diagnóstico existente quando houver cenário compatível.

A execução deve preservar:
- entradas;
- unidade/período;
- fonte;
- fórmula;
- versão da Skill;
- resultado.

### 23.7 Gate 6 — OBSERVAR

Comparar resultado esperado × resultado observado.

Quando não houver execução real, registrar `NÃO LOCALIZADO` para o realizado. Cenário simulado deve permanecer identificado como cenário controlado.

### 23.8 Gate 7 — VALIDAR

Encaminhar evidência elegível pelo adapter de domínio `pcp_evidence_bridge.py` ao mecanismo canônico do Simbionte:

`pcp_evidence_bridge → DecisionLifecycle → SymbiontSkillRuntime → SymbiontLabAdapter`

O Simbionte verifica proveniência, evidência, regressão, generalização, risco e proprietário existente.

### 23.9 Gate 8 — EVOLUTION GATE

A classificação deve determinar a disposição da evidência:

- reutilizar capacidade existente;
- fortalecer/adaptar capacidade existente;
- manter candidato governado;
- bloquear por conflito/incompatibilidade.

A Skill não executa promoção por conta própria.

### 23.10 Gate 9 — REGISTRAR

Persistir somente no mecanismo canônico correspondente:

- experiência → `elo_aprendizado_experiencias`;
- conceito → `elo_aprendizado_conceitos`;
- padrão → `elo_aprendizado_padroes_raciocinio`;
- PCP → `elo_aprendizado_pcp_planejamento`;
- relação → `elo_aprendizado_relacoes`.

### 23.11 Gate 10 — EVOLUIR

Somente após validação suficiente:

`CANDIDATO → TESTADO → VALIDADO → CONSOLIDADO`

A evolução deve reutilizar o proprietário existente. Não criar uma segunda autoridade para uma capacidade que já existe.

### 23.12 Primeiro ciclo iniciado

O primeiro ciclo controlado foi iniciado com o cenário atualmente disponível no Supabase.

Evidências recuperadas:
- existem demandas simuladas abertas;
- existe o fluxo produtivo modular de referência;
- o fluxo possui etapas estruturadas;
- o próprio registro do fluxo informa que tempos, capacidades e recursos específicos devem ser preenchidos somente com evidência operacional validada.

Consequentemente, nesta primeira passagem:
- fluxo e etapas podem ser analisados;
- capacidade quantitativa não deve ser inventada;
- gargalo não deve ser declarado sem carga/capacidade suficiente;
- planejado × realizado não deve ser calculado sem execução real;
- o conhecimento permanece candidato.

**Estado do ciclo:** `RETRIEVE/EVIDÊNCIA concluídos → CONFRONTAÇÃO iniciada → EXECUÇÃO controlada pendente de cenário quantitativo`.


## 24. Capacidades desenvolvidas sem depender de dados operacionais

Para permitir que a alimentação futura do PCP complete o sistema sem exigir novo desenho estrutural, foram adicionadas utilidades determinísticas em `src/elo/cognitive/pcp_control.py`.

### 24.1 Planejado × realizado

O módulo compara, sem inferência:

- quantidade planejada × realizada;
- tempo planejado × realizado;
- data planejada × realizada.

Quando o realizado não existir, o resultado permanece `NAO_LOCALIZADO`.

Isso permite alimentar posteriormente as tabelas canônicas:

- `mt_planos_pcp`;
- `mt_linhas_plano_pcp`;
- `mt_ordens_producao`;
- `mt_operacoes_ordem_producao`;
- `mt_eventos_fluxo_modular`.

### 24.2 Suficiência de dados orientada à meta

A função `evaluate_goal()` em `pcp_data_questions.py` avalia se os dados localizados são suficientes para o objetivo, sem exigir que todas as fontes operacionais estejam preenchidas.

A avaliação separa:

- requisitos essenciais;
- requisitos condicionais;
- requisitos complementares;
- grupos mínimos de evidência;
- lacunas bloqueantes;
- próxima evidência mínima.

A resposta pode ser total ou parcial. A ausência de uma fonte complementar não transforma automaticamente o cenário em `ANALISE_BLOQUEADA`.

A regra de governança é:

`DADO AUSENTE ≠ ANÁLISE BLOQUEADA`

Somente a ausência de evidência necessária ao próximo resultado pretendido bloqueia aquele avanço.

O mecanismo não cria dados, não infere valores e não persiste decisões.

### 24.3 Pacote de evidência PCP

`build_pcp_evidence()` padroniza:

`proveniência + evidências + baseline + experimento + esperado + observado + resultado + regressão + generalização + risco + owner + métricas`.

Não persiste, não aprende e não promove.

### 24.4 Evolution Gate

`evaluate_pcp_evolution()` não cria um Gate PCP. Ele instancia e utiliza o `EvolutionGate` canônico.

Regra:

`PCP → proposta/evidência → EvolutionGate → classificação`.

A função não executa mutação canônica nem promoção.

### 24.5 Alimentação futura

A próxima alimentação de dados pode ser feita diretamente nas estruturas PCP já existentes. O desenvolvimento de código não precisa aguardar os dados reais para essas capacidades.

Dados reais continuam necessários para comprovar:

- execução automática com dados operacionais;
- planejado × realizado real;
- persistência completa do ciclo;
- generalização;
- evolução validada;
- promoção governada.



## 25. Contrato de resposta orientado à meta

Toda execução da Skill deve organizar a resposta, quando aplicável, em:

1. **META**
2. **ESCOPO**
3. **DADOS LOCALIZADOS**
4. **DADOS AUSENTES**
5. **SUFICIÊNCIA**
6. **CÁLCULOS**
7. **CONFRONTAÇÃO**
8. **CONCLUSÃO**
9. **LIMITAÇÕES**
10. **PRÓXIMA EVIDÊNCIA**

Se uma parte da meta estiver respondível e outra não, entregar a parte sustentada e registrar explicitamente o bloqueio restante. Não substituir lacunas por plausibilidade.

## 26. Monotonicidade e reanálise

Quando nova evidência for incorporada:

- se for compatível, preservar a conclusão anterior e aprofundar a análise;
- se preencher uma lacuna, elevar o nível de resposta;
- se contradizer um dado anterior, registrar a divergência e recalcular;
- se alterar a conclusão, registrar qual evidência provocou a mudança.

O mesmo conjunto de dados, meta e versão da Skill deve produzir o mesmo resultado quantitativo determinístico.
