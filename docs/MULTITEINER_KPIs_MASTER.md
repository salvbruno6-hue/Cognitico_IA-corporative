# MULTITEINER — ARQUITETURA MESTRE DE KPIs DO ELO

## Objetivo

Estabelecer a camada corporativa de indicadores da Multiteiner dentro do Projeto ELO, conectando demanda, capacidade, execução, entrega, ativos, resultado e aprendizado organizacional.

A lógica central é:

**Demanda → Capacidade → Atendimento → Execução → Entrega → Ativo → Resultado → Aprendizado**

O objetivo não é criar dezenas de indicadores independentes, mas uma cadeia de KPIs capaz de responder às perguntas da operação e, principalmente, do Comercial:

> **Quantos módulos conseguimos atender, quando conseguimos entregar e onde existe risco de não atendimento?**

---

# 1. KPI CENTRAL — ÍNDICE DE CAPACIDADE DE ATENDIMENTO COMERCIAL (ICAC)

## Pergunta respondida

**A operação possui capacidade para atender a demanda comercial?**

## Fórmula

```text
ICAC = Capacidade Disponível para o Comercial ÷ Demanda Comercial × 100
```

## Capacidade Disponível

```text
Estoque disponível
+ Produção com previsão de conclusão
+ Reparo com previsão de liberação
+ Reserva recuperável
- Comprometimentos
- Bloqueios
- Perdas
```

## Exemplo

| Família | Demanda | Estoque | Produção | Reparo | Comprometido | Capacidade | ICAC |
|---|---:|---:|---:|---:|---:|---:|---:|
| MLT-24 | 40 | 18 | 12 | 4 | 10 | 24 | 60% |
| MLT-36 | 30 | 5 | 8 | 3 | 6 | 10 | 33% |
| MLT-48 | 30 | 0 | 10 | 5 | 4 | 11 | 37% |

## Resposta ao Comercial

O indicador deve permitir respostas como:

- MLT-24: capacidade atende 60% da demanda;
- MLT-36: existe gap de 20 módulos;
- MLT-48: existe gap de 19 módulos.

---

# 2. CAPACIDADE COMERCIAL DISPONÍVEL

## Objetivo

Separar estoque físico de capacidade realmente disponível para venda ou locação.

## Fórmula conceitual

```text
Estoque
+ Em Produção
+ Em Reparo
+ Reserva
- Reservados
- Bloqueados
= Capacidade Disponível
```

| Família | Estoque | Em Produção | Em Reparo | Reservado | Disponível Comercial |
|---|---:|---:|---:|---:|---:|
| MLT-24 | 18 | 12 | 4 | 10 | 24 |
| MLT-36 | 5 | 8 | 3 | 6 | 10 |
| MLT-48 | 0 | 10 | 5 | 4 | 11 |

---

# 3. PRODUÇÃO PARA ESTOQUE

## Regra da Multiteiner

**Fabricado = OF interna concluída para formação de estoque.**

## KPI

### Quantidade de OFs Fabricadas

Contagem de OFs internas de fabricação concluídas no período.

Dimensões:

- dia;
- semana;
- mês;
- família;
- modelo.

Exemplo:

| Semana | OF Fabricadas |
|---|---:|
| S1 | 18 |
| S2 | 22 |
| S3 | 17 |
| S4 | 25 |

---

# 4. RECUPERAÇÃO POR REPARO

## KPI

### OFs Reparadas

**OF Reparadas = OFs de reparo concluídas e liberadas para reserva/estoque.**

Comparação recomendada:

| Período | Fabricadas | Reparadas | Total Recuperado |
|---|---:|---:|---:|
| Mês 1 | 80 | 35 | 115 |
| Mês 2 | 75 | 42 | 117 |
| Mês 3 | 90 | 50 | 140 |

---

# 5. TAXA DE RECUPERAÇÃO DO ATIVO

```text
Taxa de Recuperação = Módulos Recuperados ÷ Módulos Enviados para Reparo × 100
```

Classificar os não recuperados em:

- sucata;
- perda;
- aguardando material;
- aguardando decisão;
- inviável economicamente;
- bloqueado.

---

# 6. DISPONIBILIDADE COMERCIAL

```text
Disponibilidade Comercial = Módulos Aptos para Comercialização ÷ Estoque Potencial × 100
```

Objetivo: medir quanto do patrimônio físico está efetivamente apto a gerar receita.

---

# 7. UTILIZAÇÃO DOS ATIVOS

Especialmente para locação.

```text
Taxa de Utilização = Dias Locados ÷ Dias Disponíveis × 100
```

Analisar por:

- módulo;
- modelo;
- família;
- região;
- cliente.

---

# 8. TEMPO PARADO DO ATIVO

Medir o período em que o módulo não está gerando utilização.

Classificar:

- estoque;
- aguardando reparo;
- aguardando orçamento;
- aguardando cliente;
- aguardando logística;
- bloqueado.

Indicador recomendado:

**Dias médios parado por módulo/família.**

---

# 9. LEAD TIME DE RECUPERAÇÃO

