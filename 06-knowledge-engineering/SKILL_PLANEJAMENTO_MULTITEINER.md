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

`DEMANDA → FLUXO → ETAPAS → DEPENDÊNCIAS`

A cadeia resumida acima é a âncora mínima para identificar o caminho de planejamento antes de aprofundar capacidade, materiais, estoque, programação, execução, qualidade, exceções, recuperação, expedição e aprendizado.

A cadeia completa é:

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


## 27. Capacidade de RH aplicada à montagem externa

A camada de evidência PCP passa a reconhecer a necessidade de capacidade humana sem criar uma nova autoridade de RH.

A fonte operacional é a equipe planejada da montagem externa:

- `mt_equipe_montagem_externa`;
- `mt_funcoes_montagem`.

A visão `v_elo_pcp_capacidade_rh_montagem` consolida, por data e função:

- colaboradores simultâneos planejados;
- ordens simultâneas;
- código e nome da função.

A leitura cognitiva é:

`DEMANDA/PLANO → ORDEM → EQUIPE → FUNÇÃO → PICO SIMULTÂNEO`

### 27.1 Regra de capacidade

O pico de colaboradores é uma evidência de necessidade de mão de obra planejada, não uma afirmação de capacidade disponível.

A comparação com disponibilidade real de RH somente deve ser calculada quando existir fonte operacional que registre essa disponibilidade na mesma unidade e período.

Portanto:

- `PICO_COLABORADORES` = necessidade planejada observada;
- `CAPACIDADE_RH_DISPONIVEL` = somente quando houver fonte compatível;
- `GAP_RH` = somente quando ambos forem localizados e comparáveis.

Não utilizar `mt_capacidade_diaria` para representar automaticamente capacidade de pessoas, pois sua estrutura registra capacidade quantitativa de centro de trabalho e não estabelece, por si só, equivalência com colaboradores.

### 27.2 Evidência atual

No estado atual do Supabase, as estruturas de montagem externa e PCP consultadas não possuem registros operacionais. Assim, a visão está implementada e validada estruturalmente, mas ainda não há pico real calculável.

O próximo dado operacional necessário para fechar o ciclo é o preenchimento de equipes planejadas com datas, funções e pessoas e, posteriormente, uma fonte compatível de disponibilidade de RH.



## 28. Catálogo de views PCP disponíveis para solicitação

Quando o usuário pedir uma análise, o ELO pode oferecer diretamente as views já implementadas abaixo. O nome deve ser tratado como identificador operacional da consulta.

### 28.1 Views já prontas

| View | Finalidade | Principais informações |
|---|---|---|
| `v_elo_pcp_inteligente` | Visão integrada do PCP | demanda, planejamento e indicadores já consolidados pela estrutura existente |
| `v_elo_pcp_montagem_externa` | Acompanhamento de montagem externa | ordens, clientes, módulos, equipe, horas, aderência e prazo |
| `v_elo_pcp_capacidade_montagem_externa` | Capacidade planejada de equipe | função, período, colaboradores, horas e ordens |
| `v_elo_pcp_indicadores_montagem_externa` | Indicadores consolidados da montagem | ordens, atrasos, módulos, equipe, horas e aderência |
| `v_elo_pcp_montagem_externa_integrada` | PCP + montagem externa | quantidade PCP, planos, módulos, equipe, cobertura e produtividade planejada |
| `v_elo_pcp_capacidade_rh_montagem` | Pico de necessidade de RH | colaboradores simultâneos, ordens simultâneas e função por data |
| `v_elo_pcp_carga_capacidade_periodo` | Carga PCP × capacidade por período | carga teórica, capacidade disponível, folga e utilização quando as unidades forem compatíveis |
| `v_elo_pcp_referencia_demanda_comparavel` | Referência histórica comparável | histórico × previsão por modelo, natureza e chave de comparabilidade, com GAPs explícitos |

### 28.2 Pedidos que o usuário pode fazer

O usuário pode solicitar, por exemplo:

- **“Abra a visão geral do PCP.”**
- **“Mostre a montagem externa.”**
- **“Mostre a capacidade da equipe de montagem.”**
- **“Mostre os indicadores da montagem externa.”**
- **“Cruze PCP com montagem externa.”**
- **“Mostre o pico de necessidade de RH por função.”**
- **“Mostre os pedidos atrasados da montagem externa.”**
- **“Mostre a aderência entre horas planejadas e realizadas.”**
- **“Mostre módulos por colaborador.”**
- **“Mostre a cobertura de módulos pelo PCP.”**
- **“Mostre o desvio de prazo por ordem.”**
- **“Mostre a necessidade de equipe por dia.”**

O ELO deve primeiro consultar a view existente antes de propor uma nova estrutura.

## 29. Sugestões de novas views que podem ser solicitadas

As sugestões abaixo são oportunidades de evolução e **não significam que essas views já existam**.

### PCP e capacidade

1. **Demanda × capacidade por período**
   - demanda planejada;
   - capacidade disponível;
   - diferença;
   - utilização;
   - período.

