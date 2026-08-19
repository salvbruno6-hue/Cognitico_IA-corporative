# ELO — Impacto da Alteração de Endereço Canônico

## Objetivo

Definir o que precisa ser atualizado quando um artefato de conhecimento mudar de endereço, sem confundir mudança física com mudança conceitual.

## Regra central

```text
artifact_id permanece
concept_id permanece
canonical_path pode mudar
legacy_path pode desaparecer somente após migração
```

## Camadas impactadas

| Camada | Impacto | Tratamento |
|---|---|---|
| Índice canônico | direto | atualizar `canonical_path` |
| Aliases | direto | registrar caminho anterior |
| Documentação | alto | localizar links e referências |
| Knowledge Engineering | alto | resolver por identidade, não por caminho rígido |
| Source Resolution | controlado | consumir identidade/resolução governada |
| RAG | futuro/alto | indexar identidade e proveniência |
| Memory | futuro/alto | preservar identidade do conhecimento |
| Agentes | alto | evitar hard-code de caminhos históricos |
| Evidence | alto | manter origem e hash |
| Governance | alto | registrar decisão e estado |
| Testes | alto | validar caminho novo e alias |
| CI | gate | impedir referência órfã |
| Runtime Core | baixo nesta fase | não alterar sem necessidade comprovada |

## Sequência de migração

### A — Descoberta
Localizar consumidores e referências ao caminho histórico.

### B — Registro
Associar o caminho ao `artifact_id`.

### C — Alias
Adicionar o caminho antigo como alias temporário.

### D — Consumidores
Atualizar referências para a identidade canônica ou novo caminho autorizado.

### E — Validação
Testar resolução pelo endereço novo e pelo alias.

### F — Depreciação
Marcar o caminho antigo como `DEPRECATED`.

### G — Remoção
Somente quando todos os gates estiverem verdes e não houver conteúdo exclusivo.

## Falhas que o processo deve impedir

- dois arquivos tratados como autoridade simultânea;
- agente consultando conteúdo obsoleto sem saber;
- RAG indexando cópia histórica como verdade atual;
- Memory perdendo proveniência;
- links quebrados;
- evidência apontando para arquivo inexistente;
- migração que altera significado sem decisão;
- exclusão de conhecimento complementar.

## Critério de sucesso

Uma alteração de endereço deve ser transparente para qualquer consumidor que utilize a identidade canônica, preservando conteúdo, proveniência, versionamento e rastreabilidade.
