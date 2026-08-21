# ELO — Modelo de Dados Canônico de Orçamento

## 1. Escopo

Este documento define quais informações devem ser estruturadas para que o motor de orçamento possa consultar, relacionar, auditar e explicar uma composição.

## 2. Núcleo do catálogo

```text
family
  ↓
model
  ↓
dimension
  ↓
configuration
  ↓
component
```

### Family

Representa uma família comercial/técnica, por exemplo `MLT.M`.

### Model

Representa o modelo específico, por exemplo `MLT.M01`.

### Dimension

Representa comprimento, largura, altura e área relevante.

### Configuration

Representa variações do modelo sem duplicar o modelo-base.

### Component

Representa portas, janelas, tomadas, luminárias, divisórias e demais elementos.

## 3. Orçamento

Cada orçamento deve possuir:

- identificador;
- versão;
- origem da solicitação;
- cliente/contexto;
- modelo(s) candidato(s);
- itens;
- composições;
- relações;
- mão de obra;
- valores;
- evidências;
- confiança;
- decisão do especialista, quando aplicável.

## 4. Item de orçamento

Campos mínimos:

```text
item_id
budget_id
source_type
source_id
family_id
model_id
component_id
quantity
unit
unit_price
price_source
labor_profile_id
composition_id
relation_id
is_excess
confidence
status
```

## 5. Relações

A relação é uma entidade de primeira classe.

Exemplos:

```text
component → requires → composition
component → affects → electrical_circuit
component → affects → hydraulic_network
model → includes → component
model → compatible_with → dimension
budget_item → depends_on → budget_item
```

Isso permite que o ELO faça auditoria relacional antes de fechar uma composição.

## 6. Mão de obra

A estrutura deve suportar pelo menos:

```text
ajudante
profissional
encarregado
```

A associação deve ocorrer por composição/atividade e não diretamente pelo texto livre do orçamento.

## 7. Composições

Exemplos de famílias de composição:

- interligação elétrica;
- interligação hidráulica;
- nivelamento;
- carro de apoio;
- munck/içamento;
- instalação;
- acabamento;
- transporte;
- desmontagem;
- adequação normativa.

## 8. Lista-Mãe

A Lista-Mãe deve funcionar como fonte governada para itens e valores empresariais.

Entrada nova:

```text
nova atualização
  ↓
auditoria semântica
  ↓
verificação de duplicidade
  ↓
verificação de unidade
  ↓
verificação de família/modelo
  ↓
verificação de relações
  ↓
aprovação
  ↓
Lista-Mãe canônica
```

## 9. Regra de preço

O item com preço fechado deve apontar para sua fonte de preço.

```text
price_source = lista_mae
```

O motor não deve substituir esse valor por estimativa sem autorização explícita.

## 10. Excedentes

Excedentes devem ser armazenados separadamente do modelo-base.

```text
base_model = MLT.M01
excess:
  - janela x3
  - divisória x1
  - tomada x1
```

Cada excedente deve poder apontar para uma composição e para as relações acionadas por sua inclusão.

## 11. Dimensões

A dimensão deve ser normalizada para permitir comparação entre modelos.

Campos:

```text
length_mm
width_mm
height_mm
internal_area_m2
external_area_m2
foot_size
```

O modelo atualizado de referência informado para a família deve considerar altura externa de `3010 mm`, enquanto a área interna deve ser armazenada como atributo específico do modelo/configuração, não inferida automaticamente da área externa.

## 12. Auditoria

Toda alteração relevante deve preservar:

- origem;
- autor/agente;
- timestamp;
- versão;
- justificativa;
- evidência;
- decisão;
- resultado dos gates.

## 13. Regra de ouro

**Documento explica. SQL relaciona. Motor executa. Especialista decide quando necessário. Evolution Gate canoniza.**