2. **Gargalos de capacidade**
   - recurso/centro;
   - carga;
   - capacidade;
   - ocupação;
   - excesso de carga.

3. **Carga futura do PCP**
   - ordens abertas;
   - horas planejadas;
   - distribuição por semana/mês;
   - concentração de carga.

### RH

4. **Gap de RH por função**
   - necessidade;
   - disponibilidade;
   - gap;
   - período.

5. **Custo de mão de obra planejada**
   - necessidade de colaboradores;
   - custo diário/mensal disponível;
   - custo estimado;
   - função/cargo.

6. **Produtividade de equipe**
   - horas planejadas;
   - horas realizadas;
   - módulos;
   - horas por módulo;
   - módulos por colaborador.

### Prazo e execução

7. **Atrasos por ordem**
   - prazo planejado;
   - prazo realizado;
   - dias de desvio;
   - status.

8. **Planejado × realizado**
   - quantidade;
   - horas;
   - início;
   - fim;
   - desvio percentual.

9. **Mapa de ordens críticas**
   - atraso;
   - carga;
   - falta de capacidade;
   - dependências;
   - evidências disponíveis.

### Demanda e comercial

10. **Demanda confirmada × previsão**
    - pedido confirmado;
    - previsão;
    - quantidade líquida;
    - horizonte.

11. **Demanda por cliente/localização**
    - cliente;
    - localização;
    - quantidade;
    - modelos;
    - prazo.

12. **Demanda por modelo**
    - modelo;
    - quantidade;
    - pedidos;
    - período.

### Estoque e sincronização

13. **Componentes críticos para montagem**
    - necessidade;
    - estoque;
    - faltante;
    - produção;
    - situação de sincronização.

14. **Estrutura × componentes × montagem**
    - módulos;
    - componentes necessários;
    - disponibilidade;
    - condição para montagem.

### Regra para solicitar novas views

Quando uma view sugerida for solicitada, o ELO deve:

`META → verificar views existentes → verificar tabelas/fontes → identificar sobreposição → definir indicadores → implementar somente se houver justificativa → testar → validar`

Não criar uma view apenas porque um indicador pode ser imaginado. A nova view deve representar uma necessidade analítica real e não duplicar uma autoridade existente.

### 29.1 Pedido atualmente incorporado

O pedido que originou este catálogo fica registrado como requisito funcional:

> **“Incluir uma lista de opções de views que já estão prontas e sugestões de views que podem ser solicitadas, permitindo ao usuário escolher diretamente a próxima análise.”**

Esse catálogo deve ser atualizado sempre que uma nova view for criada e validada.


## 30. Carga PCP × capacidade por período

A view `v_elo_pcp_carga_capacidade_periodo` foi adicionada como evidência analítica para comparar a carga teórica do planejamento com a capacidade diária dos centros de trabalho.

### 30.1 Fonte e cálculo

A view combina:

- `mt_linhas_plano_pcp` — quantidade e intervalo planejado;
- `mt_operacoes_roteiro` — centro de trabalho e tempos padrão/setup;
- `mt_capacidade_diaria` — capacidade padrão, recuperação, bloqueada e disponível;
- `mt_centros_trabalho` — unidade de capacidade e identificação do recurso.

A carga horária é distribuída entre os dias do intervalo planejado da linha. Essa distribuição é uma **carga teórica para análise**, não uma programação finita de operações.

### 30.2 Regra de comparabilidade

A view somente calcula `folga_horas`, `utilizacao_pct` e `excesso_carga` quando a unidade de capacidade do centro está registrada como hora.

Quando a unidade não for compatível com horas:

- a capacidade continua sendo exibida;
- a carga teórica continua sendo exibida;
- não é produzido percentual de utilização;
- não é declarado excesso de carga.

Portanto:

`CARGA × CAPACIDADE` só pode gerar um diagnóstico de utilização quando as unidades forem comparáveis.

### 30.3 Estado atual

No estado atual do Supabase, as estruturas operacionais de PCP, roteiro e capacidade consultadas estão sem registros. A view foi criada e consultada com sucesso, mas ainda não há carga ou capacidade operacional para calcular utilização.

A análise futura deve preservar a distinção:

- **DADO** — carga/capacidade registrada;
- **INFERÊNCIA CONTROLADA** — carga teórica derivada do plano e roteiro;
- **NÃO LOCALIZADO** — comparação impossível quando a unidade não é compatível ou quando faltam dados.

### 30.4 Solicitação

O usuário pode solicitar:

> “Mostre a carga PCP versus capacidade por período.”

A Skill deve consultar primeiro `v_elo_pcp_carga_capacidade_periodo` antes de propor outra estrutura para a mesma análise.


## 31. Gap de disponibilidade de RH por função

A análise de necessidade de RH da montagem externa foi confrontada com as estruturas existentes para verificar se já existe uma autoridade de capacidade/disponibilidade humana.

### 31.1 Evidência localizada

Existem fontes para:

