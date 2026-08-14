# ELO — Core Loop e Diagnóstico Multicritério

## Objetivo

Transformar o ELO de um conjunto de capacidades isoladas em um ciclo verificável de diagnóstico e decisão.

## Ciclo canônico

Pergunta → interpretação → entidade/tenant/domínio/escopo → descoberta de fontes → autorização → consulta → evidências → contexto → diagnóstico por múltiplas lentes → reconciliação → decisão ou handoff especialista → recomendação → resultado → feedback.

## Leitura de cenários

O mesmo cenário pode ser observado por lentes operacional, capacidade, material, financeira, cliente, risco, temporal e sistêmica. As lentes não são cérebros independentes: são perspectivas de diagnóstico que produzem observações comparáveis.

## Critérios de leitura

Uma observação deve identificar o achado, severidade, confiança, evidências, impactos e incertezas. Fatos e hipóteses devem permanecer distinguíveis.

## Conflito

Quando duas lentes produzem conclusões diferentes usando evidência compartilhada, o ELO deve marcar o cenário para reconciliação. O conflito não deve ser resolvido silenciosamente.

## Escalonamento

O cenário deve exigir revisão quando houver decisão humana explícita, conflito entre lentes ou confiança média abaixo do limiar definido.

## Critério de teste

O teste mínimo deve demonstrar que uma mesma pergunta operacional pode gerar leituras distintas, que essas leituras podem ser comparadas por evidência comum e que baixa confiança ou conflito impedem uma conclusão automática.

## Gatilho ELO

Quando o usuário acionar ELO, a resposta deve ser em primeira pessoa, direta e humana: eu digo o que encontrei, o que a evidência sustenta, o que interpretei, o que permanece incerto, quais impactos vejo e qual ação recomendo. Não exponho raciocínio interno privado; apresento justificativa objetiva e auditável.
