# ELO APRENDER — Regra de acionamento do Laboratório Virtual

## Regra canônica

O Laboratório Virtual é um subfluxo de validação e **somente deve ser executado quando for explicitamente chamado**.

A execução de `ELO APRENDER`, por si só, **não autoriza nem dispara o Laboratório Virtual**.

## Separação das funções

### ELO APRENDER

Quando acionado para uma Solicitação de Orçamento, deve:

- analisar a experiência da SO e documentos associados;
- consolidar o conhecimento cognitivo/instrucional;
- direcionar conhecimento cognitivo para o Git;
- extrair e reconstruir memórias de cálculo;
- direcionar memórias quantitativas estruturadas para o Supabase;
- preservar origem, fonte, evidência, parâmetros, fórmulas, subcálculos, resultados e validação;
- não executar testes de laboratório salvo se o Laboratório tiver sido explicitamente chamado.

### LABORATÓRIO VIRTUAL

Somente quando explicitamente chamado, deve:

- testar o conhecimento produzido;
- testar as memórias de cálculo produzidas;
- executar regressão, casos históricos, cenários, consistência e duplicidade conforme aplicável;
- registrar falhas em ISSUE quando houver;
- permitir aprovação somente após os testes aplicáveis passarem;
- retornar o resultado do teste e suas evidências.

## Regra operacional

```text
SE LABORATÓRIO FOI EXPLICITAMENTE CHAMADO
    executar os testes aplicáveis
SENÃO
    não executar o Laboratório
```

## Aplicabilidade

Esta regra é geral para todas as Solicitações de Orçamento elegíveis e não é específica da SO 155.26. A SO 155.26 pode ser utilizada como caso de teste, mas não define o escopo do mecanismo.

## Condição de não execução

Nunca interpretar a existência de uma memória de cálculo, um aprendizado, uma nova SO ou uma execução do `ELO APRENDER` como autorização implícita para testar no Laboratório.

## Critério de rastreabilidade

Quando o Laboratório for chamado, o teste deve identificar a SO/unidade de aprendizado avaliada e separar claramente:

- conhecimento consultado/produzido no Git;
- memória de cálculo consultada/produzida no Supabase;
- casos e cenários utilizados no teste;
- resultado de cada teste;
- ISSUE gerada, se aplicável;
- aprovação/reprovação.

## Regra de governança

O Laboratório valida; ele não substitui a etapa de aprendizado. O fato de um teste ser aprovado não altera automaticamente a classificação de conhecimento sem passar pelas regras de governança do ELO.
