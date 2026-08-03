# Decision Engine

## Objetivo

Definir a camada responsável por consolidar análise, contexto e conhecimento em recomendações, decisões assistidas ou decisões automatizadas sob governança.

## Função

O Decision Engine recebe saídas do Reasoning Engine e converte o raciocínio em decisão operacional, recomendação executável ou solicitação de aprovação humana, conforme políticas vigentes.

## Responsabilidades

- consolidar alternativas e impactos
- avaliar confiança, risco e prioridade
- registrar justificativas e evidências
- aplicar políticas de governança e segurança
- distinguir recomendação, decisão assistida e decisão automatizada
- sinalizar quando há necessidade de aprovação humana

## Tipos de saída

- recomendação
- decisão assistida
- decisão automatizada autorizada
- solicitação de aprovação
- alerta de risco
- plano de ação preliminar

## Princípios

- a decisão deve ser rastreável
- a decisão deve respeitar escopo, permissões e governança
- a confiança da saída deve ser explícita quando aplicável
- decisões críticas devem poder exigir intervenção humana
- a engine não deve produzir ações sem política ou contexto suficiente

## Relação com a EIP

Esta camada fecha o ciclo cognitivo do ELO ao transformar interpretação e raciocínio em ação orientada a negócio. Ela é central para a proposta de uma EIP industrial, porque conecta múltiplas fontes de informação a decisões operacionais e estratégicas.

## Evolução futura

A implementação pode incluir:

- pontuação de decisão
- ranking de alternativas
- classificação de risco
- políticas de autonomia por domínio
- integração com workflows e aprovações
