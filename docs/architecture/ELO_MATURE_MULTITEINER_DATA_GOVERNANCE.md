# ELO MATURE — GOVERNANÇA DE DADOS MULTITEINER PARA PCP

## 1. Objetivo

Este documento estabelece a relação entre **setores, fluxo operacional, tabelas PCP/Multiteiner, dados necessários, impactos e perguntas obrigatórias quando uma informação ausente impede atingir uma meta ou responder uma pergunta de negócio**.

A cadeia corporativa de referência é:

DEMANDA → CAPACIDADE → ATENDIMENTO → EXECUÇÃO → ENTREGA → ATIVO → RESULTADO → APRENDIZADO

A camada PCP detalha principalmente:

PLANO → ORDEM DE PRODUÇÃO → OPERAÇÕES / MATERIAIS / CAPACIDADE → ESTOQUE → EVENTOS REAIS → PLANEJADO × REALIZADO → DIAGNÓSTICO → EVIDÊNCIA → SYMBIONT

## 2. Princípio de governança

As tabelas armazenam **fatos operacionais**. O PCP calcula indicadores e confrontações. O diagnóstico não pode inventar causas. Quando a evidência necessária não existir, o ELO deve:

1. identificar o alvo;
2. identificar o dado ausente;
3. localizar a tabela/setor responsável;
4. formular a pergunta mínima necessária;
5. bloquear a conclusão dependente desse dado;
6. registrar a lacuna;
7. reavaliar após a resposta.

**Ausência de dado não é autorização para inferência.**

## 3. Setores e responsabilidades

| Setor/camada | Responsabilidade | Dados primários |
|---|---|---|
| Comercial | Demanda e compromisso de atendimento | demanda, prazo, modelo/família, quantidade, prioridade |
| PCP | Planejamento e sincronização | plano, OP, horizonte, quantidades e datas |
| Engenharia/Produto | Definição técnica | modelo, BOM/lista-mãe, versão, roteiro/operações |
| Produção | Execução | quantidades concluídas, operações, início/fim, status |
| Planejamento de capacidade | Disponibilidade dos centros | capacidade padrão, recuperação, bloqueios, disponível |
| Compras/Suprimentos | Atendimento de materiais | necessidade, comprado, prazo, status |
| Almoxarifado/Estoque | Existência física | lote, quantidade disponível, reservada, localização |
| Qualidade | Liberação e retrabalho | inspeção, aprovação, retrabalho, evidência |
| Logística/Expedição | Disponibilização e entrega | liberação, programação, expedição, entrega |
| Manutenção/Reparo | Recuperação de ativos | entrada, reparo, liberação, avaria |
| ELO/PCP analítico | Confrontar e diagnosticar | gaps, cobertura, utilização, gargalos, atrasos |
| Symbiont | Observar evidência e governar evolução | observação, experimento, resultado, Evolution Gate |

A tabela descreve responsabilidades de fluxo e não cria novas autoridades arquiteturais.

## 4. Tabelas PCP e impactos

### 4.1 mt_planos_pcp

**Função:** representar o plano PCP e seu horizonte.

Campos atuais:

- id
- tenant_id
- codigo_plano
- versao
- status
- horizonte_inicio
- horizonte_fim
- aprovado_em
- aprovado_por

**Setor primário:** PCP.

**Impactos:**

- define o horizonte contra o qual as OPs são avaliadas;
- identifica a versão vigente do planejamento;
- sustenta comparação temporal;
- sem horizonte válido, análises por período ficam incompletas.

**Perguntas quando ausente:**

- Qual plano PCP está vigente?
- Qual versão deve ser considerada?
- Qual é o horizonte inicial e final?
- O plano foi aprovado? Quando e por quem?

### 4.2 mt_ordens_producao

**Função:** representar o que deve ser produzido e o que efetivamente foi produzido.

Campos atuais:

- id
- tenant_id
- numero_ordem
- linha_plano_pcp_id
- modelo_id
- bom_versao_id
- quantidade_planejada
- quantidade_produzida
- status
- inicio_planejado
- fim_planejado
- inicio_real
- fim_real

**Setor primário:** PCP + Produção.

**Impactos:**

- conecta plano, produto e execução;
- permite quantidade planejada × produzida;
- permite datas planejadas × reais;
- é fonte central para medir atendimento da produção.

**Perguntas:**

- Qual OP atende essa demanda?
- Qual modelo está sendo produzido?
- Qual versão da BOM foi utilizada?
- Quantas unidades foram planejadas?
- Quantas foram efetivamente produzidas?
- Qual era o prazo?
- Qual foi a data real de conclusão?
- Qual o status atual?

### 4.3 mt_operacoes_ordem_producao

**Função:** detalhar a execução por operação e sequência.

Campos atuais:

- id
- ordem_producao_id
- operacao_roteiro_id
- sequencia
- quantidade_planejada
- quantidade_concluida
- status
- inicio_planejado
- fim_planejado
- inicio_real
- fim_real

**Setor primário:** Produção.

**Impactos:**

- localiza em qual etapa ocorreu a divergência;
- suporta duração planejada × real;
- permite identificar operação incompleta;
- conecta OP ao processo produtivo.

