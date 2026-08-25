---
id: ELO-PROC-MULTITEINER-001
name: Multiteiner End-to-End Process Flow
type: reference
layer: process
owner: Multiteiner process knowledge / ELO process context
status: draft
authority: reference
version: 0.1
related:
  - ELO-012
  - MULTITEINER_ORGANIZATIONAL_CONTEXT
  - MULTITEINER_METODOLOGIA_ORCAMENTO_ELO
  - ELO-012_MULTITEINER_FLOW_MODULAR_PROTOCOL
depends_on: []
---

# MULTITEINER — FLUXO END-TO-END DETALHADO

## 1. Finalidade

Este documento é a referência de processo para permitir que o ELO reconstrua, em pesquisa, a sequência operacional da Multiteiner de forma progressiva e minuciosa.

Ele não é apenas um desenho visual. Cada etapa é descrita por:

- entrada;
- decisão/gate;
- atividade;
- saída;
- setor envolvido;
- dependências;
- dados esperados;
- exceções;
- retorno do fluxo;
- pontos de integração com o ELO.

O documento deve ser recuperado quando a pergunta envolver, por exemplo:

- fluxo da Multiteiner;
- fluxo completo;
- fluxo do PCP;
- caminho de uma AF;
- fluxo modular;
- fluxo customizado;
- fluxo de reparos;
- retorno de módulo;
- quarentena;
- oficinas;
- estoque de segurança;
- relação entre Comercial, Orçamento, PCP, Almoxarifado, Produção, Qualidade, Expedição e Reparos;
- onde uma informação entra ou sai do processo;
- qual é a sequência de uma operação.

## 2. Limite epistemológico

Este artefato consolida o fluxo operacional de referência a partir do contexto organizacional existente e do fluxo operacional fornecido para a Multiteiner.

Quando uma etapa, regra, responsável, sistema, tempo ou critério ainda não estiver formalmente validado, o ELO deve tratá-lo como:

`DOCUMENTADO / A VALIDAR`

ou

`OBSERVADO / A VALIDAR`

e não inventar detalhes ausentes.

O fluxo atual observado pode divergir do fluxo projetado. Divergência deve ser registrada como desvio de processo, não usada silenciosamente para sobrescrever o processo documentado.

---

# 3. VISÃO MACRO

```text
COMERCIAL / LOCAÇÃO
        ↓
RECEBIMENTO DA AF
        ↓
PLANEJAMENTO / PCP
        ↓
PADRÃO OU PERSONALIZADO?
   ↙                    ↘
PADRÃO              PERSONALIZADO
   ↘                    ↙
   EXCEDENTES / REQUISITOS / MATERIAIS
                ↓
          ALMOXARIFADO
                ↓
       MATERIAL DISPONÍVEL?
          ↙            ↘
        SIM             NÃO
         ↓               ↓
      PICKING          COMPRAS
         ↘               ↙
             PRODUÇÃO
                ↓
            QUALIDADE
          ↙          ↘
     APROVADO       FALHA
        ↓              ↓
   EXPEDIÇÃO         REPARO
                       ↓
             QUARENTENA / LIMPEZA
                       ↓
                  DIAGNÓSTICO
                       ↓
                    OFICINAS
                       ↓
                    TESTES
                    ↙    ↘
              APROVADO   FALHA
                 ↓          ↓
          ESTOQUE SEG.   RETRABALHO
                 ↓
              EXPEDIÇÃO
                 ↓
             CLIENTE/CAMPO
                 ↓
               RETORNO
                 ↓
             NOVO CICLO
```

O fluxo modular e o fluxo customizado são tratados como linhas paralelas de atendimento que compartilham recursos e interfaces de planejamento, materiais, qualidade e expedição.

---

# 4. FLUXO 01 — COMERCIAL / LOCAÇÃO → AF

## 4.1 Entrada

A demanda nasce no Comercial/Locação e é formalizada por AF.

## 4.2 Dados mínimos esperados

- cliente;
- modalidade: venda ou locação;
- produto/modelo;
- quantidade;
- configuração;
- prazo;
- requisitos especiais;
- necessidade de customização;
- informações técnicas disponíveis.

## 4.3 Saída

`AF recebida e disponível para análise do planejamento.`

## 4.4 Exceções

- AF incompleta;
- mudança de escopo;
- alteração de quantidade;
- alteração de prazo;
- customização não especificada;
- necessidade de complementação técnica.

## 4.5 Interface ELO

O ELO deve relacionar a AF com demanda, modelo, configuração, prazo, modalidade, histórico e demais objetos de planejamento disponíveis.

---

