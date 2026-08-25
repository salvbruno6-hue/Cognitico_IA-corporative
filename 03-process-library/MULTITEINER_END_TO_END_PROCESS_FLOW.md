---
id: ELO-PROC-MULTITEINER-001
name: Multiteiner End-to-End Functional Process Flow
type: reference
layer: process
owner: Multiteiner process knowledge / ELO process context
status: draft
authority: reference
version: 0.2
related:
  - ELO-012
  - MULTITEINER_ORGANIZATIONAL_CONTEXT
  - MULTITEINER_METODOLOGIA_ORCAMENTO_ELO
  - ELO-012_MULTITEINER_FLOW_MODULAR_PROTOCOL
---

# MULTITEINER — FLUXO END-TO-END FUNCIONAL

## 1. Finalidade

Este documento é a referência canônica de processo para o ELO reconstruir, pesquisar e explicar o fluxo operacional da Multiteiner em diferentes níveis de detalhe.

O objetivo não é produzir somente um fluxograma visual. O objetivo é representar um processo funcional, rastreável e pesquisável, no qual cada passagem possa ser entendida por:

- entrada;
- atividade;
- decisão/gate;
- condição de passagem;
- saída;
- setor/interface;
- informação gerada;
- recurso/material;
- dependência;
- exceção;
- retorno/retrabalho;
- evidência necessária;
- ponto de integração com o ELO.

Quando uma regra, responsável, tempo, capacidade, custo, critério ou sistema não estiver formalmente validado, deve permanecer como `A VALIDAR`. O ELO não deve inventar dados para completar o processo.

---

# 2. PRINCÍPIO DE FUNCIONAMENTO

O fluxo deve ser entendido como um ciclo integrado, e não como uma linha que termina na entrega.

```text
DEMANDA
  ↓
COMERCIAL / LOCAÇÃO
  ↓
AF
  ↓
PCP / PLANEJAMENTO
  ↓
PADRÃO × CUSTOMIZADO
  ↓
ORÇAMENTO / ENGENHARIA quando aplicável
  ↓
LM / OS / NECESSIDADES
  ↓
ALMOXARIFADO / COMPRAS
  ↓
PRODUÇÃO
  ↓
QUALIDADE
  ↓
EXPEDIÇÃO
  ↓
CLIENTE / CAMPO / LOCAÇÃO
  ↓
RETORNO
  ↓
QUARENTENA / LIMPEZA / INSPEÇÃO
  ↓
REPAROS quando necessário
  ↓
QUALIDADE
  ↓
ESTOQUE DE SEGURANÇA / DISPONIBILIDADE
  ↓
NOVA DEMANDA
```

O ciclo possui dois grandes fluxos produtivos paralelos:

1. `FLUXO MODULAR` — linha de produção puxada para módulos e componentes padronizados;
2. `FLUXO CUSTOMIZADO` — atendimento com variações, modificações e requisitos específicos.

Ambos compartilham interfaces de PCP, materiais, qualidade e expedição, mas não devem ser confundidos.

---

# 3. MAPA MACRO CANÔNICO

```text
                         ┌──────────────────────┐
                         │ COMERCIAL / LOCAÇÃO  │
                         └──────────┬───────────┘
                                    ↓
                                  AF
                                    ↓
                         ┌──────────────────────┐
                         │ PCP / PLANEJAMENTO   │
                         └──────────┬───────────┘
                                    ↓
                         PADRÃO OU CUSTOMIZADO?
                              ↙             ↘
                           PADRÃO        CUSTOMIZADO
                              ↓               ↓
                       FLUXO MODULAR   ORÇAMENTO / ENG.
                              ↓               ↓
                              └──────┬────────┘
                                     ↓
                                LM / OS / NEC.
                                     ↓
                         ┌──────────────────────┐
                         │ ALMOXARIFADO / CD    │
                         └──────────┬───────────┘
                                    ↓
                          MATERIAL DISPONÍVEL?
                              ↙             ↘
                            SIM              NÃO
                             ↓                ↓
                          PICKING          COMPRAS
                             │                ↓
                             │        RECEBIMENTO / ESTOQUE
                             └────────┬───────┘
                                      ↓
                                  PRODUÇÃO
                              ↙             ↘
                         MODULAR        CUSTOMIZADA
                              ↘             ↙
                               └─────┬─────┘
                                     ↓
                                  QUALIDADE
                               ↙             ↘
                          APROVADO           FALHA
                             ↓                 ↓
                         EXPEDIÇÃO         O.S. REPARO
                             │                 ↓
                             │          QUARENTENA / LIMPEZA
                             │                 ↓
                             │             DIAGNÓSTICO
                             │                 ↓
                             │               OFICINAS
                             │                 ↓
                             │               TESTES
                             │              ↙     ↘
                             │        APROVADO     FALHA
                             │           ↓            ↓
                             │      ESTOQUE SEG.   RETRABALHO
                             │           ↓            │
                             └───────────┴────────────┘
                                         ↓
                                      ENTREGA
                                         ↓
                                  CAMPO / LOCAÇÃO
                                         ↓
                                      RETORNO
                                         ↓
                                  NOVO CICLO
```

