# FABRICAÇÃO CUSTOMIZADA — MAPA DE CAMPOS E GAPS DE INTEGRAÇÃO

## Objetivo

Este documento transforma a investigação da fabricação customizada em uma ficha de trabalho para o ELO e para o especialista.

A regra é:

`processo real → campo existente → fonte → evidência → validação → inserção`

Não se deve criar um significado para um campo apenas pelo nome.

## 1. Entrada da customização

### `mt_pedidos_venda_itens`

| Campo | Papel a investigar | Pergunta ao especialista | Evidência |
|---|---|---|---|
| `id` | Identidade do item | Qual item da AF está sendo customizado? | pedido/item |
| `pedido_venda_id` | Origem comercial | Qual pedido originou a demanda? | pedido |
| `modelo_id` | Modelo base | Qual modelo serve de base? | cadastro/projeto |
| `lista_mae_id` | Estrutura material | Qual L.M. está associada ao item? | L.M. |
| `quantidade` | Demanda | Quantas unidades foram solicitadas? | AF/pedido |
| `data_solicitada` | Prazo solicitado | Qual data foi solicitada? | AF/pedido |
| `personalizado` | Indicador de customização | Qual regra determina verdadeiro/falso? | pedido/projeto |
| `status_personalizacao` | Estado da customização | Quais estados são usados e quem altera? | processo aprovado |
| `observacoes` | Informação complementar | O que precisa ser registrado aqui e o que deve ir para documento específico? | fonte identificada |

**Regra:** `personalizado = true` só deve representar customização conforme a regra validada pelo especialista. O ELO não deve inferir isso pela descrição.

---

## 2. Versão do roteiro personalizado

### `mt_versoes_roteiro_personalizado`

| Campo | Papel |
|---|---|
| `id` | Identidade da versão |
| `tenant_id` | Contexto organizacional |
| `pedido_venda_item_id` | vínculo da versão ao item comercial |
| `modelo_base_id` | modelo de referência |
| `versao` | identificação/versionamento |
| `status` | estado da versão |
| `aprovado_em` | evidência temporal da aprovação |
| `aprovado_por` | responsável pela aprovação |
| `observacoes` | informação complementar |

### Perguntas obrigatórias

- O que gera uma nova versão?
- Quem pode criar?
- Quem pode alterar?
- Quais estados existem?
- O que significa cada estado?
- O que torna uma versão apta para produção?
- Uma versão aprovada pode ser alterada?
- Se houver alteração, gera nova versão?
- Onde fica registrada a justificativa da alteração?

### Regra do ELO

Uma versão aprovada **não significa que a produção ocorreu**. Ela significa apenas que existe uma configuração de roteiro aprovada, conforme o significado confirmado pelo especialista.

---

## 3. Operações do roteiro personalizado

### `mt_operacoes_roteiro_personalizado`

Campos atuais confirmados:

- `roteiro_personalizado_id`
- `sequencia`
- `codigo_operacao`
- `nome_operacao`
- `centro_trabalho_id`
- `minutos_padrao`
- `minutos_setup`

### O especialista precisa definir

| Informação | Pergunta |
|---|---|
| Sequência | Qual é a ordem real das operações? |
| Código | Como o código é definido? |
| Nome | Qual é o nome operacional usado no chão de fábrica? |
| Centro | Qual centro executa? |
| Tempo padrão | Como o tempo é definido? |
| Setup | O que está incluído no setup? |

### Customização da operação

O ELO deve registrar se a operação é:

- mantida do padrão;
- nova;
- removida;
- alterada;
- reordenada.

Isso é uma **classificação de processo que precisa ser ensinada pelo especialista**; não existe hoje, nesses campos confirmados, um campo específico que represente automaticamente essa classificação.

---

# 4. Passagem para a Ordem de Produção

### `mt_ordens_producao`

Campos relevantes:

- `linha_plano_pcp_id`
- `modelo_id`
- `bom_versao_id`
- `quantidade_planejada`
- `quantidade_produzida`
- `status`
- `inicio_planejado`
- `fim_planejado`
- `inicio_real`
- `fim_real`

A OP está fisicamente vinculada à linha do PCP e ao modelo.

`bom_versao_id` referencia `mt_versoes_bom`.

### Perguntas ao especialista

- Como uma versão personalizada chega à OP?
- A OP utiliza uma BOM personalizada?
- Quem cria essa relação?
- Como a OP identifica que é customizada?
- Existe algum documento que acompanha a OP?
- Uma mesma OP pode conter itens customizados e padrão?
- A customização altera quantidade, prazo ou capacidade?