# 5. FLUXO 02 — PCP / PLANEJAMENTO

## 5.1 Entrada

`AF + requisitos comerciais/técnicos + disponibilidade conhecida.`

## 5.2 Sequência

```text
Receber AF
→ analisar escopo
→ validar configuração
→ verificar padrão x personalizado
→ identificar excedentes/variações
→ verificar materiais
→ verificar capacidade
→ verificar prazo
→ verificar dependências
→ definir sequência/prioridade
→ liberar planejamento para execução
```

## 5.3 Gate principal

**Projeto/configuração padrão ou personalizado?**

### Padrão
Segue o fluxo modular padronizado, sujeito a disponibilidade de materiais, capacidade e sequência.

### Personalizado
Segue tratamento específico de requisitos, materiais, engenharia/orçamento e interfaces adicionais.

## 5.4 PCP como orquestrador

O PCP não é apenas uma etapa do fluxo. Na arquitetura ELO ele funciona como camada de planejamento e orquestração entre demanda, capacidade, materiais, produção, qualidade, expedição e exceções.

O ELO deve conseguir responder:

- o que está planejado;
- o que foi realizado;
- qual o desvio;
- qual restrição apareceu;
- qual dependência foi afetada;
- qual decisão precisa ser tomada;
- qual plano deve ser revisto.

---

# 6. FLUXO 03 — ORÇAMENTO / CUSTOMIZAÇÃO

O orçamento é especialmente relevante quando a montagem do módulo é customizada ou quando o Comercial solicita modificações.

## 6.1 Informações de interesse para o ELO

- módulos mais locados;
- módulos mais vendidos;
- materiais mais utilizados;
- modelos mais modificados;
- tipos de customização recorrentes;
- sazonalidade de customizados;
- materiais utilizados em customizações;
- materiais associados a avarias por modelo;
- histórico de custos;
- relação entre modelo, configuração e excedentes.

## 6.2 Fluxo

```text
Necessidade comercial
→ requisitos
→ análise do modelo
→ identificação de padrão
→ identificação de excedentes/variações
→ materiais/serviços/mão de obra
→ composição/orçamento
→ validação
→ resultado para planejamento
```

## 6.3 Relação com PCP

A informação de orçamento não deve ficar isolada. Deve alimentar planejamento com conhecimento sobre variabilidade, recorrência de customização, materiais e carga potencial.

---

# 7. FLUXO 04 — ALMOXARIFADO / ABASTECIMENTO

## 7.1 Entrada

`Lista de materiais / necessidade do planejamento / excedentes.`

## 7.2 Sequência

```text
Recebimento
→ conferência
→ endereçamento
→ estoque
→ verificação de disponibilidade
→ reserva/picking
→ entrega ao processo
```

## 7.3 Decisão

**Material disponível?**

### Sim

`Picking → abastecimento da produção/reparo.`

### Não

`Necessidade → Compras → acompanhamento → recebimento → conferência → estoque → abastecimento.`

## 7.4 Dados relevantes

- disponibilidade real;
- reserva;
- ruptura;
- material crítico;
- quantidade;
- código;
- consumo;
- requisição;
- lead time de compra;
- devolução;
- origem do consumo.

## 7.5 Relação com reparos

O Almoxarifado também deve registrar materiais efetivamente consumidos em reparos, permitindo calcular custo por módulo, modelo, avaria e intervenção.

---

# 8. FLUXO 05 — PRODUÇÃO MODULAR

O fluxo modular é tratado como uma linha de produção puxada, paralela ao fluxo customizado.

## 8.1 Sequência de referência

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

A sequência é uma referência operacional. Tempos padrão, capacidade e critérios de passagem devem ser obtidos de dados e documentos validados.

## 8.2 Interfaces críticas

- pintura;
- componentes complementares;
- materiais;
- oficinas;
- movimentação;
- qualidade;
- expedição.

## 8.3 Componentes complementares

Entre os componentes identificados como capazes de limitar o fluxo em determinados momentos estão:

- telhas de concreto/fibra de vidro conforme o contexto operacional aplicável;
- lavatórios;
- mictórios;
- cubas;
- divisórias sanitárias;
- boxes de chuveiro.

A relação causal com um gargalo específico deve ser comprovada por dados quando analisada pelo ELO.

---

# 9. FLUXO 06 — PRODUÇÃO CUSTOMIZADA

O fluxo customizado compartilha recursos com o fluxo modular, mas exige tratamento adicional de requisitos.

```text
Demanda customizada
→ análise comercial
→ orçamento
→ requisitos técnicos
→ configuração/excedentes
→ materiais
→ planejamento
→ produção/customização
→ qualidade
→ expedição
```

