# ELO — Arquitetura Física de Execução de Orçamentos

## 1. Objetivo

Transformar a inteligência de orçamento do ELO em um fluxo executável, auditável e evolutivo, conectando Lista-Mãe, taxonomia MLT, modelos, dimensões, componentes, mão de obra, composições, relações, especialista, PTS e memória.

## 2. Princípio

**O ELO interpreta, relaciona, audita e orquestra. O especialista valida decisões técnicas e econômicas quando necessário. O SQL mantém os dados estruturados; documentos mantêm regras, contexto e conhecimento explicativo.**

A arquitetura deve operar em **loop cognitivo-orçamentário**, não em linha única:

`PTS TÉCNICA → VARRER RECORRÊNCIAS → ORÇAMENTO → PTS PÓS → VARRER RECORRÊNCIAS → CORRIGIR/VALIDAR → APRENDER`

## 3. Fluxo físico

```text
ENTRADA / DOCUMENTAÇÃO
  │
  ▼
[1] Classificação da demanda
  │
  ▼
[2] PTS Técnica / requisitos e solução
  │
  ▼
[3] Varredura obrigatória de recorrências
  │      ├─ aplicação
  │      ├─ dependências
  │      ├─ itens complementares
  │      ├─ precedentes/memórias
  │      └─ alertas de verificação
  │
  ▼
[4] Consulta Lista-Mãe
  │
  ▼
[5] Resolução Taxonomia MLT
  │
  ▼
[6] Matching de Modelo / Família / Dimensão
  │
  ▼
[7] Composição do orçamento-base
  │
  ├──────────────► [8] Auditoria de excedentes
  │                       │
  │                       ▼
  │                materiais / serviços / MO-FAB / MO-INST
  │
  ├──────────────► [9] Auditoria de relações
  │                       │
  │                       ├─ elétrica / dados
  │                       ├─ hidráulica
  │                       ├─ abertura / reforço / acabamento
  │                       ├─ nivelamento
  │                       ├─ logística / Munck
  │                       ├─ carro de apoio / hospedagem / pedágio
  │                       └─ demais composições
  │
  ▼
[10] Motor de orçamento
  │
  ▼
[11] PTS Pós-Orçamento
  │
  ▼
[12] Segunda varredura obrigatória de recorrências
  │      ├─ esperado × orçado
  │      ├─ omissões
  │      ├─ duplicidades
  │      ├─ não aplicáveis
  │      ├─ pendências
  │      └─ novas associações candidatas
  │
  ▼
[13] Auditoria de confiança e lacunas
  │
  ├── suficiente ─────────────► fechamento / arbitragem
  │
  └── insuficiente ───────────► especialista
                                      │
                                      ▼
                              decisão / correção
                                      │
                                      ▼
                              orçamento REV.N
                                      │
                                      ▼
                              PTS Pós REV.N
                                      │
                                      └────────► volta a [12]

FECHAMENTO / ARBITRAGEM
  │
  ▼
[14] Registro da experiência
  │
  ▼
[15] Aprendizado candidato
  │
  ▼
[16] Evolution Gate
  │
  ├─ regra canônica → estrutura
  └─ experiência temporal → memória
```

## 3.1 Loop cognitivo obrigatório

A PTS Técnica e a PTS Pós são dois pontos obrigatórios de inspeção do mesmo sistema.

### Loop A — antes do orçamento

```text
REQUISITO
→ SOLUÇÃO TÉCNICA
→ IDENTIFICAR FAMÍLIA RECORRENTE
→ VERIFICAR APLICAÇÃO
→ VERIFICAR DEPENDÊNCIAS
→ CONSULTAR PRECEDENTE/MEMÓRIA
→ GERAR ALERTA/CHECKLIST
→ ORÇAR SOMENTE O QUE SE APLICA
```

### Loop B — depois do orçamento

```text
PTS TÉCNICA
→ ORÇAMENTO
→ EXPECTATIVAS DE RECORRÊNCIA
→ ITENS EFETIVAMENTE ORÇADOS
→ OMISSÕES / DUPLICIDADES / PENDÊNCIAS
→ CORREÇÃO OU JUSTIFICATIVA
→ NOVA PTS PÓS
→ NOVA VARREDURA
```

O loop só termina quando as divergências materiais estiverem resolvidas, justificadas ou arbitradas.

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
- evidências de auditoria;
- memórias quantitativas e precedentes de cálculo.

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
- padrões de comportamento do ELO;
- catálogo cognitivo de serviços e itens recorrentes;
- critérios de aplicação e associações entre famílias de custo.