---

# 4. OBJETOS DE RASTREABILIDADE

O ELO deve conseguir relacionar, quando os dados existirem:

`AF → módulo → modelo → configuração → LM/OS → material → etapa → equipe → qualidade → expedição → retorno → avaria → reparo → custo → estoque`.

Identificadores relevantes:

- AF;
- ID do módulo/ativo;
- modelo;
- configuração;
- LM/OS;
- ID da avaria;
- código do material;
- ordem/requisição de compra quando existente;
- registro de qualidade;
- registro de reparo.

A existência e o formato exato de cada identificador devem ser validados na implementação.

---

# 5. FLUXO 01 — COMERCIAL / LOCAÇÃO → AF

## Entrada

Necessidade comercial, locação ou venda.

## Sequência

```text
Demanda
→ negociação / definição do atendimento
→ especificação do produto
→ quantidade
→ configuração
→ prazo
→ requisitos especiais
→ AF
→ envio para PCP / planejamento
```

## Gate de completude

Antes de planejar, verificar se a AF contém informação suficiente para análise.

Se incompleta:

`AF → pendência → complementação → nova análise`.

Se completa:

`AF → PCP`.

## Dados de interesse

- cliente;
- modalidade;
- modelo;
- quantidade;
- configuração;
- prazo;
- local;
- requisitos especiais;
- necessidade de customização.

## ELO

Registrar a demanda como origem do planejamento e relacionar com histórico, modelo, configuração e sazonalidade quando houver dados.

---

# 6. FLUXO 02 — PCP / PLANEJAMENTO

## Função

O PCP é a camada operacional de orquestração do fluxo. Na arquitetura ELO, seus dados devem ser conectados aos demais setores para planejamento estratégico, tático e operacional.

## Sequência funcional

```text
Receber AF
→ conferir escopo
→ analisar projeto/configuração
→ identificar modelo
→ verificar padrão/customização
→ identificar excedentes
→ verificar materiais
→ verificar capacidade conhecida
→ verificar dependências
→ verificar prazo
→ definir prioridade
→ definir sequência
→ gerar/liberar LM/OS conforme processo aplicável
→ acompanhar execução
→ tratar desvios
```

## Gate — padrão x customizado

### Padrão

Encaminhar para fluxo modular conforme planejamento e disponibilidade.

### Customizado

Encaminhar para orçamento/engenharia/requisitos adicionais antes da liberação produtiva, conforme aplicabilidade.

## Controle de desvio

O ELO deve comparar:

`planejado × realizado × restrição × impacto × ação`.

Não confundir um plano documentado com a situação operacional atual.

---

# 7. FLUXO 03 — ORÇAMENTO / CUSTOMIZAÇÃO / ENGENHARIA

O orçamento é uma interface estratégica e operacional importante para módulos customizados.

## Quando entra

- modificação solicitada pelo Comercial;
- configuração fora do padrão;
- necessidade de materiais adicionais;
- alteração de componentes;
- customização de montagem;
- necessidade de composição específica.

## Sequência

```text
Solicitação
→ análise do modelo
→ identificar padrão existente
→ identificar alteração
→ identificar materiais
→ identificar mão de obra/serviços aplicáveis
→ composição/orçamento
→ validação
→ requisitos para PCP
→ LM/OS conforme processo
→ execução
```

## Base histórica que deve alimentar o ELO