O ELO deve manter a distinção entre:

`MODELO PADRÃO`

`VARIAÇÃO`

`EXCEDENTE`

`CUSTOMIZAÇÃO`

para evitar que uma alteração de um atendimento específico seja interpretada automaticamente como alteração do modelo padrão.

---

# 10. FLUXO 07 — QUALIDADE

## 10.1 Entrada

Módulo/produto concluído em uma etapa produtiva ou recuperado em reparo.

## 10.2 Sequência

```text
Receber para inspeção
→ verificar critérios
→ executar testes aplicáveis
→ registrar resultado
```

### Aprovado

`Liberação → expedição ou estoque, conforme o fluxo.`

### Falha

`Não conformidade → reparo/retrabalho → nova inspeção.`

## 10.3 Regra ELO

Falha de qualidade não deve desaparecer do histórico. Deve permanecer vinculada ao módulo, modelo, etapa, causa, intervenção e resultado.

---

# 11. FLUXO 08 — EXPEDIÇÃO

## 11.1 Sequência de referência

```text
Módulo liberado
→ segregação no pátio
→ verificação da necessidade de instalação
→ packing
→ conferência
→ gate
→ saída controlada
→ entrega/cliente/campo
```

No contexto operacional também há referências a equipamento etiquetado, checklist, NF, conformidade, sistema operacional e liberação do motorista. Detalhes de cada responsabilidade devem ser validados com a documentação operacional correspondente.

---

# 12. FLUXO 09 — LOCAÇÃO / CAMPO

```text
Expedição
→ transporte
→ montagem/instalação quando aplicável
→ uso
→ manutenção/ocorrências
→ desmobilização
→ retorno
```

Eventos de campo devem permanecer vinculados ao ativo/módulo sempre que houver rastreabilidade disponível.

---

# 13. FLUXO 10 — RETORNO / PÓS-LOCAÇÃO

## 13.1 Entrada

Retorno do módulo/ativo ao pátio/operação.

## 13.2 Sequência

```text
Aviso de retorno
→ recebimento
→ descarregamento
→ identificação
→ vistoria
→ classificação da condição
```

## 13.3 Estados possíveis

```text
ATIVO OK
ATIVO EM REPARO
ATIVO EM QUARENTENA
```

O retorno alimenta novamente o ciclo operacional.

---

# 14. FLUXO 11 — REPAROS / RECUPERAÇÃO

Este fluxo deve ser tratado pelo ELO como um subprocesso rastreável do ciclo de retorno.

## 14.1 Sequência principal

```text
RETORNO
  ↓
RECEBIMENTO
  ↓
QUARENTENA
  ↓
LIMPEZA
  ↓
IDENTIFICAÇÃO / CHECKLIST DE AVARIAS
  ↓
DIAGNÓSTICO
  ↓
DEFINIÇÃO DE INTERVENÇÃO
  ↓
MATERIAL DISPONÍVEL?
  ↙              ↘
SIM              NÃO
 ↓                 ↓
OFICINA         ALMOXARIFADO/COMPRAS
 ↘                 ↙
       REPARO
          ↓
       TESTES
          ↓
   QUALIDADE APROVADA?
       ↙          ↘
     SIM          NÃO
      ↓             ↓
ESTOQUE SEG.    RETRABALHO
      ↓             │
      └─────────────┘
```

## 14.2 Quarentena

Objetivo: impedir que o módulo seja tratado como disponível antes da avaliação.

Dados mínimos:

- ID do módulo;
- AF/origem quando disponível;
- modelo;
- configuração;
- data de retorno;
- localização;
- condição inicial;
- responsável pelo recebimento.

## 14.3 Limpeza

Preparar o módulo para inspeção e intervenção, registrando quando necessário:

- entrada;
- conclusão;
- equipe;
- observações;
- condições encontradas.

## 14.4 Checklist de avarias

Registrar por ocorrência:

- ID da avaria;
- módulo;
- modelo;
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

## 14.5 Diagnóstico

```text
Avaria identificada
→ avaliar causa provável
→ definir intervenção
→ definir oficina/recurso
→ verificar material
→ programar reparo
```

## 14.6 Oficinas

As oficinas devem ser tratadas como capacidades produtivas. O registro deve permitir saber:

- qual oficina executou;
- equipe;
- número de pessoas;
- início;
- fim;
- horas;
- etapa;
- retrabalho;
- motivo do retrabalho.

## 14.7 Materiais do reparo

Registrar:

- código;
- material;
- unidade;
- quantidade;
- custo unitário;
- custo total;
- requisição;
- origem;
- módulo;
- modelo;
- avaria.

