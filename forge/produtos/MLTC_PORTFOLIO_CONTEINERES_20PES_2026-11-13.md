# Família MLT.C — Portfólio técnico de contêineres 20 pés

Data de registro: 2026-11-13  
Enriquecimento estrutural: 2026-11-17

## Escopo e fronteira

Este registro preserva conhecimento documental da família **MLT.C**, baseada em contêiner marítimo Dry adaptado.

**Regra de governança:** informações de MLT.C não devem ser transferidas automaticamente para MLT.M. Requisitos de um modelo MLT.C também não são automaticamente transferíveis a outro modelo MLT.C.

A fonte distingue três estados de informação: **DOCUMENTADO**, **VISUAL** e **PENDENTE**. Fotografia comprova apenas o que é visível e não substitui desenho, memorial, lista ou revisão aprovada.

Esta evolução **não promove** dados documentais para BOM e **não altera** a família MLT.M.

## Modelos registrados

| Código fonte | Código canônico | Produto | Maturidade documental |
|---|---|---|---|
| MLTC06 | MLT.C06 | Depósito | FICHA_PRELIMINAR |
| MLTC10 | MLT.C10 | Escritório forrado | CADERNO_PRELIMINAR |
| MLTC13 | MLT.C13 | Escritório simples | CADERNO_TECNICO |
| MLTC20 | MLT.C20 | Sanitário · 7 chuveiros | CADERNO_TECNICO |
| MLTC21 | MLT.C21 | Sanitário coletivo cabinado · 7 vasos | PORTFOLIO_TECNICO |
| MLTC25 | MLT.C25 | Suíte forrada | CADERNO_PRELIMINAR |

## Estruturas Supabase alimentadas

### Identidade de produto

Os seis modelos foram registrados em:
- `public.taxonomia`
- `public.modelos`

A dimensão canônica **não foi preenchida** quando a documentação contém conflito ou ausência de cota validada.

### Documento de engenharia

O portfólio foi registrado por modelo em:
- `public.mt_documentos_engenharia`

Status usado: `REFERENCIA_NAO_LIBERADA`.

O registro do documento não equivale a revisão aprovada de engenharia.

### Conhecimento cognitivo

Os registros do núcleo `CONHECIMENTO_PRODUTOS` foram enriquecidos em `public.elo_conhecimento_itens`:
- `FAMILIA_MLTC_DRY_ADAPTADO`
- `PORTFOLIO_MLTC06_20261113`
- `PORTFOLIO_MLTC10_20261113`
- `PORTFOLIO_MLTC13_20261113`
- `PORTFOLIO_MLTC20_20261113`
- `PORTFOLIO_MLTC21_20261113`
- `PORTFOLIO_MLTC25_20261113`

Os conteúdos agora preservam maturidade documental, dados documentados/visuais, pendências, GAPs e a regra de não promoção automática para BOM.

## Workbook técnico de trabalho

Foi criado um Google Sheet de apoio operacional:

https://docs.google.com/spreadsheets/d/1ClMoYo6RKYUoXQbQXRW3vUpiUKyE0rYpXw1gQC6W-Vg/edit

Abas:
1. `01_MODELOS`
2. `02_ESPEC_EVIDENCIAS`
3. `03_COMPOSICAO_TECNICA`
4. `04_GAPS_VALIDACOES`
5. `05_DOCUMENTOS_REVISOES`
6. `06_MATURIDADE`

O workbook contém **122 linhas de composição documental** e **39 GAPs/pendências estruturadas**. Ele é interface de trabalho e validação; **não é nova autoridade canônica**.

## GAPs preservados

### MLTC13
- Porta: 800 × 2.100 mm × 850 × 2.100 mm.
- Comprimento: 6.058 mm × 6.050 mm.
- Janela: 800 × 1.000 mm × 800 × 1.200 mm.
- Projeto/custo: 2 bocais; lista PDF: 4.
- Projeto e lista divergem em tomadas de AC/telefonia.
- Projeto/aba e lista divergem em comando e QDF.
- Disjuntores divergem entre tabela, referência impressa e lista.
- PDF GERAL C28 presente no pacote não deve ser usado como custo do C13.

### MLTC20
- Esgoto: Ø100 mm × Ø75 mm.
- Basculantes: 3 × 2.
- Comprimento: 6.058 mm × 6.050 mm.
- Disjuntor: 4 A × 10 A 2P.
- Carimbo/pacote C20 × nomes de arquivo M09.
- ARQ Rev. 0 consta para aprovação.

### MLTC21
- Portas internas: 600 × 1.600 mm × 600 × 1.900 mm.
- Basculantes: 2 × 3.
- Alimentação elétrica: bifásica × monofásica.
- Descrição do disjuntor apresenta divergência mono/bi.
- Carimbo ARQ traz “7 chuveiros”; planta, descrição e materiais são de 7 vasos.
- Saída Ø100 está nas notas, mas o arquivo ESG não detalha o coletor.

## Composição documental

As listas documentais de MLTC13, MLTC20 e MLTC21 foram transcritas para o workbook, preservando:
- item de origem;
- sistema;
- descrição da fonte;
- quantidade;
- unidade original;
- evidência;
- status de validação;
- pendência de vínculo com a Lista Mãe.

**Não houve carga em `estrutura_modular_itens`**, porque os itens ainda precisam ser mapeados com segurança para `public.lista_mae`.

## Objetos deliberadamente não alterados

Nesta evolução não foram alterados:
- `public.dimensoes`
- `public.estrutura_modular_itens`
- `public.mt_versoes_bom`
- `public.mt_bom_itens`
- BOMs, kits, custos ou parâmetros da família MLT.M.

## Gate de promoção

Fluxo obrigatório para evolução da composição:

`documento → evidência → compatibilização de GAP → vínculo Lista Mãe → validação → versão de BOM → aprovação`

Nenhuma composição documental deve ser tratada como BOM liberada antes desse gate.

## Governança

A operação foi registrada em `public.tb_elo_eventos_governanca` como:

`ENRIQUECIMENTO_PORTFOLIO_MLTC_20261113`

Os conflitos permanecem como evidência documental divergente. A estrutura atual deve ser **reutilizada e fortalecida**, evitando criação de autoridades ou tabelas paralelas.
