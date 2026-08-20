# Enterprise Manifest

## Papel canônico
Este é o **documento agregador da Família 00**. Define a intenção empresarial em nível superior e aponta para os sete artefatos especializados que formam sua composição canônica.

Ele não concorre semanticamente com esses documentos: não replica seu conteúdo detalhado e não deve se tornar um segundo owner.

## Cadeia lógica canônica

`Missão → Objetivos → Capacidades → Cadeia de Valor → Modelo Operacional → Stakeholders → Regras Estratégicas`

## Responsabilidade
- estabelecer a intenção empresarial do ELO;
- definir o escopo da família;
- declarar a composição canônica;
- preservar a ordem lógica entre os artefatos;
- servir como entrada estratégica para as famílias arquiteturais posteriores.

## Composição canônica
1. [`01_Missao.md`](./01_Missao.md) — por que o ELO existe;
2. [`02_Objetivos.md`](./02_Objetivos.md) — quais resultados estratégicos busca;
3. [`03_Capacidades.md`](./03_Capacidades.md) — do que precisa ser capaz;
4. [`04_Cadeia_de_Valor.md`](./04_Cadeia_de_Valor.md) — como cria valor;
5. [`05_Modelo_Operacional.md`](./05_Modelo_Operacional.md) — como pretende operar;
6. [`06_Stakeholders.md`](./06_Stakeholders.md) — quem influencia, utiliza ou é afetado;
7. [`07_Regras_Estrategicas.md`](./07_Regras_Estrategicas.md) — quais invariantes mantêm a coerência.

## Regra de manutenção lógica
Toda inclusão, alteração, migração ou remoção dentro desta família deve ser analisada contra a cadeia lógica completa. Se um artefato passar a exercer responsabilidade de outro, o conteúdo deve ser redistribuído e o owner canônico corrigido antes do fechamento.

## Regra de não duplicidade
Não criar outro artefato com a mesma responsabilidade sem uma decisão arquitetural explícita registrada. Variantes linguísticas, históricas ou de nomenclatura não constituem automaticamente novos owners.

## Proveniência
Consolidado a partir de `00-empresa-manifesto/ENTERPRISE_MANIFESTO.md` e ajustado para funcionar como agregador canônico da Família 00.