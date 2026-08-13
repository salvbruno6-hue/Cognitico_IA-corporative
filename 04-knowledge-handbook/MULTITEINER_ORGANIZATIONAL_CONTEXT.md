# MULTITEINER — CONTEXTO ORGANIZACIONAL

> Fonte canônica de contexto organizacional da Multiteiner para o ecossistema ELO.

Este documento descreve identidade, fluxo end-to-end, setores, entidades, relações, riscos, conhecimento e governança contextual. Não substitui contratos, políticas ou procedimentos normativos.

## 1. IDENTIDADE DA EMPRESA

### 1.1 Modelo de negócio
A Multiteiner atua no segmento de soluções/construção modular e combina fabricação, venda, locação, montagem/desmontagem e produção/customização conforme demanda.

A operação apresenta simultaneamente produção padronizada para estoque e produção customizada, aumentando a complexidade de sincronização entre demanda, engenharia, materiais, capacidade e expedição.

### 1.2 Venda
Modalidade de fornecimento em que o produto é vendido ao cliente.

Detalhes adicionais: a validar nos documentos comerciais e contratuais oficiais.

### 1.3 Locação
Ciclo de referência:

```text
Comercial → preparação → expedição → cliente/campo → uso → desmobilização
→ retorno → recebimento → inspeção → reparo/reprocesso → estoque → nova expedição
```

### 1.4 Montagem e desmontagem
Parte do atendimento externo e do ciclo de locação.

Detalhes de responsabilidade, recursos e critérios: a validar.

### 1.5 Produção modular sob demanda
A organização opera com produção para estoque e produção/customização para necessidades específicas dos clientes.

## 2. VISÃO END-TO-END

```text
COMERCIAL
→ ENGENHARIA
→ ORÇAMENTO
→ PCP
→ COMPRAS
→ ALMOXARIFADO
→ PRODUÇÃO
→ EXPEDIÇÃO
→ CLIENTE/LOCAÇÃO
→ RETORNO
→ RECEBIMENTO
→ INSPEÇÃO
→ REPARO/REPROCESSO
→ ESTOQUE
→ NOVA EXPEDIÇÃO
```

Para cada transição o ELO deve buscar: entrada, saída, responsável, informação necessária, sistema de registro, decisão, dependência, recurso, indicador, risco, exceção e evidência disponível.

## 3. COMERCIAL

### 3.1 Entrada da AF
A AF é fonte formal de demanda contratada/solicitada, devendo preservar rastreabilidade.

### 3.2 Venda x locação
Cada demanda deve identificar a modalidade.

### 3.3 Padrão x personalizado
Há produtos padronizados e produtos customizados.

### 3.4 Escopo
Registrar cliente, produto, quantidade, configuração, prazo, modalidade, requisitos e necessidades técnicas.

### 3.5 Prazo
Prazo é variável crítica para Comercial, PCP, Produção e Expedição.

### 3.6 Interface com planejamento
O Comercial alimenta o planejamento com demanda, alterações e compromissos.

### 3.7 Riscos comerciais
Alterações de escopo, quantidade, prazo, customização, complementações, nova AF e informação incompleta.

## 4. ENGENHARIA / PROJETOS

### 4.1 CAD
Ferramenta de engenharia/projetos referenciada no contexto.

### 4.2 Levantamento dimensional / As-Built
Usado quando a condição real precisa ser comparada ao projeto.

### 4.3 Padronização
Necessária para reduzir variabilidade, retrabalho e inconsistências.

### 4.4 Excedentes
Devem ser relacionados ao conhecimento de engenharia e gestão de materiais.

### 4.5 Lista de materiais
BOM/LM é elemento crítico; inconsistências em listas técnicas aparecem entre fatores relevantes de perda.

### 4.6 Liberação técnica
Deve funcionar como gate para etapas dependentes.

## 5. PLANEJAMENTO / PCP

### 5.1 Missão
Integrar demanda, capacidade, materiais, recursos, sequência, prazo, produção e acompanhamento.

### 5.2 Gate de SO
Avaliar escopo, engenharia, materiais, capacidade, prazo, configuração, documentação e aprovação.

### 5.3 Capacidade
Considerar pessoas, equipamentos, oficinas, pintura, componentes complementares, movimentação e expedição.

### 5.4 Sequenciamento
Considerar prazo, prioridade, materiais, capacidade, gargalos, configuração e dependências.

### 5.5 Planejamento semanal
Estruturar PLANEJADO × REALIZADO × DESVIO.

