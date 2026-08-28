# ELO — PADRÃO CANÔNICO DE RETORNO

## 1. Finalidade

Definir o retorno obrigatório do ELO para `ELO APRENDER` e para consultas posteriores sobre uma Solicitação de Orçamento (SO).

## 2. Retorno consolidado obrigatório

Quando o usuário solicitar `ELO APRENDER` ou `ELO — o que sabemos sobre a SO X`, o ELO deve consultar e consolidar, preservando a origem de cada camada:

1. Identificação da SO, cliente, objeto, contratação, local e quantitativos disponíveis;
2. SO/TR e demais documentos de origem;
3. PTS Técnica;
4. tratamento e resolução do orçamento;
5. excedentes, customizações e composições;
6. PTS Pós-Orçamento;
7. incongruências, decisões e soluções adotadas;
8. conhecimento cognitivo/instrucional aprendido → Git;
9. memória quantitativa/de cálculo → Supabase;
10. referências de outras SOs, sempre identificadas como referências consultivas;
11. aplicabilidade, limitações e validações necessárias.

O ELO não deve retornar somente o conhecimento textual quando houver memória de cálculo persistida.

## 3. Memória de cálculo — formato canônico

Quando houver registros no Supabase, apresentar a memória em tabela com esta ordem obrigatória:

| ID | ID Memória | Categoria | Item | Fonte | Entrada/Base | Unidade | Parâmetro/Premissa | Fórmula | Subcálculo | Resultado | Unidade Resultado | Validação | Origem |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

A memória deve permitir reconstruir o raciocínio:

`FONTE → DADO ENCONTRADO → PARÂMETRO/PREMISSA → ID → ID MEMÓRIA → FÓRMULA → SUBCÁLCULOS → QUANTITATIVO RESULTANTE → COMPOSIÇÃO → CUSTO → VALIDAÇÃO → ORIGEM`

Não apresentar apenas o número final.

## 4. Separação canônica de armazenamento

- **Git:** conhecimento cognitivo, instruções, critérios, decisões, precedentes e aprendizados do Especialista de Orçamento.
- **Supabase:** memória quantitativa e cálculos estruturados, seus IDs, evidências, parâmetros, fórmulas, subcálculos, resultados e validações.
- **Documentos da SO:** fontes para reconstrução da experiência.

O fluxo de cálculo já definido deve ser executado como subfluxo obrigatório de `ELO APRENDER` para SOs de orçamento; ele não substitui o fluxo cognitivo do Git.

## 5. Fonte e referência

Uma informação recuperada de outra SO nunca pode ser apresentada como origem da SO atual.

O retorno deve mostrar:

- SO/documento de origem;
- informação recuperada;
- item/conceito;
- características relevantes;
- motivo da comparação;
- motivo pelo qual pode se aplicar;
- equivalências e diferenças;
- premissas;
- validação necessária.

Exemplo de linguagem obrigatória:

> `Referência consultiva da SO 155.26. Pode ser considerada porque possui características técnicas equivalentes, unidade compatível e referência temporal adequada. Validar dimensões, material, espessura, especificação e contexto antes da aplicação.`

A referência nunca altera a origem do cálculo ou aprendizado.

## 6. Estados da memória de cálculo

Quando aplicável, usar:

- `CALCULATION_CONFIRMED`;
- `CALCULATION_PARTIAL`;
- `CALCULATION_REFERENCE`;
- `CALCULATION_NOT_RECONSTRUCTABLE`;
- `NO_CALCULATION_FOUND`.

Se não houver cálculo localizado, informar explicitamente `NO_CALCULATION_FOUND`. Nunca inventar memória.

## 7. Consulta posterior

Ao pedir informações sobre uma SO, o ELO deve consultar simultaneamente:

`GIT → conhecimento cognitivo`

`SUPABASE → memória de cálculo`

E apresentar um retorno integrado, sem perder a separação de origem.

## 8. Laboratório

O Laboratório é um subfluxo independente. Só deve ser executado quando o usuário chamar explicitamente o Laboratório. A consulta normal de `ELO APRENDER` ou `ELO — informações` não deve acioná-lo automaticamente.

## 9. Critério de completude

O retorno de uma SO de orçamento é considerado completo somente quando o ELO tiver verificado as duas camadas aplicáveis:

`CONHECIMENTO COGNITIVO + MEMÓRIA DE CÁLCULO`

Se uma delas não possuir informação, declarar a ausência, sem fabricar dados.

## 10. Destino dos novos aprendizados

Todo aprendizado pertencente ao domínio do Especialista de Orçamento originado de uma SO deve ser criado ou consolidado exclusivamente em:

`08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/`

Não criar novos aprendizados de orçamento em `memory/solicitations/`, `memory/solicitations_learning/`, `04-knowledge-handbook/` ou outros destinos paralelos.

Registros históricos nesses locais podem ser fontes legadas para migração/consolidação, preservando sua proveniência.
