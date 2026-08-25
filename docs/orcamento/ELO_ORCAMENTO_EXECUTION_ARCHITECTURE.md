# ELO — Arquitetura Física de Execução de Orçamentos

## 1. Objetivo

Transformar a inteligência de orçamento do ELO em um fluxo executável, auditável e evolutivo, conectando Lista-Mãe, taxonomia MLT, modelos, dimensões, componentes, mão de obra, composições, relações, especialista e memória.

## 2. Princípio

**O ELO interpreta, relaciona, audita e orquestra. O especialista valida decisões técnicas e econômicas quando necessário. O SQL mantém os dados estruturados; documentos mantêm regras, contexto e conhecimento explicativo.**

## 3. Fluxo físico

```text
ENTRADA
  │
  ▼
[1] Classificação da demanda
  │
  ▼
[2] Consulta Lista-Mãe
  │
  ▼
[3] Resolução Taxonomia MLT
  │
  ▼
[4] Matching de Modelo / Família / Dimensão
  │
  ▼
[5] Composição do orçamento-base
  │
  ├──────────────► [6] Auditoria de excedentes
  │                       │
  │                       ▼
  │                materiais / serviços
  │
  ├──────────────► [7] Auditoria de relações
  │                       │
  │                       ├─ elétrica
  │                       ├─ hidráulica
  │                       ├─ nivelamento
  │                       ├─ içamento / munck
  │                       ├─ carro de apoio
  │                       └─ demais composições
  │
  ▼
[8] Motor de orçamento
  │
  ▼
[9] Auditoria de confiança e lacunas
  │
  ├── suficiente ─────────────► proposta técnica/econômica
  │
  └── insuficiente ───────────► especialista
                                      │
                                      ▼
                              decisão / correção
                                      │
                                      ▼
                              [10] Registro da experiência
                                      │
                                      ▼
                              [11] Evolution Gate
                                      │
                                      ├─ regra canônica → estrutura
                                      └─ experiência temporal → memória
```

## 4. Camadas

### 4.1 Dados estruturados — SQL

Devem permanecer em SQL:

- lista-mãe;
- famílias de produtos;
- modelos MLT;
- dimensões;
- unidades;
- componentes;
- preços;
- mão de obra;
- composições;
- relações entre itens;
- regras de aplicação estruturáveis;
- histórico versionado;
- evidências de auditoria.

### 4.2 Conhecimento documental

Devem permanecer em documentos:

- regras técnicas extensas;
- critérios de interpretação;
- justificativas;
- normas;
- manuais;
- decisões arquiteturais;
- contratos de especialistas;
- explicações de composição;
- padrões de comportamento do ELO.

### 4.3 Orquestração

O ELO deve executar a sequência sem transformar conhecimento temporal em regra permanente automaticamente.

## 5. Entidades mínimas

```text
produto
 ├── família
 ├── modelo
 ├── dimensão
 ├── configuração
 └── composição

orçamento
 ├── item
 ├── quantidade
 ├── unidade
 ├── preço-base
 ├── excedente
 ├── relação
 ├── mão-de-obra
 └── evidência

experiência
 ├── solicitação
 ├── interpretação
 ├── decisão do especialista
 ├── resultado
 ├── confiança
 └── elegibilidade para evolução
```

## 6. Regra do modelo

Se uma entrada puder ser adequadamente representada por um modelo MLT conhecido, o ELO deve reutilizar esse modelo como referência.

Exemplo:

`TR → MLT.M01`

O ELO deve comparar:

- dimensões;
- finalidade;
- quantidade de ambientes;
- instalações;
- esquadrias;
- pontos elétricos;
- componentes construtivos;
- acessórios;
- requisitos normativos;
- diferenças em relação ao padrão.

## 7. Excedentes

Excedente não deve alterar silenciosamente o modelo-base.

Exemplo:

```text
MLT.M01
├── configuração-base
├── +3 janelas
├── +1 divisória
├── +1 tomada
└── +relações necessárias
```

Cada excedente recebe origem, unidade, quantidade, justificativa e relação com o modelo-base.

## 8. Relações como gatilhos

Uma relação conhecida pode disparar automaticamente uma verificação.

Exemplo:

```text
nova tomada
   ↓
auditar circuito
   ↓
auditar carga
   ↓
auditar proteção
   ↓
auditar interligação
```

Se a relação estiver fora do conhecimento canônico, o ELO deve encaminhar ao especialista.

## 9. Valores

Quando o item possuir preço fechado na Lista-Mãe, o motor deve utilizar a referência cadastrada.

Não deve inventar ou recalcular o preço-base sem uma regra explícita.

O valor de mão de obra deve ser relacionado por função, por exemplo:

- ajudante;
- profissional;
- encarregado.

## 10. Especialista

O especialista recebe um contexto já preparado pelo ELO:

```text
demanda original
→ modelo identificado
→ diferenças encontradas
→ relações suspeitas
→ composição sugerida
→ lacunas
→ perguntas objetivas
→ evidências
```

O especialista não deve precisar reconstruir toda a análise manualmente.

## 11. Aprendizagem

Uma experiência somente pode alterar a identidade canônica quando passar pelo Evolution Gate.

Experiências úteis, mas ainda não canonizadas, permanecem temporais e contextualizadas.

```text
experiência
   ↓
validação
   ↓
repetição / evidência
   ↓
avaliação de impacto
   ↓
Evolution Gate
   ↓
regra canônica
```

## 12. Contrato de execução

O contrato principal está em:

`prompts/ELO_ORCAMENTO_EXECUTION_CONTRACT.yaml`

A interface física está em:

`frontend/src/components/ELOOrcamentoView.tsx`

## 13. Próxima camada

A implementação deve avançar nesta ordem:

1. schemas SQL;
2. repositórios de dados;
3. resolver Lista-Mãe;
4. resolver taxonomia MLT;
5. motor de matching;
6. motor de excedentes;
7. grafo de relações;
8. composição de mão de obra;
9. motor de orçamento;
10. gateway do especialista;
11. memória de experiências;
12. Evolution Gate;
13. testes integrados;
14. observabilidade.

## 14. Critério de conclusão

O módulo somente é considerado operacional quando uma solicitação de orçamento puder percorrer o fluxo completo com rastreabilidade desde a entrada até a decisão final, incluindo todas as relações relevantes e a evidência utilizada.