### 5.6 Gargalos
Foram identificados gargalos em pintura, componentes complementares, informação, materiais/BOM e reprogramações. Entre componentes citados: telhas de fibra de vidro, lavatórios, mictórios, cubas, divisórias sanitárias e boxes de chuveiro.

### 5.7 Indicadores
Lead Time, OEE, capacidade, aderência à programação, reprogramações, desvios, gargalos, produtividade e qualidade.

### 5.8 Exceções
Atrasos, falta de material, falta de capacidade, mudanças comerciais, alteração de projeto, gargalo, retrabalho, avaria e prazos críticos.

### 5.9 Interface diretoria
Fornecer capacidade, riscos, gargalos, prazos, desvios e necessidades de decisão.

## 6. COMPRAS

1. Demanda recebida
2. Cotação
3. Pedido
4. Lead time
5. Materiais críticos
6. Follow-up

A cadeia deve manter vínculo entre necessidade, fornecedor, pedido, prazo, recebimento e impacto na produção.

## 7. ALMOXARIFADO

1. Recebimento
2. Conferência
3. Endereçamento
4. Estoque
5. Picking
6. Requisição para compras
7. Devoluções
8. Rastreamento

O estoque deve distinguir disponibilidade real, reservas e materiais indisponíveis.

## 8. PRODUÇÃO

Fluxo de referência:

```text
Triagem
→ Chassi
→ Escovação
→ Pintura de tratamento
→ Acabamento branco
→ Estoque de estruturas
→ Movimentação
→ Piso
→ Teto
→ Colunas
→ Trilho
→ Pintura modular
→ Paredes
→ Instalações
→ Acabamento
→ Testes
→ Liberação
```

A pintura foi identificada como ponto crítico de capacidade no diagnóstico. Também há dependência de componentes complementares e recursos compartilhados.

## 9. OFICINAS E APOIO INDUSTRIAL

Corte e dobra; solda; serralheria; reparo; manutenção; pintura; escovação; oficinas especializadas; recursos compartilhados.

Esses recursos devem ser tratados como capacidades que podem restringir o fluxo.

## 10. LOGÍSTICA INTERNA

Empilhadeiras; pórticos; trilhos; rotas; movimentação de cargas; pátio; segurança.

A logística interna integra o fluxo de produção e deve ser analisada por capacidade, rota, utilização, tempo e risco.

## 11. EXPEDIÇÃO

1. Equipamento etiquetado
2. Checklist
3. NF
4. Conformidade
5. Oficina de reparo
6. Sistema Najason
7. Carregamento
8. Liberação do motorista

O Najason é referenciado no contexto operacional, especialmente na expedição; funções detalhadas a validar.

## 12. LOCAÇÃO / CAMPO

Transporte; montagem; uso; manutenção; ocorrências; desmobilização; retorno.

## 13. RECEBIMENTO / PÓS-LOCAÇÃO

Aviso da logística; NF; descarregamento; vistoria; avarias; quarentena; oficina; liberação ao estoque.

O retorno deve distinguir, quando aplicável:

```text
ATIVO OK
ATIVO EM REPARO
ATIVO EM QUARENTENA
```

## 14. GESTÃO DE AVARIAS

Identificação → material → mão de obra → movimentação → orçamento → recuperação → cobrança → histórico.

Para fins de análise, separar os componentes de custo e manter histórico do ativo e da causa identificada.

## 15. DIRETORIA / GESTÃO

Metas; capacidade; margem; investimentos; riscos; crescimento; exceções.

A gestão deve receber conhecimento estruturado, não apenas indicadores.

## 16. COMUNICAÇÃO ORGANIZACIONAL

Reuniões; WhatsApp; documentos; responsabilidades; escalonamento.

A comunicação informal pode ser fonte de sinal, mas decisões e estados críticos devem possuir registro governado quando aplicável.

## 17. DADOS E SISTEMAS

### 17.1 Najason
Sistema referenciado na operação.

### 17.2 CAD
Ferramenta de engenharia/projetos.

### 17.3 Planilhas
Utilizadas como instrumentos de controle e informação.

### 17.4 Banco de dados
Estrutura necessária para consolidação futura; implementação atual deve ser validada.

### 17.5 IA
Parte da arquitetura futura do ELO, subordinada a provenance, tenant, need-to-know, confidencialidade e human-in-the-loop.

### 17.6 Integrações
Devem conectar processos e sistemas preservando governança.