- módulos mais locados;
- módulos mais vendidos;
- modelos mais modificados;
- materiais mais utilizados;
- tipos de customização recorrentes;
- sazonalidade de customizados;
- materiais utilizados por customização;
- custos históricos;
- frequência de alterações por modelo.

## Regra

Uma customização específica não deve automaticamente alterar o cadastro do modelo padrão. O ELO deve distinguir `MODELO`, `VARIAÇÃO`, `CUSTOMIZAÇÃO` e `EXCEDENTE`.

---

# 8. FLUXO 04 — ALMOXARIFADO / CD / ABASTECIMENTO

## Entrada

Necessidades oriundas do planejamento, produção ou reparo.

## Fluxo logístico

```text
Necessidade
→ verificação
→ recebimento/conferência quando material chega
→ registro no CD/estoque
→ disponibilidade
→ reserva quando aplicável
→ picking
→ entrega ao processo
```

## Gate — material disponível?

### SIM

`Estoque → Picking → Abastecimento`.

### NÃO

```text
Necessidade
→ Compras
→ Ordem de Compra
→ acompanhamento
→ chegada
→ recebimento
→ conferência
→ registro no estoque
→ picking
→ abastecimento
```

## Dados

- código;
- material;
- quantidade;
- unidade;
- disponibilidade;
- reserva;
- consumo;
- requisição;
- origem;
- fornecedor/compra quando disponível;
- lead time quando validado.

## Interface com reparos

O consumo de materiais de reparo deve ser registrado por módulo/modelo/avaria para permitir análise de:

`avaria → material → quantidade → custo → modelo → oficina → resultado`.

---

# 9. FLUXO 05 — PRODUÇÃO MODULAR

O fluxo modular é uma linha de produção puxada paralela ao customizado.

## Sequência de referência

```text
Peças metálicas
→ estrutura metálica
→ preparação/escovação
→ pintura
→ módulo estrutural
→ piso
→ teto
→ PIR/isolamento
→ esquadrias
→ hidráulica
→ elétrica
→ dados
→ acabamentos/complementos
→ testes
→ qualidade
→ liberação
```

Os nomes e a ordem detalhada de operações devem ser confrontados com o roteiro produtivo oficial de cada família de produto.

## Componentes complementares

A análise do fluxo identificou que componentes complementares podem, em determinadas condições, limitar o avanço do conjunto. Entre os itens observados estão:

- telhas;
- lavatórios;
- mictórios;
- cubas;
- boxes;
- divisórias sanitárias.

A existência de gargalo deve ser demonstrada por dados de capacidade, fila, tempo ou disponibilidade; não utilizar percentuais não validados.

---

# 10. FLUXO 06 — PRODUÇÃO CUSTOMIZADA

## Sequência

```text
Necessidade customizada
→ requisitos
→ orçamento/engenharia
→ definição da alteração
→ materiais
→ planejamento
→ preparação
→ execução
→ montagem
→ inspeção
→ testes
→ qualidade
→ expedição
```

## Interface com modular

O ELO deve identificar recursos compartilhados entre os dois fluxos:

- mão de obra;
- oficinas;
- materiais;
- equipamentos;
- movimentação;
- qualidade;
- expedição.

Isso permite analisar conflito de capacidade entre produção modular e customizada.

---

# 11. FLUXO 07 — QUALIDADE NA PRODUÇÃO

## Entrada

Módulo ou conjunto concluído.

## Sequência

```text
Receber para teste
→ verificar critérios
→ executar testes
→ registrar resultado
```

### APROVADO

```text
Qualidade
→ registro/AS-BUILT quando aplicável
→ liberação
→ expedição ou estoque conforme destino
```

### FALHA

```text
Qualidade
→ não conformidade
→ O.S. de reparo/retrabalho
→ intervenção
→ teste
→ nova decisão
```

Toda falha deve permanecer rastreável.

---

# 12. FLUXO 08 — EXPEDIÇÃO

## Sequência

```text
Módulo liberado
→ segregação no pátio
→ identificar necessidade de instalação
→ packing
→ conferência final
→ gate de expedição
→ saída controlada
→ transporte
→ entrega
```

Quando instalação de excedentes no local for aplicável:

`Segregação → instalação → packing/conferência conforme fluxo → gate → saída`.

Quando não for aplicável:

`Segregação → packing → conferência → gate → saída`.

Responsabilidades, documentos e sistemas específicos devem ser validados na documentação operacional.

