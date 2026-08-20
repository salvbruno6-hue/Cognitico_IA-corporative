# 00 — Enterprise Manifest

Owner canônico dos fundamentos empresariais do ELO.

## Cadeia lógica

A família deve ser lida nesta ordem:

`01 Missão → 02 Objetivos → 03 Capacidades → 04 Cadeia de Valor → 05 Modelo Operacional → 06 Stakeholders → 07 Regras Estratégicas`

| Artefato | Função | Pergunta que responde |
|---|---|---|
| `01_Missao.md` | Intenção institucional | Por que o ELO existe? |
| `02_Objetivos.md` | Resultados estratégicos | O que o ELO deve alcançar? |
| `03_Capacidades.md` | Habilitações empresariais | Do que o ELO precisa ser capaz? |
| `04_Cadeia_de_Valor.md` | Criação de valor | Como capacidades e recursos geram valor? |
| `05_Modelo_Operacional.md` | Operação desejada | Como o ELO pretende operar? |
| `06_Stakeholders.md` | Atores e interesses | Quem influencia, utiliza ou é afetado? |
| `07_Regras_Estrategicas.md` | Invariantes estratégicas | O que deve permanecer coerente? |
| `ENTERPRISE_MANIFEST.md` | Agregador canônico | Como os sete artefatos se encaixam? |

## Regra de manutenção lógica automática

A Família 00 deve ser mantida como um sistema semântico, não como uma coleção independente de arquivos.

Em qualquer manutenção, o ELO deve:

1. identificar o owner canônico antes de criar ou alterar um artefato;
2. verificar se o conteúdo pertence à responsabilidade daquele owner;
3. comparar contra os demais artefatos da família para detectar sobreposição;
4. preservar a cadeia `Missão → Objetivos → Capacidades → Cadeia de Valor → Modelo Operacional → Stakeholders → Regras`;
5. mover conteúdo complementar para o owner correto em vez de criar duplicatas;
6. registrar proveniência quando houver migração;
7. atualizar referências e consumidores quando um caminho for alterado;
8. somente remover um legado após resolver conteúdo, aliases, referências, consumidores e validações;
9. impedir o fechamento de uma consolidação quando houver conflito semântico não decidido.

## Regra de evolução
Nomes semelhantes, traduções, versões históricas e caminhos legados devem ser tratados como candidatos à reconciliação, nunca como owners independentes por padrão.

A mesma lógica deve ser aplicada às demais famílias do repositório quando houver consolidação, migração ou remoção de artefatos.