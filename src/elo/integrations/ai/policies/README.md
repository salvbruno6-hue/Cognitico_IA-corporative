# AI Policies

## Objetivo

Definir as políticas que governam o uso de provedores de IA na EIP, incluindo autonomia, custo, segurança, aprovação humana e prioridade de roteamento.

## Função

As políticas determinam quando, como e com quais limites a EIP pode utilizar um provedor de IA específico.

## Dimensões de política

- autonomia
- custo
- latência
- risco
- privacidade
- segurança
- criticidade do domínio
- necessidade de aprovação humana
- disponibilidade do provider
- preferências por ambiente ou empresa

## Exemplos de decisões de política

- permitir ou bloquear chamadas externas
- exigir aprovação humana para uma ação
- priorizar provider local antes de cloud
- selecionar provider por custo ou latência
- restringir domínios sensíveis a modelos aprovados
- limitar volume ou frequência de chamadas

## Princípios

- política deve ser explícita
- política deve ser configurável
- política deve ser auditável
- política deve ser separada do provider e do domínio
- política deve proteger dados, conhecimento e governança

## Estrutura prevista

```text
policies/
├── README.md
├── router.py
├── autonomy.py
├── cost.py
├── security.py
├── approval.py
└── domain_rules.py
```

## Regras

- nenhuma chamada de IA deve ocorrer sem passar por política aplicável
- domínios críticos podem exigir políticas mais restritivas
- políticas devem ser versionadas e rastreáveis
- a política aplicada deve constar no provenance da resposta