---

# 13. FLUXO 09 — CAMPO / LOCAÇÃO

```text
Expedição
→ transporte
→ recebimento no local
→ instalação/montagem quando aplicável
→ operação/locação
→ ocorrência ou necessidade de manutenção quando aplicável
→ desmobilização
→ retorno
```

O módulo deve manter vínculo com sua identificação sempre que houver rastreabilidade disponível.

---

# 14. FLUXO 10 — RETORNO

## Entrada

Módulo retornado de locação, campo ou outra origem operacional.

## Sequência

```text
Aviso/solicitação de retorno
→ recebimento
→ entrada no pátio
→ identificação
→ descarregamento
→ vistoria inicial
→ classificação
```

## Gate — condição do módulo

### Sem necessidade de reparo

`liberação → disponibilidade/estoque conforme regra`.

### Necessita avaliação/reparo

`quarentena → limpeza → checklist → diagnóstico`.

### Condição não definida

`quarentena → avaliação técnica`.

O critério exato de cada estado deve ser validado operacionalmente.

---

# 15. FLUXO 11 — REPAROS / RECUPERAÇÃO

Este subprocesso possui duas entradas principais:

1. `falha na qualidade da produção`;
2. `retorno de módulo/ativo da locação/campo`.

Não tratar as duas origens como se fossem o mesmo evento.

## 15.1 Entrada A — falha de produção

```text
Produção
→ qualidade
→ falha
→ O.S. de reparo/retrabalho
→ diagnóstico/intervenção
→ oficina
→ teste
→ qualidade
```

## 15.2 Entrada B — retorno da locação

```text
Retorno
→ quarentena
→ limpeza/higienização
→ identificação
→ checklist de avarias
→ diagnóstico
→ programação do reparo
```

## 15.3 Fluxo comum de reparo

```text
Diagnóstico
→ definir intervenção
→ definir oficina
→ verificar material
→ executar reparo
→ registrar horas/equipe
→ registrar materiais
→ inspeção/teste
```

## Gate — material disponível?

### SIM

`material → oficina → execução`.

### NÃO

`necessidade → almoxarifado/compras → recebimento → material → oficina`.

## Gate — reparo aprovado?

### SIM

`liberação → estoque de segurança/disponibilidade`.

### NÃO

`falha → retrabalho → nova inspeção/teste`.

---

# 16. REPAROS — QUARENTENA

## Objetivo

Impedir que um módulo retornado seja tratado como disponível antes da avaliação.

## Registro mínimo

- ID do módulo;
- AF/origem quando disponível;
- modelo;
- configuração;
- data/hora de entrada;
- localização;
- responsável pelo recebimento;
- condição inicial;
- status.

## Estado

`QUARENTENA` significa indisponibilidade até conclusão da avaliação aplicável.

---

# 17. REPAROS — LIMPEZA / HIGIENIZAÇÃO

## Objetivo

Preparar o módulo para inspeção e intervenção.

## Registro

- módulo;
- data/hora;
- equipe;
- início/fim quando aplicável;
- condição encontrada;
- observações;
- necessidade de nova limpeza quando identificada.

A duração real deve ser obtida por apontamento, não estimada pelo ELO.

---

# 18. REPAROS — CHECKLIST DE AVARIAS

Cada ocorrência deve ser registrada individualmente quando possível.

## Campos

- ID da avaria;
- ID do módulo;
- AF;
- modelo;
- data da inspeção;
- inspetor;
- componente;
- condição;
- tipo de avaria;
- severidade;
- causa provável;
- descrição;
- evidência/foto;
- necessidade de reparo;
- prioridade;
- data do diagnóstico.

## Tipos de análise

- estrutural;
- pintura/acabamento;
- piso;
- teto/cobertura;
- PIR/isolamento;
- esquadrias;
- hidráulica;
- elétrica;
- dados;
- mobiliário/complementos;
- limpeza;
- outros.

---

# 19. REPAROS — DIAGNÓSTICO E DIRECIONAMENTO

```text
Avaria
→ avaliar extensão
→ determinar causa provável
→ definir intervenção
→ determinar oficina
→ verificar materiais
→ definir prioridade
→ liberar execução
```

O direcionamento pode envolver, conforme a ocorrência:

- hidráulica;
- elétrica;
- estrutura;
- pintura;
- marcenaria;
- acabamento;
- outras capacidades validadas.

