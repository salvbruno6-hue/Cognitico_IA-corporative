# ELO — Loop Cognitivo de Orçamento

## Objetivo

Definir o ciclo canônico pelo qual o ELO interpreta uma necessidade de orçamento, consulta a Lista Mãe, sugere materiais por `COD_PRODUT`, registra sua própria experiência, recebe arbitragem do especialista e transforma o resultado em evidência reutilizável.

## Invariantes

1. `lista_mae` é a fonte mestre do material.
2. `COD_PRODUT` é a chave operacional usada para identificação e rastreamento do material pelo Almoxarifado.
3. O ELO nunca inventa `COD_PRODUT`.
4. A descrição oficial do material permanece na Lista Mãe.
5. Kits não criam cadastros paralelos de materiais.
6. Uma sugestão do ELO é uma hipótese cognitiva, não uma verdade técnica.
7. A sugestão deve ser registrada como experiência, mesmo antes da arbitragem.
8. A arbitragem humana produz evidência de maior autoridade.
9. Rejeições reduzem a confiança da associação; aprovações e ajustes validados aumentam ou recalibram a confiança.
10. Memória, associação e cadastro mestre são camadas distintas.

## Fluxo

```text
necessidade de orçamento
        ↓
interpretação de aplicação + contexto
        ↓
consulta à Lista Mãe
        ↓
sugestão de materiais + COD_PRODUT
        ↓
registro da experiência do ELO
        ↓
arbitragem do especialista
        ↓
aprovado / ajustado / rejeitado
        ↓
MERGE da evidência
        ↓
recalibração de associação e confiança
        ↓
memória de cálculo e experiência
        ↓
próxima sugestão
```

## Memória cognitiva

A experiência deve preservar, quando disponível:

- aplicação;
- necessidade;
- contexto;
- material;
- `lista_mae_id`;
- `COD_ITEM`;
- `COD_PRODUT`;
- quantidade;
- unidade;
- memória de cálculo;
- justificativa;
- resultado;
- origem da experiência;
- decisão do especialista;
- confiança;
- ocorrências;
- rejeições e evidências.

## Raciocínio como nervuras

O ELO deve formar relações reutilizáveis entre:

`necessidade → aplicação → contexto → material → COD_PRODUT → cálculo → resultado`

Cada experiência fortalece, enfraquece ou mantém essas relações. O objetivo não é memorizar somente respostas, mas acumular evidências sobre as condições em que uma associação se mostrou adequada.

## Governança

O ELO pode sugerir, comparar, calcular e recuperar experiências. A decisão técnica final permanece com o especialista autorizado quando a situação exigir julgamento profissional.

O MERGE não deve alterar a Lista Mãe como efeito colateral do aprendizado. O aprendizado pertence às estruturas de memória e associação.

## Gate de conclusão

Uma implementação só é considerada consolidada quando:

- o fluxo de sugestão está registrado;
- a arbitragem é registrada;
- o MERGE é auditável;
- `COD_PRODUT` é validado contra a Lista Mãe;
- o histórico permanece preservado;
- não há duplicação de cadastro por kit;
- testes confirmam sugestão → arbitragem → aprendizado → nova sugestão;
- banco e Git permanecem alinhados.
