# ELO — VIEW DE CONSULTA DE SO

## Finalidade

Criar uma camada independente de consulta e apresentação para informações já aprendidas sobre uma Solicitação de Orçamento (SO), sem alterar o fluxo `ELO APRENDER`.

## Gatilho canônico

Quando o usuário solicitar:

`ELO SOBRE SO XXX.XX`

interpretar como consulta estruturada da SO, utilizando o conhecimento já persistido no Git e a memória quantitativa/cálculos disponíveis no Supabase.

Este gatilho NÃO inicia novo aprendizado por si só e NÃO deve substituir, modificar ou duplicar o fluxo de `ELO APRENDER`.

## Fluxo

```text
SO solicitada
↓
consultar conhecimento cognitivo no Git
↓
consultar memória quantitativa no Supabase
↓
relacionar os registros pela SO e origem
↓
organizar os dados
↓
apresentar retorno canônico
```

## Regra de separação

- `ELO APRENDER`: aprende, reconstrói, valida e grava.
- `ELO SOBRE SO XXX.XX`: consulta, consolida e apresenta.
- A VIEW não deve gravar novamente um conhecimento já existente como se fosse novo aprendizado.
- A VIEW não deve alterar registros do Supabase.
- A VIEW não deve alterar regras cognitivas do Git.
- A VIEW não deve criar arquitetura paralela de armazenamento.

## Retorno obrigatório

### 1. ANÁLISE COGNITIVA DO ORÇAMENTO

Apresentar tabela visual:

| PARÂMETRO | IDENTIFICADO NA SO/TR | ADOTADO / RESULTADO |
|---|---|---|
| Cliente / órgão | | |
| Objeto | | |
| Local | | |
| Quantidade total | | |
| Composição original | | |
| Complementações | | |
| Exigências da TR | | |
| Produto / modelo | | |
| Equivalências | | |
| Diferenças | | |
| Excedentes | | |
| Adaptações | | |
| Itens de maior impacto | | |
| Riscos da TR | | |
| Riscos contratuais | | |
| Riscos orçamentários | | |
| Substituições sugeridas | | |
| Decisões do orçamentista | | |
| Premissas relevantes | | |

O objetivo é apresentar visualmente quem é o orçamento, o que foi solicitado, o que foi adotado, o que foi alterado, os riscos, os impactos e as decisões.

### 2. REGISTRO ESTRUTURADO — SUPABASE

Quando houver memória quantitativa/cálculo, apresentar obrigatoriamente:

| ID | ID Memória | Categoria | Item | Fonte | Entrada/Base | Unidade | Parâmetro/Premissa | Fórmula | Subcálculo | Resultado | Unidade Resultado | Validação | Origem |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Não apresentar somente o resultado. Preservar a cadeia:

`FONTE → ENTRADA → PARÂMETRO/PREMISSA → FÓRMULA → SUBCÁLCULO → RESULTADO → VALIDAÇÃO → ORIGEM`

### 3. CONCLUSÃO APLICADA — INTELIGÊNCIA DO ELO

Apresentar:

| CONHECIMENTO APRENDIDO | REGRA EXTRAÍDA | CONDIÇÃO DE REUTILIZAÇÃO | EXEMPLO DE APLICAÇÃO |
|---|---|---|---|
| | | | |

A conclusão deve transformar o conhecimento já armazenado em orientação aplicável a futuras SOs. Não deve inventar regras ausentes no conhecimento consultado.

### 4. HISTÓRICO DE APRENDIZADO

Apresentar:

| SO | CONHECIMENTO | PRECEDENTE | REGRA REUTILIZÁVEL | VALIDAÇÃO | GIT | SUPABASE |
|---|---|---|---|---|---|---|
| | | | | | | |

## Regra para precedentes

Quando o conhecimento de outra SO aparecer, identificar explicitamente sua origem. A VIEW pode apresentar o precedente, mas não deve tratá-lo como dado da SO consultada.

Antes de sugerir aplicação de um precedente, apresentar, quando disponível:

- SO de origem;
- conceito;
- variáveis;
- motivo da comparação;
- equivalências;
- diferenças;
- condição de reutilização;
- necessidade de validação.

## Ausência de dados

Se o Git não possuir conhecimento para a SO, informar:

`CONHECIMENTO COGNITIVO NÃO LOCALIZADO.`

Se o Supabase não possuir memória aplicável, informar:

`MEMÓRIA DE CÁLCULO NÃO LOCALIZADA.`

Nunca preencher lacunas com informação inventada.

## Princípio

A VIEW é uma camada de leitura e apresentação. O aprendizado permanece no fluxo existente.

```text
ELO APRENDER
→ grava conhecimento e memória

ELO SOBRE SO XXX.XX
→ consulta conhecimento e memória
→ organiza
→ apresenta
```

O formato da VIEW pode evoluir sem alterar o mecanismo de aprendizado.