---

# 5. GAP FÍSICO CONFIRMADO

Foi verificado diretamente no Supabase:

`mt_operacoes_ordem_producao.operacao_roteiro_id`

possui FK para:

`mt_operacoes_roteiro.id`

e **não** para:

`mt_operacoes_roteiro_personalizado.id`

Portanto, atualmente não existe uma FK física direta:

`OP → operação de roteiro personalizado`

### Consequência

Não devemos afirmar que:

`mt_operacoes_roteiro_personalizado → mt_operacoes_ordem_producao`

já está integrado fisicamente.

A relação é uma **necessidade conceitual do fluxo customizado que precisa ser resolvida/validada pela arquitetura do banco**.

### O ELO deve fazer o quê?

Até a resolução desse gap:

1. identificar a customização;
2. registrar a versão personalizada;
3. registrar suas operações;
4. registrar a OP;
5. registrar a execução onde o schema atualmente permite;
6. apontar a ausência da relação física;
7. não fabricar uma FK lógica escondida;
8. não copiar dados para outra tabela apenas para “fechar” o fluxo.

---

# 6. Execução real

### `mt_operacoes_ordem_producao`

Campos:

- `quantidade_planejada`
- `quantidade_concluida`
- `inicio_planejado`
- `fim_planejado`
- `inicio_real`
- `fim_real`
- `status`

Esses campos permitem o confronto planejado × realizado **da operação registrada na OP**.

Mas o vínculo atual aponta para roteiro padrão.

### `mt_eventos_fluxo_modular`

Campos:

- `unidade_modular_id`
- `centro_trabalho_id`
- `nome_operacao`
- `tipo_evento`
- `inicio`
- `fim`
- `quantidade`
- `status`
- `operador_id`
- `observacoes`

Esses registros são candidatos a evidência operacional do realizado, conforme validação do especialista.

O ELO deve descobrir com o especialista qual evento significa:

- início;
- execução;
- pausa;
- conclusão;
- retrabalho;
- parada;
- liberação.

Não assumir esses significados pelo nome do campo.

---

# 7. Qualidade

### `mt_inspecoes`

Campos confirmados:

- `unidade_modular_id`
- `pedido_venda_id`
- `tipo_inspecao`
- `status`
- `inspecionado_em`
- `inspetor_id`
- `referencia_checklist`
- `observacoes`

### `mt_nao_conformidades`

Campos confirmados:

- `inspecao_id`
- `unidade_modular_id`
- `tipo_nao_conformidade_id`
- `codigo`
- `descricao`
- `severidade`
- `status`
- `detectada_em`
- `encerrada_em`

Existe uma FK de não conformidade para inspeção.

A cadeia operacional a investigar é:

`customização → produção → inspeção → não conformidade → recuperação → nova inspeção/liberação`

O ELO deve confirmar com o especialista se essa é efetivamente a sequência usada na operação.

---

# 8. Ficha de orientação que o ELO deverá aplicar

Para cada campo:

### Pergunta

> O que este campo representa no seu processo?

### Fonte

> De onde vem essa informação?

### Momento

> Quando ela deve ser registrada?

### Responsável

> Quem possui autoridade para informar ou alterar?

### Evidência

> Qual documento/evento comprova?

### Validação

> Como sabemos que o valor está correto?

### Relação

> Qual outra tabela precisa reconhecer essa informação?

### Resultado

`VALIDADO | INCOMPLETO | DIVERGENTE | NÃO LOCALIZADO`

---

# 9. Resultado esperado da sessão com especialista

O ELO deverá sair de cada sessão com:

`PROCESSO COMPREENDIDO`

↓

`CAMPOS MAPEADOS`

↓

`FONTES IDENTIFICADAS`

↓

`RESPONSÁVEIS IDENTIFICADOS`

↓

`REGRAS VALIDADAS`

↓

`GAPS IDENTIFICADOS`

↓

`INSERÇÃO ORIENTADA`

O aprendizado permanente somente poderá ocorrer depois do fluxo de governança já estabelecido.

## Estado deste estudo

**Compreendido:** estrutura das tabelas e principais campos.

**Confirmado:** vínculo do pedido/item com o roteiro personalizado e vínculo das operações personalizadas com sua versão.

**Gap confirmado:** operação da OP aponta fisicamente para `mt_operacoes_roteiro`, não para `mt_operacoes_roteiro_personalizado`.

**Ainda precisa do especialista:** significado operacional dos status, critérios de customização, regras de aprovação, execução real e tratamento das alterações durante fabricação.