**Perguntas:**

- Qual operação está incompleta?
- Qual a sequência correta?
- Qual quantidade deveria ter sido concluída?
- Qual quantidade foi concluída?
- Quando deveria terminar?
- Quando terminou?
- Existe evidência explícita do motivo da parada?

### 4.4 mt_capacidade_diaria

**Função:** representar a capacidade diária disponível por centro de trabalho.

Campos atuais:

- id
- centro_trabalho_id
- data_capacidade
- quantidade_padrao
- quantidade_recuperacao
- quantidade_bloqueada
- quantidade_disponivel

**Setor primário:** PCP/Capacidade.

**Impactos:**

- permite confrontar carga com capacidade;
- suporta identificação de saturação;
- sustenta análise de gargalo;
- mantém recuperação e bloqueio separados.

**Perguntas:**

- Qual centro de trabalho atende a operação?
- Qual capacidade padrão existia na data?
- Houve recuperação?
- Quanto foi bloqueado?
- Qual capacidade efetivamente disponível?
- A capacidade corresponde ao calendário operacional vigente?

### 4.5 mt_necessidades_materiais

**Função:** representar a necessidade de material vinculada à OP.

Campos atuais:

- id
- ordem_producao_id
- lista_mae_id
- quantidade_bruta
- quantidade_alocada
- quantidade_comprada
- data_necessidade
- status

**Setor primário:** PCP + Suprimentos.

**Impactos:**

- dimensiona necessidade bruta;
- separa alocação de compra;
- permite avaliar atendimento na data;
- não se deve somar alocado + comprado como se fossem o mesmo estoque realizado.

**Perguntas:**

- Qual material é requerido?
- Qual a quantidade bruta?
- Quanto já foi alocado?
- Quanto foi comprado?
- Qual a data de necessidade?
- Qual o status?
- Existe pedido de compra associado?

### 4.6 mt_lotes_estoque

**Função:** representar estoque físico por lote/série/local.

Campos atuais:

- id
- tenant_id
- lista_mae_id
- codigo_lote
- codigo_serie
- local_id
- quantidade_disponivel
- quantidade_reservada
- status
- recebido_em
- ordem_compra_item_id

**Setor primário:** Almoxarifado/Estoque.

**Impactos:**

- fornece disponibilidade física;
- diferencia disponível de reservado;
- permite confrontar necessidade × estoque;
- suporta cobertura e déficit material.

**Perguntas:**

- Qual lote atende a necessidade?
- Quanto está fisicamente disponível?
- Quanto está reservado?
- Onde está armazenado?
- O lote está liberado?
- Existe vínculo com compra?
- O saldo foi fisicamente conferido?

### 4.7 mt_eventos_fluxo_modular

**Função:** registrar o que efetivamente aconteceu no fluxo modular.

Campos atuais:

- id
- unidade_modular_id
- centro_trabalho_id
- nome_operacao
- tipo_evento
- inicio
- fim
- quantidade
- status
- operador_id
- observacoes

**Setor primário:** Produção/Operação.

**Impactos:**

- constitui evidência temporal da execução;
- permite reconstruir o fluxo real;
- permite comparar eventos com planejamento;
- observações são evidência contextual, não causa automática.

**Perguntas:**

- Qual unidade foi processada?
- Em qual centro?
- Qual operação ocorreu?
- Qual evento foi registrado?
- Quando começou?
- Quando terminou?
- Qual quantidade foi processada?
- Qual o status?
- Existe observação ou evidência da ocorrência?

## 5. Relações

PLANO PCP
↓
ORDENS DE PRODUÇÃO
├── OPERAÇÕES
├── NECESSIDADES DE MATERIAIS → ESTOQUE
└── CAPACIDADE
↓
EVENTOS REAIS
↓
PLANEJADO × REALIZADO
↓
DIAGNÓSTICO
↓
EVIDÊNCIA
↓
SYMBIONT

As relações devem ser validadas pelos identificadores reais existentes. O fluxo conceitual não autoriza criar chaves inexistentes.

## 6. Impacto entre setores

### Comercial → PCP

Pergunta: **Temos capacidade para atender a demanda no prazo?**

Dados mínimos: demanda, produto/família, quantidade, prazo, capacidade, estoque, produção prevista, reparo previsto quando aplicável e compromissos/reservas.

### PCP → Produção

Pergunta: **O plano pode ser executado?**

Dados: OP, quantidade, sequência, datas, capacidade, roteiro e materiais.

### PCP/Produção → Suprimentos

Pergunta: **O material estará disponível quando a produção precisar?**

Dados: necessidade bruta, alocação, compra, data de necessidade, estoque e prazo/status de compra quando existente.

### Produção → Qualidade

Pergunta: **O produzido foi aprovado sem retorno?**

Dados: quantidade processada, aprovada, reprovação, retrabalho e evidência de inspeção.

### Produção → Logística

Pergunta: **O liberado está disponível para expedição/entrega?**

Dados: quantidade liberada, data de liberação, programação, data real e status.

### Operação → ELO

Pergunta: **O que está diferente do plano e qual evidência explica a diferença?**