### 4.3 Orquestração

O ELO deve executar a sequência sem transformar conhecimento temporal em regra permanente automaticamente.

**Regra:** recorrência é um gatilho de verificação, não uma autorização de inclusão.

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

recorrência
 ├── família
 ├── gatilho
 ├── aplicação
 ├── dependência
 ├── memória de referência
 ├── condição de não aplicação
 └── resultado da verificação

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

Antes de criar novo excedente, o loop consulta catálogo, memórias e excedentes existentes para detectar equivalência ou precedente.

## 8. Relações como gatilhos

Uma relação conhecida dispara automaticamente uma **verificação**, não uma inclusão.

Exemplo:

```text
nova janela
   ↓
verificar abertura de vão
   ↓
verificar reforço estrutural
   ↓
verificar acabamento do vão
   ↓
verificar fabricação da janela
   ↓
verificar instalação
   ↓
verificar grade, se exigida
```

Outro exemplo:

```text
mão de obra externa
   ↓
verificar dias de mobilização
   ↓
carro de apoio
   ↓
rota / pedágio
   ↓
hospedagem por pernoite
   ↓
transporte principal / Munck, se aplicável
```

Se a relação estiver fora do conhecimento canônico, o ELO encaminha ao especialista e pode gerar candidato de aprendizado após validação.

## 9. Valores

Quando o item possuir preço fechado na Lista-Mãe, o motor deve utilizar a referência cadastrada.

Não deve inventar ou recalcular o preço-base sem uma regra explícita.

Preço histórico não é preço vigente. Precedente transfere método e lógica; o cenário atual deve ser recalculado.

O valor de mão de obra deve ser relacionado por função e por natureza:

- MO-FAB — fabricação;
- MO-INST — instalação;
- MO-EXT — execução em campo;
- ajudante;
- profissional;
- encarregado;
- especialidades quando aplicáveis.

## 10. Especialista

O especialista recebe um contexto já preparado pelo ELO:

```text
demanda original
→ PTS Técnica
→ modelo identificado
→ diferenças encontradas
→ recorrências detectadas
→ relações suspeitas
→ precedentes/memórias relevantes
→ composição sugerida
→ lacunas
→ perguntas objetivas
→ evidências
```

O especialista não deve precisar reconstruir toda a análise manualmente.

Na saída, deve devolver não apenas valores, mas também:

```text
itens aplicados
→ itens recorrentes verificados
→ itens considerados não aplicáveis
→ memórias utilizadas
→ novos cálculos
→ relações encontradas
→ lacunas
→ pontos para PTS Pós
```

## 11. Aprendizagem

Uma experiência somente pode alterar a identidade canônica quando passar pelo Evolution Gate.

Experiências úteis, mas ainda não canonizadas, permanecem temporais e contextualizadas.

```text
experiência
   ↓
PTS Pós identifica padrão/erro/associação
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

O aprendizado deve distinguir:

- resultado específico de SO;
- memória quantitativa;
- precedente;
- associação recorrente;
- regra validada.

Método e aplicação permanecem na camada documental; memória quantitativa permanece na persistência estruturada.

## 12. Contrato de execução

O contrato principal está em:

`prompts/ELO_ORCAMENTO_EXECUTION_CONTRACT.yaml`

O catálogo cognitivo do especialista está em:

`08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/CATALOGO_SERVICOS_ITENS_RECORRENTES.md`

A interface física está em:

`frontend/src/components/ELOOrcamentoView.tsx`

## 13. Próxima camada

A implementação deve avançar nesta ordem:

1. schemas SQL;
2. repositórios de dados;
3. resolver Lista-Mãe;
4. resolver taxonomia MLT;
5. motor de matching;
6. catálogo/índice de recorrências;
7. motor de excedentes;
8. grafo de relações;
9. composição de mão de obra;
10. motor de orçamento;
11. integração PTS Técnica;
12. integração PTS Pós;
13. loop de recorrências;
14. gateway do especialista;
15. memória de experiências;
16. Evolution Gate;
17. testes integrados;
18. observabilidade.

## 14. Critério de conclusão

O módulo somente é considerado operacional quando uma solicitação de orçamento puder percorrer o fluxo completo com rastreabilidade desde a entrada até a decisão final, incluindo:

- PTS Técnica;
- primeira varredura de recorrências;
- orçamento;
- PTS Pós;
- segunda varredura de recorrências;
- correções e reentrada no loop quando necessárias;
- aprendizado candidato;
- todas as relações relevantes e a evidência utilizada.