O conjunto exato de oficinas deve ser mantido como cadastro configurável.

---

# 20. REPAROS — EXECUÇÃO

Cada etapa deve gerar apontamento.

## Dados mínimos

- módulo;
- modelo;
- oficina;
- equipe;
- número de pessoas;
- início;
- fim;
- horas calculadas;
- etapa;
- status;
- retrabalho;
- motivo do retrabalho.

## Estrutura de medição

```text
TEMPO DE CICLO
= fim da etapa - início da etapa
```

A capacidade diária não deve ser assumida. Deve ser calculada posteriormente a partir dos apontamentos reais.

---

# 21. REPAROS — MATERIAIS E CUSTOS

Cada material consumido deve estar relacionado ao módulo/reparo quando houver rastreabilidade.

## Dados

- código;
- material;
- unidade;
- quantidade;
- custo unitário;
- custo total;
- origem;
- requisição;
- responsável;
- ID da avaria quando disponível.

## Relações analíticas

```text
Modelo
  ↓
Avaria
  ↓
Material
  ↓
Quantidade
  ↓
Custo
```

Isso permite ao ELO identificar posteriormente materiais recorrentes por modelo e avarias com maior impacto de consumo.

---

# 22. REPAROS — QUALIDADE E TESTES

```text
Reparo concluído
→ inspeção
→ teste aplicável
→ resultado
```

### Aprovado

`liberação`.

### Aprovado com pendência

`registrar pendência → definir tratamento → liberação somente conforme regra validada`.

### Reprovado

`O.S./retrabalho → oficina → novo teste`.

O teste deve preservar evidência e responsável quando disponíveis.

---

# 23. ESTOQUE DE SEGURANÇA

## Finalidade

Disponibilizar módulos recuperados para atender demanda futura, conforme política definida pela Multiteiner.

## Fluxo

```text
Reparo aprovado
→ liberação
→ classificação do módulo
→ localização
→ entrada no estoque de segurança
→ disponibilidade para PCP
```

## PCP deve enxergar

- quantidade pronta;
- quantidade em reparo;
- quantidade em quarentena;
- quantidade disponível;
- modelo;
- configuração;
- localização;
- idade do estoque quando houver data confiável.

## Regra

Não definir percentual ou quantidade mínima sem base histórica e validação da política da empresa.

O ELO deve primeiro construir a série histórica de:

`demanda × retornos × reparos × disponibilidade × tempo de recuperação`.

Depois poderá apoiar a definição de estoque de segurança.

---

# 24. FECHAMENTO DO CICLO

O fluxo não termina em estoque.

```text
ESTOQUE / DISPONIBILIDADE
        ↓
PCP
        ↓
NOVA DEMANDA
        ↓
EXPEDIÇÃO
        ↓
CAMPO / LOCAÇÃO
        ↓
RETORNO
        ↓
QUARENTENA
        ↓
REPARO QUANDO NECESSÁRIO
        ↓
ESTOQUE
```

Isso transforma o processo em ciclo de vida do módulo.

---

# 25. GATES PRINCIPAIS DO PROCESSO

| Gate | Pergunta | Saída SIM | Saída NÃO |
|---|---|---|---|
| G01 | AF está completa? | PCP | Pendência/complementação |
| G02 | Padrão ou customizado? | Modular | Customizado |
| G03 | Material disponível? | Picking | Compras |
| G04 | Produção concluída? | Qualidade | Continuação produtiva |
| G05 | Qualidade aprovada? | Expedição/estoque | Reparo/retrabalho |
| G06 | Módulo retornado necessita reparo? | Quarentena/reparo | Disponibilidade |
| G07 | Material de reparo disponível? | Oficina | Almoxarifado/compras |
| G08 | Reparo aprovado? | Estoque/liberação | Retrabalho |
| G09 | Módulo disponível para demanda? | PCP/expedição | Recuperação/produção |

Os critérios formais dos gates devem ser validados com os responsáveis do processo.

---

# 26. ESTADOS DO MÓDULO

O ELO deve tratar estado como diferente de processo.

Exemplo de estados:

