# EXC-044 — Instalação de exaustor em cozinha M01

**Estado vigente:** ATIVO / VALIDADO  
**Data da validação:** 2026-11-19  
**Contexto:** M01 / MLT.M01 Habitacional Amplo — instalação em painel PIR 40 mm

## Equipamento canônico

O equipamento foi cadastrado na Lista Mãe como:

- **cod_item:** `ELE171`
- **descrição:** EXAUSTOR INDUSTRIAL ITC 350 MOTOR BLINDADO BIVOLT 92W 990M3/H ALUMINIO
- **unidade:** PÇ
- **valor unitário canônico:** **R$ 425,00**
- **cod_produt:** pendente de código ERP; não inventado
- **ativo:** sim

Validação de preço em 19/11/2026:
- Mercado Livre / Safanelli: **R$ 425,00** — referência de aquisição adotada;
- loja oficial ITC: **R$ 500,18** — referência de fabricante.

Fontes:
- https://www.mercadolivre.com.br/exaustor-industrial-itc-350-motor-blindado-vazao-990-mh-aluminio/p/MLB52633874
- https://www.loja.itcexaustores.com.br/exaustores
- https://www.itcexaustores.com.br/_files/ugd/0b129f_bf4e5f41d22b4ea6af3e8532c6785aa9.pdf

Referência técnica usada: 92 W, 990 m³/h, bivolt, saída Ø350 mm e furo de instalação Ø360 mm.

## Composição validada do EXC-044

A composição histórica foi reconciliada com o padrão vigente do ELO. A rota de 3 m informada no orçamento de 2022 foi preservada e aplicada aos três condutores do ponto.

| Item | Quantidade | Referência |
|---|---:|---|
| ELE171 — Exaustor ITC 350 | 1 PÇ | R$ 425,00 |
| ELE052 — Cabo 2,5 mm² preto | 3 MT | Lista Mãe |
| ELE051 — Cabo 2,5 mm² azul | 3 MT | Lista Mãe |
| ELE053 — Cabo 2,5 mm² verde | 3 MT | Lista Mãe |
| ELE132 — Tomada 2P+T 20A/250V | 1 PÇ | Lista Mãe |
| ELE002 — Caixa D300 Dutopop | 1 PÇ | Lista Mãe |
| ELE125 — Espelho D300-K | 1 PÇ | Lista Mãe |
| ELE005 — Dutopop 16×16×2000 mm | 1 PÇ | Lista Mãe |

**Materiais:** R$ 481,67.

Mão de obra:
- profissional: 0,2 dia × R$ 275,82 = R$ 55,16;
- ajudante: 0,2 dia × R$ 235,92 = R$ 47,18.

**Mão de obra:** R$ 102,34.

## Valor ativo

**EXC-044 = R$ 584,01 / UN**

O valor é derivado da composição vigente e não do total histórico de 2022.

## Governança

- `EXC-044.ativo = true`;
- aprendizado promovido pelo fluxo canônico `elo_commit_aprendizado_merged`;
- classificação: `VALIDATED_LEARNING`;
- não altera a BOM base do M01;
- permanece como excedente/opcional;
- nenhuma planilha é alterada;
- o código ERP do exaustor continua pendente e não foi inventado.
