# ELO Forge — Plano Construtor do Cognitico

## Papel canônico

O ELO Forge é o **plano construtor** do ELO Cognitivo dentro do mesmo repositório.

- **Cognitivo / Canonical** define o que o ELO é, suas regras, arquitetura, contratos e decisões aceitas.
- **Forge** constrói, experimenta, adapta, testa e prepara mudanças para promoção ao canônico.
- O Forge não cria uma segunda autoridade arquitetural.
- O Forge não substitui o canônico.
- O Forge não promove mudanças diretamente sem passar pelo contrato de promoção.

## Relação com o antigo repositório ELO-Forge

O repositório `salvbruno6-hue/ELO-Forge` passa a ser tratado como **fonte histórica e área de transição**, não como segundo núcleo arquitetural.

O conteúdo útil deve ser extraído por finalidade e incorporado ao `Cognitico_IA-corporative` somente quando compatível com o cânone.

Não há obrigação de copiar a estrutura física do repositório antigo.

## Modelo operacional

```text
CANONICAL ELO
     │
     │ objetivo / contrato / restrições
     ▼
   FORGE
     │
     ├── construir
     ├── experimentar
     ├── simular
     ├── testar
     ├── corrigir
     └── preparar promoção
     │
     ▼
VALIDAÇÃO CANÔNICA
     │
     ├── compatível → PROMOVER
     ├── ajustável   → CORRIGIR E VALIDAR
     └── conflitante → REJEITAR / ISOLAR
     │
     ▼
CANONICAL ELO
```

## O que pertence ao Forge

- implementações em construção;
- protótipos;
- experimentos;
- testes de arquitetura;
- adaptadores;
- agentes construtores;
- automações de construção;
- artefatos de engenharia;
- candidatos a promoção;
- resultados de experimentos.

## O que não pertence ao Forge como autoridade

- definição final do cânone;
- alteração silenciosa de regras canônicas;
- substituição de arquitetura por conveniência;
- decisão de segurança sem governança;
- promoção sem validação;
- cópia indiscriminada de artefatos externos.

## Regra de divergência

Quando uma construção do Forge divergir do cânone, o Forge deve parar a promoção e produzir uma decisão explícita:

`ADAPTAR_FORGE | AJUSTAR_CANONICO | EXPERIMENTAR | REJEITAR`

O Forge nunca resolve a divergência apagando ou sobrescrevendo o cânone silenciosamente.

## Fonte externa

Projetos externos, inclusive o antigo `ELO-Forge`, podem fornecer ideias, documentação e padrões. Eles são **fontes de evidência**, não autoridade.

## Exclusão deliberada

O plano construtor não promove automaticamente SQL operacional, migrations, dados operacionais ou implementações legadas apenas porque existem no antigo Forge. Esses artefatos podem conter divergências e devem permanecer fora da promoção cognitiva salvo decisão específica posterior.