```text
DEMANDA
→ PLANEJADO
→ EM PRODUÇÃO
→ EM QUALIDADE
→ LIBERADO
→ EM EXPEDIÇÃO
→ EM CAMPO/LOCAÇÃO
→ EM RETORNO
→ QUARENTENA
→ EM LIMPEZA
→ EM DIAGNÓSTICO
→ EM REPARO
→ EM TESTE
→ ESTOQUE DE SEGURANÇA
→ DISPONÍVEL
```

Um módulo pode retornar a um estado anterior por falha/retrabalho.

---

# 27. FLUXO DE EXCEÇÕES

O ELO deve preservar os caminhos alternativos.

## AF incompleta

`Comercial → AF → PCP → pendência → Comercial → AF revisada → PCP`.

## Material indisponível

`PCP → Almoxarifado → Compras → Recebimento → Estoque → Picking → Produção`.

## Falha de qualidade

`Produção → Qualidade → Reparo → Teste → Qualidade`.

## Retorno com avaria

`Locação → Retorno → Quarentena → Limpeza → Checklist → Diagnóstico → Reparo`.

## Reparo reprovado

`Teste → Falha → Retrabalho → Teste`.

## Mudança de escopo

`Demanda/AF → PCP → replanejamento → orçamento/engenharia quando aplicável → execução`.

---

# 28. DADOS POR SETOR

| Setor | Dados principais para o ELO |
|---|---|
| Comercial/Locação | demanda, AF, cliente, modalidade, modelo, quantidade, prazo |
| PCP | prioridade, sequência, plano, restrições, dependências, status |
| Orçamento | customização, modelo, materiais, recorrência, custos, sazonalidade |
| Engenharia | requisitos técnicos, configuração, alterações |
| Almoxarifado | estoque, reserva, picking, consumo, ruptura |
| Compras | necessidade, OC, chegada, prazo, recebimento |
| Produção | etapa, início/fim, equipe, quantidade, status |
| Qualidade | teste, resultado, não conformidade, retrabalho |
| Expedição | segregação, packing, conferência, gate, saída |
| Campo/Locação | entrega, instalação, utilização, ocorrência, retorno |
| Reparos | avaria, diagnóstico, oficina, equipe, tempo, material, custo |
| RH | disponibilidade e composição da equipe quando aplicável |

---

# 29. MODELO DE DADOS PARA O ELO

A arquitetura deve permitir relações entre entidades.

```text
AF
 ├── cliente
 ├── modelo
 ├── configuração
 ├── quantidade
 └── prazo
      │
      ▼
PLANEJAMENTO
 ├── prioridade
 ├── sequência
 ├── LM/OS
 └── restrições
      │
      ▼
MÓDULO
 ├── produção
 ├── qualidade
 ├── expedição
 ├── campo
 ├── retorno
 └── reparos
       │
       ├── AVARIA
       │    ├── causa
       │    ├── severidade
       │    └── componente
       │
       ├── ETAPA DE REPARO
       │    ├── oficina
       │    ├── equipe
       │    └── tempo
       │
       └── MATERIAL
            ├── quantidade
            └── custo
```

---

# 30. O QUE O ELO DEVE RESPONDER SOBRE O FLUXO

Perguntas de recuperação:

- Qual é o fluxo completo da Multiteiner?
- Qual é o fluxo desde a AF até a entrega?
- Qual é o fluxo do PCP?
- Como uma AF entra na produção?
- Qual a diferença entre modular e customizado?
- Onde entra o orçamento?
- Como o Almoxarifado abastece a produção?
- O que acontece quando falta material?
- Qual o caminho de uma falha de qualidade?
- Qual o fluxo de reparos?
- Como um módulo retornado entra em quarentena?
- Como funciona o checklist de avarias?
- Como o módulo é direcionado para oficina?
- Como o custo do reparo é calculado?
- Como o módulo volta ao estoque de segurança?
- Como o retorno da locação fecha o ciclo?
- Quais setores alimentam o PCP?
- Quais informações do orçamento devem alimentar o planejamento?

---

# 31. NÍVEIS DE RECUPERAÇÃO

Quando o usuário solicitar o fluxo, o ELO deve responder progressivamente:

### Nível 1 — Macro

`Comercial → PCP → Materiais → Produção → Qualidade → Expedição → Campo → Retorno → Reparos → Estoque`.

### Nível 2 — Processo

Abrir os subprocessos de cada bloco.

### Nível 3 — Etapa

Mostrar entrada, atividade, gate, saída e responsável/setor quando validado.

