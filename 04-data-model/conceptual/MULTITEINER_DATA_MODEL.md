---
id: ELO-DATA-MULTITEINER-001
name: Multiteiner ELO Virtual Data Model
type: canonical-reference
layer: data
status: draft
---

# MULTITEINER — MODELO CONCEITUAL DE DADOS DO ELO

## 1. Princípio

O modelo de dados é subordinado ao fluxo mestre da Multiteiner. Nenhuma entidade deve existir isoladamente: cada dado deve ter origem, responsável, consumidor, etapa do processo e finalidade decisória identificáveis.

O modelo é lógico/conceitual. Não representa ainda o banco físico de produção.

## 2. Domínios

| Domínio | Entidades centrais | Dono primário |
|---|---|---|
| Demanda | demanda, AF, AF item | Comercial / Locação |
| Orçamento | orçamento, customização | Orçamento / Comercial |
| PCP | ordem_pcp, prioridade, janela | PCP |
| Materiais | LM, estoque, movimentos | Almoxarifado |
| Compras | ordem_compra | Compras |
| Produção | ordem_producao, etapa | Produção |
| Qualidade | inspeção, teste | Qualidade |
| Ativo | módulo, patrimônio | Operação |
| Expedição | expedição | Expedição |
| Retorno | retorno, quarentena | Operação / PCP |
| Avarias | avaria, diagnóstico | Reparos / Qualidade |
| Reparos | ordem_reparo, etapas, materiais, apontamentos | Reparos |
| Segurança | estoque_seguranca | PCP |
| Inteligência ELO | evento, sinal, plano_tatico | ELO / PCP |

## 3. Relações principais

```text
DEMANDA
  └── AF
       ├── ORÇAMENTO
       │    └── CUSTOMIZAÇÃO
       └── ORDEM PCP
            └── LISTA MATERIAL
                 └── ESTOQUE / COMPRAS
                      └── PRODUÇÃO
                           └── QUALIDADE
                                ├── APROVADO → EXPEDIÇÃO
                                └── FALHA → REPARO

EXPEDIÇÃO
  └── VENDA → encerramento
  └── LOCAÇÃO → UTILIZAÇÃO → RETORNO
                              └── QUARENTENA
                                   └── AVARIA
                                        └── ORDEM REPARO
                                             ├── MATERIAL
                                             ├── EQUIPE / HORAS
                                             ├── OFICINA
                                             └── TESTE
                                                  ├── APROVADO → ESTOQUE SEGURANÇA
                                                  └── FALHA → RETRABALHO

TODOS OS DOMÍNIOS
  └── ELO EVENTO
       └── ELO SINAL
            └── ELO PLANO TÁTICO
```

## 4. Linhas operacionais

### Fluxo modular
Linha de produção puxada baseada em modelos/configurações padronizadas, sujeita a disponibilidade de materiais, capacidade e sequência.

### Fluxo customizado
Linha paralela que incorpora requisitos específicos, orçamento, materiais adicionais, engenharia/projeto e validação.

### Fluxo de recuperação
Ciclo iniciado por retorno ou falha, passando por quarentena, limpeza, checklist, diagnóstico, materiais, oficinas, apontamentos, testes e eventual estoque de segurança.

## 5. Regra de rastreabilidade

Cada módulo deve poder ser relacionado, quando os dados existirem, a:

`demanda → AF → planejamento → produção/reparo → qualidade → expedição → utilização → retorno → reparo → estoque de segurança → nova demanda`.

## 6. Uso pelo ELO

O ELO usa o modelo para responder quatro perguntas:

1. Onde o dado nasceu?
2. Quem é responsável por ele?
3. Quem precisa consumi-lo?
4. Que decisão operacional, tática ou estratégica ele suporta?

O ELO não deve inferir que uma informação é verdadeira apenas porque existe no modelo. O valor deve possuir evidência ou status de validação.