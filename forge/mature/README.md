# FORGE.MATURE — Camada de mecanismos amadurecidos

## Status

CANÔNICO COMO CAMADA INTERNA DO FORGE.

## Regra estrutural

`FORGE.MATURE` não é um pilar, núcleo, autoridade, agente ou arquitetura independente. É uma camada interna do Forge destinada a mecanismos operacionais amadurecidos, recuperados ou estabilizados.

A tricotomia do ELO não é alterada por esta camada.

- **SOUL** mantém as invariantes irrevogáveis.
- **CORE** mantém a governança e a autoridade de promoção.
- **FORGE** constrói, experimenta, testa e prepara.
- **FORGE.MATURE** preserva mecanismos suficientemente amadurecidos dentro do Forge.
- **COGNITIVE** interpreta, raciocina, decide e aprende.
- **SIMBIONTE** é uma natureza do Cognitive, não uma camada independente.

## Proveniência

O antigo repositório `salvbruno6-hue/ELO-Forge` e o antigo projeto `Elo_mature` são fontes históricas. Nenhum deles é autoridade arquitetural.

Mecanismos recuperados devem manter sua origem e permanecer sujeitos a comparação canônica antes de integração.

## Critérios de entrada

Um mecanismo somente deve ser colocado em `FORGE.MATURE` quando:

1. sua finalidade estiver identificada;
2. houver owner semântico dentro do ELO;
3. sua proveniência estiver registrada;
4. não existir autoridade paralela;
5. sua compatibilidade com as invariantes estiver demonstrada;
6. houver teste ou evidência suficiente para classificá-lo como amadurecido.

## Limite de autoridade

`FORGE.MATURE` não pode:

- redefinir a arquitetura do ELO;
- alterar a Soul;
- promover conhecimento ao cânone por conta própria;
- criar um Core, Cognitive ou memória canônica paralela;
- substituir o Cognitive;
- executar mudança estrutural sem o fluxo de governança.

## Assimilação do histórico Mature

O histórico de mecanismos amadurecidos segue:

```text
HISTÓRICO / ELO_MATURE
        ↓
FORGE — recuperar e classificar
        ↓
FORGE.MATURE — preservar mecanismo elegível
        ↓
COGNITIVE / SIMBIONTE — absorver, relacionar, aprender e experimentar
        ↓
COGNITIVE — avaliar necessidade de evolução
        ↓
CORE — governar promoção ou rejeição
```

A existência de um mecanismo em `FORGE.MATURE` não implica promoção ao cânone.