### Nível 4 — Dados

Mostrar quais dados são gerados/consumidos.

### Nível 5 — Operacional

Mostrar sequência, exceções, retrabalho e interfaces.

### Nível 6 — Analítico

Mostrar indicadores, sinais, desvios, gargalos e relações somente quando existirem dados/evidências suficientes.

---

# 32. PROCESSO × ESTADO × TELEMETRIA

O ELO deve manter três camadas separadas:

### Processo documentado

Como o fluxo deve ser entendido/documentado.

### Estado operacional

Onde cada módulo/ordem está agora.

### Telemetria/medição

O que os dados reais mostram sobre tempo, quantidade, custo, capacidade, falha e produtividade.

Não utilizar este documento para afirmar que determinada capacidade, percentual ou tempo é o valor real atual.

---

# 33. PROCESSO × ELO

O ELO não substitui o processo físico.

Ele atua como camada de integração e inteligência:

```text
PROCESSOS DOS SETORES
        ↓
DADOS
        ↓
INTEGRAÇÃO
        ↓
ESTADO ATUAL
        ↓
INDICADORES
        ↓
CORRELAÇÕES
        ↓
SINAIS / DESVIOS
        ↓
DIAGNÓSTICO
        ↓
DECISÃO ESTRATÉGICA
        ↓
PLANO TÁTICO
        ↓
EXECUÇÃO
        ↓
NOVOS DADOS
```

O PCP é uma das principais camadas de orquestração operacional, enquanto o ELO fornece a visão integrada para planejamento estratégico, tático e operacional.

---

# 34. REGRAS DE GOVERNANÇA

1. Não transformar hipótese em fato.
2. Não inserir produtividade sem apontamento real.
3. Não inserir custo sem origem identificável.
4. Não definir estoque de segurança por percentual inventado.
5. Não alterar o processo documentado silenciosamente com base em um caso isolado.
6. Registrar divergências como desvios ou pontos a validar.
7. Preservar a origem dos dados.
8. Manter o vínculo entre módulo e eventos sempre que possível.
9. Diferenciar processo, estado atual e telemetria.
10. Quando houver conflito entre fontes, informar a divergência e indicar a fonte/versão a validar.

---

# 35. CRITÉRIO DE COMPLETUDE

O fluxo será considerado funcional quando for possível responder, para qualquer módulo ou ordem rastreável:

```text
DE ONDE VEIO?
      ↓
O QUE FOI SOLICITADO?
      ↓
COMO FOI PLANEJADO?
      ↓
PADRÃO OU CUSTOMIZADO?
      ↓
QUAIS MATERIAIS?
      ↓
ONDE FOI PRODUZIDO?
      ↓
QUEM EXECUTOU?
      ↓
FOI APROVADO?
      ↓
FOI EXPEDIDO?
      ↓
FOI UTILIZADO/LOCADO?
      ↓
RETORNOU?
      ↓
TEVE AVARIA?
      ↓
QUAL AVARIA?
      ↓
QUAL OFICINA?
      ↓
QUAIS MATERIAIS?
      ↓
QUANTO TEMPO?
      ↓
QUAL CUSTO?
      ↓
PASSOU NA QUALIDADE?
      ↓
FOI PARA ESTOQUE DE SEGURANÇA?
      ↓
ESTÁ DISPONÍVEL PARA NOVA DEMANDA?
```

Se uma pergunta não puder ser respondida, o ELO deve indicar que o dado não está disponível ou não está validado, em vez de completar a resposta por inferência não sustentada.

---

# 36. STATUS DE VALIDAÇÃO

Este documento representa o **fluxo de referência em evolução** da Multiteiner.

A estrutura macro está consolidada para uso do ELO, enquanto detalhes operacionais específicos devem continuar sendo validados com documentos, registros e responsáveis de cada setor.

Os próximos incrementos de maturidade devem transformar cada etapa em registro operacional mensurável, especialmente:

- tempos reais;
- capacidade real;
- filas;
- quantidade por etapa;
- custos;
- produtividade;
- causas de retrabalho;
- consumo de materiais;
- frequência de avarias;
- disponibilidade de equipes;
- demanda;
- retorno de módulos;
- estoque de segurança.

O princípio é: **primeiro medir, depois estabelecer parâmetro; primeiro registrar, depois otimizar.**
