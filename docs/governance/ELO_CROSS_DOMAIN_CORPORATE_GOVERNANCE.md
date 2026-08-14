# ELO — Governança Cross-Domain Corporativa

**Versão:** 1.0-proposal  
**Issue:** #78  
**Status:** proposta para validação e testes

## 1. Finalidade

Estabelecer uma camada de governança transversal para que o ELO consiga cruzar fatos, requisitos, decisões, custos, projetos, execução e resultados entre domínios corporativos sem fundi-los e sem perder proveniência.

A camada deve responder não apenas **o que existe em cada domínio**, mas **como os elementos se relacionam, em que período, sob qual contexto, com qual evidência e com qual impacto**.

## 2. Domínios canônicos

### 2.1 COMERCIAL

Representa oportunidade, cliente, negociação, proposta, condição comercial, contrato e pós-venda.

**Natureza predominante:** intenção de negócio e relação comercial.

### 2.2 LICITAÇÕES

Representa edital, termo de referência, esclarecimentos, requisitos, habilitação, obrigações e condições contratuais de processos licitatórios.

**Natureza predominante:** requisito formal, obrigação e restrição contratual.

**Invariante:** LICITAÇÕES não é sinônimo de COMERCIAL, mesmo quando ambos participam da mesma oportunidade.

### 2.3 ORÇAMENTO

Representa composição econômica, premissas, quantidades, custos, excedentes, mobilização, logística, riscos, margem e viabilidade.

**Natureza predominante:** estimativa econômica e técnico-operacional.

### 2.4 PROJETOS / ENGENHARIA

Representa solução técnica, layout, especificações, adaptações, disciplinas, responsabilidades e documentação de engenharia.

**Natureza predominante:** definição da solução técnica.

### 2.5 COMPRAS / SUPRIMENTOS

Representa necessidades de aquisição, fornecedores, cotações, pedidos, prazos e abastecimento.

**Natureza predominante:** obtenção de recursos.

### 2.6 PRODUÇÃO

Representa ordens, execução, materiais consumidos, capacidade, qualidade, retrabalho e estado produtivo.

**Natureza predominante:** transformação/execução.

### 2.7 PCP

Representa planejamento, programação, sequenciamento, capacidade, prioridades e restrições.

**Natureza predominante:** coordenação temporal da execução.

### 2.8 LOGÍSTICA / EXPEDIÇÃO

Representa mobilização, transporte, carga, descarga, expedição, instalação, retirada e movimentação.

**Natureza predominante:** movimentação física e entrega.

### 2.9 RESULTADO / PÓS-EXECUÇÃO

Representa realizado versus previsto, desvios, causas, desempenho, incidentes, satisfação e aprendizado.

**Natureza predominante:** resultado observado e feedback.

## 3. Regra de separação

Uma entidade ou fato deve possuir um **domínio de origem**. O relacionamento com outro domínio não altera sua origem.

Exemplo:

> Uma exigência de edital continua sendo `LICITACOES`, mesmo quando impacta `ORCAMENTO`, `PROJETO` e `PRODUCAO`.

Da mesma forma:

> Uma premissa de orçamento não se transforma automaticamente em requisito contratual.

## 4. Modelo lógico de relação

O ELO deve representar relações conceitualmente como:

`SOURCE_ENTITY → RELATION → TARGET_ENTITY`

com metadados mínimos:

- `tenant_id`
- `domain`
- `source_domain`
- `target_domain`
- `relation_type`
- `source_id`
- `target_id`
- `valid_from`
- `valid_until`
- `provenance`
- `evidence`
- `confidence`
- `responsible_party`
- `impact`
- `status`

Esse modelo é conceitual nesta etapa. Não autoriza criar armazenamento paralelo antes da validação arquitetural.

## 5. Relações corporativas prioritárias

### Comercial ↔ Licitações

- oportunidade originada de licitação;
- cliente/órgão relacionado;
- requisitos que impactam proposta;
- diferenças entre negociação e obrigação formal.

### Licitações ↔ Orçamento

- requisito → item orçamentário;
- obrigação → custo;
- prazo → mobilização;
- requisito → excedente;
- requisito sem cobertura orçamentária.

### Comercial ↔ Orçamento

- condição comercial → premissa;
- preço → margem;
- desconto → impacto econômico;
- promessa comercial → capacidade necessária.

### Orçamento ↔ Projetos

- solução → custo;
- adaptação → excedente;
- projeto → quantitativo;
- premissa → requisito técnico.

### Orçamento ↔ Compras

- item orçado → necessidade de compra;
- custo estimado → cotação;
- prazo estimado → lead time;
- fornecedor → risco de custo/prazo.

