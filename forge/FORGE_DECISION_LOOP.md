# ELO Forge — Decision Loop

## Propósito

Definir como o Forge transforma um problema de construção em uma decisão técnica de implementação sem confundir hipótese, evidência, teste e aprovação.

## Loop

```
PROBLEMA
  ↓
OBJETIVO OBSERVÁVEL
  ↓
RESTRIÇÕES
  ↓
ALTERNATIVAS DE CONSTRUÇÃO
  ↓
CRITÉRIOS DE TESTE
  ↓
EXPERIMENTO / IMPLEMENTAÇÃO
  ↓
RESULTADO OBSERVADO
  ↓
ANÁLISE
  ↓
DECISÃO
  ├─ manter
  ├─ corrigir
  ├─ experimentar novamente
  ├─ promover como candidato
  └─ rejeitar / isolar
```

## Regra de alternativas

Quando houver mais de uma implementação tecnicamente plausível, o Forge deve registrar as alternativas relevantes antes de consolidar a escolha. A alternativa não escolhida permanece identificada e recebe o motivo da exclusão quando isso for necessário para rastreabilidade.

O Forge não deve transformar uma possibilidade em fato apenas porque foi a primeira encontrada.

## Regra de evidência

Cada conclusão deve ser classificável como:

- FATO: observado diretamente;
- EVIDÊNCIA: resultado de teste ou fonte identificada;
- PREMISSA: condição assumida explicitamente;
- HIPÓTESE: possibilidade ainda não comprovada;
- DECISÃO: escolha operacional do construtor;
- DIVERGÊNCIA: incompatibilidade detectada;
- VALIDAÇÃO: confirmação contra critério definido;
- GAP: informação necessária ainda ausente.

## Regra de incerteza

Incerteza não autoriza invenção. Quando os dados forem insuficientes, o Forge deve:

1. identificar o GAP;
2. verificar se pode obter evidência adicional;
3. testar uma hipótese somente se o experimento for seguro e reversível;
4. manter a condição como não resolvida quando não houver base suficiente.

## Regra de encerramento

O loop somente pode ser encerrado quando houver:

- objetivo identificado;
- escopo delimitado;
- construção reproduzível;
- teste executado ou justificativa documentada para teste não aplicável;
- comparação canônica;
- decisão explícita;
- status de promoção definido.
