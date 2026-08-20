# ELO — Loop de Relações de Produto, Orçamento e Aprendizado

**Status:** NORMATIVE — proposta operacional para validação pelos gates
**Owner:** ELO Core / Governance
**Escopo:** Multiteiner como tenant de validação

## 1. Objetivo

Estabelecer a relação canônica entre Lista-Mãe, taxonomia MLT, fichas técnicas, dimensões, configuração padrão, excedentes, materiais, serviços, mão de obra, composições, interligações, orçamento, especialista e memória de experiência.

O objetivo é permitir que o ELO reconheça um modelo durante uma solicitação de orçamento, recupere automaticamente seus parâmetros conhecidos, identifique o que pertence ao padrão e o que excede o padrão, cobre do especialista as relações ainda necessárias e registre aprendizados sem transformar experiência isolada em regra canônica sem validação.

## 2. Princípio de separação

Tabelas relacionais e valores estruturados devem ser mantidos em SQL. Relações explicativas, justificativas técnicas, conhecimento normativo e contexto documental permanecem em documentos/Knowledge. O Core governa a interpretação e as transições entre esses domínios.

## 3. Modelo canônico

```text
LISTA-MÃE
  ↓ auditoria de entrada
TAXONOMIA / FAMÍLIA
  ↓
MODELO MLT
  ↓
FICHA TÉCNICA / CONFIGURAÇÃO PADRÃO
  ↓
DIMENSÕES + COMPONENTES + QUANTIDADES
  ↓
REQUISITO DO ORÇAMENTO
  ↓
MATCH SEMÂNTICO
  ↓
┌───────────────────────────────┐
│ PADRÃO                        │
│ EXCEDENTE                     │
│ VARIAÇÃO / CUSTOMIZAÇÃO       │
│ COMPOSIÇÃO / INTERLIGAÇÃO     │
│ LACUNA / AMBIGUIDADE          │
└───────────────────────────────┘
  ↓
MATERIAIS + SERVIÇOS + MÃO DE OBRA
  ↓
ORÇAMENTO VERSIONADO
  ↓
AUDITORIA ELO
  ↓
ESPECIALISTA
  ↓
RESULTADO OBSERVADO
  ↓
EXPERIÊNCIA TEMPORAL
  ↓ avaliação
EVOLUÇÃO CANDIDATA
  ↓ gates
REGRA / CONHECIMENTO CANÔNICO
```

## 4. Dimensões

A referência dimensional vigente recebida para os módulos é:

| Tamanho | Comprimento | Largura | Altura | Área |
|---|---:|---:|---:|---:|
| 20 pés | 6000 mm | 2440 mm | 3010 mm | 14,6 m² |
| 15 pés | 4500 mm | 2440 mm | 3010 mm | 11,0 m² |
| 10 pés | 3000 mm | 2440 mm | 3010 mm | 7,3 m² |
| 8,5 pés | 2600 mm | 2440 mm | 3010 mm | 6,3 m² |
| 8 pés | 2400 mm | 2440 mm | 3010 mm | 5,8 m² |
| 6 pés | 1800 mm | 2440 mm | 3010 mm | 4,4 m² |

Para o MLT.M01, a dimensão vigente é **6000 × 2440 × 3010 mm**, com **14,6 m² de área dimensional** e **13,63 m² de área útil interna**.

Área dimensional e área útil interna são atributos distintos e nunca devem ser sobrescritos um pelo outro.

Dados anteriores, como a altura de 2985 mm, permanecem como histórico/versionamento quando existirem em artefatos anteriores; não são considerados conflito contra a atualização validada de 3010 mm.

## 5. Relações SQL mínimas

A estrutura relacional deve contemplar, no mínimo:

- `product_families`
- `product_models`
- `product_dimensions`
- `product_versions`
- `product_components`
- `product_standard_quantities`
- `product_variants`
- `master_list_items`
- `labor_roles`
- `compositions`
- `composition_items`
- `interconnections`
- `pricing_versions`
- `budget_requests`
- `budget_lines`
- `budget_variations`
- `budget_audit_events`
- `specialist_decisions`
- `experience_records`
- `evolution_candidates`

Todas as entidades devem possuir identidade estável, status, versão quando aplicável, origem/proveniência e relacionamento auditável.

## 6. Exemplo MLT.M01

O MLT.M01 é um modelo padrão. Sua ficha técnica define os componentes esperados. Se uma solicitação contiver três janelas além das duas previstas no padrão, o ELO deve representar:

```text
MLT.M01 × quantidade
+ 3 janelas = EXCEDENTE
```

O excedente não altera silenciosamente a definição do MLT.M01. Ele entra como linha adicional do orçamento e pode possuir material, serviço, mão de obra e composição próprios.

O mesmo mecanismo deve reconhecer, quando suportado pela taxonomia e pelos dados autorizados, divisórias, tomadas, portas, pontos elétricos, pontos hidráulicos e outros elementos adicionais.

## 7. Interligações como relação obrigatória quando aplicável

