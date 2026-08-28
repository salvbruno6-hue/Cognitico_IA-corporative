# ELO APRENDER — Retorno Estruturado de Memória de Cálculo

## Padrão operacional

Toda chamada `ELO APRENDER` que recuperar informações persistidas deve retornar a cadeia completa:

**ID → ID Memória → Categoria → Item → Fonte → Entrada/Base → Unidade → Parâmetro/Premissa → Fórmula → Subcálculo → Resultado → Unidade Resultado → Validação → Origem**

## Regras

1. O **ID** retornado deve ser o identificador persistido no Supabase e nunca deve ser inventado ou reutilizado.
2. O **ID Memória** deve manter o vínculo direto com a memória que gerou o cálculo.
3. Parâmetros e premissas devem retornar junto com a memória de cálculo.
4. Fórmula e subcálculo devem permitir reconstruir o resultado.
5. O resultado deve apresentar o quantitativo ou valor efetivamente obtido e sua unidade.
6. A validação só pode ser declarada quando a memória puder ser reconstruída a partir dos dados persistidos.
7. Fonte/origem deve permanecer vinculada ao registro.
8. Se houver registro incompleto, vínculo ausente ou cálculo não reconstruível, retornar **NÃO VALIDADO** e apontar a inconsistência.
9. O retorno não deve reduzir a informação persistida a uma simples lista de resultados.
10. O mesmo padrão deve ser utilizado em todos os orçamentos e solicitações processados pelo ELO.

## Estrutura de retorno

| ID | ID Memória | Categoria | Item | Fonte | Entrada/Base | Unidade | Parâmetro/Premissa | Fórmula | Subcálculo | Resultado | Unidade Resultado | Validação | Origem |
|---:|---:|---|---|---|---|---|---|---|---|---|---|---|---|

## Regra de validação

O ELO APRENDER deve considerar a informação válida somente após verificar:

**registro → ID → memória → parâmetros → fórmula → subcálculo → resultado → evidência/origem → reconstrução**.

O retorno textual `SALVO` ou `VALIDADO` nunca substitui a conferência da persistência.

## Aplicação

Este padrão deve ser aplicado à recuperação de aprendizados, parâmetros de cálculo e memórias de cálculo de todas as SOs, mantendo rastreabilidade individual e permitindo auditoria e reconstrução do cálculo original.
