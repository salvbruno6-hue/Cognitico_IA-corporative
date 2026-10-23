# ELO — Reconciliação contextual dos reparos MT

Data: 2026-10-23

## Objetivo

Qualificar corretamente o estado dos 133 reparos legados sem transformar ausência de `tenant_id` em ausência de contexto empresarial.

## Evidência ao vivo

- 133 reparos persistidos;
- 133/133 com identificador no padrão `MLTM + numérico`;
- 132/133 com seis dígitos após o prefixo;
- 124 identificadores físicos distintos;
- 103/133 linhas mapeiam para modelo canônico ativo quando a normalização aceita tanto `Mxx` quanto `MLT.Mxx`;
- 97 identificadores distintos pertencem a esse grupo já reconhecido;
- 30/133 linhas, correspondendo a 27 identificadores, apontam para códigos de modelo ainda não representados no cadastro canônico atual;
- `mt_unidades_modulares` possui 0 linhas;
- portanto 0/133 reparos possuem correspondência física canônica disponível;
- 133/133 continuam com `unidade_modular_id` nulo;
- 133/133 continuam com `tenant_id` nulo;
- 0/133 possuem proveniência persistida em `mt_proveniencia_registros`.

## Interpretação governada

`tenant_id IS NULL` não deve ser apresentado isoladamente como se os reparos fossem dados sem contexto Multiteiner.

A classificação adequada é:

`CONTEXT_CONFIRMED_PERSISTENCE_PENDING`

O conjunto possui forte identidade operacional/contextual, mas ainda não possui materialização de unidade física nem proveniência suficiente para promover automaticamente vínculo persistente de tenant.

## Correção do probe

O health probe existente `supabase/health/elo_mt_repair_provenance_gap.sql` foi estendido em vez de criar estrutura paralela.

A correção:

1. normaliza o código de modelo extraído do identificador;
2. reconhece tanto `Mxx` quanto `MLT.Mxx` no cadastro canônico;
3. mede identificadores com e sem modelo canônico;
4. mede correspondência real com `mt_unidades_modulares`;
5. expõe explicitamente `CONTEXT_CONFIRMED_PERSISTENCE_PENDING`;
6. preserva `GAP_HIGH` enquanto unidade física/proveniência não forem reconciliadas;
7. não cria unidades, modelos, tenant links ou proveniência retroativa.

## Próximo gate

O próximo avanço seguro é investigar a materialização das 124 unidades físicas e os 3 códigos de modelo do conjunto que ainda não possuem representação canônica suficiente, sem fabricar registros ou inferir classificação textual conflitante.
