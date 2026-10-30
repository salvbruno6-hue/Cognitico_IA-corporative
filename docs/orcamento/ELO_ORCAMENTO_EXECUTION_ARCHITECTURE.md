# ELO — Arquitetura Física de Execução de Orçamentos

## 1. Objetivo

Transformar a inteligência de orçamento do ELO em um fluxo executável, auditável e evolutivo, conectando Lista-Mãe, taxonomia MLT, modelos, dimensões, componentes, mão de obra, composições, relações, PTS, especialista e memória.

## 2. Princípio

**O ELO interpreta, relaciona, audita e orquestra. O especialista valida decisões técnicas e econômicas quando necessário. O SQL mantém os dados estruturados; documentos mantêm regras, contexto e conhecimento explicativo.**

A arquitetura opera em loop:

`PTS TÉCNICA → VARRER RECORRÊNCIAS → CONFRONTAR COMPOSIÇÃO × MEMÓRIAS → ORÇAMENTO → PTS PÓS → NOVA VARREDURA → NOVA RECONCILIAÇÃO → CORRIGIR/VALIDAR → QUESTIONAR → APRENDER`

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
[4] Confronto obrigatório composição × memórias
  │      ├─ abrir composição-base / EXC
  │      ├─ classificar componentes e etapas
  │      ├─ localizar memórias específicas
  │      ├─ integrado × complementar
  │      ├─ duplicidade
  │      └─ conflito de memória
  │
  ▼
[5] Consulta Lista-Mãe
  │
  ▼
[6] Resolução Taxonomia MLT
  │
  ▼
[7] Matching de Modelo / Família / Dimensão
  │
  ▼
[8] Composição do orçamento-base
  │
  ├──────────────► [9] Auditoria de excedentes
  │                       │
  │                       ▼
  │                materiais / serviços / MO-FAB / MO-INST / MO-EXT
  │
  ├──────────────► [10] Auditoria de relações
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
[11] Motor de orçamento
  │
  ▼
[12] PTS Pós-Orçamento
  │
  ▼
[13] Segunda varredura obrigatória de recorrências
  │      ├─ esperado × orçado
  │      ├─ omissões
  │      ├─ duplicidades
  │      ├─ não aplicáveis
  │      ├─ pendências
  │      └─ novas associações candidatas
  │
  ▼
[14] Reconciliação pós-orçamento composição × memórias
  │      ├─ valor orçado
  │      ├─ composição-base
  │      ├─ memória específica
  │      ├─ etapa integrada ou separada
  │      ├─ duplicidade
  │      └─ conflito/questionamento
  │
  ▼
[15] Auditoria de confiança e lacunas
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
                                      └────────► volta a [13] e [14]

FECHAMENTO / ARBITRAGEM
  │
  ▼
[16] Explicação de como foi orçado
  │
  ▼
[17] Revisão de aprendizado da SO (>=10 questões)
  │
  ▼
[18] Registro da experiência
  │
  ▼
[19] Aprendizado candidato
  │
  ▼
[20] Evolution Gate
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
→ ABRIR COMPOSIÇÃO-BASE
→ LOCALIZAR MEMÓRIAS ESPECÍFICAS ASSOCIADAS
→ CONFRONTAR ETAPAS E VALORES
→ GERAR ALERTA/CHECKLIST
→ ORÇAR SOMENTE O QUE SE APLICA
```

### Loop B — depois do orçamento

```text
PTS TÉCNICA
→ ORÇAMENTO
→ EXPECTATIVAS DE RECORRÊNCIA
→ ITENS EFETIVAMENTE ORÇADOS
→ CONFRONTO COMPOSIÇÃO-BASE × MEMÓRIAS ESPECÍFICAS
→ OMISSÕES / DUPLICIDADES / CONFLITOS / PENDÊNCIAS
→ CORREÇÃO OU JUSTIFICATIVA
→ NOVA PTS PÓS
→ NOVA VARREDURA E RECONCILIAÇÃO
```

O loop só termina quando as divergências materiais estiverem resolvidas, justificadas ou arbitradas.

## 3.2 Princípio de reconciliação de composição e memória

O orçamento não pode decidir se uma etapa está incluída apenas pelo texto descritivo de uma memória ou EXC.

A decisão deve seguir:

`COMPOSIÇÃO DETALHADA → COMPONENTES → ETAPAS EXECUTIVAS → MEMÓRIAS ESPECÍFICAS → VÍNCULOS → DECISÃO VALIDADA → TEXTO-RESUMO`

Hierarquia operacional:

1. componentes efetivamente precificados na composição;
2. memória específica da etapa;
3. vínculo entre EXC e memória;
4. decisão explícita validada pelo especialista/orçamentista;
5. texto-resumo genérico.

Se existir uma memória específica de instalação e a composição-base não demonstrar explicitamente essa mesma instalação, a memória específica deve ser tratada como parcela complementar. Um rótulo genérico de função, como `Soldador/Montador`, não prova sozinho a inclusão da instalação final.

Classificações:

- `INTEGRADO_NA_COMPOSIÇÃO`;
- `COMPLEMENTAR_SEPARADO`;
- `DUPLICIDADE`;
- `CONFLITO_DE_MEMÓRIA`;
- `PENDENTE_DE_VALIDAÇÃO`.

### Caso de referência — porta metálica

```text
MC-PORTA-EXTERNA-CORTEN-800X2100
R$ 600,22
= materiais + fabricação + acabamento

