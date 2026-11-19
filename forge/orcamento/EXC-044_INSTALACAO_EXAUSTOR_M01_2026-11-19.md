# EXC-044 — Instalação de exaustor em cozinha M01

**Data de consolidação:** 2026-11-19  
**Estado:** referencial, inativo, custo total em aberto  
**Contexto:** M01 / MLT.M01 Habitacional Amplo — interface em painel PIR 40 mm

## Fonte histórica

Orçamento interno de 24/10/2022:

- cliente: PRODUÇÃO INTERNA;
- escopo: colocação de um exaustor de cozinha, ponto 2P+T 220 V / 20 A, módulo com painel PIR 40;
- exaustor histórico: 50 cm, alta rotação, vazão informada de 21.000 m³/h;
- materiais históricos: R$ 469,30;
- mão de obra listada: 1 profissional/dia R$ 275,82 + 1 ajudante/dia R$ 235,92 = R$ 511,74/dia;
- linha “serviços executados no dia”: 5, equivalente matematicamente a R$ 102,348 por serviço;
- o total exibido no documento repete R$ 469,30 e não fecha materiais + mão de obra.

O orçamento é preservado como precedente, não como preço atual.

## Equipamento candidato atual

O usuário indicou o **ITC 350 Industrial**, versão 220 V.

Referência técnica do fabricante:
- potência: 92 W;
- vazão: 990 m³/h;
- rotação: 1550 rpm;
- hélice: Ø300 mm;
- saída: Ø350 mm;
- furo de instalação: Ø360 mm;
- aplicação declarada pelo fabricante: ambientes de até 80 m².

O ITC 350 **não é equivalente** ao equipamento histórico de 50 cm / 21.000 m³/h. A diferença de vazão impede substituição automática.

## Composição atual estruturada

Itens vinculados à Lista Mãe:

| Cod. item | Componente | Quantidade | Valor unitário | Parcial |
|---|---|---:|---:|---:|
| ELE052 | Cabo 2,5 mm² preto | 3 m | R$ 2,43 | R$ 7,29 |
| ELE005 | Dutopop PVC 16×16×2000 mm | 1 pç | R$ 19,11 | R$ 19,11 |
| ELE132 | Tomada 2P+T 20A/250 V | 1 pç | R$ 6,15 | R$ 6,15 |

Material canônico conhecido: **R$ 32,55**.

Itens ainda não fechados:
- exaustor ITC 350: sem cadastro/preço homologado na Lista Mãe;
- tampa/espelho: descrição histórica insuficiente para vínculo inequívoco;
- cabo verde: existe no histórico sem quantidade; permanece com quantidade zero no EXC até definição de projeto.

## Mão de obra candidata

Usando apenas como referência a produtividade histórica de 5 serviços/dia:

- profissional: 0,2 dia × R$ 275,82 = R$ 55,164;
- ajudante: 0,2 dia × R$ 235,92 = R$ 47,184;
- total candidato: **R$ 102,348**.

A produtividade precisa ser revalidada antes da ativação.

## Parcial conhecido

Materiais canônicos R$ 32,55 + mão de obra candidata R$ 102,348 = **R$ 134,898**.

Esse valor **não é o custo do EXC**. O campo de custo total permanece nulo porque faltam o exaustor homologado e a tampa/espelho, além da validação da produtividade.

## Governança

- código: `EXC-044`;
- `ativo=false`;
- não altera a BOM base M01;
- não cria item na Lista Mãe;
- não altera planilhas;
- permanece em Forge como precedente/composição referencial;
- ativação exige fechamento do equipamento, acabamento da tomada e produtividade de instalação.
