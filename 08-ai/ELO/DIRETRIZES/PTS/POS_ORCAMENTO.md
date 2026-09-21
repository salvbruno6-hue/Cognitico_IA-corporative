# PTS Pós-Orçamento — Estrutura Canônica do ELO

**Status:** IMPLEMENTED  
**Owner canônico:** `08-ai/ELO/DIRETRIZES/PTS/`

## Princípio

A PTS Pós-Orçamento acontece **depois do orçamento**. Ela não refaz a PTS Técnica e não substitui a planilha orçamentária. Sua função é confrontar o que foi tecnicamente identificado com o que efetivamente foi orçado.

Fluxo canônico:

```text
TR
 ↓
PTS TÉCNICA
 ↓
decisão técnica
 ↓
ORÇAMENTO
 ↓
PTS PÓS-ORÇAMENTO
 ↓
VALIDAÇÃO CRUZADA
 ↓
RESULTADO ARBITRADO
 ↓
ELO APRENDER
```

A PTS Técnica e a PTS Pós são entradas independentes da **VALIDAÇÃO**. A Pós deve provar a correspondência, ausência ou divergência entre elas.

## 0. Referência à PTS Técnica

A PTS Pós deve preservar:

- `pts_tecnica_ref`;
- `itens_herdados`;
- `consultas_abertas`.

A referência técnica é uma chave de rastreabilidade, não uma cópia do conteúdo da PTS Técnica.

## 1. Identificação e objetivo

Identifica SO, cliente, objeto, revisão, referência da PTS Técnica e objetivo da auditoria pós-orçamento.

## 2. Documentos utilizados

Registra as fontes efetivamente utilizadas para a análise. Fontes históricas ou consultivas podem apoiar o raciocínio do ELO, mas não podem ser apresentadas como origem da SO atual sem evidência de aplicação.

## 3. Matriz principal — TR × Orçamento

Matriz obrigatória:

| Nº | Ref. Técnica | Tópico | Ref. TR | Requisito | Q.Prev | Q.Orç | Ref.Orç | Valor | Status | Divergência |
|---|---|---|---|---|---:|---:|---|---:|---|---|

`ref_tecnica` deve apontar para um ID existente da PTS Técnica.

A cadeia de cada item é:

**TR → requisito → PTS Técnica → solução → quantitativo previsto → orçamento → quantitativo orçado → valor → divergência.**

Não criar referência artificial.

## 4. Conferência de quantitativos

Compara quantitativo previsto e quantitativo orçado. Deve distinguir:

- quantidade calculada;
- quantidade adotada;
- quantidade orçada;
- unidade;
- diferença;
- motivo;
- status.

Diferenças devem ser explicadas ou registradas como pendência.

## 5. Conferência de valores

Confere composição, subtotal, taxa administrativa, BDI e total. Valores devem permanecer vinculados à referência do orçamento e à sua fonte.

## 6. Auditoria reversa — principais custos

Parte do custo orçado e reconstrói sua origem:

**valor → item orçamento → composição → base → justificativa → requisito/solução quando aplicável.**

A ausência de origem deve ser explicitada.

## 7. Itens orçados por premissa

Registra itens cuja composição depende de hipótese, critério, estimativa ou condição operacional:

**item → origem → premissa → impacto → tratamento.**

Premissa não comprovada não deve ser convertida em fato.

## 8. Logística

Registra transporte, mobilização, equipamentos, acessos e demais componentes logísticos, com cálculo, valor e critério.

## 9. Mão de obra

Registra composição de mão de obra, função, dias, colaboradores, valor unitário, parcial e total.

## 10. Exclusões e responsabilidades

Explicita o que não foi orçado, quem é responsável e qual o status da exclusão.

## 11. Matriz de divergências

| Nº | Item | Tipo | Previsto | Orçado | Motivo | Impacto | Ação |
|---|---|---|---|---|---|---|---|

Divergência pode ser de requisito, solução, quantitativo, composição, valor, premissa, responsabilidade ou evidência.

## 12. Matriz de riscos

| Risco | Tipo | Impacto | Condição | Tratamento |
|---|---|---|---|---|

Risco não é decisão. Deve permanecer separado da recomendação e da arbitragem.

## 13. Pendências

Consultas abertas da PTS Técnica que tenham relação comprovável com o orçamento podem ser convertidas em pendências:

**origem → impacto → ação → status.**

A PTS Pós não resolve silenciosamente uma consulta ainda não confirmada.

## 14. Itens não orçados / não confirmados

Relaciona requisitos, soluções ou componentes sem correspondente confirmado no orçamento.

Ausência de correspondência é um resultado válido da auditoria.

## 15. Checklist de completude

O checklist verifica, no mínimo:

1. requisitos principais possuem correspondência;
2. itens possuem origem/justificativa;
3. quantitativos foram confrontados;
4. áreas molhadas foram reavaliadas;
5. valores foram conferidos;
6. maiores custos foram justificados;
7. premissas foram registradas;
8. exclusões foram registradas;
9. pendências foram registradas;
10. riscos foram registrados;
11. responsabilidades foram verificadas;
12. logística foi conferida;
13. licenças/ART/RRT foram confirmadas;
14. BDI/taxa/total foram conferidos.

## 16. Conclusão e validação

A conclusão deve separar:

- atendimento;
- divergência;
- ausência de evidência;
- risco;
- pendência;
- necessidade de decisão.

A PTS Pós **não aprova automaticamente** alteração de orçamento, Lista-Mãe, conhecimento canônico, Core ou aprendizado.

A validação cruzada deve receber:

```text
PTS Técnica ──────┐
                  ├──► VALIDAÇÃO
PTS Pós ──────────┘
```

Resultado possível:

- `VALIDADO`;
- `VALIDADO_COM_PENDÊNCIAS`;
- `NÃO_VALIDADO`.

## 17. Regra de rastreabilidade

A cadeia canônica completa é:

```text
TR
→ item_tr
→ PTS Técnica
→ ref_tecnica
→ solução
→ quantitativo previsto
→ orçamento
→ ref_orc
→ quantidade orçada
→ valor
→ PTS Pós
→ divergência / justificativa
→ risco / pendência
→ VALIDAÇÃO
→ resultado arbitrado
→ ELO APRENDER
```

O **ELO APRENDER** somente recebe resultado depois de análise e governança. A PTS Pós é evidência estruturada do caso; não é autoridade automática para promover regra ou conhecimento ao Core.

## Fronteira documental

Aplicar sempre:

**ACERVO CONSULTIVO → ELO → SO ATUAL → ORÇAMENTO ATUAL → PTS PÓS**

Informação recuperada de outra SO, orçamento, PTS, PTS Pós, memória de cálculo ou experiência permanece consultiva até que a evidência demonstre sua aplicação à SO atual.

## Regra de reutilização

O mesmo template deve servir para N SOs. A variação pertence ao JSON da SO, não ao template.

Não criar uma segunda pasta de PTS Pós-Orçamento. O owner permanece:

`08-ai/ELO/DIRETRIZES/PTS/`