```text
LTR = Data de Liberação do Reparo - Data de Entrada no Reparo
```

Exemplo:

Entrada: 01/08  
Liberação: 07/08  
LTR: 6 dias

Objetivo: medir quanto tempo a empresa leva para recuperar capacidade existente.

---

# 10. ATENDIMENTO POR FABRICAÇÃO

```text
AF = Módulos Fabricados para Estoque ÷ Módulos Necessários para Atender a Demanda
```

Exemplo:

Demanda = 60  
Produção = 45  
AF = 75%

Gap = 15 módulos.

---

# 11. GAP DE CAPACIDADE COMERCIAL

```text
Gap = Demanda Comercial - Capacidade Disponível
```

| Família | Demanda | Disponível | GAP |
|---|---:|---:|---:|
| MLT-24 | 40 | 38 | 2 |
| MLT-36 | 30 | 22 | 8 |
| MLT-48 | 30 | 12 | 18 |

Uso principal: definir onde fabricar ou recuperar primeiro.

---

# 12. PRAZO DE ATENDIMENTO COMERCIAL

```text
Lead Time Comercial = Data de Disponibilização - Data da Solicitação
```

Acompanhar por família/modelo.

Exemplo:

| Família | Prazo Médio |
|---|---:|
| MLT-24 | 5 dias |
| MLT-36 | 12 dias |
| MLT-48 | 20 dias |

---

# 13. GARGALO OPERACIONAL

## Índice de Gargalo por Etapa

```text
Índice de Gargalo = Tempo de Espera ÷ Tempo Total do Processo × 100
```

| Etapa | Tempo Total | Espera | Índice |
|---|---:|---:|---:|
| Pintura | 10 dias | 3 | 30% |
| Instalação | 8 dias | 1 | 12,5% |
| Componentes | 12 dias | 6 | 50% |

Priorizar etapas com maior tempo improdutivo e maior impacto sistêmico.

---

# 14. ÍNDICE DE ESPERA / "AGUARDANDO"

```text
IE = OFs com status aguardando ÷ OFs totais × 100
```

Motivos obrigatoriamente categorizáveis:

- aguardando material;
- aguardando pintura;
- aguardando componente;
- aguardando engenharia;
- aguardando aprovação;
- aguardando transporte;
- aguardando manutenção.

Objetivo: identificar por que a produção está parada.

---

# 15. RETRABALHO

```text
Taxa de Retrabalho = OFs que retornaram para etapa anterior ÷ OFs totais × 100
```

Analisar por oficina, etapa, família e causa.

---

# 16. QUALIDADE — FIRST PASS YIELD

```text
FPY = Módulos aprovados na primeira passagem ÷ Módulos processados × 100
```

Aplicar em:

- pintura;
- instalações;
- acabamento;
- testes;
- inspeção final.

---

# 17. EXPEDIÇÃO

## Prontidão para Expedição

```text
PE = Módulos Liberados ÷ Módulos Programados × 100
```

## Entrega no Prazo — OTD

```text
OTD = Entregas no Prazo ÷ Entregas Totais × 100
```

---

# 18. AVARIAS

## Taxa de Avaria

```text
TA = Módulos Retornados com Avaria ÷ Módulos Retornados × 100
```

Relacionar:

**Avaria → Causa → Custo → Oficina → Tempo de Recuperação → Reincidência**

---

# 19. CUSTO DE RECUPERAÇÃO

```text
CMR = Custo Total de Reparos ÷ Módulos Reparados
```

Considerar:

- material;
- mão de obra;
- movimentação;
- transporte;
- terceiros.

---

# 20. REINCIDÊNCIA DE AVARIA

```text
IR = Módulos com Nova Avaria após Reparo ÷ Módulos Reparados × 100
```

Pergunta estratégica:

> Estamos resolvendo a causa ou apenas recuperando o módulo temporariamente?

---

# 21. COMPRAS

## Atendimento de Materiais Críticos

```text
AMC = Itens Críticos Disponíveis no Prazo ÷ Itens Críticos Necessários × 100
```

## OTIF de Compras

```text
OTIF = Pedidos Recebidos Completos e no Prazo ÷ Pedidos Totais × 100
```

---

# 22. ALMOXARIFADO

## Acuracidade do Estoque

```text
AE = Itens Fisicamente Corretos ÷ Itens Inventariados × 100
```

Acompanhar também:

- ruptura;
- cobertura;
- giro;
- picking;
- devoluções;
- divergências.

---

# 23. ENGENHARIA

## Taxa de Alteração de Projeto

```text
TAP = Projetos Alterados após Liberação ÷ Projetos Liberados × 100
```

## Alteração Pós-Congelamento

```text
APC = Alterações após Congelamento ÷ Projetos Congelados × 100
```

Mensurar também impacto em prazo, custo, retrabalho e aprovação.

---

# 24. EXCEDENTES

## Recorrência de Excedentes

```text
RE = Solicitações com Determinado Excedente ÷ Solicitações Totais × 100
```

## Impacto do Excedente

Avaliar:

**frequência × valor × impacto no prazo × impacto na aprovação**

Objetivo: identificar quando uma exceção começa a se tornar padrão de produto.

---

# 25. COMPLEXIDADE

Classificação:

- Baixa;
- Média;
- Alta.

## Conversão por Complexidade

```text
TC = Aprovações da Categoria ÷ Solicitações da Categoria × 100
```

| Complexidade | Solicitações | Aprovações | Conversão |
|---|---:|---:|---:|
| Baixa | 100 | 72 | 72% |
| Média | 80 | 48 | 60% |
| Alta | 40 | 12 | 30% |

---

# 26. APROVAÇÃO G2

## Taxa de Aprovação G2

```text
G2 = Propostas Aprovadas ÷ Propostas Submetidas × 100
```

Cruzar por:

- comercial;
- cliente;
- modelo;
- família;
- complexidade;
- região;
- tipo de contratação;
- excedentes;
- prazo;
- motivo de perda.

---

# 27. MOTIVOS DE PERDA

Monitorar:

- preço;
- prazo;
- concorrência;
- escopo inadequado;
- cancelamento;
- outros.

Separar:

**perdas evitáveis × perdas não evitáveis.**

---

# 28. APRENDIZADO ORGANIZACIONAL

## Aprendizados Capturados

Contar novos aprendizados validados no período.

## Taxa de Reutilização

```text
TRU = Casos que Reutilizaram Aprendizado ÷ Casos Aplicáveis × 100
```

## Índice de Aprendizado Reutilizado

Avaliar a cadeia:

```text
Aprendizado Capturado
→ Diretriz
→ Aplicação
→ Resultado
```

O ELO deve medir não apenas quantos aprendizados foram registrados, mas quantos produziram efeito mensurável.

---

# 29. PREVISÃO DE DEMANDA

## Erro de Previsão — MAPE

Comparar:

**Demanda prevista × demanda realizada**

Dimensões:

- família;
- modelo;
- região;
- venda;
- locação.

---

# 30. DASHBOARD EXECUTIVO ELO

## Bloco 1 — DEMANDA

- solicitações;
- demanda prevista;
- demanda realizada;
- modelos mais demandados.

## Bloco 2 — CAPACIDADE

- estoque;
- em produção;
- em reparo;
- reserva;
- capacidade disponível;
- gap comercial.

## Bloco 3 — PRODUÇÃO

- OF fabricadas;
- OF reparadas;
- produtividade;
- retrabalho;
- gargalos;
- aguardando.

## Bloco 4 — COMERCIAL

- aprovação G2;
- conversão;
- perdas;
- complexidade;
- excedentes.

## Bloco 5 — ENTREGA

- cronograma;
- Lead Time;
- OTD;
- expedição;
- atrasos.

## Bloco 6 — ATIVOS

- ocupação;
- dias parados;
- locações;
- receita por módulo;
- custo de reparo;
- reincidência.

## Bloco 7 — INTELIGÊNCIA ELO

- aprendizados capturados;
- reutilização;
- novas diretrizes;
- excedentes recorrentes;
- alertas;
- previsões.

---

# 31. CADEIA CORPORATIVA DOS KPIs

```text
DEMANDA
   ↓
CAPACIDADE
   ↓
ATENDIMENTO COMERCIAL
   ↓
PRODUÇÃO / REPARO
   ↓
ENTREGA
   ↓
UTILIZAÇÃO DO ATIVO
   ↓
AVARIA / MANUTENÇÃO
   ↓
CUSTO / RENTABILIDADE
   ↓
APRENDIZADO
   ↓
NOVA PREVISÃO
```

A arquitetura deve priorizar indicadores que expliquem a relação entre as etapas, evitando KPIs isolados sem causa ou consequência identificável.

---

# 32. PRINCÍPIO DE GOVERNANÇA

Cada KPI deverá possuir, no mínimo:

- nome;
- definição;
- pergunta de negócio que responde;
- fórmula;
- fonte dos dados;
- periodicidade;
- responsável;
- dimensão de análise;
- regra de cálculo;
- meta, quando existir;
- faixa de alerta;
- ação esperada diante do desvio;
- provenance;
- data de atualização.

Nenhum KPI deve ser publicado como definitivo sem que a fonte e a regra de cálculo estejam claras.

---

# 33. PRINCÍPIO CENTRAL

O objetivo dos KPIs do ELO não é simplesmente medir a empresa.

O objetivo é permitir decisões melhores.

O painel deve conseguir responder:

> **O que está acontecendo?**

> **Por que está acontecendo?**

> **Qual impacto isso possui?**

> **O que devemos fazer agora?**

> **Quem precisa agir?**

> **O que aprendemos para a próxima decisão?**

---

## Status

**Documento:** MULTITEINER_KPIs_MASTER.md  
**Sistema:** Projeto ELO  
**Categoria:** Governança de Indicadores  
**Escopo:** End-to-End Multiteiner  
**Princípio:** Demanda → Capacidade → Execução → Entrega → Ativo → Resultado → Aprendizado