### Projeto ↔ Produção

- especificação → ordem;
- layout → configuração;
- adaptação → operação;
- mudança de projeto → impacto produtivo.

### Compras ↔ Produção / PCP

- material → necessidade;
- pedido → prazo;
- atraso → restrição produtiva;
- substituição → impacto técnico.

### Produção / PCP ↔ Logística

- conclusão → expedição;
- programação → mobilização;
- capacidade → prazo;
- atraso → compromisso de entrega.

### Resultado ↔ todos

- previsto → realizado;
- desvio → causa;
- causa → decisão;
- decisão → resultado;
- resultado validado → candidato a aprendizado.

## 6. Cadeia sistêmica de referência

`COMERCIAL/LICITAÇÕES → ORÇAMENTO → PROJETO → COMPRAS → PRODUÇÃO/PCP → LOGÍSTICA → RESULTADO`

A cadeia é uma visão de relacionamento, não uma sequência rígida. Um domínio pode gerar eventos ou restrições que retornam a montante.

Exemplo:

`PRODUÇÃO → restrição → ORÇAMENTO → revisão de viabilidade → COMERCIAL`

## 7. Proveniência e autoridade

A autoridade da informação depende do tipo de fato.

- documento oficial vigente da licitação: autoridade sobre requisito formal;
- contrato vigente: autoridade sobre obrigação contratual;
- documento de projeto aprovado: autoridade sobre solução técnica;
- sistema operacional autorizado: autoridade sobre execução observada;
- orçamento: autoridade sobre sua própria composição, não sobre fatos externos que apenas estima;
- histórico: evidência contextual, não regra automática.

Conflitos não devem ser resolvidos silenciosamente.

## 8. Temporalidade

Toda relação relevante deve poder ser interpretada no tempo.

O ELO deve distinguir:

- vigente;
- expirado;
- futuro;
- histórico;
- substituído;
- desconhecido.

Uma relação válida ontem não deve ser aplicada automaticamente ao estado atual.

## 9. Tenant e domínio

O cruzamento entre domínios não autoriza cruzamento entre tenants.

`tenant A + Comercial` pode relacionar-se com `tenant A + Orçamento`.

`tenant A + Comercial` não pode buscar silenciosamente `tenant B + Orçamento`.

O domínio também deve permanecer explícito para evitar contaminação semântica.

## 10. Governança do especialista

Os prompts dos especialistas continuam sendo **diretrizes de domínio**.

O ELO Core deve fornecer:

- contexto;
- identidade;
- descoberta;
- autorização;
- evidência;
- proveniência;
- relações;
- decisão;
- memória;
- Evolution Gate.

O especialista não deve criar sua própria memória corporativa nem redefinir contratos do Core.

## 11. Caso de referência: orçamento

Para uma SO/LIC, o ELO deve poder reconstruir:

`TR/EDITAL → requisito → solução → modelo → quantidade → excedente → orçamento → projeto → compra → produção → entrega → resultado`

Cada elo precisa poder indicar sua fonte, confiança e situação.

## 12. Testes obrigatórios

1. Relação Comercial → Orçamento válida.
2. Relação Licitações → Orçamento válida.
3. Relação Orçamento → Projeto válida.
4. Relação Projeto → Produção válida.
5. Relação Compras → Produção válida.
6. Relação Produção → Logística válida.
7. Resultado retroalimentando uma decisão.
8. Relação entre tenants diferentes deve ser bloqueada.
9. Conflito entre documento vigente e histórico deve priorizar o vigente.
10. Relação expirada não pode ser tratada como vigente.
11. Premissa de orçamento não pode ser promovida automaticamente a requisito contratual.
12. Experiência isolada não pode virar regra corporativa.
13. Relação sem proveniência suficiente deve ficar em estado de incerteza/pêndencia.
14. Provider externo não pode redefinir o domínio ou a autoridade da informação.

## 13. Relação com contratos existentes

Esta camada deve reutilizar os contratos existentes de Context, SourceDiscovery, Evidence, Knowledge, Memory, Provenance, Decision, Evolution Memory e as primitivas previstas em ELO-CORE-001 (#44).

Não criar:

- segundo Cognitive Core;
- banco paralelo por domínio;
- memória paralela;
- autoridade paralela;
- engine de decisão independente.

## 14. Critério de promoção

Esta proposta só poderá ser promovida ao baseline quando:

1. o modelo for revisado;
2. os contratos existentes forem confirmados;
3. os testes prioritários forem implementados;
4. a suíte passar;
5. os casos adversariais passarem;
6. o Evolution Gate autorizar;
7. a alteração for revisada no PR.

**Estado atual: PROPOSTA / ADAPT_REQUIRED.**