Isso permite construir posteriormente:

`modelo → avaria → material → custo → horas → resultado`.

## 14.8 Testes de qualidade

Registrar:

- item testado;
- critério;
- resultado;
- evidência;
- necessidade de retrabalho;
- reinspeção;
- resultado final.

## 14.9 Liberação

Somente após resultado compatível com os critérios definidos:

`Qualidade → Pronto → Estoque de Segurança`, quando aplicável.

---

# 15. FLUXO 12 — ESTOQUE DE SEGURANÇA

O estoque de segurança deve ser tratado como consequência de análise de demanda, retorno, disponibilidade e capacidade de recuperação.

Não assumir percentual ou quantidade mínima sem apuração.

## 15.1 Estados

```text
QUARENTENA
EM REPARO
EM QUALIDADE
PRONTO
ESTOQUE SEGURANÇA
```

## 15.2 Informação mínima

- modelo;
- configuração;
- quantidade em cada estado;
- estoque mínimo validado;
- gap;
- prioridade;
- localização;
- data da atualização.

## 15.3 Decisão ELO

O ELO pode sinalizar:

`demanda futura + estoque disponível + módulos em recuperação + capacidade de reparo → risco de disponibilidade`

A decisão de estoque mínimo deve permanecer baseada em evidência e governança.

---

# 16. FLUXO DE RETORNO DO REPARO PARA O PCP

O reparo não termina no estoque. O dado retorna ao planejamento.

```text
AVARIA
 ↓
MODELO
 ↓
CAUSA / COMPONENTE
 ↓
TEMPO DE REPARO
 ↓
MATERIAL CONSUMIDO
 ↓
CUSTO
 ↓
QUALIDADE
 ↓
DISPONIBILIDADE RECUPERADA
 ↓
ESTOQUE
 ↓
PCP
```

Isso permite ao ELO relacionar o comportamento de reparos com:

- demanda;
- modelo;
- customização;
- almoxarifado;
- produção;
- qualidade;
- RH/capacidade;
- orçamento;
- locação.

---

# 17. MAPA DE DADOS POR SETOR

| Setor | Dados que alimentam o ELO |
|---|---|
| Comercial/Locação | AF, demanda, modalidade, prazo, alterações |
| Orçamento | modelo, customização, excedentes, materiais, custos, recorrência |
| Engenharia | projeto, configuração, BOM, requisitos, liberação técnica |
| PCP | plano, sequência, capacidade, prioridade, realizado, desvio |
| Compras | fornecedor, pedido, lead time, atraso, material crítico |
| Almoxarifado | estoque, reserva, picking, consumo, ruptura, requisição |
| Produção | etapas, tempos, quantidade, WIP, produtividade, retrabalho |
| Oficinas | capacidade, equipe, horas, reparos, fila |
| Qualidade | testes, falhas, aprovação, retrabalho |
| Expedição | packing, conferência, gate, saída |
| Campo/Locação | montagem, uso, ocorrências, desmobilização, retorno |
| Reparos | avarias, diagnóstico, materiais, custo, horas, resultado |
| RH | disponibilidade/capacidade de pessoas, quando autorizado e necessário |

---

# 18. MAPA DE DECISÕES

```text
AF recebida?
→ sim: analisar
→ não: aguardar informação

Padrão ou personalizado?
→ padrão: fluxo modular
→ personalizado: fluxo customizado

Material disponível?
→ sim: picking/abastecimento
→ não: compras

Capacidade disponível?
→ sim: sequenciar
→ não: replanejar/escalar

Produto conforme?
→ sim: liberar
→ não: reparar/retrabalhar

Avaria no retorno?
→ não: estoque
→ sim: quarentena/diagnóstico/reparo

Reparo concluído?
→ sim: qualidade
→ não: permanecer em reparo

Qualidade aprovada?
→ sim: estoque segurança/pronto
→ não: retrabalho
```

---

# 19. COMO O ELO DEVE RESPONDER A PESQUISAS SOBRE O FLUXO

Quando o usuário perguntar genericamente:

> "Qual é o fluxo da Multiteiner?"

O ELO deve recuperar primeiro a visão macro e depois oferecer a decomposição por subprocesso.

Quando perguntar:

> "Como funciona o PCP?"

Recuperar a seção PCP e as interfaces com Comercial, Orçamento, Almoxarifado, Produção, Qualidade, Expedição e Reparos.

Quando perguntar:

> "Qual o fluxo de reparo?"

Recuperar diretamente:

`Retorno → Recebimento → Quarentena → Limpeza → Checklist → Diagnóstico → Material → Oficinas → Testes → Qualidade → Estoque de Segurança / Retrabalho`.

