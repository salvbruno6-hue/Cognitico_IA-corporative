# Família MLT.C — Estado técnico consolidado

**Estado vigente em:** 2026-11-18  
**Versão documental:** `DOC-2026-11-13`  
**Família:** MLT.C — contêiner marítimo Dry adaptado  
**Situação:** documental, não liberada para produção

## 1. Autoridades e fronteiras

- **GitHub** é a autoridade operacional/canônica.
- **Supabase** é a autoridade cognitiva/persistente.
- A Lista Mãe válida é `public.lista_mae`.
- Planilhas não são autoridade e não devem ser criadas, editadas ou sincronizadas sem solicitação explícita do usuário.
- Informações MLT.C não devem ser transferidas automaticamente para MLT.M.
- Requisitos de um modelo MLT.C não são automaticamente transferíveis a outro modelo MLT.C.

Estados de evidência preservados: **DOCUMENTADO**, **VISUAL** e **PENDENTE**.

## 2. Modelos

| Modelo | Produto | Maturidade | Kit | BOM |
|---|---|---|---|---|
| MLT.C06 | Depósito | FICHA_PRELIMINAR | documental vazio | INCOMPLETA_DOCUMENTAL |
| MLT.C10 | Escritório forrado | CADERNO_PRELIMINAR | documental vazio | INCOMPLETA_DOCUMENTAL |
| MLT.C13 | Escritório simples | CADERNO_TECNICO | documental | RASCUNHO_DOCUMENTAL |
| MLT.C20 | Sanitário · 7 chuveiros | CADERNO_TECNICO | documental | RASCUNHO_DOCUMENTAL |
| MLT.C21 | Sanitário coletivo cabinado · 7 vasos | PORTFOLIO_TECNICO | documental | RASCUNHO_DOCUMENTAL |
| MLT.C25 | Suíte forrada | CADERNO_PRELIMINAR | documental vazio | INCOMPLETA_DOCUMENTAL |

## 3. Estado consolidado da composição

| Modelo | Linhas kit | Mapeadas Lista Mãe | Elegíveis BOM | Itens BOM | GAPs | Valor parcial |
|---|---:|---:|---:|---:|---:|---:|
| MLT.C06 | 0 | 0 | 0 | 0 | 0 | — |
| MLT.C10 | 0 | 0 | 0 | 0 | 0 | — |
| MLT.C13 | 28 | 22 | 12 | 12 | 16 | R$ 491,24 |
| MLT.C20 | 45 | 23 | 20 | 20 | 25 | R$ 1.174,99 |
| MLT.C21 | 51 | 28 | 24 | 23 | 27 | R$ 1.313,77 |
| MLT.C25 | 0 | 0 | 0 | 0 | 0 | — |
| **Total** | **124** | **73** | **56** | **55** | **68** | **R$ 2.980,00** |

Os valores são **parciais** e representam somente os itens atualmente alinhados à Lista Mãe. Não constituem orçamento completo do produto.

Estrutura documental:
- 6 registros em `estrutura_modular`;
- 55 itens em `estrutura_modular_itens`;
- 0 estruturas ativas;
- 0 itens ativos;
- 0 kits operacionais;
- 0 BOMs aprovadas.

## 4. Regras técnicas vigentes validadas

### MLT.C20 — esgoto
- Coletor/saída principal: **Ø100 mm**.
- A alternativa Ø75 foi encerrada como conflito histórico e **não é vigente** para o coletor principal.
- Ramais Ø40 e Ø50 permanecem conforme documentação.
- Tê principal, Tê 100×50, luva e anel do coletor foram vinculados aos correspondentes Ø100 da Lista Mãe.
- O joelho permanece pendente somente quanto ao ângulo 45°/90°.
- O tubo principal está identificado como Ø100 × 6 m, porém a conversão documental de 6 m para 1 barra/PÇ de 6 m ainda exige validação antes de promoção.

### Cabos 2,5 mm²
Unidade vigente: **metro (MT)**.

- MLT.C20: preto **18 m**; verde **2 m**.
- MLT.C21: preto **19 m**; verde **2 m**.

### Porta principal C20/C21
A porta principal 800 × 2100 mm está vinculada a `ESQ001 — KIT PORTA SOCIAL FRONTAL 800X2100MM`.

## 5. Situação por modelo

### MLT.C06 — Depósito
Documentado como contêiner Dry 20 pés adaptado para depósito. Visualmente apresenta portas duplas em uma extremidade e volume interno sem divisórias aparentes.

Pendências principais:
- dimensões externas/úteis;
- massa e carga admissível;
- vãos e ferragens;
- piso e pintura específicos;
- elétrica e ventilação;
- lista de materiais específica.

