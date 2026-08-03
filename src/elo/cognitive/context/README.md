# Context Engine

## Objetivo

Definir a camada responsável por montar, normalizar e manter o contexto operacional e cognitivo necessário para consultas, análises e decisões dentro da EIP.

## Função

O Context Engine recebe sinais, perguntas, metadados e referências e os organiza em uma estrutura contextual pronta para consumo pelo Knowledge Engine, Reasoning Engine e Decision Engine.

## Entradas típicas

- perguntas do usuário ou agente
- dados estruturados de domínios
- eventos recentes
- histórico relevante
- regras de negócio
- permissões e escopo de acesso
- referências de conhecimento recuperado

## Saídas típicas

- contexto consolidado
- contexto resumido
- contexto enriquecido com evidências
- contexto filtrado por governança
- contexto pronto para recuperação ou raciocínio

## Princípios

- contexto deve ser rastreável
- contexto deve respeitar permissões e escopo
- contexto deve ser mínimo suficiente para a decisão
- contexto não deve misturar fontes sem origem identificada
- contexto deve poder ser reproduzido para auditoria

## Relação com o ELO

O Context Engine é a ponte entre dados, conhecimento e decisão. Ele não decide sozinho; ele organiza os elementos que permitem decidir.

## Evolução futura

A implementação futura pode incluir:

- enriquecimento automático de contexto
- compressão semântica
- priorização por relevância
- memória de curto prazo
- geração de contexto para agentes e APIs externas