## 18. CONHECIMENTO ORGANIZACIONAL

Padrões; BOM; custos; tempos; gargalos; experiências; lições aprendidas.

O conhecimento prático das equipes deve ser formalizado progressivamente em objetos de conhecimento com provenance, contexto, validade e condições de aplicabilidade.

## 19. MODELOS DE DECISÃO

1. Estoque disponível?
2. Projeto padrão?
3. SO liberada?
4. Capacidade disponível?
5. Produto conforme?
6. Avaria?
7. Necessidade de reparo?
8. Exceção?
9. Escalar para gestão?

Essas perguntas devem evoluir para regras/gates verificáveis quando houver contrato e governança apropriados.

## 20. MAPA DE ENTIDADES

Pessoas; setores; processos; atividades; produtos; módulos; contêineres; equipamentos; materiais; recursos; documentos; AF; SO; ordens de produção; orçamentos; projetos; BOM; estoques; movimentações; expedições; locações; retornos; avarias; reparos; eventos; riscos; restrições; decisões; planos; indicadores; metas; evidências; experiências; aprendizados.

## 21. MAPA DE RELAÇÕES

```text
CLIENTE → CONTRATO → AF → PROJETO → SO
SO → BOM/LM → ALMOXARIFADO → COMPRAS
SO → PCP → CAPACIDADE → SEQUENCIAMENTO → PRODUÇÃO
PRODUÇÃO → QUALIDADE → EXPEDIÇÃO
EXPEDIÇÃO → LOCAÇÃO → CAMPO → RETORNO
RETORNO → INSPEÇÃO → AVARIA → REPARO → ESTOQUE
```

Relações decisórias:

```text
DECISÃO → RESPONSÁVEL
DECISÃO → EVIDÊNCIA
DECISÃO → RISCO
DECISÃO → RESULTADO
RESULTADO → APRENDIZAGEM
APRENDIZAGEM → REGRA/PADRÃO
```

## 22. MAPA DE RISCOS

### Financeiro
Custo, margem, investimento, desperdício.

### Técnico
Projeto, BOM, customização, não conformidade.

### Operacional
Gargalos, capacidade, reprogramação, retrabalho.

### Logístico
Movimentação, transporte, pátio, prazo.

### Qualidade
Avaria, defeito, inspeção, retrabalho.

### Segurança
Movimentação, equipamentos, operação industrial.

### Prazo
Material atrasado, gargalo, alteração de escopo, capacidade insuficiente.

### Informação
Informação dispersa, comunicação verbal, documento desatualizado, inconsistência e falta de rastreabilidade.

## 23. KPIs POR SETOR

| Setor | KPIs prioritários |
|---|---|
| Comercial | demanda, contratos, alterações, prazo |
| Engenharia | projetos liberados, tempo, retrabalho, BOM |
| PCP | programação, Lead Time, reprogramações, carga × capacidade |
| Compras | Lead Time fornecedor, pedidos pendentes, atrasos, materiais críticos |
| Almoxarifado | acuracidade, rupturas, atendimento, estoque |
| Produção | produtividade, OEE, Lead Time, WIP, retrabalho |
| Oficinas | tempo de reparo, fila, capacidade, disponibilidade |
| Logística | movimentações, utilização, tempo, incidentes |
| Expedição | entregas no prazo, conformidade, pendências, carregamento |
| Campo | montagens, ocorrências, manutenção, retorno |
| Pós-locação | avarias, inspeção, reparo, liberação |
| Diretoria | receita, margem, capacidade, riscos, crescimento, investimentos |

## 24. CASOS HISTÓRICOS RELEVANTES

### Gargalo da pintura
Acúmulo de módulos aguardando cabine, associado à ausência de medição de tempo padrão e sequenciamento inadequado.

### Componentes complementares
Telhas de fibra de vidro, lavatórios, mictórios, cubas, divisórias e boxes foram identificados como componentes capazes de limitar o fluxo em determinados momentos.

### Reprogramações
Informações descentralizadas e baixa visibilidade favoreceram decisões reativas.

### BOM
Inconsistências em listas técnicas aparecem entre os fatores relevantes de perda.

### Crescimento comercial
A demanda aumentou mais rapidamente do que alguns mecanismos internos de controle.

**Aprendizado transversal:** sincronizar processos, dados, pessoas e capacidade.

## 25. REGRAS DE GOVERNANÇA DO ELO

### Provenance
Informações relevantes devem possuir origem rastreável.

