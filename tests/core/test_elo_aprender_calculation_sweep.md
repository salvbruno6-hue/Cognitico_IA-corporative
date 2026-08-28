# ELO APRENDER — Testes de aceitação do VARRER_CÁLCULOS

## Caso 1 — excedente de telhado
Entrada: orçamento contém composição/dimensionamento de estrutura de cobertura como excedente.
Esperado: cálculo identificado, reconstruído, fonte/premissas preservadas e `calculation_id` registrado no Supabase.

## Caso 2 — esgoto subterrâneo
Entrada: PTS/orçamento contém dimensionamento ou composição de instalação subterrânea.
Esperado: cálculo extraído e registrado, sem transformar o cálculo em instrução Git.

## Caso 3 — elétrica aérea
Entrada: orçamento contém quantitativo/composição de instalação elétrica aérea.
Esperado: cálculo extraído, validado quanto à evidência disponível e registrado no Supabase.

## Caso 4 — reforço estrutural
Entrada: documento contém cálculo ou quantitativo derivado para reforço.
Esperado: memória de cálculo separada da instrução e vinculada à SO de origem.

## Caso 5 — cálculo inexistente
Entrada: apenas um preço isolado sem fórmula, premissa ou evidência de cálculo.
Esperado: não inventar memória de cálculo.

## Caso 6 — duplicidade
Entrada: o mesmo cálculo aparece na PTS e no orçamento.
Esperado: um único cálculo persistido, com múltiplas evidências.

## Caso 7 — referência de outra SO
Entrada: cálculo de SO anterior é consultado para uma nova SO.
Esperado: manter a SO anterior como origem; registrar aplicação como referência consultiva, com justificativa de equivalência e validação necessária.

## Caso 8 — falha de persistência
Entrada: cálculo identificado, mas Supabase indisponível.
Esperado: `CALCULATION_NOT_REGISTERED`; experiência não pode ser marcada como plenamente consolidada.

## Caso 9 — preservação do fluxo cognitivo
Entrada: ELO APRENDER encontra cálculo e também novo conceito/instrução.
Esperado: cálculo segue para Supabase e conhecimento/instrução segue para Git; nenhum dos fluxos substitui o outro.