Interligações não devem ser tratadas como texto livre perdido no orçamento. Quando uma condição exigir conexão, infraestrutura, nivelamento, apoio, Munck, carro de apoio, mobilização ou outro serviço relacionado, o ELO deve procurar a composição correspondente.

Quando faltar um parâmetro necessário, deve gerar uma **LACUNA DE ORÇAMENTO** e solicitar ao especialista a informação ou decisão necessária.

O ELO não deve inventar preço, quantidade ou condição de execução.

## 8. Fluxo quando o especialista pede “orçar”

```text
ORÇAR
 ↓
identificar solicitação
 ↓
identificar família/taxonomia
 ↓
identificar modelo provável
 ↓
recuperar configuração padrão
 ↓
recuperar dimensões vigentes
 ↓
recuperar componentes e quantidades padrão
 ↓
comparar requisitos recebidos
 ↓
separar PADRÃO / EXCEDENTE / VARIAÇÃO / LACUNA
 ↓
associar Lista-Mãe, composições e mão de obra disponíveis
 ↓
verificar interligações e dependências
 ↓
produzir orçamento estruturado para auditoria
 ↓
ELO pergunta ao especialista somente o que não consegue resolver com evidência autorizada
```

## 9. Auditoria de relações

O ELO deve manter uma camada de **auditoria de relações**. Ela verifica:

1. se o modelo reconhecido possui família válida;
2. se a dimensão é compatível com o modelo;
3. se a versão é vigente;
4. se os componentes padrão possuem identidade;
5. se as quantidades padrão estão definidas;
6. se o item solicitado é padrão ou excedente;
7. se existe composição aplicável;
8. se mão de obra necessária está definida;
9. se existe interligação dependente de parâmetros adicionais;
10. se o preço possui fonte e versão;
11. se há contradições entre fontes;
12. se a linha pode ser calculada sem hipótese não autorizada.

## 10. Aprendizado por variação

Quando o ELO não entender uma situação de orçamento, deve registrar a lacuna agrupada por contexto, família, modelo, ambiente, componente, composição ou padrão de ocorrência.

Exemplo:

```text
VARIAÇÃO NÃO RECONHECIDA
Família: MLT
Modelo provável: M01
Ambiente: escritório
Elemento: janela adicional
Frequência: recorrente
Ação: solicitar validação do especialista
```

A recorrência não promove automaticamente uma nova regra. Ela gera uma `evolution_candidate`.

## 11. Promoção de experiência

Uma experiência pode permanecer em memória temporal ou ser candidata a evolução. Para tornar-se regra canônica, deve passar por:

```text
EXPERIÊNCIA
 ↓
AVALIAÇÃO DE QUALIDADE
 ↓
GENERALIZAÇÃO
 ↓
VERIFICAÇÃO DE CONFLITOS
 ↓
VALIDAÇÃO ESPECIALISTA
 ↓
IMPACTO ARQUITETURAL
 ↓
EVOLUTION GATE
 ↓
PROMOÇÃO
```

Experiência positiva isolada não altera a identidade canônica do ELO.

## 12. Atualização da Lista-Mãe

Toda nova versão da Lista-Mãe passa por:

```text
RECEBER
 ↓
QUARENTENA / IDENTIFICAÇÃO DA FONTE
 ↓
COMPARAR COM VERSÃO VIGENTE
 ↓
DETECTAR DUPLICIDADES
 ↓
DETECTAR CONFLITOS
 ↓
CLASSIFICAR NOVOS ITENS
 ↓
VALIDAR RELAÇÕES
 ↓
APROVAR
 ↓
VERSIONAR
 ↓
INCORPORAR À LISTA-MÃE CANÔNICA
 ↓
REVALIDAR MODELOS E ORÇAMENTOS AFETADOS
```

## 13. Loop permanente

Este fluxo é uma especialização do Loop de Conclusão do ELO. Toda alteração relevante deve retornar à auditoria de relações antes de ser considerada concluída.

```text
DETECTAR
→ AUDITAR
→ RELACIONAR
→ ABSORVER
→ TESTAR
→ GATES
→ PROMOVER OU PRESERVAR COMO EXPERIÊNCIA
→ ATUALIZAR ÍNDICES
→ VALIDAR
→ MERGE
→ REVARrer
```

Se uma relação necessária estiver ausente, o ciclo não deve ser falsamente encerrado. A pendência deve permanecer explícita até ser resolvida, aceita como lacuna ou encaminhada ao especialista.

## 14. Regra de autoridade

- SQL: dados estruturados e relações operacionais.
- Documentos/Knowledge: significado, justificativas, normas e contexto.
- Core: interpretação, classificação e decisão de fluxo.
- Especialista: validação técnica/comercial quando exigida.
- Governance/Gates: autorização de promoção estrutural.
- Memória: experiência observada, nunca autoridade canônica por si só.

Nenhum módulo de orçamento deve criar um segundo catálogo canônico ou uma segunda Lista-Mãe.