Quando perguntar:

> "Como o reparo conversa com o Almoxarifado?"

Recuperar o vínculo:

`Avaria → diagnóstico → material necessário → disponibilidade → requisição/compra → consumo → custo → resultado`.

Quando perguntar:

> "Como o orçamento conversa com o PCP?"

Recuperar:

`demanda/customização → modelo/configuração → excedentes → materiais/serviços → custo/carga → planejamento`.

---

# 20. REGRAS DE RETRIEVAL / INDEXAÇÃO

## 20.1 Termos canônicos

O conteúdo deve ser indexado pelos seguintes conceitos:

`Multiteiner`, `fluxo Multiteiner`, `processo Multiteiner`, `fluxo end-to-end`, `PCP`, `planejamento`, `AF`, `Comercial`, `Locação`, `Orçamento`, `Customizado`, `Modular`, `Almoxarifado`, `Compras`, `Produção`, `Qualidade`, `Expedição`, `Retorno`, `Pós-locação`, `Quarentena`, `Limpeza`, `Avaria`, `Diagnóstico`, `Reparo`, `Oficina`, `Teste`, `Estoque de Segurança`.

## 20.2 Sinônimos de busca

- fluxo modular = produção modular = linha modular = fluxo puxado modular;
- fluxo customizado = montagem customizada = módulo personalizado;
- retorno = pós-locação = retorno de módulo/ativo;
- reparo = recuperação = reprocesso, quando o contexto indicar;
- quarentena = módulo em quarentena;
- estoque de segurança = reserva de módulos recuperados, somente quando o contexto confirmar a intenção.

## 20.3 Recuperação hierárquica

O ELO deve preferir:

1. processo específico;
2. etapa específica;
3. interface entre etapas;
4. visão macro;
5. contexto organizacional geral.

Não retornar apenas um fragmento quando a pergunta solicitar o fluxo completo.

## 20.4 Provenance

Cada resposta baseada neste documento deve manter a referência ao artefato `ELO-PROC-MULTITEINER-001` e, quando necessário, indicar que determinado detalhe está `A VALIDAR`.

## 20.5 Contradições

Se outra fonte apresentar sequência diferente:

```text
detectar contradição
→ identificar fontes
→ comparar autoridade
→ verificar versão/data
→ preservar ambas como evidência quando necessário
→ solicitar validação
```

Não sobrescrever silenciosamente o fluxo.

---

# 21. RELAÇÃO COM O ELO

O ELO deve usar este documento como **conhecimento de processo**, não como lógica rígida de execução.

A interpretação deve seguir:

```text
PERGUNTA
  ↓
CONTEXTO
  ↓
RECUPERAÇÃO DO PROCESSO
  ↓
ETAPA(S) RELEVANTE(S)
  ↓
DADOS ATUAIS
  ↓
EVIDÊNCIAS
  ↓
ANÁLISE
  ↓
RESPOSTA / ORIENTAÇÃO
```

O fluxo documentado informa **como o processo é representado**. Dados operacionais atuais informam **como o processo está acontecendo agora**.

Essa distinção é obrigatória para que o ELO não confunda desenho de processo com estado operacional atual.

---

# 22. CICLO COGNITIVO APLICADO AO PROCESSO

Para análise de uma ocorrência no fluxo:

```text
OBSERVE
→ DETECT
→ CORRELATE
→ CONTEXTUALIZE
→ IDENTIFY GAPS
→ ASK
→ RETRIEVE
→ COMPARE EXPERIENCES
→ FORM HYPOTHESES
→ GATHER EVIDENCE
→ REASON
→ SIMULATE SCENARIOS
→ RECOMMEND
→ HUMAN DECISION
→ OBSERVE OUTCOME
→ LEARN
```

O ELO deve separar processo documentado, dado atual, hipótese, evidência, recomendação e decisão humana.

---

# 23. PRÓXIMA EVOLUÇÃO DO ARTEFATO

Este documento deve evoluir de `DRAFT` para níveis superiores somente quando houver evidência de validação operacional.

Próximas informações desejáveis:

- tempos reais por etapa;
- responsáveis formais;
- sistemas utilizados em cada gate;
- critérios de entrada e saída;
- capacidade por recurso;
- regras de prioridade;
- critérios de qualidade;
- dados reais de reparo;
- custos reais;
- relação modelo × avaria;
- estoque de segurança calculado a partir de histórico;
- evidências de aderência entre fluxo documentado e fluxo realizado.

Nenhum desses dados deve ser preenchido por estimativa apresentada como fato.