MC-INSTALACAO-PORTA-METALICA
R$ 118,15
= instalação específica
```

A existência da memória específica de instalação impede concluir que os R$ 600,22 já incluem essa etapa com base apenas em texto-resumo histórico.

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
- critérios de reconciliação entre composição-base e memórias específicas.

### 4.3 Orquestração

O ELO deve executar a sequência sem transformar conhecimento temporal em regra permanente automaticamente.

**Regra:** recorrência é gatilho de verificação, não autorização de inclusão.

**Regra:** texto-resumo é evidência secundária quando conflita com composição detalhada ou memória específica.

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

reconciliação
 ├── composição-base
 ├── componentes
 ├── etapa executiva
 ├── memória específica
 ├── vínculo
 ├── classificação
 ├── conflito
 └── decisão

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

O ELO deve comparar dimensões, finalidade, ambientes, instalações, esquadrias, pontos, componentes, acessórios, requisitos normativos e diferenças em relação ao padrão.

## 7. Excedentes

Excedente não deve alterar silenciosamente o modelo-base.

Cada excedente recebe origem, unidade, quantidade, justificativa e relação com o modelo-base.

Antes de criar novo excedente, o loop consulta catálogo, memórias e excedentes existentes para detectar equivalência ou precedente.

Antes de decidir que um EXC já contém instalação, montagem, transporte, acabamento ou outra etapa, o loop confronta sua composição com memórias específicas relacionadas.

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

Antes de somar uma MO específica, verificar se ela já aparece de forma inequívoca na composição-base. Antes de excluir uma MO específica, verificar se a composição-base realmente a contém. Em conflito, bloquear inferência e encaminhar ao especialista/questionário.

## 10. Especialista

O especialista recebe contexto preparado pelo ELO:

```text
demanda original
→ PTS Técnica
→ modelo identificado
→ diferenças encontradas
→ recorrências detectadas
→ relações suspeitas
→ composições-base
→ memórias específicas associadas
→ conflitos de inclusão/duplicidade
→ composição sugerida
→ lacunas
→ perguntas objetivas
→ evidências
```

Na saída, devolve valores, itens aplicados, recorrências verificadas, memórias utilizadas, classificação integrado/complementar, cálculos, relações, conflitos resolvidos, lacunas e pontos para PTS Pós.

## 11. Aprendizagem

Uma experiência somente pode alterar a identidade canônica quando passar pelo Evolution Gate.

O aprendizado deve distinguir resultado específico de SO, memória quantitativa, precedente, associação recorrente, etapa integrada/complementar, conflito de memória e regra validada.

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
9. reconciliador composição × memória;
10. composição de mão de obra;
11. motor de orçamento;
12. integração PTS Técnica;
13. integração PTS Pós;
14. loop de recorrências e reconciliação;
15. gateway do especialista;
16. memória de experiências;
17. Evolution Gate;
18. testes integrados;
19. observabilidade.

## 14. Critério de conclusão

O módulo somente é considerado operacional quando uma solicitação de orçamento puder percorrer o fluxo completo com rastreabilidade desde a entrada até a decisão final, incluindo PTS Técnica, varredura de recorrências, confronto composição × memória, orçamento, PTS Pós, nova varredura/reconciliação, correções, revisão de aprendizado, aprendizado candidato e evidências utilizadas.