- pessoas: `mt_pessoas`;
- funções de montagem: `mt_funcoes_montagem`;
- equipe planejada por ordem: `mt_equipe_montagem_externa`;
- mão de obra realizada: `mt_mao_obra_montagem_externa`;
- custos de mão de obra: `rh_mao_obra_custos`.

A view `v_elo_pcp_capacidade_rh_montagem` representa a **necessidade planejada/simultânea** por função e data.

### 31.2 Lacuna identificada

Não foi localizada uma fonte canônica que registre, na mesma unidade de análise, a **disponibilidade efetiva de pessoas por função e período**.

Consequentemente, ainda não é sustentado o cálculo:

`GAP_RH = NECESSIDADE_PLANEJADA - DISPONIBILIDADE_RH`

Também não deve ser usado automaticamente:

- `mt_capacidade_diaria` como capacidade de pessoas;
- quantidade total de `mt_pessoas` como disponibilidade diária;
- `rh_mao_obra_custos` como capacidade, pois essa tabela é uma base de custos e não um calendário de disponibilidade.

### 31.3 Próxima evidência mínima

Para fechar o cálculo do gap sem criar autoridade duplicada, é necessário localizar ou formalizar, sob governança do domínio RH, uma fonte que permita determinar:

- pessoa/colaborador disponível;
- função aplicável;
- período de disponibilidade;
- indisponibilidades/bloqueios relevantes;
- unidade de capacidade, quando diferente de pessoa simultânea.

Até essa evidência existir, o estado correto é:

`NECESSIDADE_RH = CALCULÁVEL QUANDO HOUVER EQUIPE PLANEJADA`

`DISPONIBILIDADE_RH = NÃO LOCALIZADA`

`GAP_RH = NÃO CALCULÁVEL`

## 32. GAP de segurança identificado no estado atual

A inspeção do Supabase identificou que `public.lista_mae_alteracoes` estava com RLS desabilitado.

A investigação do repositório encontrou o contrato canônico em `09-governance/contracts/expected_state/supabase_rls.yaml`, que já declara:

- RLS esperado: `true`;
- policies: `[]`;
- criticidade: alta;
- comportamento esperado: fail-closed.

O ADR-0017 também confirma que `lista_mae_alteracoes` é o histórico obrigatório das alterações da Lista-Mãe. O trigger `lista_mae_guard()` grava nesse histórico usando `SECURITY DEFINER`, portanto a proteção da tabela não exige criar uma policy de INSERT para usuários da aplicação.

A remediação aplicada foi somente:

```sql
ALTER TABLE public.lista_mae_alteracoes ENABLE ROW LEVEL SECURITY;
```

Nenhuma policy foi criada. Assim, não foi introduzido um novo caminho de leitura ou escrita para usuários da aplicação.

Após a alteração, a verificação do estado ao vivo confirmou:

- `rls_enabled = true`;
- nenhuma policy em `lista_mae_alteracoes`;
- nenhum registro de teste foi inserido.

A migration correspondente foi registrada em:

`supabase/migrations/20261002190000_enable_rls_lista_mae_alteracoes.sql`

Esse GAP de segurança é independente do cálculo de capacidade de RH e não deve ser misturado à lógica do PCP.



## 33. Demanda de crescimento — referência canônica

Esta skill não replica nem redefine as regras do ciclo de crescimento.

A autoridade é:
1. `06-knowledge-engineering/PCP_INSTRUCOES_GERAIS_GOVERNANCA.md` — governança e gates;
2. `06-knowledge-engineering/PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL.md` — processo de demanda;
3. instruções especializadas subordinadas ao processo;
4. views, funções e triggers do Supabase — implementação;
5. ELO — interpretação e orquestração.

Para qualquer pergunta sobre crescimento, comparabilidade, fator, cobertura, demanda humana ou RH, esta skill deve consultar a cadeia acima e aplicar exatamente o estado/gate retornado.

Esta skill pode fornecer métodos de planejamento, análise de capacidade, sequenciamento, gargalos e execução, mas não pode:
- redefinir a ordem dos gates;
- calcular com dado ausente;
- transformar experiência Multiteiner em regra geral;
- tratar `mt_pessoas` como disponibilidade de RH;
- aplicar crescimento ao quadro atual de RH;
- substituir a regra canônica do PCP.

Quando uma técnica desta skill entrar em conflito com uma regra PCP, a técnica fica subordinada à regra PCP e o conflito deve ser registrado para reconciliação documental.

### Estado operacional atual

O ciclo de crescimento permanece condicionado ao gate de referência histórica comparável. A existência de views de projeção humana ou cockpit decisório representa capacidade implantada, não autorização de execução.

### 33.1 Referências canônicas

- `PCP_INSTRUCOES_GERAIS_GOVERNANCA.md`
- `PCP_DEMANDA_CRESCIMENTO_REFERENCIA_COMPARAVEL.md`
- `PCP_VINCULO_REPARO_UNIDADE_MODULAR.md`
- `PCP_ELO_INTEGRACAO_REPAROS.md`

Demais seções desta skill devem ser interpretadas como aplicação metodológica e evidência contextual, nunca como uma segunda instrução PCP.
