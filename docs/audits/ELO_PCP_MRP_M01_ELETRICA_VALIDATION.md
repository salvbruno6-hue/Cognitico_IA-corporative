# ELO PCP — Validação da ampliação do MRP bruto M01 para elétrica

## Objeto afetado

`public.v_elo_pcp_mrp_requisito_fisico_m01`.

## Estado anterior

O read-model cobria 37 linhas em quatro processos: estrutura metálica, montagem M01, piso vinílico e telha de fibra.

## Evidência reutilizada

`public.vw_kit_eletrico_m01_completo`:

- 30 itens ativos;
- 30/30 com quantidade explícita;
- 30/30 com código de produto disponível;
- 25 linhas sem ressalva impeditiva para necessidade bruta;
- 4 linhas com evidência parcial;
- 1 linha em conflito de vínculo (`SEM_CORRESPONDÊNCIA`).

## Alteração

A mesma view de MRP bruto passa a incluir `ELETRICA_M01`, sem criar BOM paralela.

Classificações:

- `NECESSIDADE_BRUTA_CALCULADA` — consumo localizado sem ressalva impeditiva;
- `CALCULO_BRUTO_COM_GAP_CADASTRO_NAO_PROMOVER` — consumo conhecido, porém item sem `cod_produt`;
- `CALCULO_REFERENCIAL_PARCIAL_NAO_PROMOVER` — evidência elétrica parcial;
- `CALCULO_REFERENCIAL_CONFLITO_NAO_PROMOVER` — conflito de vínculo.

## Testes

Estado pós-migração:

- 67 linhas totais;
- 56 necessidades brutas calculadas sem ressalva impeditiva;
- 6 cálculos com GAP de cadastro;
- 4 cálculos elétricos parciais;
- 1 cálculo elétrico em conflito;
- 0 linhas fora do fail-closed de MRP líquido;
- `security_invoker=true`;
- `anon` e `authenticated` sem SELECT direto.

Conflito elétrico preservado:

- `ELE098` — luminária LED 36W: consumo referencial de 3 un/M01, porém `elo_situacao=SEM_CORRESPONDÊNCIA`; para 300 M01 o cálculo de 900 un permanece somente referencial e não pode ser promovido.

## Resultado

`VALIDADO_TECNICAMENTE / COBERTURA_PARCIAL_5_PROCESSOS`.

## Risco residual

- hidrossanitário, esquadrias como domínio próprio e demais composições ainda não possuem read-model equivalente localizado;
- 6 itens da montagem seguem sem `cod_produt`;
- 5 itens elétricos exigem validação/reconciliação antes de promoção;
- tenant, estoque, reservas, saldo técnico, pedidos abertos e lead time continuam bloqueando MRP líquido e compras.