### Tenant
Dados e decisões devem respeitar isolamento organizacional/contextual quando aplicável.

### Need-to-Know
Informação deve ser acessada segundo necessidade e autorização.

### Confidencialidade
Dados comerciais, financeiros, pessoais, técnicos e estratégicos devem respeitar classificação e controle de acesso.

### Human-in-the-loop
A IA pode analisar, correlacionar, identificar lacunas, formular hipóteses, simular e recomendar. Decisões críticas permanecem humanas conforme a governança.

## 26. PLANO DE ESTRUTURAÇÃO

### O que já existe
Processos operacionais; conhecimento prático; produção padronizada; produção customizada; Comercial; Engenharia; PCP; Compras; Almoxarifado; Produção; Expedição; locação/campo; retorno; reparo; sistemas e planilhas; conhecimento histórico; gargalos conhecidos; diagnóstico operacional.

### O que está documentado
Contexto; fluxo; Pareto; Ishikawa; gargalos; PCP; Gestão Visual; Lead Time; OEE; cronometragem; gestão de gargalos; resultados esperados.

### O que falta medir
Tempos reais; capacidade por recurso; capacidade da pintura; capacidade dos componentes complementares; tempos de espera; WIP; Lead Time real; aderência da programação; produtividade; retrabalho; avarias; tempo de reparo; utilização de recursos.

### O que falta integrar
```text
Comercial
↕
Engenharia
↕
PCP
↕
Compras
↕
Almoxarifado
↕
Produção
↕
Expedição
↕
Campo
↕
Retorno
↕
Reparo
↕
Estoque
```

### O que pode ser automatizado
Consolidação de dados; indicadores; alertas por exceção; programação; cálculo de capacidade; materiais; rastreamento de status; relatórios; histórico de decisões; desvios; consolidação documental.

### O que exige decisão humana
Aceitação de riscos; mudanças de prioridade crítica; investimentos; contratação; alteração de capacidade; exceções relevantes; decisões comerciais estratégicas; políticas; mudanças de processo; decisões com impacto financeiro ou organizacional significativo.

# MATRIZ DE MATURIDADE CONTEXTUAL

| Elemento | Existe | Documentado | Contratado | Implementado | Testado | Bloqueado | Pronto |
|---|---|---|---|---|---|---|---|
| Modelo de negócio | Sim | Sim | A validar | A validar | A validar | Não identificado | Não |
| Fluxo End-to-End | Sim | Sim | A validar | A validar | A validar | Não identificado | Não |
| Comercial | Sim | Parcial | A validar | A validar | A validar | Não identificado | Não |
| Engenharia | Sim | Parcial | A validar | A validar | A validar | Não identificado | Não |
| PCP | Sim | Sim | Parcial | Parcial | A validar | Não identificado | Não |
| Compras | Sim | Parcial | A validar | A validar | A validar | Não identificado | Não |
| Almoxarifado | Sim | Parcial | A validar | A validar | A validar | Não identificado | Não |
| Produção | Sim | Sim | Parcial | Parcial | A validar | Não identificado | Não |
| Expedição | Sim | Parcial | A validar | A validar | A validar | Não identificado | Não |
| Locação/Campo | Sim | Parcial | A validar | A validar | A validar | Não identificado | Não |
| Retorno/Reparo | Sim | Parcial | A validar | A validar | A validar | Não identificado | Não |
| Conhecimento organizacional | Sim | Parcial | Não | Não | Não | Não identificado | Não |
| Governança ELO | Sim | Sim | Parcial | Parcial | A validar | Não identificado | Não |

**Nota:** “A validar” significa que não existe evidência suficiente nos materiais analisados para confirmar o estado. Não significa que o recurso/processo não exista.

# REGRA DE ATUALIZAÇÃO

Quando uma nova informação organizacional for confirmada:

1. registrar a informação;
2. identificar a origem;
3. atualizar a seção correspondente;
4. revisar relações afetadas;
5. revisar riscos;
6. revisar decisões dependentes;
7. atualizar o estado de maturidade;
8. preservar histórico da alteração.

O ELO deve conseguir reconstruir:

> o que aconteceu → por que aconteceu → o que foi decidido → quem decidiu → com base em quê → qual resultado ocorreu → o que foi aprendido.

**Princípio final:** o contexto organizacional deve evoluir junto com o conhecimento da Multiteiner, preservando rastreabilidade entre fatos, processos, decisões, resultados e aprendizados.