### MLT.C10 — Escritório forrado
Informações documentadas incluem:
- piso em compensado naval pintado, referência interna de 20 mm;
- porta 850 × 2100 mm;
- 2 janelas maxim-ar, dimensões pendentes;
- vão de ar-condicionado 410 × 690 mm;
- 2 pontos de iluminação;
- 3 tomadas 127 V;
- 1 ponto AC 220 V;
- alimentação bifásica com aterramento.

Permanece sem lista de materiais específica suficiente para BOM.

### MLT.C13 — Escritório simples
Documentado:
- externo 6058 × 2440 × 2590 mm;
- interno 5908 × 2340 × 2380 mm;
- carga instalada 2,80 kW;
- alimentação 2φ 220 V;
- disjuntor geral 25 A 2P;
- forro PVC 14 m²;
- 5 cartolas de teto;
- vão AC 410 × 690 mm.

GAPs ativos:
- porta 800×2100 × 850×2100;
- comprimento 6058 × 6050;
- janela 800×1000 × 800×1200;
- quantidade de bocais;
- tomada AC/telefonia;
- comando/QDF;
- disjuntores;
- documento C28 presente no pacote não deve ser usado como custo do C13.

### MLT.C20 — Sanitário · 7 chuveiros
Documentado:
- externo 6058 × 2440 × 2590 mm;
- interno 5908 × 2340 × 2380 mm;
- 7 chuveiros de água fria;
- 3 lavatórios;
- 1 mictório coletivo;
- 7 portas de box 600 × 1600 mm;
- entrada de água Ø25 mm;
- porta principal 800 × 2100 mm;
- iluminação: 2 bocais E27, 300 W, 220 V.

Regra vigente:
- coletor/saída principal de esgoto **Ø100 mm**.

GAPs ativos prioritários:
- quantidade de basculantes 3 × 2;
- comprimento 6058 × 6050;
- disjuntor 4 A × 10 A 2P;
- identificação de arquivo C20 × M09;
- revisão ARQ 0 para aprovação;
- ângulo do joelho Ø100;
- conversão do tubo Ø100 de 6 m para barra/PÇ.

### MLT.C21 — Sanitário coletivo cabinado · 7 vasos
Documentado:
- externo 6058 × 2440 × 2590 mm;
- interno 5908 × 2340 × 2380 mm;
- 7 vasos;
- 3 lavatórios;
- 1 mictório coletivo;
- entrada de água Ø25 mm;
- saída de esgoto Ø100 mm nas notas;
- porta principal 800 × 2100 mm;
- profundidade de cabine 1200 mm;
- divisórias em chapa de aço zincado;
- piso em compensado naval pintado.

GAPs ativos:
- portas internas 600×1600 × 600×1900;
- basculantes 2 × 3;
- alimentação bifásica × monofásica;
- descrição de disjuntor mono/bi;
- carimbo ARQ “7 chuveiros” × conteúdo de 7 vasos;
- arquivo ESG sem detalhamento do coletor.

### MLT.C25 — Suíte forrada
A evidência atual é majoritariamente visual e preliminar. Não há pacote técnico suficiente para composição completa.

Pendências:
- dimensões, peso e capacidade;
- forração e isolamento;
- água e esgoto;
- circuitos e proteções;
- aquecimento do banho;
- ar-condicionado;
- materiais e quantitativos ocultos.

C25 e C28 não são intercambiáveis.

## 6. Fluxo de governança vigente

`documento → evidência → kit documental → vínculo Lista Mãe → GAP/validação → BOM rascunho → estrutura documental → Evolution Gate → aprovação`

Somente itens com vínculo inequívoco à `public.lista_mae` e sem GAP impeditivo entram na BOM rascunho.

Nenhuma BOM, kit ou estrutura documental desta família está liberada para PCP ou produção.

## 7. Próximos gates

1. MLT.C20: definir ângulo do joelho Ø100 e validar conversão da barra de tubo Ø100.
2. MLT.C21: resolver faseamento elétrico e conflitos arquitetônicos.
3. MLT.C13: compatibilizar porta, janela, comprimento e elétrica.
4. MLT.C06, C10 e C25: receber listas de materiais e pacotes técnicos específicos.
5. Somente após compatibilização, submeter nova versão ao Evolution Gate.

## 8. Rastreabilidade

O histórico de evolução permanece preservado nas migrations e em `tb_elo_eventos_governanca`. Este documento representa **o estado vigente consolidado**, substituindo interpretações intermediárias que ficaram obsoletas após validações posteriores.