Dados: planejado, realizado, timestamps, status, capacidade, material, eventos e evidências de causa.

## 7. Metas e indicadores

A arquitetura Multiteiner já registrada estabelece indicadores e perguntas sobre:

- capacidade de atendimento comercial;
- gap de capacidade;
- produção e recuperação;
- disponibilidade comercial;
- utilização e tempo parado de ativos;
- lead time de recuperação;
- atendimento por fabricação;
- gargalo;
- espera;
- retrabalho;
- FPY;
- prontidão para expedição;
- OTD;
- avarias;
- custo de recuperação;
- compras e OTIF;
- acuracidade de estoque;
- engenharia;
- excedentes;
- complexidade;
- G2;
- perdas;
- aprendizado e reutilização;
- previsão e MAPE.

Indicadores são **dados derivados**. Não devem ser tratados como fatos primários.

## 8. Motor de perguntas por ausência de dados

Arquivo:

src/elo/cognitive/pcp_data_questions.py

Responsabilidade:

META/ALVO → DADOS NECESSÁRIOS → DADOS DISPONÍVEIS → GAPS → PERGUNTAS MÍNIMAS → SETOR RESPONSÁVEL → NOVA ANÁLISE

Regra:

- se todos os requisitos existem: permitir análise;
- se faltar requisito: bloquear conclusão dependente;
- projetar perguntas;
- indicar tabela/setor;
- indicar impacto;
- não estimar;
- não criar valor padrão;
- não transformar hipótese em fato.

### Exemplo

Objetivo: determinar se uma OP ficará atrasada.

Se fim_real estiver ausente:

> Qual a previsão operacional de conclusão da OP e qual evidência sustenta essa previsão?

Se capacidade estiver ausente:

> Qual a capacidade disponível do centro de trabalho na janela restante da OP?

Se estoque do material estiver ausente:

> Qual quantidade fisicamente disponível comprova o saldo do material requerido?

Se houver diferença planejado × produzido sem ocorrência:

> Qual registro operacional explica a diferença entre a quantidade planejada e a quantidade produzida?

## 9. Estados

| Estado | Significado |
|---|---|
| DADOS_SUFICIENTES | Requisitos presentes para a análise |
| DADOS_INCOMPLETOS | Falta pelo menos um requisito |
| CAUSA_NAO_LOCALIZADA | Há desvio, mas não há evidência de causa |
| DIVERGENCIA_DE_FONTES | Fontes apresentam valores diferentes |
| ANALISE_BLOQUEADA | Objetivo não pode ser respondido sem novo dado |
| DIAGNOSTICO_CONFRONTADO | Há dados suficientes para confrontação |
| EVIDENCIA_VALIDADA | Evidência necessária foi explicitamente validada |

## 10. Pergunta obrigatória por lacuna

Toda ausência deve responder:

1. Qual meta está bloqueada?
2. Qual cálculo não pode ser executado?
3. Qual decisão fica comprometida?
4. Qual tabela deveria fornecer o dado?
5. Qual setor deve responder?
6. Qual pergunta mínima deve ser feita?
7. Qual evidência será aceita?

Assim, a ausência vira **ação operacional rastreável**, não inferência.

## 11. Governança ELO

O fluxo permanece:

ATIVAR → RETRIEVE → EVIDENCIAR → CONFRONTAR → EXECUTAR → OBSERVAR → VALIDAR → GATE → REGISTRAR → EVOLUIR

PCP permanece independente. Symbiont recebe evidência pelo contrato canônico.

Não criar:

- segundo motor de aprendizado;
- segundo Evolution Gate;
- segunda memória;
- segundo DecisionLifecycle;
- segundo roteador;
- autoridade paralela de diagnóstico.

## 12. Estado atual dos dados

Na verificação do Supabase, o schema atual das sete tabelas foi confirmado.

O estado operacional anteriormente verificado estava sem registros:

- mt_planos_pcp: 0
- mt_ordens_producao: 0
- mt_operacoes_ordem_producao: 0
- mt_capacidade_diaria: 0
- mt_necessidades_materiais: 0
- mt_lotes_estoque: 0
- mt_eventos_fluxo_modular: 0

Portanto, não devem ser criados registros fictícios para simular operação real.

## 13. Critério de maturidade

O ELO estará operacionalmente maduro para esse fluxo quando puder receber uma meta, percorrer todas as fontes necessárias e, em qualquer ponto sem evidência, gerar automaticamente:

- dado ausente;
- tabela;
- setor responsável;
- impacto;
- pergunta;
- evidência esperada;
- estado de bloqueio.

**Princípio central: dado ausente gera pergunta; nunca gera inferência.**

## 14. Referências

- docs/MULTITEINER_KPIs_MASTER.md
- SKILL_PLANEJAMENTO_MULTITEINER
- contratos PCP de planejado × realizado
- pacote de evidência operacional PCP
- ponte PCP → Symbiont
- DecisionLifecycle canônico
- Evolution Gate canônico

**Classificação:** ELO MATURE / Arquitetura de dados e decisão  
**Domínio:** Multiteiner / PCP  
**Status:** proposta documentada para implementação controlada.
